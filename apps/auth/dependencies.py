from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.auth.schemas import TokenCreate
from apps.auth.utils import verify_password
from apps.common.dependencies import get_db
from database.models import User


async def authenticate_user(
    token_data: TokenCreate,
    db: AsyncSession = Depends(get_db),
) -> User:
    query = select(User).filter(User.username == token_data.username)
    result = await db.execute(query)
    user = result.scalars().first()

    if user and verify_password(
        token_data.password.get_secret_value(),
        user.password,
    ):
        return user
    raise HTTPException(status_code=401, detail="Invalid credentials")
