from typing import Sequence
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from apps.auth.dependencies import get_request_user
from apps.users import schemas
from . import crud
from apps.dependencies import get_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("")
def get_users(
    username: str | None = None, db: Session = Depends(get_db)
) -> Sequence[schemas.UserResponse]:
    if username:
        users = crud.get_users(db, username=username)
    else:
        users = crud.get_users(db)
    return users.all()


@router.get("/me")
def get_current_user(
    current_user: schemas.UserResponse = Depends(get_request_user),
) -> schemas.UserResponse:
    return current_user


@router.post("", status_code=201)
def create_user(
    user: schemas.UserCreate, db: Session = Depends(get_db)
) -> schemas.UserResponse:
    return crud.create_user(db, user)


@router.get("/{user_id}")
def read_user(
    user_id: int, db: Session = Depends(get_db)
) -> schemas.UserResponse:
    return crud.get_user(db, id=user_id)


@router.put("/{user_id}", status_code=200)
def update_user(
    user_id: int,
    user_update: schemas.UserUpdate,
    db: Session = Depends(get_db),
) -> schemas.UserResponse:
    return crud.update_user(db, user_id, user_update)


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    crud.delete_user(db, user_id)
    return {"detail": "User deleted successfully"}
