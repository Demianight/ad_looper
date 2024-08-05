from fastapi import APIRouter

from . import auth, display_devices, media, users

core_router = APIRouter()


core_router.include_router(auth.router)
core_router.include_router(users.router)
core_router.include_router(media.router)
core_router.include_router(display_devices.router)
