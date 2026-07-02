from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth import (
    UserRegister,
    UserResponse,
    Token
)
from app.services.auth_service import (
    register_user,
    login_user
)
from app.oauth2 import admin_required

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=UserResponse
)
def register(
    user: UserRegister,
    db: Session = Depends(get_db)
):
    """
    Register the first Admin.
    After creating the first Admin, you can add
    current_user=Depends(admin_required)
    back if you want only Admins to create users.
    """
    return register_user(user, db)


@router.post(
    "/login",
    response_model=Token
)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    User Login
    """
    return login_user(user_credentials, db)