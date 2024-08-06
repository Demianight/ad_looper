from typing import Sequence

from pydantic import BaseModel

from apps.common.schemas import MediaGroupSimpleResponse, MediaSimpleResponse
from apps.media_groups.schemas import MediaGroupResponse
from apps.schedules.schemas import ScheduleResponse


class MediaCreate(BaseModel):
    name: str


class MediaUpdate(BaseModel):
    name: str | None = None


class MediaResponse(MediaSimpleResponse):
    media_groups: Sequence[MediaGroupSimpleResponse]
    schedules: Sequence[ScheduleResponse]
