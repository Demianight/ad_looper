from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.auth.schemas import TokenCreate
from apps.auth.utils import decode_access_token, verify_password
from database.models import AsyncSessionLocal, User


async def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()


BearerToken = HTTPBearer()


async def authenticate_user(
    token_data: TokenCreate,
    db: AsyncSession = Depends(get_db),
) -> str | None:
    query = select(User).filter(User.username == token_data.username)
    result = await db.execute(query)
    user = result.scalars().first()

    if user and verify_password(
        token_data.password.get_secret_value(),
        user.password,
    ):
        return token_data.username
    raise HTTPException(status_code=401, detail="Invalid credentials")


async def get_request_user(
    token: HTTPAuthorizationCredentials = Depends(BearerToken),
    db: AsyncSession = Depends(get_db),
) -> User:
    data = decode_access_token(token.credentials)
    username = data.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")
    query = select(User).filter(User.username == username)
    result = await db.execute(query)
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user
