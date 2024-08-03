from typing import Sequence
from fastapi import APIRouter

from apps.users.schemas import UserResponse
from . import crud

from sqlalchemy.orm import Session
from fastapi import Depends
from apps.dependencies import get_db

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
def get_users(db: Session = Depends(get_db)) -> Sequence[UserResponse]:
    return crud.get_all_users(db)
