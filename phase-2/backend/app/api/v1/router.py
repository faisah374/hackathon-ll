"""Main API router for Todo Backend API"""
from fastapi import APIRouter

from .endpoints import tasks, health


api_router = APIRouter()
api_router.include_router(tasks.router, prefix="/{user_id}", tags=["tasks"])
api_router.include_router(health.router, tags=["health"])