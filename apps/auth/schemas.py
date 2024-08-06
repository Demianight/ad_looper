from pydantic import BaseModel, SecretStr


class TokenCreate(BaseModel):
    username: str
    password: SecretStr


class TokenResponse(BaseModel):
    token: str
    token_type: str


class AccessTokenResponse(BaseModel):
    access_token: str
    refresh_token: str


class DeviceTokenCreate(BaseModel): ...


class TokenRefresh(BaseModel):
    token: str
