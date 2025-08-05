import sqlalchemy as sa
from sqlalchemy.orm import relationship
from app.db.base import Base
from sqlalchemy.types import Date, String, Text, Numeric

class Patient(Base):
    __tablename__ = "patients"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    name = sa.Column(String(255), nullable=False)
    dob = sa.Column(Date)

    # This will store the encrypted medical history as a string.
    # The actual encryption/decryption will be handled at the application level.
    encrypted_medical_history = sa.Column(Text)

    contact_email = sa.Column(String(255), unique=True, index=True)
    contact_phone = sa.Column(String(50))
    contact_address = sa.Column(Text)

    # To track credit/debt. Positive for credit, negative for debt.
    credit_balance = sa.Column(Numeric(10, 2), nullable=False, server_default="0.00")
