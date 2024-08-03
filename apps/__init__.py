from fastapi import APIRouter
from . import users

core_router = APIRouter()


core_router.include_router(users.router)
