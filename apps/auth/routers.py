from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from apps.auth.dependencies import authenticate_user
from apps.auth.schemas import AccessTokenResponse, TokenRefresh, TokenResponse
from apps.auth.utils import create_jwt_token
from apps.common.dependencies import get_db, get_request_user
from database.models import User

from . import crud
from apps.display_devices import crud as display_device_crud

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
async def login(
    user: User = Depends(authenticate_user),
    db: AsyncSession = Depends(get_db),
) -> AccessTokenResponse:
    access_token = create_jwt_token(
        data={"sub": user.username},
    )
    refresh_token = create_jwt_token(
        data={"sub": user.username},
        expires_delta=timedelta(days=10),
    )
    await crud.create_token(
        db,
        token=access_token,
        token_type="access",
        expires_at=datetime.utcnow() + timedelta(minutes=30),
        owner_id=user.id,
    )
    await crud.create_token(
        db,
        token=refresh_token,
        token_type="refresh",
        expires_at=datetime.utcnow() + timedelta(days=10),
        owner_id=user.id,
    )
    return AccessTokenResponse(
        access_token=access_token, refresh_token=refresh_token
    )


@router.post("/refresh")
async def refresh(
    token_data: TokenRefresh,
    db: AsyncSession = Depends(get_db),
) -> TokenResponse:
    token = await crud.get_token(db, token=token_data.token)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid token")

    if token.token_type != "refresh":
        raise HTTPException(status_code=401, detail="Refresh token required")

    if token.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Token expired")

    access_token = create_jwt_token(
        data={"sub": (await token.awaitable_attrs.owner).username},
    )
    await crud.update_token(
        db,
        token_id=token.id,
        token=access_token,
        token_type="access",
        expires_at=datetime.utcnow() + timedelta(minutes=30),
    )
    return TokenResponse(token=access_token, token_type="access")


@router.delete("/logout")
async def delete_existing_access_token(
    user: User = Depends(get_request_user),
    db: AsyncSession = Depends(get_db),
):
    token = await crud.get_token(db, owner_id=user.id, token_type="access")
    return await crud.delete_token(db, token_id=token.id)


@router.post("/display_devices/{display_device_id}/register")
async def register_display_device(
    display_device_id: int,
    user: User = Depends(get_request_user),
    db: AsyncSession = Depends(get_db),
):
    token = create_jwt_token(
        data={"sub": user.username, "display_device_id": display_device_id},
    )
    device = await display_device_crud.get_display_device(
        db, id=display_device_id
    )
    if await crud.get_device_token(db, display_device_id=display_device_id):
        raise HTTPException(
            status_code=409, detail="Device already registered"
        )
    await crud.create_device_token(
        db,
        token=token,
        token_type="access_display_device",
        expires_at=datetime.utcnow() + timedelta(days=365),
        display_device_id=device.id,
    )
    return TokenResponse(token=token, token_type="access_device")


@router.delete("/display_devices/{display_device_id}/unlink")
async def unlink_display_device(
    display_device_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await crud.delete_device_token(
        db, device_token_id=display_device_id
    )
