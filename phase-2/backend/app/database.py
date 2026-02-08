"""Database connection and session management for Todo Backend API"""
from typing import Generator
from sqlmodel import create_engine, Session
from .config import settings
import logging


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


import urllib.parse

# Determine if using PostgreSQL or SQLite and configure appropriately
parsed_url = urllib.parse.urlparse(settings.DATABASE_URL)
is_postgres = parsed_url.scheme.startswith('postgres')

connect_kwargs = {}
if is_postgres:
    connect_kwargs = {
        "sslmode": "require",  # Required for Neon connections
        "keepalives_idle": 30,  # Keep-alive settings for connection stability
        "keepalives_interval": 10,
        "keepalives_count": 3,
    }

# Create the database engine with appropriate configuration
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO,  # Enable/disable SQL query logging based on environment
    pool_pre_ping=True,  # Verify connections before use
    pool_size=settings.DB_POOL_SIZE,  # Connection pool size
    max_overflow=settings.DB_MAX_OVERFLOW,  # Additional connections beyond pool_size
    pool_recycle=settings.DB_POOL_RECYCLE,  # Recycle connections to prevent stale connections
    pool_timeout=settings.DB_POOL_TIMEOUT,  # Timeout for getting connection from pool
    connect_args=connect_kwargs
)


def get_session() -> Generator[Session, None, None]:
    """Dependency to get database session for FastAPI"""
    with Session(engine) as session:
        yield session


# Function to initialize the database tables
def init_db():
    """Initialize database tables"""
    from sqlmodel import SQLModel
    from .models.task import Task  # Import models to register them

    logger.info("Initializing database tables...")
    # Create all tables
    SQLModel.metadata.create_all(engine)
    logger.info("Database tables initialized successfully")