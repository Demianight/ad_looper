from fastapi import APIRouter
from . import users, auth

core_router = APIRouter()


core_router.include_router(auth.router)
core_router.include_router(users.router)
