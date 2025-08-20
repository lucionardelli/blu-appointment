import csv
import logging
import re
import typing as t
from datetime import date, datetime, time, timedelta
from decimal import Decimal, InvalidOperation
from pathlib import Path

from sqlalchemy.orm import Session

from app.appointments.models import Appointment, AppointmentStatus, Payment, PaymentMethod
from app.patients.models import Patient
from app.specialties.models import Specialty

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def clean_string(value: str | None) -> str | None:
    """Clean and format string values"""
    if not value or not str(value).strip():
        return None
    return str(value).strip()


def normalize_patient_name(name: str) -> str:
    """Normalize patient name to title case"""
    if not name:
        return ""
    return name.strip().title()


def is_all_caps(name: str) -> bool:
    """Check if the patient name is all in uppercase (indicates Bluroom appointment)"""
    if not name:
        return False
    # Remove spaces and check if all alphabetic characters are uppercase
    alpha_chars = "".join(c for c in name if c.isalpha())
    return alpha_chars.isupper() if alpha_chars else False


def parse_currency(value: str | None) -> Decimal | None:
    """Parse currency values from the CSV"""
    if not value or not str(value).strip():
        return None

    # Remove currency symbols and clean the string
    cleaned = re.sub(r"[$,\s]", "", str(value).strip())

    if not cleaned or cleaned == "0":
        return None

    try:
        return Decimal(cleaned)
    except (ValueError, TypeError, InvalidOperation):
        logger.warning("Could not parse currency value: %s", value)
        return None


def parse_time(time_str: str | None) -> time | None:
    """Parse time string in HH:MM format"""
    if not time_str or not str(time_str).strip():
        return None

    try:
        # Handle HH:MM format
        time_parts = str(time_str).strip().split(":")
        if len(time_parts) == 2:  # noqa: PLR2004
            hour = int(time_parts[0])
            minute = int(time_parts[1])
            return time(hour, minute)
    except (ValueError, TypeError):
        logger.warning("Could not parse time: %s", time_str)

    return None


def parse_date_from_column_a(date_str: str | None) -> date | None:
    """Parse date from column A in MM/DD/YYYY format"""
    if not date_str or not str(date_str).strip():
        return None

    try:
        # Handle MM/DD/YYYY format
        date_parts = str(date_str).strip().split("/")
        if len(date_parts) == 3:  # noqa: PLR2004
            month = int(date_parts[0])
            day = int(date_parts[1])
            year = int(date_parts[2])
            return date(year, month, day)
    except (ValueError, TypeError):
        logger.warning("Could not parse date: %s", date_str)

    return None


def find_or_create_patient(db: Session, patient_name: str, specialty_id: int) -> "Patient":
    """Find patient by name (case insensitive) or create new one"""

    normalized_name = normalize_patient_name(patient_name)

    patient = db.query(Patient).filter(Patient.name.ilike(normalized_name)).first()

    if patient:
        if not patient.default_specialty_id:
            patient.default_specialty_id = specialty_id
            logger.debug("Set default specialty for existing patient: %s", patient.name)
        return patient
    logger.debug("Creating new patient: %s", normalized_name)
    patient_data = {"name": normalized_name, "default_specialty_id": specialty_id}
    patient = Patient(**patient_data)
    db.add(patient)
    db.flush()
    return patient


def load_specialties(db: Session) -> dict[str, int]:
    """Load specialties from database"""

    specialties = {}

    # Look for bluroom and therapy specialties
    bluroom = db.query(Specialty).filter(Specialty.name.ilike("%bluroom%")).first()

    therapy = (
        db.query(Specialty).filter(Specialty.name.ilike("%therapy%")).first()
    )

    if bluroom:
        specialties["bluroom"] = bluroom.id
        logger.info("Found Bluroom specialty: %s (ID: %d)", bluroom.name, bluroom.id)
    else:
        logger.error("Bluroom specialty not found in database!")
        raise ValueError("Required specialty 'bluroom' not found")

    if therapy:
        specialties["therapy"] = therapy.id
        logger.info("Found Therapy specialty: %s (ID: %d)", therapy.name, therapy.id)
    else:
        logger.error("Therapy specialty not found in database!")
        raise ValueError("Required specialty 'therapy' not found")

    return specialties


