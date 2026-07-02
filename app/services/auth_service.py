from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.models.user import User
from app.schemas.auth import UserRegister
from app.utils import hash_password, verify_password
from app.oauth2 import create_access_token


def register_user(user: UserRegister, db: Session):
    """
    Register a new user.
    """

    existing_user = (
        db.query(User)
        .filter(
            User.email == user.email,
            User.is_deleted == False
        )
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    new_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password),
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def login_user(
    user: OAuth2PasswordRequestForm,
    db: Session
):
    """
    Authenticate user.
    """

    db_user = (
        db.query(User)
        .filter(
            User.email == user.username,
            User.is_deleted == False
        )
        .first()
    )

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        {
            "user_id": db_user.id,
            "role": db_user.role
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }