"""Task service for Todo Backend API"""
from typing import List, Optional
from sqlmodel import Session, select
from fastapi import HTTPException, status

from ..models.task import Task, TaskCreate, TaskUpdate


def get_tasks_for_user(session: Session, user_id: str) -> List[Task]:
    """Get all tasks for a specific user"""
    statement = select(Task).where(Task.user_id == user_id)
    tasks = session.exec(statement).all()
    return tasks


def get_task_by_id_and_user(session: Session, task_id: int, user_id: str) -> Optional[Task]:
    """Get a specific task by ID for a specific user"""
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()
    return task


def create_task(session: Session, task_data: TaskCreate, user_id: str) -> Task:
    """Create a new task for a user"""
    # Create task instance
    task = Task(
        title=task_data.title,
        description=task_data.description,
        completed=task_data.completed,
        user_id=user_id
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def update_task(session: Session, task_id: int, task_data: TaskUpdate, user_id: str) -> Optional[Task]:
    """Update a task for a user"""
    task = get_task_by_id_and_user(session, task_id, user_id)
    if not task:
        return None

    # Update only the fields that are provided
    update_data = task_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def delete_task(session: Session, task_id: int, user_id: str) -> bool:
    """Delete a task for a user"""
    task = get_task_by_id_and_user(session, task_id, user_id)
    if not task:
        return False

    session.delete(task)
    session.commit()
    return True


def toggle_task_completion(session: Session, task_id: int, user_id: str) -> Optional[Task]:
    """Toggle the completion status of a task for a user"""
    task = get_task_by_id_and_user(session, task_id, user_id)
    if not task:
        return None

    task.completed = not task.completed
    session.add(task)
    session.commit()
    session.refresh(task)
    return task