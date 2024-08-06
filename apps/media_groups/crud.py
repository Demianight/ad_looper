from typing import Sequence

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database.models import MediaGroup, MediaGroupMedia

from .schemas import MediaGroupCreate, MediaGroupUpdate


async def create_media_group(
    db: AsyncSession, media_group: MediaGroupCreate, owner_id: int
) -> MediaGroup:
    db_media_group = MediaGroup(name=media_group.name, owner_id=owner_id)
    db.add(db_media_group)
    await db.commit()
    await db.refresh(db_media_group)
    return db_media_group


async def get_media_group(db: AsyncSession, **kwargs) -> MediaGroup:
    query = select(MediaGroup)
    for key, value in kwargs.items():
        if hasattr(MediaGroup, key):
            query = query.filter(getattr(MediaGroup, key) == value)
        else:
            raise HTTPException(status_code=400, detail="Invalid filter")

    result = await db.execute(query)
    db_media_group = result.scalars().first()
    if db_media_group is None:
        raise HTTPException(status_code=404, detail="MediaGroup not found")
    return db_media_group


async def get_media_group_list(
    db: AsyncSession, **kwargs
) -> Sequence[MediaGroup]:
    query = select(MediaGroup)
    for key, value in kwargs.items():
        if hasattr(MediaGroup, key):
            query = query.filter(getattr(MediaGroup, key) == value)
        else:
            raise HTTPException(status_code=400, detail="Invalid filter")

    result = await db.execute(query)
    return result.scalars().all()


async def update_media_group(
    db: AsyncSession, media_group_id: int, media_group_update: MediaGroupUpdate
) -> MediaGroup:
    query = select(MediaGroup).filter(MediaGroup.id == media_group_id)
    result = await db.execute(query)
    db_media_group = result.scalars().first()
    if db_media_group is None:
        raise HTTPException(status_code=404, detail="MediaGroup not found")

    if media_group_update.name is not None:
        db_media_group.name = media_group_update.name

    db.add(db_media_group)
    await db.commit()  # Commit the transaction
    await db.refresh(db_media_group)  # Refresh the media group instance
    return db_media_group


async def delete_media_group(db: AsyncSession, media_group_id: int) -> None:
    db_media_group = await get_media_group(db, id=media_group_id)
    if db_media_group is None:
        raise HTTPException(status_code=404, detail="MediaGroup not found")

    await db.delete(db_media_group)
    await db.commit()  # Commit the transaction


async def add_media_to_media_group(
    db: AsyncSession, media_group_id: int, media_id: int
):
    media_group_media_db = MediaGroupMedia(
        media_id=media_id, media_group_id=media_group_id
    )
    db.add(media_group_media_db)
    await db.commit()
    await db.refresh(media_group_media_db)
    return media_group_media_db
