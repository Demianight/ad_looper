from pydantic import BaseModel, ConfigDict


class MediaGroupSimpleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    owner_id: int


class MediaSimpleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    filename: str | None
    owner_id: int
