from sqlalchemy import DateTime, ForeignKey, Integer, String, Time, func
from sqlalchemy.ext.asyncio import (AsyncAttrs, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import (DeclarativeBase, Mapped, declared_attr,
                            mapped_column, relationship)

from ad_looper.config import settings


class Base(AsyncAttrs, DeclarativeBase):
    pass


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


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    password: Mapped[str] = mapped_column(String)

    media: Mapped[list["Media"]] = relationship(
        "Media", back_populates="owner"
    )
    media_groups: Mapped[list["MediaGroup"]] = relationship(
        "MediaGroup", back_populates="owner"
    )
    display_devices: Mapped[list["DisplayDevice"]] = relationship(
        "DisplayDevice", back_populates="owner"
    )


class DisplayDevice(Base, Owned, TimestampMixin):
    __tablename__ = "display_devices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(String)

    owner: Mapped["User"] = relationship(
        "User", back_populates="display_devices"
    )


class Media(Base, Owned, TimestampMixin):
    __tablename__ = "media"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String)
    filename: Mapped[str] = mapped_column(String, nullable=True)

    owner: Mapped["User"] = relationship("User", back_populates="media")
    media_groups: Mapped[list["MediaGroup"]] = relationship(
        "MediaGroup",
        secondary="media_group_media",
        back_populates="media_items",
    )
    schedules: Mapped[list["Schedule"]] = relationship(
        "Schedule", back_populates="media"
    )


class MediaGroup(Base, Owned, TimestampMixin):
    __tablename__ = "media_groups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String)

    owner: Mapped["User"] = relationship("User", back_populates="media_groups")
    media_items: Mapped[list["Media"]] = relationship(
        "Media",
        secondary="media_group_media",
        back_populates="media_groups",
    )
    schedules: Mapped[list["Schedule"]] = relationship(
        "Schedule", back_populates="media_group"
    )


class MediaGroupMedia(Base):
    __tablename__ = "media_group_media"

    media_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("media.id"), primary_key=True
    )
    media_group_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("media_groups.id"),
        primary_key=True,
    )


class Schedule(Base, TimestampMixin):
    __tablename__ = "schedules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    trigger_time: Mapped[Time] = mapped_column(Time)

    media_id: Mapped[int] = mapped_column(Integer, ForeignKey("media.id"))
    media_group_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("media_groups.id")
    )

    media: Mapped["Media"] = relationship("Media", back_populates="schedules")
    media_group: Mapped["MediaGroup"] = relationship(
        "MediaGroup", back_populates="schedules"
    )


# Configure your database URL here
DATABASE_URL = settings.db.url

async_engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
)
