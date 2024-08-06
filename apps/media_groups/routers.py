from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from apps.common.schemas import MediaGroupSimpleResponse
from apps.common.dependencies import get_db, get_request_user
from database.models import User

from . import crud
from .schemas import MediaGroupCreate, MediaGroupResponse, MediaGroupUpdate

router = APIRouter(prefix="/media_groups", tags=["MediaGroups"])


@router.get("")
async def read_media_groups(
    user: User = Depends(get_request_user),
) -> Sequence[MediaGroupSimpleResponse]:
    return await user.awaitable_attrs.media_groups


@router.get("/{media_group_id}")
async def read_media_group(
    media_group_id: int,
    user: User = Depends(get_request_user),
    db: AsyncSession = Depends(get_db),
) -> MediaGroupResponse:
    media_group = await crud.get_media_group(db, id=media_group_id)
    if media_group is None:
        raise HTTPException(status_code=404, detail="MediaGroup not found")
    if user != media_group.owner:
        raise HTTPException(status_code=403, detail="Forbidden")

    return media_group


@router.post(
    "",
    status_code=201,
    description="Create a new media group",
)
async def create_media_group(
    media_group: MediaGroupCreate,
    user: User = Depends(get_request_user),
    db: AsyncSession = Depends(get_db),
) -> MediaGroupResponse:
    return await crud.create_media_group(db, media_group, user.id)


@router.patch("/{media_group_id}")
async def update_media_group(
    media_group_id: int,
    media_group_update: MediaGroupUpdate,
    user: User = Depends(get_request_user),
    db: AsyncSession = Depends(get_db),
) -> MediaGroupResponse:
    media_group = await crud.get_media_group(db, id=media_group_id)
    if media_group is None:
        raise HTTPException(status_code=404, detail="MediaGroup not found")
    if user != media_group.owner:
        raise HTTPException(status_code=403, detail="Forbidden")
    return await crud.update_media_group(
        db,
        media_group_id,
        media_group_update,
    )


@router.delete("/{media_group_id}", status_code=204)
async def delete_media_group(
    media_group_id: int,
    user: User = Depends(get_request_user),
    db: AsyncSession = Depends(get_db),
):
    media_group = await crud.get_media_group(db, id=media_group_id)
    if media_group is None:
        raise HTTPException(status_code=404, detail="MediaGroup not found")
    if user != media_group.owner:
        raise HTTPException(status_code=403, detail="Forbidden")
    return await crud.delete_media_group(db, media_group_id)


@router.post("/{media_group_id}/add/{media_id}", status_code=201)
async def add_media_to_media_group(
    media_group_id: int,
    media_id: int,
    user: User = Depends(get_request_user),
    db: AsyncSession = Depends(get_db),
):
    media_group = await crud.get_media_group(db, id=media_group_id)
    if media_group is None:
        raise HTTPException(status_code=404, detail="MediaGroup not found")
    if user != media_group.owner:
        raise HTTPException(status_code=403, detail="Forbidden")
    return await crud.add_media_to_media_group(db, media_group_id, media_id)
