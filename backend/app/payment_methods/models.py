import sqlalchemy as sa
from sqlalchemy.types import String

from app.db.base import Base


class PaymentMethod(Base):
    __tablename__ = "payment_methods"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    name = sa.Column(String(255), nullable=False, unique=True)
