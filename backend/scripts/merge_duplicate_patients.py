"""A script to find and merge duplicate patient records in the database.

This script will:
1. Create a backup of the database.
2. Find potential duplicate patients based on name similarity.
3. For each pair of potential duplicates, prompt the user to choose which one to keep.
4. Merge the data from the "to-be-removed" patient into the "surviving" patient.
5. Delete the "to-be-removed" patient.
"""

from __future__ import annotations

import argparse
import logging
import sys
from difflib import SequenceMatcher
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

# Add the project root to the Python path to allow importing from 'app'
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.appointments.models import Appointment
from app.core.config import settings
from app.patients.models import (
    EmergencyContact,
    Patient,
    PatientSpecialtyPrice,
)
from app.payments.models import Payment

from scripts.utils import backup_database

# --- Configuration ---
SIMILARITY_THRESHOLD = 0.85  # How similar names must be to be considered a match (0.0 to 1.0)
DB_URL = settings.DATABASE_URL
DB_PATH = DB_URL.split("sqlite:///")[-1]

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def get_db_session() -> tuple[Session, str]:
    """Initializes and returns a new SQLAlchemy database session."""
    engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
    db_path = engine.url.database
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return session_local(), db_path


def find_potential_duplicates(db_session: Session, threshold: float) -> list[tuple[Patient, Patient]]:
    """Finds and returns pairs of patients with similar names."""
    logger.info(f"Searching for potential duplicate patients with similarity threshold: {threshold}...")
    patients: list[Patient] = db_session.query(Patient).all()
    potential_duplicates: list[tuple[Patient, Patient]] = []
    processed_ids: set[int] = set()

    for i in range(len(patients)):
        patient1 = patients[i]
        if patient1.id in processed_ids:
            continue

        # Normalize name for comparison
        name1 = (patient1.name or "").lower().strip()

        for j in range(i + 1, len(patients)):
            patient2 = patients[j]
            if patient2.id in processed_ids:
                continue

            name2 = (patient2.name or "").lower().strip()

            similarity = SequenceMatcher(None, name1, name2).ratio()

            if similarity >= threshold:
                potential_duplicates.append((patient1, patient2))
                # Add both to processed_ids to avoid including them in future pairs
                processed_ids.add(patient1.id)
                processed_ids.add(patient2.id)
                # Once a match is found for patient1, move to the next patient
                break

    logger.info(f"Found {len(potential_duplicates)} potential duplicate pairs.")
    return potential_duplicates


def merge_patients(db_session: Session, surviving_patient: Patient, tbr_patient: Patient) -> None:
    """Merges data from tbr_patient to surviving_patient and deletes tbr_patient."""
    logger.info(f"Merging patient ID {tbr_patient.id} into patient ID {surviving_patient.id}...")

    try:
        # 1. Re-assign Appointments
        db_session.query(Appointment).filter(Appointment.patient_id == tbr_patient.id).update(
            {"patient_id": surviving_patient.id}
        )

        # 2. Re-assign Payments
        db_session.query(Payment).filter(Payment.patient_id == tbr_patient.id).update(
            {"patient_id": surviving_patient.id}
        )

        # 3. Re-assign Emergency Contacts
        db_session.query(EmergencyContact).filter(EmergencyContact.patient_id == tbr_patient.id).update(
            {"patient_id": surviving_patient.id}
        )

        # 4. Re-assign Special Prices (handle potential conflicts)
        for tbr_price in tbr_patient.special_prices:
            # Check if a price for the same specialty already exists for the survivor
            survivor_has_price = (
                db_session.query(PatientSpecialtyPrice)
                .filter_by(patient_id=surviving_patient.id, specialty_id=tbr_price.specialty_id)
                .first()
            )
            if not survivor_has_price:
                tbr_price.patient_id = surviving_patient.id
            else:
                # If conflict, we just delete the TBR price. Could be improved to ask user.
                db_session.delete(tbr_price)

        # 5. Re-assign Referrals (patients referred *by* the TBR patient)
        db_session.query(Patient).filter(Patient.referred_by_patient_id == tbr_patient.id).update(
            {"referred_by_patient_id": surviving_patient.id}
        )

        # 6. Transfer data from TBR to SP if SP's field is empty
        fields_to_transfer = [
            "nickname",
            "email",
            "cellphone",
            "phone",
            "address",
            "how_they_found_us",
            "dob",
            "encrypted_medical_history",
            "referred_by_patient_id",
            "default_specialty_id",
        ]
        for field in fields_to_transfer:
            sp_value = getattr(surviving_patient, field)
            tbr_value = getattr(tbr_patient, field)
            if (sp_value is None or sp_value == "") and (tbr_value is not None and tbr_value != ""):
                setattr(surviving_patient, field, tbr_value)
                logger.info(f"  Transferred '{field}': '{tbr_value}' from TBR to SP.")

        # 7. Delete the to-be-removed patient
        db_session.delete(tbr_patient)

        # 8. Commit the transaction
        db_session.commit()
        logger.info("Merge successful.")

    except Exception:
        logger.exception("An error occurred during the merge")
        logger.info("Rolling back changes.")
        db_session.rollback()


