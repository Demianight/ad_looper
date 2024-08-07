from typing import Sequence

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database.models import Schedule

from .schemas import ScheduleCreate, ScheduleUpdate


async def create_schedule(
    db: AsyncSession,
    schedule: ScheduleCreate,
    owner_id: int,
) -> Schedule:
    existing_schedule = (
        (
            await db.execute(
                select(Schedule).where(
                    Schedule.media_group_id != schedule.media_group_id,
                    Schedule.media_id == schedule.media_id,
                )
            )
        )
        .scalars()
        .first()
    )
    if existing_schedule is not None:
        raise HTTPException(
            status_code=400,
            detail="A schedule already exists in a different media group",
        )

    db_schedule = Schedule(
        trigger_time=schedule.trigger_time,
        media_id=schedule.media_id,
        media_group_id=schedule.media_group_id,
        owner_id=owner_id,
    )
    db.add(db_schedule)
    await db.commit()
    await db.refresh(db_schedule)
    return db_schedule


async def get_schedule(db: AsyncSession, **kwargs) -> Schedule:
    query = select(Schedule)
    for key, value in kwargs.items():
        if hasattr(Schedule, key):
            query = query.filter(getattr(Schedule, key) == value)
        else:
            raise HTTPException(status_code=400, detail="Invalid filter")

    result = await db.execute(query)
    db_schedule = result.scalars().first()
    if db_schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return db_schedule


async def get_schedule_list(db: AsyncSession, **kwargs) -> Sequence[Schedule]:
    query = select(Schedule)
    for key, value in kwargs.items():
        if hasattr(Schedule, key):
            query = query.filter(getattr(Schedule, key) == value)
        else:
            raise HTTPException(status_code=400, detail="Invalid filter")

    result = await db.execute(query)
    return result.scalars().all()


async def update_schedule(
    db: AsyncSession, schedule_id: int, schedule_update: ScheduleUpdate
) -> Schedule:
    query = select(Schedule).filter(Schedule.id == schedule_id)
    result = await db.execute(query)
    db_schedule = result.scalars().first()
    if db_schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")

    if schedule_update.trigger_time is not None:
        db_schedule.trigger_time = schedule_update.trigger_time
    if schedule_update.media_id is not None:
        db_schedule.media_id = schedule_update.media_id
    if schedule_update.media_group_id is not None:
        db_schedule.media_group_id = schedule_update.media_group_id

    db.add(db_schedule)
    await db.commit()  # Commit the transaction
    await db.refresh(db_schedule)  # Refresh the schedule instance
    return db_schedule


async def delete_schedule(db: AsyncSession, schedule_id: int) -> None:
    db_schedule = await get_schedule(db, id=schedule_id)
    if db_schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")

    await db.delete(db_schedule)
    await db.commit()  # Commit the transaction
