from sqlalchemy.orm import Session
from fastapi import HTTPException
from database.models import User
from .schemas import UserCreate, UserUpdate


def create_user(db: Session, user: UserCreate) -> User:
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already exists.")
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already exists.")

    db_user = User(username=user.username, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int) -> User:
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


def get_user_by_username(db: Session, username: str) -> User:
    db_user = db.query(User).filter(User.username == username).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


def get_all_users(db: Session) -> list[User]:
    return db.query(User).all()


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
        db_user.username = user_update.username

    if user_update.email is not None and user_update.email != db_user.email:
        if db.query(User).filter(User.email == user_update.email).first():
            raise HTTPException(
                status_code=400, detail="Email already exists."
            )
        db_user.email = user_update.email

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> None:
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
