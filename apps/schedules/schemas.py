from datetime import time

from pydantic import BaseModel, ConfigDict


class ScheduleCreate(BaseModel):
    trigger_time: time
    media_id: int
    media_group_id: int


class ScheduleUpdate(BaseModel):
    trigger_time: time | None = None
    media_id: int | None = None
    media_group_id: int | None = None


class ScheduleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    trigger_time: time
    media_id: int
    media_group_id: int
