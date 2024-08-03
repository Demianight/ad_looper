from sqlalchemy.orm import Session
from fastapi import HTTPException
from apps.users.utils import hash_password
from database.models import User
from .schemas import UserCreate, UserUpdate


def create_user(db: Session, user: UserCreate) -> User:
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already exists.")
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already exists.")

    db_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password.get_secret_value()),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, **kwargs) -> User:
    query = db.query(User)
    for key, value in kwargs.items():
        try:
            query = query.filter(getattr(User, key) == value)
        except AttributeError:
            raise HTTPException(status_code=400, detail="Invalid filter")

    db_user = query.first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_users(db: Session, **kwargs):
    query = db.query(User)
    for key, value in kwargs.items():
        query = query.filter(getattr(User, key) == value)
    return query


def update_user(db: Session, user_id: int, user_update: UserUpdate) -> User:
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if (
        user_update.username is not None
        and user_update.username != db_user.username
    ):
        if (
            db.query(User)
            .filter(User.username == user_update.username)
            .first()
        ):
            raise HTTPException(
                status_code=400, detail="Username already exists."
            )
        db_user.username = user_update.username  # type: ignore

    if user_update.email is not None and user_update.email != db_user.email:
        if db.query(User).filter(User.email == user_update.email).first():
            raise HTTPException(
                status_code=400, detail="Email already exists."
            )
        db_user.email = user_update.email  # type: ignore

    if user_update.password is not None:
        db_user.password = hash_password(  # type: ignore
            user_update.password.get_secret_value()
        )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> None:
    db_user = get_user(db, id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
