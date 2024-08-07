from pydantic import BaseModel, ConfigDict


class LogCreate(BaseModel):
    url: str
    method: str
    status_code: int
    device_id: int | None = None


class LogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    url: str
    method: str
    status_code: int
    device_id: int | None = None
