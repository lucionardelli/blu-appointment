import csv
import logging
import re
from datetime import date

from sqlalchemy.orm import Session
from app.specialties.models import Specialty

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def determine_phone_type(phone: str) -> str:
    """Determine if a phone number is cellphone or landline.
    Currently always returns 'cellphone'
    """
    return "cellphone"


def clean_phone_number(phone: str) -> str | None:
    """Clean and format phone number"""
    if not phone or not str(phone).strip():
        return None

    # Remove common separators and spaces
    cleaned = re.sub(r"[-\s\(\)\.]", "", str(phone).strip())

    # Return None if empty after cleaning or contains non-digits
    if not cleaned or not cleaned.replace("+", "").isdigit():
        return None

    return cleaned


def parse_year_to_date(year_value: int | str | None) -> date | None:
    """Convert year to January 1st of that year"""
    if not year_value or not str(year_value).strip():
        return None

    try:
        year = int(float(str(year_value).strip()))
        # Validate reasonable year range
        if 1900 <= year <= 2025:
            return date(year, 1, 1)
        logger.warning(f"Year {year} is outside reasonable range")
        return None
    except (ValueError, TypeError):
        logger.warning(f"Could not parse year: {year_value}")
        return None


def is_empty(value) -> bool:
    """Check if a value is empty or just whitespace."""
    return not value or not str(value).strip()


def parse_emergency_contact_data(row: list[str]) -> list[dict]:
    """Parse emergency contact data from columns G-K (indices 6-10)"""
    emergency_contacts = []

    try:
        # Get emergency contact data from columns G-K (indices 6-10)
        g_col = row[6] if len(row) > 6 else ""
        h_col = row[7] if len(row) > 7 else ""
        i_col = row[8] if len(row) > 8 else ""
        j_col = row[9] if len(row) > 9 else ""
        k_col = row[10] if len(row) > 10 else ""

        # Create full name from columns G and H
        name_parts = []
        if not is_empty(g_col):
            name_parts.append(str(g_col).strip())
        if not is_empty(h_col):
            name_parts.append(str(h_col).strip())

        full_name = " ".join(name_parts) if name_parts else None

        # Get relationship from column I
        relationship = str(i_col).strip().lower() if not is_empty(i_col) else None

        # Clean phone numbers from columns J and K
        phone_j = clean_phone_number(j_col)
        phone_k = clean_phone_number(k_col)

        # Determine phone assignments
        cellphone = None
        phone = None

        if phone_j and phone_k:
            # If we have both, J is cellphone, K is phone
            cellphone = phone_j
            phone = phone_k
        elif phone_j:
            # Only J, assume it's cellphone
            cellphone = phone_j
        elif phone_k:
            # Only K, assume it's cellphone
            cellphone = phone_k

        # Only create emergency contact if we have at least a name
        if full_name:
            emergency_contact = {
                "full_name": full_name,
                "patient_relationship": relationship,
                "cellphone": cellphone,
                "phone_number": phone,
                "priority": 0,
            }
            emergency_contacts.append(emergency_contact)

    except Exception as e:
        logger.error(f"Error parsing emergency contact data: {e}")

    return emergency_contacts


def clean_string(name: str | None, title:bool = True) -> str | None:
    """Clean and format full name"""
    if not name or not str(name).strip():
        return None

    # Remove leading/trailing whitespace and normalize spaces
    cleaned_name = " ".join(str(name).strip().split())

    # Check if the cleaned name is empty
    if not cleaned_name:
        return None

    if title:
        cleaned_name = cleaned_name.title()
    return cleaned_name


def clean_email(email: str | None) -> str | None:
    """Clean and validate email address"""
    if not email or not str(email).strip():
        return None

    # Remove leading/trailing whitespace
    cleaned_email = str(email).strip()

    # Basic validation for email format
    if "@" in cleaned_email and "." in cleaned_email:
        return cleaned_email.lower()  # Normalize to lowercase
    else:
        logger.debug(f"Invalid email format: {cleaned_email}")
        return None

def get_blu_specialty_id(db: Session) -> int:
    # Look for bluroom specialty
    bluroom = db.query(Specialty).filter(Specialty.name.ilike("%bluroom%")).first()
    if not bluroom:
        logger.error("Bluroom specialty not found in database!")
        raise ValueError("Required specialty 'bluroom' not found")
    logger.info("Found Bluroom specialty: %s (ID: %d)", bluroom.name, bluroom.id)
    return bluroom.id


