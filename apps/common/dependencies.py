from datetime import datetime

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import AsyncSessionLocal, DeviceToken, Token, User


async def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()


BearerToken = HTTPBearer()


async def get_valid_token(
    raw_token: HTTPAuthorizationCredentials = Depends(BearerToken),
    db: AsyncSession = Depends(get_db),
) -> Token | DeviceToken:
    query1 = select(Token).filter(Token.token == raw_token.credentials)
    result1 = await db.execute(query1)
    user_token = result1.scalars().first()

    query2 = select(DeviceToken).filter(
        DeviceToken.token == raw_token.credentials
    )
    result2 = await db.execute(query2)
    device_token = result2.scalars().first()

    token = user_token or device_token

    if not token or not token.is_active:
        raise HTTPException(status_code=401, detail="Invalid or revoked token")
    if token.token_type != "access":
        raise HTTPException(status_code=401, detail="Access token required")
    if token.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Token expired")
    return token


async def get_request_user(token: Token = Depends(get_valid_token)) -> User:
    return await token.awaitable_attrs.owner
