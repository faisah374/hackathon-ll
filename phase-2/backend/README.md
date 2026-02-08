# Todo Backend API

A FastAPI-based backend for the Todo application with JWT authentication and PostgreSQL database.

## Features

- RESTful API endpoints for todo management
- JWT-based authentication using Better Auth tokens
- User isolation - users can only access their own tasks
- PostgreSQL database with SQLModel ORM
- Docker-ready for easy deployment

## Prerequisites

- Python 3.9+
- PostgreSQL database (or Neon Serverless PostgreSQL)
- Better Auth configured for frontend

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables (copy `.env.example` to `.env` and fill in values)

## Environment Variables

Copy `.env.example` to `.env` and set the following variables:

- `DATABASE_URL`: PostgreSQL connection string
- `BETTER_AUTH_SECRET`: Secret key for JWT verification
- `ALGORITHM`: JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time (default: 30)

## Running Locally

```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.

API documentation will be available at `http://localhost:8000/docs`.

## Running with Docker

```bash
docker-compose up --build
```

## API Endpoints

All API endpoints are prefixed with `/api`.

- `GET /api/{user_id}/tasks` - Get all tasks for user
- `POST /api/{user_id}/tasks` - Create a new task
- `GET /api/{user_id}/tasks/{id}` - Get a specific task
- `PUT /api/{user_id}/tasks/{id}` - Update a task
- `DELETE /api/{user_id}/tasks/{id}` - Delete a task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle task completion

All endpoints require a valid JWT token in the `Authorization` header:

```
Authorization: Bearer <jwt_token>
```

## Database Initialization

To initialize the database tables manually:

```bash
python scripts/init_db.py
```

## Testing

Run the tests using pytest:

```bash
pip install -r requirements-dev.txt
pytest
```

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app instance
│   ├── config.py               # Configuration and environment variables
│   ├── database.py             # Database connection and session management
│   ├── security.py             # JWT utilities and authentication logic
│   ├── models/                 # Data models and schemas
│   │   ├── __init__.py
│   │   └── task.py             # Task model definition
│   ├── schemas/                # Pydantic schemas for validation
│   │   ├── __init__.py
│   │   └── task.py             # Task schemas (create, update, read)
│   ├── services/               # Business logic services
│   │   ├── __init__.py
│   │   └── task_service.py     # Task business operations
│   └── api/                    # API routes and dependencies
│       ├── __init__.py
│       ├── deps.py             # Common dependencies
│       ├── auth_deps.py        # Authentication dependencies
│       └── v1/                 # API version 1
│           ├── __init__.py
│           ├── router.py       # Main API router
│           └── endpoints/      # Individual endpoint modules
│               ├── __init__.py
│               ├── tasks.py    # Task-related endpoints
│               └── health.py   # Health check endpoint
├── scripts/
│   ├── __init__.py
│   └── init_db.py              # Database initialization script
├── tests/
├── requirements.txt
├── requirements-dev.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```