def import_patients_from_csv(file_path: str, db: Session):
    """Import patients from CSV file into database.

    Expected CSV columns:
    0: APELLIDO Y NOMBRE
    1: AÑO NAC.
    2: EDAD
    3: ORIGEN
    4: TELEFONO
    5: MAIL
    6: (empty column)
    7: (empty column)
    8: (empty column)
    9-13: CONTACTO DE EMERGENCIA columns (G-K)

    Args:
        file_path: Path to the CSV file
        db: SQLAlchemy database session

    """
    try:
        logger.info(f"Reading CSV file: {file_path}")

        successful_imports = 0
        sucessful_updates = 0
        failed_imports = 0
        blu_specialty_id = get_blu_specialty_id(db)

        with open(file_path, encoding="utf-8", newline="") as csvfile:
            reader = csv.reader(csvfile)

            # Skip header row
            headers = next(reader, None)
            if headers:
                logger.debug(f"CSV headers: {headers}")

            for row_num, row in enumerate(reader, start=2):  # Start at 2 because of header
                try:
                    # Pad row with empty strings if it's shorter than expected
                    while len(row) < 11:
                        row.append("")

                    # Extract data from columns
                    full_name = clean_string(row[0])
                    birth_year = row[1] if row[1] else None
                    # age = row[2] if row[2] else None
                    origin = clean_string(row[3])
                    telefono = row[4] if row[4] else None
                    email = clean_email(row[5])

                    # Skip if no name
                    if not full_name:
                        logger.warning(f"Row {row_num}: Skipping - no name provided")
                        failed_imports += 1
                        continue

                    # Convert birth year to date
                    dob = parse_year_to_date(birth_year)

                    # Clean phone number and determine type
                    cleaned_phone = clean_phone_number(telefono)
                    phone_type = determine_phone_type(telefono) if cleaned_phone else None

                    # Assign phone to appropriate field
                    cellphone = cleaned_phone if phone_type == "cellphone" else None
                    phone = cleaned_phone if phone_type == "phone" else None

                    # Parse emergency contacts
                    emergency_contacts_data = parse_emergency_contact_data(row)

                    # Create Patient data
                    patient_data = {
                        "name": full_name,
                        "dob": dob,
                        "email": email,
                        "cellphone": cellphone,
                        "phone": phone,
                        "how_they_found_us": origin,
                        "default_specialty_id": blu_specialty_id,
                    }

                    # Remove None values
                    patient_data = {k: v for k, v in patient_data.items() if v is not None}

                    logger.debug(f"Row {row_num}: Creating patient - {full_name}")
                    logger.debug(f"Patient data: {patient_data}")

                    patient = db.query(Patient).filter_by(name=full_name).first()
                    if patient is not None:
                        logger.debug(f"  Patient {full_name} already exists. Updating record.")
                        try:
                            for key, value in patient_data.items():
                                setattr(patient, key, value)
                            db.flush()
                        except Exception as e:
                            logger.debug(f"Row {row_num}: Error updating patient object - {e!s}")
                            raise
                        sucessful_updates += 1
                    else:
                        try:
                            patient = Patient(**patient_data)
                            db.add(patient)
                            db.flush()
                            successful_imports += 1
                        except Exception as e:
                            logger.debug(f"Row {row_num}: Error creating patient object - {e!s}")
                            raise

                    # Create emergency contacts
                    for ec_data in emergency_contacts_data:
                        logger.debug(f"  Adding emergency contact: {ec_data['full_name']}")
                        logger.debug(f"  Emergency contact data: {ec_data}")

                        ec_data['patient_id'] = patient.id
                        try:
                            emergency_contact = EmergencyContact(**ec_data)
                            db.add(emergency_contact)
                            db.flush()
                        except Exception as e:
                            logger.debug(f"Row {row_num}: Error creating emergency contact - {e!s}")
                            raise


                except Exception as e:
                    logger.error(f"Row {row_num}: Failed to import patient - {e!s}")
                    failed_imports += 1
                    # db.rollback()  # Rollback the failed transaction
                    continue

        logger.info(f"Import completed. Successful: {successful_imports}, Updated: {sucessful_updates}, Failed: {failed_imports}")

    except Exception as e:
        logger.error(f"Error reading CSV file: {e!s}")
        raise


if __name__ == "__main__":
    from app.patients.models import Patient, EmergencyContact
    from app.db.base import get_db_context
    with get_db_context() as db:
        import_patients_from_csv("./patients.csv", db)
        db.commit()
