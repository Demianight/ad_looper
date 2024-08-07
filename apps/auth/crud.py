from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import DeviceToken, Token


async def create_token(
    db: AsyncSession,
    token: str,
    token_type: str,
    expires_at: datetime,
    owner_id: int,
) -> Token:
    db_token = Token(
        token=token,
        token_type=token_type,
        expires_at=expires_at,
        owner_id=owner_id,
    )
    db.add(db_token)
    await db.commit()
    await db.refresh(db_token)
    return db_token


async def get_token(db: AsyncSession, **kwargs) -> Token:
    query = select(Token)
    for key, value in kwargs.items():
        if hasattr(Token, key):
            query = query.filter(getattr(Token, key) == value)
        else:
            raise HTTPException(status_code=400, detail="Invalid filter")
    result = await db.execute(query)
    db_token = result.scalars().first()
    if db_token is None:
        raise HTTPException(status_code=404, detail="Token not found")
    return db_token


async def get_tokens(db: AsyncSession, **kwargs):
    query = select(Token)
    for key, value in kwargs.items():
        if hasattr(Token, key):
            query = query.filter(getattr(Token, key) == value)
        else:
            raise HTTPException(status_code=400, detail="Invalid filter")
    result = await db.execute(query)
    return result.scalars().all()


async def update_token(db: AsyncSession, token_id: int, **kwargs) -> Token:
    query = select(Token).filter(Token.id == token_id)
    result = await db.execute(query)
    db_token = result.scalars().first()
    if db_token is None:
        raise HTTPException(status_code=404, detail="Token not found")
    for key, value in kwargs.items():
        if hasattr(db_token, key):
            setattr(db_token, key, value)
        else:
            raise HTTPException(status_code=400, detail="Invalid attribute")
    db.add(db_token)
    await db.commit()
    await db.refresh(db_token)
    return db_token


async def delete_token(db: AsyncSession, token_id: int) -> None:
    db_token = await get_token(db, id=token_id)
    await db.delete(db_token)
    await db.commit()


async def create_device_token(
    db: AsyncSession,
    token: str,
    expires_at: datetime,
    token_type: str,
    display_device_id: int,
    owner_id: int,
) -> DeviceToken:
    db_device_token = DeviceToken(
        token=token,
        expires_at=expires_at,
        display_device_id=display_device_id,
        token_type=token_type,
        owner_id=owner_id,
    )
    db.add(db_device_token)
    await db.commit()
    await db.refresh(db_device_token)
    return db_device_token


async def device_token_exists(
    async_session: AsyncSession, display_device_id: int
) -> bool:
    stmt = select(
        exists().where(DeviceToken.display_device_id == display_device_id)
    )
    result = await async_session.execute(stmt)
    return result.scalar()


async def get_device_token(db: AsyncSession, **kwargs) -> DeviceToken:
    query = select(DeviceToken)
    for key, value in kwargs.items():
        if hasattr(DeviceToken, key):
            query = query.filter(getattr(DeviceToken, key) == value)
        else:
            raise HTTPException(status_code=400, detail="Invalid filter")
    result = await db.execute(query)
    db_device_token = result.scalars().first()
    if db_device_token is None:
        raise HTTPException(status_code=404, detail="DeviceToken not found")
    return db_device_token


async def get_device_tokens(db: AsyncSession, **kwargs):
    query = select(DeviceToken)
    for key, value in kwargs.items():
        if hasattr(DeviceToken, key):
            query = query.filter(getattr(DeviceToken, key) == value)
        else:
            raise HTTPException(status_code=400, detail="Invalid filter")
    result = await db.execute(query)
    return result.scalars().all()


async def update_device_token(
    db: AsyncSession, device_token_id: int, **kwargs
) -> DeviceToken:
    query = select(DeviceToken).filter(DeviceToken.id == device_token_id)
    result = await db.execute(query)
    db_device_token = result.scalars().first()
    if db_device_token is None:
        raise HTTPException(status_code=404, detail="DeviceToken not found")
    for key, value in kwargs.items():
        if hasattr(db_device_token, key):
            setattr(db_device_token, key, value)
        else:
            raise HTTPException(status_code=400, detail="Invalid attribute")
    db.add(db_device_token)
    await db.commit()
    await db.refresh(db_device_token)
    return db_device_token


async def delete_device_token(db: AsyncSession, device_token_id: int) -> None:
    db_device_token = await get_device_token(db, id=device_token_id)
    await db.delete(db_device_token)
    await db.commit()
