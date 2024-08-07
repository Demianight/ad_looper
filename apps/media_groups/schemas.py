from __future__ import annotations

from typing import Sequence

from pydantic import BaseModel

from apps.common.schemas import MediaGroupSimpleResponse, MediaSimpleResponse
from apps.schedules.schemas import ScheduleResponse


class MediaGroupCreate(BaseModel):
    name: str


class MediaGroupUpdate(BaseModel):
    name: str | None = None


class MediaGroupResponse(MediaGroupSimpleResponse):
    media_items: Sequence[MediaSimpleResponse]
    schedules: Sequence[ScheduleResponse]
