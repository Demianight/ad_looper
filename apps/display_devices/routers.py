from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from apps.dependencies import get_db, get_request_user
from database.models import User

from . import crud
from .schemas import (DisplayDeviceCreate, DisplayDeviceResponse,
                      DisplayDeviceUpdate)

router = APIRouter(prefix="/display_devices", tags=["DisplayDevices"])


@router.get("")
async def read_display_devices(
    user: User = Depends(get_request_user),
) -> Sequence[DisplayDeviceResponse]:
    return await user.awaitable_attrs.display_devices


@router.get("/{device_id}")
async def read_display_device(
    device_id: int,
    user: User = Depends(get_request_user),
    db: AsyncSession = Depends(get_db),
) -> DisplayDeviceResponse:
    display_device = await crud.get_display_device(db, id=device_id)
    if display_device is None:
        raise HTTPException(status_code=404, detail="DisplayDevice not found")
    if user != display_device.owner:
        raise HTTPException(status_code=403, detail="Forbidden")
    return display_device


@router.post("", status_code=201)
async def create_display_device(
    display_device: DisplayDeviceCreate,
    user: User = Depends(get_request_user),
    db: AsyncSession = Depends(get_db),
) -> DisplayDeviceResponse:
    return await crud.create_display_device(db, display_device, user.id)  # type: ignore


@router.patch("/{device_id}", status_code=200)
async def update_display_device(
    device_id: int,
    display_device_update: DisplayDeviceUpdate,
    user: User = Depends(get_request_user),
    db: AsyncSession = Depends(get_db),
) -> DisplayDeviceResponse:
    if user != (await crud.get_display_device(db, id=device_id)).owner:
        raise HTTPException(status_code=403, detail="Forbidden")
    return await crud.update_display_device(
        db,
        device_id,
        display_device_update,
    )


@router.delete("/{device_id}", status_code=204)
async def delete_display_device(
    device_id: int,
    user: User = Depends(get_request_user),
    db: AsyncSession = Depends(get_db),
):
    if user != (await crud.get_display_device(db, id=device_id)).owner:
        raise HTTPException(status_code=403, detail="Forbidden")
    return await crud.delete_display_device(db, device_id)
