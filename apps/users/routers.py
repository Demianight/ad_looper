from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.common.dependencies import get_db, get_request_user
from apps.users import schemas
from database.models import User

from . import crud

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me")
def read_current_user(
    current_user: schemas.UserResponse = Depends(get_request_user),
) -> schemas.UserResponse:
    return current_user


@router.post("", status_code=201)
async def create_user(
    user: schemas.UserCreate, db: AsyncSession = Depends(get_db)
) -> schemas.UserResponse:
    return await crud.create_user(db, user)


@router.get("/{user_id}")
async def read_user(
    user_id: int, db: AsyncSession = Depends(get_db)
) -> schemas.UserResponse:
    return await crud.get_user(db, id=user_id)


@router.patch("/{user_id}", status_code=200)
async def update_user(
    user_update: schemas.UserUpdate,
    user: User = Depends(get_request_user),
    db: AsyncSession = Depends(get_db),
) -> schemas.UserResponse:
    return await crud.update_user(db, user.id, user_update)


@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user: User = Depends(get_request_user), db: AsyncSession = Depends(get_db)
):
    return await crud.delete_user(db, user.id)
