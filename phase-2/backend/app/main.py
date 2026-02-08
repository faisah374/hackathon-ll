"""Main application entry point for Todo Backend API"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .api.v1.router import api_router
from .database import init_db


def create_app() -> FastAPI:
    """Create and configure the FastAPI application"""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )

    # Initialize the database
    init_db()

    # Set all CORS enabled origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, replace with specific frontend URL
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routes
    app.include_router(api_router, prefix=settings.API_V1_STR)

    return app


app = create_app()


@app.get("/")
def read_root():
    """Root endpoint to verify API is running"""
    return {
        "message": "Welcome to Todo Backend API",
        "version": settings.VERSION,
        "docs": "/docs"
    }