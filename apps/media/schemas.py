from pydantic import BaseModel, ConfigDict


class MediaCreate(BaseModel):
    name: str


class MediaUpdate(BaseModel):
    name: str | None = None


class MediaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    filename: str | None
    owner_id: int
