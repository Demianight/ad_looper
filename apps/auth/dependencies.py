from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from apps.auth.schemas import TokenCreate
from apps.auth.utils import decode_access_token
from apps.dependencies import get_db
from apps.users.crud import get_user_by_username
from apps.users.utils import verify_password


def authenticate_user(
    token_data: TokenCreate,
    db: Session = Depends(get_db),
) -> str | None:
    user = get_user_by_username(db, token_data.username)
    if user and verify_password(
        token_data.password.get_secret_value(),
        user.password,  # type: ignore
    ):
        return token_data.username
    raise HTTPException(status_code=401, detail="Invalid credentials")


BearerToken = HTTPBearer()


def get_request_user(
    token: HTTPAuthorizationCredentials = Depends(BearerToken),
    db: Session = Depends(get_db),
):
    data = decode_access_token(token.credentials)
    username = data.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user
