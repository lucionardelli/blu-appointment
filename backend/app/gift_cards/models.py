import datetime
import uuid
from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Boolean,
    ForeignKey,
    Table,
    DateTime,
)
from sqlalchemy.orm import relationship
from app.db.base import Base

gift_card_patients = Table(
    "gift_card_patients",
    Base.metadata,
    Column("gift_card_id", Integer, ForeignKey("gift_cards.id")),
    Column("patient_id", Integer, ForeignKey("patients.id")),
)

class GiftCard(Base):
    __tablename__ = "gift_cards"

    id = Column(Integer, primary_key=True, index=True)
    specialty_id = Column(Integer, ForeignKey("specialties.id"), nullable=False)
    number_of_sessions = Column(Integer, nullable=False)
    sessions_left = Column(Integer, nullable=False)
    expiration_date = Column(Date, nullable=False)
    code = Column(String, unique=True, index=True, default=lambda: str(uuid.uuid4()))
    to_patient_id = Column(Integer, ForeignKey("patients.id"), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
    )

    specialty = relationship("Specialty", back_populates="gift_cards")
    to_patient = relationship("Patient", back_populates="gift_cards_received", foreign_keys=[to_patient_id])
    from_patients = relationship(
        "Patient", secondary=gift_card_patients, back_populates="gift_cards_sent"
    )
