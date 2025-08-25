from sqlalchemy.orm import Session
from app.gift_cards import models, schemas
from app.patients.models import Patient


class GiftCardService:
    def __init__(self, db: Session):
        self.db = db

    def create_gift_card(self, gift_card: schemas.GiftCardCreate) -> models.GiftCard:
        from_patients = (
            self.db.query(Patient).filter(Patient.id.in_(gift_card.from_patient_ids)).all()
        )
        if len(from_patients) != len(gift_card.from_patient_ids):
            raise ValueError("One or more from_patients not found")

        db_gift_card = models.GiftCard(
            specialty_id=gift_card.specialty_id,
            number_of_sessions=gift_card.number_of_sessions,
            sessions_left=gift_card.number_of_sessions,
            expiration_date=gift_card.expiration_date,
            to_patient_id=gift_card.to_patient_id,
            from_patients=from_patients,
        )
        self.db.add(db_gift_card)
        self.db.commit()
        self.db.refresh(db_gift_card)
        return db_gift_card

    def get_gift_card(self, gift_card_id: int) -> models.GiftCard | None:
        return self.db.query(models.GiftCard).filter(models.GiftCard.id == gift_card_id).first()

    def get_gift_card_by_code(self, code: str) -> models.GiftCard | None:
        return self.db.query(models.GiftCard).filter(models.GiftCard.code == code).first()

    def list_gift_cards(self) -> list[models.GiftCard]:
        return self.db.query(models.GiftCard).all()

    def update_gift_card(
        self, gift_card_id: int, gift_card: schemas.GiftCardUpdate
    ) -> models.GiftCard | None:
        db_gift_card = self.get_gift_card(gift_card_id)
        if not db_gift_card:
            return None

        update_data = gift_card.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_gift_card, key, value)

        self.db.commit()
        self.db.refresh(db_gift_card)
        return db_gift_card

    def deactivate_gift_card(self, gift_card_id: int) -> models.GiftCard | None:
        db_gift_card = self.get_gift_card(gift_card_id)
        if not db_gift_card:
            return None

        db_gift_card.is_active = False
        self.db.commit()
        self.db.refresh(db_gift_card)
        return db_gift_card

    def use_gift_card(self, gift_card: models.GiftCard) -> models.GiftCard:
        if gift_card.sessions_left <= 0:
            raise ValueError("Gift card has no sessions left")

        gift_card.sessions_left -= 1
        if gift_card.sessions_left == 0:
            gift_card.is_active = False

        self.db.commit()
        self.db.refresh(gift_card)
        return gift_card
