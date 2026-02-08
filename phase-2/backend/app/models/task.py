"""Task model definition for Todo Backend API"""
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Column, DateTime
from sqlalchemy import func
import sqlalchemy.dialects.postgresql as pg


class TaskBase(SQLModel):
    """Base class for Task model containing common fields"""
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)


class Task(TaskBase, table=True):
    """Task model for database storage"""
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(max_length=255)  # Using string to match JWT token user_id format
    created_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False, server_default=func.current_timestamp())
    )
    updated_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False, server_default=func.current_timestamp(), onupdate=datetime.now)
    )


class TaskRead(TaskBase):
    """Schema for reading Task data"""
    id: int
    user_id: str
    created_at: datetime
    updated_at: datetime


class TaskCreate(TaskBase):
    """Schema for creating Task data"""
    title: str = Field(min_length=1, max_length=255)  # Title is required for creation


class TaskUpdate(SQLModel):
    """Schema for updating Task data"""
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = None