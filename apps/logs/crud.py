from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database.models import Log


async def create_log(
    db: AsyncSession,
    url: str,
    method: str,
    status_code: int,
    device_id: int,
) -> Log:
    db_log = Log(
        url=url, method=method, status_code=status_code, device_id=device_id
    )
    db.add(db_log)
    await db.commit()
    await db.refresh(db_log)
    return db_log


async def get_log(db: AsyncSession, **kwargs) -> Log:
    query = select(Log)
    for key, value in kwargs.items():
        if hasattr(Log, key):
            query = query.filter(getattr(Log, key) == value)
        else:
            raise HTTPException(status_code=400, detail="Invalid filter")

    result = await db.execute(query)
    db_log = result.scalars().first()
    if db_log is None:
        raise HTTPException(status_code=404, detail="Log not found")
    return db_log


async def get_log_list(db: AsyncSession, **kwargs):
    query = select(Log)
    for key, value in kwargs.items():
        if hasattr(Log, key):
            query = query.filter(getattr(Log, key) == value)
        else:
            raise HTTPException(status_code=400, detail="Invalid filter")

    result = await db.execute(query)
    return result.scalars().all()


async def delete_log(db: AsyncSession, log_id: int) -> None:
    db_log = await get_log(db, id=log_id)
    if db_log is None:
        raise HTTPException(status_code=404, detail="Log not found")

    await db.delete(db_log)
    await db.commit()  # Commit the transaction
