from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import DisplayDevice

from .schemas import DisplayDeviceCreate, DisplayDeviceUpdate


async def create_display_device(
    db: AsyncSession, display_device: DisplayDeviceCreate, owner_id: int
) -> DisplayDevice:
    db_display_device = DisplayDevice(
        name=display_device.name,
        description=display_device.description,
        owner_id=owner_id,
        media_group_id=display_device.media_group_id,
    )

    # Add the new device and commit the transaction
    db.add(db_display_device)
    await db.commit()
    await db.refresh(db_display_device)
    return db_display_device


async def get_display_device(db: AsyncSession, **kwargs) -> DisplayDevice:
    query = select(DisplayDevice)
    for key, value in kwargs.items():
        if hasattr(DisplayDevice, key):
            query = query.filter(getattr(DisplayDevice, key) == value)
        else:
            raise HTTPException(status_code=400, detail="Invalid filter")

    result = await db.execute(query)
    db_display_device = result.scalars().first()
    if db_display_device is None:
        raise HTTPException(status_code=404, detail="Display device not found")
    return db_display_device


async def get_display_devices(db: AsyncSession, **kwargs):
    query = select(DisplayDevice)
    for key, value in kwargs.items():
        if hasattr(DisplayDevice, key):
            query = query.filter(getattr(DisplayDevice, key) == value)
        else:
            raise HTTPException(status_code=400, detail="Invalid filter")

    result = await db.execute(query)
    return result.scalars().all()


async def update_display_device(
    db: AsyncSession,
    device_id: int,
    display_device_update: DisplayDeviceUpdate,
) -> DisplayDevice:
    # Retrieve the existing device
    query = select(DisplayDevice).filter(DisplayDevice.id == device_id)
    result = await db.execute(query)
    db_display_device = result.scalars().first()
    if db_display_device is None:
        raise HTTPException(status_code=404, detail="DisplayDevice not found")

    # Update the device properties
    if display_device_update.name is not None:
        db_display_device.name = display_device_update.name

    if display_device_update.description is not None:
        db_display_device.description = display_device_update.description

    if display_device_update.media_group_id is not None:
        db_display_device.media_group_id = display_device_update.media_group_id

    db.add(db_display_device)
    await db.commit()
    await db.refresh(db_display_device)
    return db_display_device


async def delete_display_device(db: AsyncSession, device_id: int) -> None:
    db_display_device = await get_display_device(db, id=device_id)
    await db.delete(db_display_device)
    await db.commit()
