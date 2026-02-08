"""Common API dependencies for Todo Backend API"""
from typing import Generator
from sqlmodel import Session

from ..database import get_session


def get_db_session() -> Generator[Session, None, None]:
    """Dependency to get database session for API endpoints"""
    yield from get_session()