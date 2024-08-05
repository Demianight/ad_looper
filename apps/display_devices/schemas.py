from pydantic import BaseModel, ConfigDict


class DisplayDeviceCreate(BaseModel):
    name: str
    description: str | None = None


class DisplayDeviceUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class DisplayDeviceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None = None
    owner_id: int
