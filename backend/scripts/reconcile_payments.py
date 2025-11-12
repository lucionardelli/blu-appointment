import argparse
import logging
import sys
from datetime import UTC, datetime
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


from app.appointments.models import Appointment
from app.core.config import settings
from app.patients.models import Patient  # noqa: F401
from app.payments.models import Payment, PaymentMethod
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import sessionmaker

from scripts.utils import backup_database

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def reconcile_payments(date_str: str, *, dry_run: bool) -> None:  # noqa: C901, PLR0912, PLR0915
    """Reconciles payments on a per-appointment basis.

    - Removes payments that are not associated with any appointment.
    - For each appointment up to the given date:
        - If underpaid, creates a new payment for the remaining amount.
        - If overpaid, adjusts existing payments to match the appointment cost.
    """
    engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    db_path = engine.url.database
    if not dry_run:
        if not backup_database(db_path, logger=logger):
            logger.warning("Failed to create a backup. Aborting script.")
            return

    db = session_local()

    try:
        reconciliation_date = datetime.strptime(date_str, "%Y-%m-%d").date()  # noqa: DTZ007

        report = {
            "orphan_payments_removed": [],
            "overpaid": [],
            "underpaid": [],
            "balanced": [],
            "summary": {
                "orphan_removed": 0,
                "overpaid_adjusted": 0,
                "underpaid_created": 0,
                "balanced": 0,
            },
        }

        # 1. Remove orphan payments (not associated with any appointment)
        logger.info("--- Step 1: Removing orphan payments ---")
        orphan_payments_query = select(Payment).where(Payment.appointment_id.is_(None))
        orphan_payments = db.execute(orphan_payments_query).scalars().all()

        if orphan_payments:
            for payment in orphan_payments:
                action = (
                    f"Deleted orphan payment {payment.id} of amount {payment.amount} "
                    f"from date {payment.payment_date.date()}."
                )
                report["orphan_payments_removed"].append(action)
                if not dry_run:
                    db.delete(payment)
            report["summary"]["orphan_removed"] = len(orphan_payments)
        logger.info(f"Found and removed {len(orphan_payments)} orphan payments.")

        # 2. Reconcile payments per appointment
        logger.info("\n--- Step 2: Reconciling payments per appointment ---")

        default_payment_method = (
            db.execute(select(PaymentMethod).where(PaymentMethod.is_active.is_(True))).scalars().first()
        )
        if not default_payment_method:
            raise ValueError("No active payment method found. Cannot create new payments for underpaid appointments.")  # noqa: TRY301

        appointments_query = select(Appointment).where(func.date(Appointment.start_time) <= reconciliation_date)
        appointments = db.execute(appointments_query).scalars().all()

        for appt in appointments:
            total_paid = sum(p.amount for p in appt.payments)
            balance = total_paid - appt.cost

            if balance < 0:
                # Underpaid
                amount_due = -balance
                action = (
                    f"Appointment {appt.id} (cost: {appt.cost}, paid: {total_paid}):"
                    f"created payment for remaining {amount_due}."
                )
                report["underpaid"].append(action)
                report["summary"]["underpaid_created"] += 1

                if not dry_run:
                    new_payment = Payment(
                        amount=amount_due,
                        payment_date=datetime.now(UTC),
                        payment_method_id=default_payment_method.id,
                        appointment_id=appt.id,
                        patient_id=appt.patient_id,
                    )
                    db.add(new_payment)

            elif balance > 0:
                # Overpaid
                amount_to_adjust = balance
                actions = []
                report["summary"]["overpaid_adjusted"] += 1

                sorted_payments = sorted(appt.payments, key=lambda p: p.payment_date, reverse=True)

                for payment in sorted_payments:
                    if amount_to_adjust <= 0:
                        break

                    if payment.amount > amount_to_adjust:
                        action = (
                            f"Reduced payment {payment.id} (amount {payment.amount}) by "
                            f"{amount_to_adjust} to {payment.amount - amount_to_adjust}."
                        )
                        actions.append(action)
                        if not dry_run:
                            payment.amount -= amount_to_adjust
                        amount_to_adjust = 0
                    else:
                        action = f"Deleted payment {payment.id} of amount {payment.amount}."
                        actions.append(action)
                        if not dry_run:
                            db.delete(payment)
                        amount_to_adjust -= payment.amount

                report["overpaid"].append({"appointment_id": appt.id, "overpaid_amount": balance, "actions": actions})

            else:
                # Balanced
                report["balanced"].append(f"Appointment {appt.id} (cost: {appt.cost}) is balanced.")
                report["summary"]["balanced"] += 1

        if not dry_run:
            logger.info("Committing changes to the database...")
            db.commit()
        else:
            logger.info("Dry run complete. No changes were made.")

        # Print report
        logger.info("\n--- Payment Reconciliation Report ---")
        logger.info(f"Reconciliation Date: {reconciliation_date}")
        logger.info(f"Dry Run: {dry_run}\n")

        logger.info(
            f"Summary: {report['summary']['orphan_removed']} orphan payments removed, "
            f"{report['summary']['underpaid_created']} underpaid appointments fixed, "
            f"{report['summary']['overpaid_adjusted']} overpaid appointments fixed, "
            f"{report['summary']['balanced']} appointments already balanced."
        )

        if report["orphan_payments_removed"]:
            logger.info("\n--- Orphan Payments Removed ---")
            for action in report["orphan_payments_removed"]:
                logger.info(f"  - {action}")

        if report["underpaid"]:
            logger.info("\n--- Underpaid Appointments Fixed ---")
            for action in report["underpaid"]:
                logger.info(f"  - {action}")

        if report["overpaid"]:
            logger.info("\n--- Overpaid Appointments Adjusted ---")
            for item in report["overpaid"]:
                logger.info(f"\n  Appointment: {item['appointment_id']} (Overpaid by: {item['overpaid_amount']})")
                for action in item["actions"]:
                    logger.info(f"    - {action}")

    except Exception:
        logger.exception("An error occurred during reconciliation")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reconcile appointment payments.")
    parser.add_argument("--date", required=True, help="Reconciliation date in YYYY-MM-DD format.")
    parser.add_argument("--dry-run", action="store_true", help="Perform a dry run without making changes.")
    args = parser.parse_args()

    reconcile_payments(args.date, dry_run=args.dry_run)
