from fastapi import APIRouter
from app.models.user_models import UserRegisterRequest, UserLoginRequest
from app.services.auth_service import (
    register_user_service,
    login_user_service
)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", status_code=201)
def register(req: UserRegisterRequest):
    return register_user_service(req.dict())


@router.post("/login")
def login(req: UserLoginRequest):
    return login_user_service(req.dict())
