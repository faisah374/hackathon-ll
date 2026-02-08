# Data Model: AI-Powered Conversational Chatbot

## Entities

### Task
- **id** (integer): Primary key, auto-incrementing
- **user_id** (string): Foreign key linking to authenticated user
- **title** (string): Task title (required, max 255 chars)
- **description** (string): Optional task description
- **completed** (boolean): Task completion status, default false
- **created_at** (timestamp): Auto-generated on creation
- **updated_at** (timestamp): Auto-updated on modification

**Validation rules**:
- title cannot be empty (requirement FR-001)
- user_id must exist and match authenticated user (requirement FR-010)
- user isolation enforced in all queries (requirement FR-010)

**State transitions**:
- created → active (initial state when created via add_task)
- active → completed (when complete_task is called)
- completed → active (when uncompleted via update_task)

### Conversation
- **id** (integer): Primary key, auto-incrementing
- **user_id** (string): Foreign key linking to authenticated user
- **created_at** (timestamp): Auto-generated on creation

**Validation rules**:
- user_id must exist and match authenticated user (requirement FR-010)
- user isolation enforced in all queries (requirement FR-010)

### Message
- **id** (integer): Primary key, auto-incrementing
- **conversation_id** (integer): Foreign key linking to conversation
- **role** (string): Message role ('user' or 'assistant')
- **content** (string): Message content
- **timestamp** (timestamp): Auto-generated on creation

**Validation rules**:
- conversation_id must reference existing conversation
- role must be either 'user' or 'assistant'
- user isolation enforced in all queries (requirement FR-010)

## Relationships
- User → 1:N → Conversations (one user to many conversations)
- Conversation → 1:N → Messages (one conversation to many messages)
- User → 1:N → Tasks (one user to many tasks)

## Indexes
- tasks.user_id_idx (for efficient user isolation queries)
- conversations.user_id_idx (for efficient user isolation queries)
- messages.conversation_id_idx (for efficient conversation history loading)
- messages.timestamp_idx (for chronological ordering of messages)