from pydantic import BaseModel, SecretStr


class TokenCreate(BaseModel):
    username: str
    password: SecretStr
