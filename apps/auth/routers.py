from fastapi import APIRouter, Depends

from apps.auth.utils import create_access_token
from apps.dependencies import authenticate_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
def login(username: str = Depends(authenticate_user)):
    access_token = create_access_token(data={"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}
