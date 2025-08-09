import sqlalchemy as sa
from sqlalchemy import Enum

from app.common.enums import Language
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    username = sa.Column(sa.String, unique=True, index=True, nullable=False)
    hashed_password = sa.Column(sa.String, nullable=False)
    default_timezone = sa.Column(sa.String, nullable=False, server_default="UTC")
    language = sa.Column(Enum(Language), nullable=False, server_default=Language.ENGLISH.value)
