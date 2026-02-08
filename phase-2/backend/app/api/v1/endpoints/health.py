"""Health check endpoint for Todo Backend API"""
from fastapi import APIRouter
from typing import Dict
from datetime import datetime


router = APIRouter()


@router.get("/health", status_code=200)
async def health_check():
    """Health check endpoint to verify API is running"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "Todo Backend API"
    }