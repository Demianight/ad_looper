from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database.models import User
from .schemas import UserCreate, UserUpdate


def create_user(db: Session, user: UserCreate) -> User:
    db_user = User(username=user.username, email=user.email)
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
    except IntegrityError:
        db.rollback()
        raise ValueError("Username or email already exists.")
    return db_user


def get_user(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()


def get_all_users(db: Session) -> list[User]:
    return db.query(User).all()


def update_user(
    db: Session, user_id: int, user_update: UserUpdate
) -> User | None:
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        return None
    if user_update.username is not None:
        db_user.username = user_update.username
    if user_update.email is not None:
        db_user.email = user_update.email
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> bool:
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        return False
    db.delete(db_user)
    db.commit()
    return True
