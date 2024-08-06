from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import (
    Mapped,
    declared_attr,
    mapped_column,
)


class TimestampMixin:
    @declared_attr
    def created_at(cls) -> Mapped[DateTime]:
        return mapped_column(DateTime, default=func.now(), nullable=False)

    @declared_attr
    def updated_at(cls) -> Mapped[DateTime]:
        return mapped_column(
            DateTime, default=func.now(), onupdate=func.now(), nullable=False
        )


class Owned:
    @declared_attr
    def owner_id(cls) -> Mapped[int]:
        return mapped_column(Integer, ForeignKey("users.id"))


class TokenBase(TimestampMixin):
    @declared_attr
    def token(cls) -> Mapped[str]:
        return mapped_column(unique=True, nullable=False)

    @declared_attr
    def token_type(cls) -> Mapped[str]:
        return mapped_column(nullable=False)

    @declared_attr
    def is_active(cls) -> Mapped[bool]:
        return mapped_column(default=True)

    @declared_attr
    def expires_at(cls) -> Mapped[datetime]:
        return mapped_column(nullable=False)
