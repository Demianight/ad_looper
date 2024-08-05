from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database.models import Media

from .schemas import MediaCreate, MediaUpdate


async def create_media(
    db: AsyncSession, media: MediaCreate, owner_id: int
) -> Media:
    db_media = Media(name=media.name, owner_id=owner_id)
    db.add(db_media)
    await db.commit()
    await db.refresh(db_media)
    return db_media


async def get_media(db: AsyncSession, **kwargs) -> Media:
    query = select(Media)
    for key, value in kwargs.items():
        if hasattr(Media, key):
            query = query.filter(getattr(Media, key) == value)
        else:
            raise HTTPException(status_code=400, detail="Invalid filter")

    result = await db.execute(query)
    db_media = result.scalars().first()
    if db_media is None:
        raise HTTPException(status_code=404, detail="Media not found")
    return db_media


async def get_media_list(db: AsyncSession, **kwargs):
    query = select(Media)
    for key, value in kwargs.items():
        if hasattr(Media, key):
            query = query.filter(getattr(Media, key) == value)
        else:
            raise HTTPException(status_code=400, detail="Invalid filter")

    result = await db.execute(query)
    return result.scalars().all()


async def update_media(
    db: AsyncSession, media_id: int, media_update: MediaUpdate
) -> Media:
    query = select(Media).filter(Media.id == media_id)
    result = await db.execute(query)
    db_media = result.scalars().first()
    if db_media is None:
        raise HTTPException(status_code=404, detail="Media not found")

    if media_update.name is not None:
        db_media.name = media_update.name

    db.add(db_media)
    await db.commit()  # Commit the transaction
    await db.refresh(db_media)  # Refresh the media instance
    return db_media


async def set_media_filename(
    db: AsyncSession, media_id: int, filename: str
) -> Media:
    db_media = await get_media(db, id=media_id)
    if db_media is None:
        raise HTTPException(status_code=404, detail="Media not found")

    db_media.filename = filename
    db.add(db_media)
    await db.commit()  # Commit the transaction
    await db.refresh(db_media)  # Refresh the media instance
    return db_media


async def delete_media(db: AsyncSession, media_id: int) -> None:
    db_media = await get_media(db, id=media_id)
    if db_media is None:
        raise HTTPException(status_code=404, detail="Media not found")

    await db.delete(db_media)
    await db.commit()  # Commit the transaction
