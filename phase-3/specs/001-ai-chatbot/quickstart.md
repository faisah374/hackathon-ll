# Quickstart Guide: AI-Powered Conversational Chatbot

## Prerequisites

- Python 3.10+
- Poetry (dependency management)
- Neon PostgreSQL account
- OpenAI API key
- MCP server running

## Setup

### 1. Environment Variables

Create a `.env` file with:

```bash
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname
MCP_SERVER_URL=http://localhost:8080
JWT_SECRET=your_jwt_secret_key
```

### 2. Install Dependencies

```bash
poetry install
poetry shell
```

### 3. Database Setup

```bash
# Apply database migrations
python -m scripts.migrate_db
```

### 4. Start Services

```bash
# Terminal 1: Start MCP tools server
python -m services.mcp_server

# Terminal 2: Start the main API server
python -m services.main_server
```

## Usage

### API Endpoints

1. **Chat Endpoint** - `/chat` (POST)
   Send natural language messages to the AI agent

2. **Tasks Endpoints** - `/tasks` (GET/POST), `/tasks/{id}` (GET/PUT/DELETE)
   Direct task management API

### Example Requests

#### Chat with the AI
```bash
curl -X POST http://localhost:8000/chat \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Add a task to buy milk",
    "user_id": "user_12345"
  }'
```

#### List your tasks
```bash
curl -X GET http://localhost:8000/tasks \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Running Tests

```bash
# Unit tests
poetry run pytest tests/unit/

# Integration tests
poetry run pytest tests/integration/
```

## MCP Tools Overview

The AI agent has access to these tools:

- `add_task(title, description, user_id)` - Create a new task
- `list_tasks(user_id, status="all")` - List tasks with optional status filter
- `update_task(id, title, description, user_id)` - Update an existing task
- `delete_task(id, user_id)` - Delete a task
- `complete_task(id, user_id)` - Mark a task as complete

All tools enforce user isolation and authentication.