from pydantic import BaseModel, ConfigDict, EmailStr, SecretStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: SecretStr


class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: SecretStr | None = None


class UserResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    username: str
    email: EmailStr