def import_appointments_from_csv(file_path: str, db: Session) -> None:  # noqa: C901, PLR0912, PLR0915
    """Import appointments from CSV file into database.

    Expected CSV columns (0-indexed):
    0: Date in MM/DD/YYYY format - Column A
    1: DÍA (ignored)
    2: # (ignored)
    3: MES (ignored)
    4: HORA (time HH:MM) - Column E
    5: APELLIDO Y NOMBRE (patient name) - Column F
    6: SESION N° (session number) - Column G
    7-10: (various columns, ignored)
    11: A PAGAR (appointment cost) - Column L
    12: EFECTIVO (cash payment) - Column M
    13: TARJETA (card payment) - Column N

    """

    try:
        logger.info("Reading CSV file: %s", file_path)

        specialties = load_specialties(db)

        successful_imports = 0
        failed_imports = 0
        already_exists = 0
        last_appointment_time = None

        file_path = Path(file_path)
        with file_path.open(encoding="utf-8", newline="") as csvfile:
            reader = csv.reader(csvfile)

            # Skip header row
            headers = next(reader, None)
            if headers:
                logger.debug("CSV headers: %s", headers)

            for row_num, row in enumerate(reader, start=2):
                try:
                    # Pad row with empty strings if it's shorter than expected
                    while len(row) < 14:  # noqa: PLR2004
                        row.append("")

                    # Column F (index 5) - Patient name
                    patient_name = clean_string(row[5])

                    # Skip rows with no patient name
                    if not patient_name:
                        logger.debug("Row %s: Skipping - no patient name in column F", row_num)
                        continue

                    # Column E (index 4) - Time
                    time_str = clean_string(row[4])

                    # If no time, use previous time + 15 minutes
                    if not time_str:
                        if last_appointment_time:
                            appointment_time_obj = datetime.combine(date.today(), last_appointment_time) + timedelta(  # noqa: DTZ011
                                minutes=15
                            )
                            appointment_time = appointment_time_obj.time()
                            logger.debug(
                                "Row %s: Using calculated time %s (+15 min from previous)", row_num, appointment_time
                            )
                        else:
                            logger.warning("Row %s: No time specified and no previous time available", row_num)
                            failed_imports += 1
                            continue
                    else:
                        appointment_time = parse_time(time_str)
                        if not appointment_time:
                            logger.warning("Row %s: Could not parse time: %s", row_num, time_str)
                            failed_imports += 1
                            continue

                    # Update last appointment time for next iteration
                    last_appointment_time = appointment_time

                    # Determine specialty based on patient name case
                    if is_all_caps(patient_name):
                        specialty_id = specialties["bluroom"]
                        logger.debug("Row %s: Bluroom appointment (name in caps: %s)", row_num, patient_name)
                    else:
                        specialty_id = specialties["therapy"]
                        logger.debug("Row %s: therapy appointment (name: %s)", row_num, patient_name)

                    # Find or create patient
                    patient = find_or_create_patient(db, patient_name, specialty_id)

                    # Column G (index 6) - Session number
                    session_num_str = clean_string(row[6])
                    if session_num_str:
                        # This is just a sanity check. We don't do anything with the session number
                        # but we log it for potential future use. We need to figure out what was the purpose of this column.
                        if session_num_str.lower() != "no":
                            try:
                                session_num = int(session_num_str)
                                if session_num > 1:
                                    logger.info(
                                        "Row %s: Patient %s consecutive session #%s", row_num, patient.name, session_num
                                    )
                            except (ValueError, TypeError):
                                logger.warning("Row %s: Could not parse session number: %s", row_num, session_num_str)

                    # Column L (index 11) - Appointment cost
                    cost_str = clean_string(row[11])
                    cost = parse_currency(cost_str) or Decimal("0.00")

                    # Column A (index 0) - Date in MM/DD/YYYY format
                    date_str = clean_string(row[0])
                    appointment_date = parse_date_from_column_a(date_str)

                    if not appointment_date:
                        logger.warning("Row %s: Could not parse date from column A: %s", row_num, date_str)
                        failed_imports += 1
                        continue

                    # Create datetime objects
                    start_datetime = datetime.combine(appointment_date, appointment_time)
                    end_datetime = start_datetime + timedelta(minutes=60)  # Default 60-minute sessions

                    # Create appointment data
                    appointment_data = {
                        "start_time": start_datetime,
                        "end_time": end_datetime,
                        "cost": cost,
                        "status": AppointmentStatus.COMPLETED,
                        "patient_id": patient.id,
                        "specialty_id": specialty_id,
                    }

                    existing_appointment = (
                        db.query(Appointment)
                        .filter(
                            Appointment.start_time == start_datetime,
                            Appointment.end_time == end_datetime,
                            Appointment.patient_id == patient.id,
                            Appointment.specialty_id == specialty_id,
                        )
                        .first()
                    )
                    if existing_appointment:
                        logger.debug(
                            "Row %s: Appointment already exists for %s at %s - skipping",
                            row_num,
                            patient.name,
                            start_datetime,
                        )
                        already_exists += 1
                        continue

                    logger.debug("Row %s: Creating appointment for %s at %s", row_num, patient.name, start_datetime)

                    # Create appointment
                    appointment = Appointment(**appointment_data)
                    db.add(appointment)
                    db.flush()  # Get the appointment ID

                    # Column M (index 12) - Cash payment
                    cash_payment = parse_currency(clean_string(row[12]))
                    if cash_payment:
                        cash_payment_data = {
                            "amount": cash_payment,
                            "method": PaymentMethod.CASH,
                            "payment_date": start_datetime,
                            "appointment_id": appointment.id,
                        }
                        logger.debug("  Adding cash payment: $%s", cash_payment)
                        payment = Payment(**cash_payment_data)
                        db.add(payment)

                    # Column N (index 13) - Credit card payment
                    card_payment = parse_currency(clean_string(row[13]))
                    if card_payment:
                        card_payment_data = {
                            "amount": card_payment,
                            "method": PaymentMethod.CREDIT_CARD,
                            "payment_date": start_datetime,
                            "appointment_id": appointment.id,
                        }
                        logger.debug("  Adding card payment: $%s", card_payment)
                        payment = Payment(**card_payment_data)
                        db.add(payment)

                    successful_imports += 1

                except (ValueError, TypeError, AttributeError) as e:
                    logger.error("Row %s: Failed to import appointment - %s", row_num, e)
                    failed_imports += 1
                    db.rollback()  # Rollback the failed transaction
                    continue
                except Exception as e:  # noqa: BLE001
                    logger.error("Row %s: Unexpected error during import - %s", row_num, e)
                    failed_imports += 1
                    db.rollback()
                    continue

        logger.info("Import completed. Successful: %s, Existing appointments: %s, Failed: %s", successful_imports, already_exists, failed_imports)

    except FileNotFoundError as e:
        logger.error("CSV file not found: %s", e)
        raise
    except PermissionError as e:
        logger.error("Permission denied accessing CSV file: %s", e)
        raise
    except UnicodeDecodeError as e:
        logger.error("Error decoding CSV file (encoding issue): %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected error reading CSV file: %s", e)
        raise


if __name__ == "__main__":
    from app.db.base import get_db_context

    with get_db_context() as db:
        import_appointments_from_csv("./appointments.csv", db)
        db.commit()
