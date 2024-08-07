from datetime import time

from sqlalchemy import ForeignKey, Integer, Time
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
    relationship,
)

from ad_looper.config import settings
from database.mixins import Owned, TimestampMixin, TokenBase


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Model(Base):
    __abstract__ = True

    @declared_attr
    def id(cls) -> Mapped[int]:
        return mapped_column(Integer, primary_key=True, index=True)


class Token(Model, TokenBase):
    __tablename__ = "tokens"

    owner: Mapped["User"] = relationship("User", back_populates="tokens")


class DeviceToken(Model, TokenBase):
    __tablename__ = "display_device_tokens"

    display_device_id: Mapped[int] = mapped_column(
        ForeignKey("display_devices.id")
    )

    owner: Mapped["User"] = relationship(
        "User",
        back_populates="display_device_tokens",
        lazy="selectin",
    )
    display_device: Mapped["DisplayDevice"] = relationship(
        "DisplayDevice", back_populates="tokens"
    )


class User(Model):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str]

    media: Mapped[list["Media"]] = relationship(
        "Media",
        back_populates="owner",
        cascade="all, delete-orphan",
    )
    media_groups: Mapped[list["MediaGroup"]] = relationship(
        "MediaGroup",
        back_populates="owner",
        cascade="all, delete-orphan",
    )
    display_devices: Mapped[list["DisplayDevice"]] = relationship(
        "DisplayDevice",
        back_populates="owner",
        cascade="all, delete-orphan",
    )
    schedules: Mapped[list["Schedule"]] = relationship(
        "Schedule",
        back_populates="owner",
        cascade="all, delete-orphan",
    )
    tokens: Mapped[list["Token"]] = relationship(
        "Token",
        back_populates="owner",
        cascade="all, delete-orphan",
    )
    display_device_tokens: Mapped[list["DeviceToken"]] = relationship(
        "DeviceToken",
        back_populates="owner",
        cascade="all, delete-orphan",
    )


class DisplayDevice(Model, Owned, TimestampMixin):
    __tablename__ = "display_devices"

    name: Mapped[str] = mapped_column(index=True)
    description: Mapped[str] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)

    media_group_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("media_groups.id"), nullable=True
    )

    owner: Mapped["User"] = relationship(
        "User",
        back_populates="display_devices",
        lazy="selectin",
    )
    media_group: Mapped["MediaGroup"] = relationship(
        "MediaGroup",
        back_populates="display_devices",
        lazy="selectin",
    )
    tokens: Mapped[list["DeviceToken"]] = relationship(
        "DeviceToken",
        back_populates="display_device",
    )
    logs: Mapped[list["Log"]] = relationship(
        "Log",
        back_populates="device",
        lazy="selectin",
    )


class Media(Model, Owned, TimestampMixin):
    __tablename__ = "media"

    name: Mapped[str]
    filename: Mapped[str] = mapped_column(nullable=True)

    owner: Mapped["User"] = relationship("User", back_populates="media")
    media_groups: Mapped[list["MediaGroup"]] = relationship(
        "MediaGroup",
        secondary="media_group_media",
        back_populates="media_items",
        lazy="selectin",
    )
    schedules: Mapped[list["Schedule"]] = relationship(
        "Schedule",
        back_populates="media",
        lazy="selectin",
    )


class MediaGroup(Model, Owned, TimestampMixin):
    __tablename__ = "media_groups"

    name: Mapped[str]

    owner: Mapped["User"] = relationship(
        "User",
        back_populates="media_groups",
        lazy="selectin",
    )
    media_items: Mapped[list["Media"]] = relationship(
        "Media",
        secondary="media_group_media",
        back_populates="media_groups",
        lazy="selectin",
    )
    schedules: Mapped[list["Schedule"]] = relationship(
        "Schedule",
        back_populates="media_group",
        lazy="selectin",
    )
    display_devices: Mapped[list["DisplayDevice"]] = relationship(
        "DisplayDevice",
        back_populates="media_group",
        lazy="selectin",
    )


class MediaGroupMedia(Base):
    __tablename__ = "media_group_media"

    media_id: Mapped[int] = mapped_column(
        ForeignKey("media.id"), primary_key=True
    )
    media_group_id: Mapped[int] = mapped_column(
        ForeignKey("media_groups.id"),
        primary_key=True,
    )


class Schedule(Model, TimestampMixin, Owned):
    __tablename__ = "schedules"

    trigger_time: Mapped[time] = mapped_column(Time)

    media_id: Mapped[int] = mapped_column(ForeignKey("media.id"))
    media_group_id: Mapped[int] = mapped_column(ForeignKey("media_groups.id"))

    owner: Mapped["User"] = relationship("User", back_populates="schedules")
    media: Mapped["Media"] = relationship("Media", back_populates="schedules")
    media_group: Mapped["MediaGroup"] = relationship(
        "MediaGroup", back_populates="schedules"
    )


class Log(Model, TimestampMixin):
    __tablename__ = "logs"

    url: Mapped[str]
    method: Mapped[str]
    status_code: Mapped[int]

    device_id: Mapped[int] = mapped_column(
        ForeignKey("display_devices.id"), nullable=True
    )

    device: Mapped["DisplayDevice"] = relationship(
        "DisplayDevice", back_populates="logs"
    )


async_engine = create_async_engine(settings.db.url)
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
)
