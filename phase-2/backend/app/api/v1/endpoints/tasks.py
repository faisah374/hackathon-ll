"""Tasks endpoints for Todo Backend API"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from ....models.task import Task, TaskRead, TaskCreate, TaskUpdate
from ....services.task_service import (
    get_tasks_for_user, get_task_by_id_and_user, create_task,
    update_task, delete_task, toggle_task_completion
)
from ....api.deps import get_db_session
from ....api.auth_deps import get_authenticated_user, verify_user_ownership


router = APIRouter()


@router.get("/tasks", response_model=List[TaskRead], status_code=status.HTTP_200_OK)
def get_tasks(
    user_id: str,
    current_user: dict = Depends(verify_user_ownership),
    db_session: Session = Depends(get_db_session)
):
    """Retrieve all tasks for the authenticated user"""
    # Verify that the user_id in the route matches the authenticated user
    if current_user["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resource"
        )

    tasks = get_tasks_for_user(db_session, user_id)
    return tasks


@router.post("/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_new_task(
    user_id: str,
    task_create: TaskCreate,
    current_user: dict = Depends(verify_user_ownership),
    db_session: Session = Depends(get_db_session)
):
    """Create a new task for the authenticated user"""
    # Verify that the user_id in the route matches the authenticated user
    if current_user["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resource"
        )

    task = create_task(db_session, task_create, user_id)
    return task


@router.get("/tasks/{id}", response_model=TaskRead, status_code=status.HTTP_200_OK)
def get_single_task(
    user_id: str,
    id: int,
    current_user: dict = Depends(verify_user_ownership),
    db_session: Session = Depends(get_db_session)
):
    """Retrieve a specific task for the authenticated user"""
    # Verify that the user_id in the route matches the authenticated user
    if current_user["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resource"
        )

    task = get_task_by_id_and_user(db_session, id, user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@router.put("/tasks/{id}", response_model=TaskRead, status_code=status.HTTP_200_OK)
def update_existing_task(
    user_id: str,
    id: int,
    task_update: TaskUpdate,
    current_user: dict = Depends(verify_user_ownership),
    db_session: Session = Depends(get_db_session)
):
    """Update a specific task for the authenticated user"""
    # Verify that the user_id in the route matches the authenticated user
    if current_user["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resource"
        )

    task = update_task(db_session, id, task_update, user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@router.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_task(
    user_id: str,
    id: int,
    current_user: dict = Depends(verify_user_ownership),
    db_session: Session = Depends(get_db_session)
):
    """Delete a specific task for the authenticated user"""
    # Verify that the user_id in the route matches the authenticated user
    if current_user["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resource"
        )

    success = delete_task(db_session, id, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Return 204 No Content on successful deletion
    return


@router.patch("/tasks/{id}/complete", response_model=TaskRead, status_code=status.HTTP_200_OK)
def toggle_task_completion_status(
    user_id: str,
    id: int,
    current_user: dict = Depends(verify_user_ownership),
    db_session: Session = Depends(get_db_session)
):
    """Toggle the completion status of a specific task for the authenticated user"""
    # Verify that the user_id in the route matches the authenticated user
    if current_user["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resource"
        )

    task = toggle_task_completion(db_session, id, user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task