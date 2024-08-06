from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from apps.common.dependencies import get_db, get_request_user
from database.models import User

from . import crud
from .schemas import ScheduleCreate, ScheduleResponse, ScheduleUpdate

router = APIRouter(prefix="/schedules", tags=["Schedules"])


@router.get("")
async def read_schedules(
    user: User = Depends(get_request_user),
) -> list[ScheduleResponse]:
    return await user.awaitable_attrs.schedules


@router.get("/{schedule_id}")
async def read_schedule(
    schedule_id: int,
    user: User = Depends(get_request_user),
    db: AsyncSession = Depends(get_db),
) -> ScheduleResponse:
    schedule = await crud.get_schedule(db, id=schedule_id)
    if schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")
    if user != schedule.owner:
        raise HTTPException(status_code=403, detail="Forbidden")
    return schedule


@router.post(
    "",
    status_code=201,
    description="Create a new schedule",
)
async def create_schedule(
    schedule: ScheduleCreate,
    user: User = Depends(get_request_user),
    db: AsyncSession = Depends(get_db),
) -> ScheduleResponse:
    return await crud.create_schedule(db, schedule, user.id)


@router.patch("/{schedule_id}")
async def update_schedule(
    schedule_id: int,
    schedule_update: ScheduleUpdate,
    user: User = Depends(get_request_user),
    db: AsyncSession = Depends(get_db),
) -> ScheduleResponse:
    schedule = await crud.get_schedule(db, id=schedule_id)
    if schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return await crud.update_schedule(db, schedule_id, schedule_update)


@router.delete("/{schedule_id}", status_code=204)
async def delete_schedule(
    schedule_id: int,
    user: User = Depends(get_request_user),
    db: AsyncSession = Depends(get_db),
):
    schedule = await crud.get_schedule(db, id=schedule_id)
    if schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")
    await crud.delete_schedule(db, schedule_id)
    return
