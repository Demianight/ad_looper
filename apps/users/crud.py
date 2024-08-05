from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.auth.utils import hash_password
from database.models import User

from .schemas import UserCreate, UserUpdate


async def create_user(db: AsyncSession, user: UserCreate) -> User:
    query = select(User).filter(User.username == user.username)
    result = await db.execute(query)
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Username already exists.")

    query = select(User).filter(User.email == user.email)
    result = await db.execute(query)
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Email already exists.")
    db_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password.get_secret_value()),
    )

    # Add user and commit transaction
    db.add(db_user)
    await db.commit()  # Commit the transaction

    # Refresh the user instance
    await db.refresh(db_user)
    return db_user


async def get_user(db: AsyncSession, **kwargs) -> User:
    query = select(User)
    for key, value in kwargs.items():
        if hasattr(User, key):
            query = query.filter(getattr(User, key) == value)
        else:
            raise HTTPException(status_code=400, detail="Invalid filter")

    result = await db.execute(query)
    db_user = result.scalars().first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


async def get_users(db: AsyncSession, **kwargs):
    query = select(User)
    for key, value in kwargs.items():
        if hasattr(User, key):
            query = query.filter(getattr(User, key) == value)
        else:
            raise HTTPException(status_code=400, detail="Invalid filter")

    result = await db.execute(query)
    return result.scalars().all()


async def update_user(
    db: AsyncSession, user_id: int, user_update: UserUpdate
) -> User:
    query = select(User).filter(User.id == user_id)
    result = await db.execute(query)
    db_user = result.scalars().first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if username or email already exists
    if (
        user_update.username is not None
        and user_update.username != db_user.username
    ):
        query = select(User).filter(User.username == user_update.username)
        result = await db.execute(query)
        if result.scalars().first():
            raise HTTPException(
                status_code=400, detail="Username already exists."
            )
        db_user.username = user_update.username

    if user_update.email is not None and user_update.email != db_user.email:
        query = select(User).filter(User.email == user_update.email)
        result = await db.execute(query)
        if result.scalars().first():
            raise HTTPException(
                status_code=400, detail="Email already exists."
            )
        db_user.email = user_update.email

    if user_update.password is not None:
        db_user.password = hash_password(
            user_update.password.get_secret_value()
        )

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def delete_user(db: AsyncSession, user_id: int) -> None:
    db_user = await get_user(db, id=user_id)
    await db.delete(db_user)
    await db.commit()
