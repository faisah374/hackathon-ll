"""Authentication dependencies for Todo Backend API"""
from typing import Callable, Dict, Any
from fastapi import Depends, HTTPException, status

from ..security import get_current_user, verify_user_owns_resource
from ..models.task import Task


def get_authenticated_user(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Dependency to get the authenticated user"""
    return current_user


def verify_user_ownership(user_id: str, current_user: Dict[str, Any] = Depends(get_current_user)):
    """Dependency to verify that the current user owns the resource they're trying to access"""
    if not verify_user_owns_resource(current_user, user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resource"
        )
    return current_user