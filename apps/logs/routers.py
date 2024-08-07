from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from apps.common.dependencies import get_db, get_request_user
from apps.logs.schemas import LogResponse
from database.models import User
from . import crud
from apps.display_devices import crud as display_device_crud

router = APIRouter(prefix="/logs", tags=["Logs"])


@router.get("/devices/{device_id}/logs")
async def get_device_logs(
    device_id: int,
    user: User = Depends(get_request_user),
    db: AsyncSession = Depends(get_db),
) -> LogResponse:
    if (
        user
        != (
            await display_device_crud.get_display_device(db, id=device_id)
        ).owner
    ):
        raise HTTPException(status_code=403, detail="Forbidden")
    return await crud.get_log_list(db, device_id=device_id)
