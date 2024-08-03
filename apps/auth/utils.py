import jwt
from datetime import datetime, timedelta
from ad_looper.config import settings


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None,
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.token.access_token_expire_minutes
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.token.secret_key,
        algorithm=settings.token.algorithm,
    )
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    try:
        decoded_jwt = jwt.decode(
            token,
            settings.token.secret_key,
            algorithms=[settings.token.algorithm],
        )
        return decoded_jwt
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Decoded invalid token")
