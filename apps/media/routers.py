from pathlib import Path
from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import FileResponse

from apps.common.dependencies import get_db, get_request_user
from apps.media.utils import write_file
from database.models import User

from . import crud
from .schemas import MediaCreate, MediaResponse, MediaUpdate

router = APIRouter(prefix="/media", tags=["Media"])


@router.get("")
async def read_media(
    user: User = Depends(get_request_user),
) -> Sequence[MediaResponse]:
    return await user.awaitable_attrs.media


@router.get("/{media_id}")
async def read_media_item(
    media_id: int,
    user: User = Depends(get_request_user),
    db: AsyncSession = Depends(get_db),
) -> MediaResponse:
    media_item = await crud.get_media(db, id=media_id)
    if media_item is None:
        raise HTTPException(status_code=404, detail="Media not found")
    if user != media_item.owner:
        raise HTTPException(status_code=403, detail="Forbidden")
    return media_item


@router.get(
    "/{media_id}/download",
    description="The file will be sent in bytes",
)
async def download_media_item(
    media_id: int,
    user: User = Depends(get_request_user),
    db: AsyncSession = Depends(get_db),
):
    media_item = await crud.get_media(db, id=media_id)
    if media_item is None:
        raise HTTPException(status_code=404, detail="Media not found")
    if user != media_item.owner:
        raise HTTPException(status_code=403, detail="Forbidden")
    file_path = Path("uploaded_media") / str(media_item.filename)

    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        file_path,
        filename=media_item.filename,
        media_type="application/octet-stream",
    )


@router.post(
    "",
    status_code=201,
    description="After creating a media item, the actual file should be uploaded using the `upload` endpoint",
)
async def create_media_item(
    media: MediaCreate,
    user: User = Depends(get_request_user),
    db: AsyncSession = Depends(get_db),
) -> MediaResponse:
    return await crud.create_media(db, media, user.id)


@router.post(
    "/{media_id}/upload",
    status_code=201,
    description="The file should be uploaded using this endpoint. Only bytes should be sent",
)
async def upload_media_item(
    media_id: int,
    file: UploadFile,
    user: User = Depends(get_request_user),
    db: AsyncSession = Depends(get_db),
) -> MediaResponse:
    if user != (await crud.get_media(db, id=media_id)).owner:
        raise HTTPException(status_code=403, detail="Forbidden")
    if file.filename is None:
        raise HTTPException(status_code=400, detail="Error reading filename")

    await write_file(file)

    return await crud.set_media_filename(db, media_id, file.filename)


@router.patch("/{media_id}")
async def update_media_item(
    media_id: int,
    media_update: MediaUpdate,
    user: User = Depends(get_request_user),
    db: AsyncSession = Depends(get_db),
) -> MediaResponse:
    media_item = await crud.get_media(db, id=media_id)
    if media_item is None:
        raise HTTPException(status_code=404, detail="Media not found")
    if user != media_item.owner:
        raise HTTPException(status_code=403, detail="Forbidden")
    return await crud.update_media(db, media_id, media_update)


@router.delete("/{media_id}", status_code=204)
async def delete_media_item(
    media_id: int,
    user: User = Depends(get_request_user),
    db: AsyncSession = Depends(get_db),
):
    media_item = await crud.get_media(db, id=media_id)
    if media_item is None:
        raise HTTPException(status_code=404, detail="Media not found")
    if user != media_item.owner:
        raise HTTPException(status_code=403, detail="Forbidden")
    await crud.delete_media(db, media_id)
    return
