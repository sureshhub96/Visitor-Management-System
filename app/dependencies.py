from fastapi import Depends

from app.oauth2 import (
    get_current_user,
    admin_required,
    receptionist_required
)


def get_logged_in_user(
    current_user=Depends(get_current_user)
):
    """
    Returns the currently authenticated user.
    """
    return current_user


def get_admin(
    current_user=Depends(admin_required)
):
    """
    Allows only Admin users.
    """
    return current_user


def get_receptionist(
    current_user=Depends(receptionist_required)
):
    """
    Allows Admin and Receptionist users.
    """
    return current_user