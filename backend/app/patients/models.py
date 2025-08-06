import sqlalchemy as sa
from sqlalchemy.types import Date, Numeric, String, Text

from app.db.base import Base


class Patient(Base):
    __tablename__ = "patients"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    name = sa.Column(String(255), nullable=False)
    dob = sa.Column(Date)

    # This will store the encrypted medical history as a string.
    # The actual encryption/decryption will be handled at the application level.
    encrypted_medical_history = sa.Column(Text)

    email = sa.Column(String(255), unique=True, index=True)
    cellphone = sa.Column(String(50), unique=True, index=True)
    phone = sa.Column(String(50))
    address = sa.Column(Text)

    # To track credit/debt. Positive for credit, negative for debt.
    credit_balance = sa.Column(Numeric(10, 2), nullable=False, server_default="0.00")