def main() -> None:  # noqa: C901, PLR0912
    """Main function to run the script."""
    parser = argparse.ArgumentParser(description="Find and merge duplicate patient records.")
    parser.add_argument(
        "--count",
        action="store_true",
        help="Only count the number of potential duplicate pairs found and exit.",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=SIMILARITY_THRESHOLD,
        help=f"Similarity threshold for matching names (0.0 to 1.0). Default: {SIMILARITY_THRESHOLD}",
    )
    args = parser.parse_args()

    db, db_path = get_db_session()

    if not Path(db_path).exists():
        logger.error(f"Database not found at '{db_path}'.")
        logger.error("Please ensure the script is run from the correct directory and the DB exists.")
        return

    try:
        if args.count:
            find_potential_duplicates(db, args.threshold)
            return

        logger.info("--- Patient Merge Script ---")

        # 1. Backup the database
        if not backup_database(db_path, logger=logger):
            logger.warning("Failed to create a backup. Aborting script.")
            return

        # 2. Find duplicates
        duplicate_pairs = find_potential_duplicates(db, args.threshold)

        if not duplicate_pairs:
            logger.info("No duplicate patients found.")
            return

        # 3. Interactive merge loop
        for patient1, patient2 in duplicate_pairs:
            logger.info(f"\n{'=' * 50}")
            logger.info("Potential Duplicate Found:")
            logger.info(
                f"1: ID={patient1.id}, Name='{patient1.name}', "
                f"Nickname='{patient1.nickname}', Cell='{patient1.cellphone}'"
            )
            logger.info(
                f"2: ID={patient2.id}, Name='{patient2.name}', "
                f"Nickname='{patient2.nickname}', Cell='{patient2.cellphone}'"
            )
            logger.info("=" * 50)

            choice = ""
            while choice not in ["1", "2", "s", "q"]:
                choice = input("Choose surviving patient (1 or 2), or (s)kip, (q)uit: ").lower().strip()

            if choice == "q":
                logger.info("Quitting.")
                break
            if choice == "s":
                logger.info("Skipping.")
                continue

            surviving_patient = patient1 if choice == "1" else patient2
            tbr_patient = patient2 if choice == "1" else patient1

            confirm = (
                input(
                    f"Are you sure you want to merge '{tbr_patient.name}' (ID: {tbr_patient.id}) "
                    f"into '{surviving_patient.name}' (ID: {surviving_patient.id})? "
                    "This is irreversible. (y/n, default: y): "
                )
                .lower()
                .strip()
            )

            if confirm == "":  # If Enter is pressed, default to 'y'
                confirm = "y"

            if confirm == "y":
                merge_patients(db, surviving_patient, tbr_patient)
            else:
                logger.info("Merge cancelled.")

    finally:
        db.close()
        if not args.count:
            logger.info("Script finished.")


if __name__ == "__main__":
    main()
