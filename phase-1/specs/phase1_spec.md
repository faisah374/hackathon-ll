# Phase 1 Specification — Todo Console App

## Project Overview

This specification defines the requirements for a console-based Todo application.
The app runs entirely in memory and allows users to manage tasks through terminal commands.

This phase focuses on core CRUD behavior only.

No persistence, networking, or external integrations are allowed.

---

## User Persona

Primary user:

A single user interacting with a command-line interface who wants to quickly
manage personal tasks.

The system does not support multi-user environments.

---

## Core User Journey

The user launches the app → interacts via commands → manages tasks → exits.

The workflow must feel simple, fast, and predictable.

---

## Functional Requirements

### FR-1: Add Task

User can create a new task.

Inputs:
- Title (required)
- Description (optional)

System behavior:
- Assign unique numeric ID
- Default status = incomplete
- Store in memory

Acceptance criteria:
- Task appears in task list immediately
- Empty title is rejected
- ID must never duplicate

---

### FR-2: View Tasks

User can list all tasks.

System behavior:
- Display all tasks
- Show ID, title, description, status

Acceptance criteria:
- Empty list message shown if no tasks exist
- Completed tasks clearly marked
- Output must be readable and structured

---

### FR-3: Update Task

User can modify an existing task.

Inputs:
- Task ID
- New title (optional)
- New description (optional)

System behavior:
- Only update provided fields
- Keep unchanged fields intact

Acceptance criteria:
- Invalid ID returns error
- Updated task reflects immediately
- No silent failures

---

### FR-4: Delete Task

User can remove a task.

Inputs:
- Task ID

System behavior:
- Remove task from memory

Acceptance criteria:
- Task no longer appears in list
- Invalid ID returns error
- Deleting does not crash system

---

### FR-5: Toggle Completion

User can mark task complete or incomplete.

Inputs:
- Task ID

System behavior:
- Toggles the completion status of the task.

Acceptance criteria:
- Task status is updated correctly.
- Invalid ID returns error.
- Operation does not crash the system.

---

## Non-Functional Requirements

### NFR-1: In-Memory Storage
- All task data exists only in memory during runtime.
- No persistence, databases, or file storage.

### NFR-2: Deterministic Behavior
- All operations must be predictable and repeatable.
- No silent failures; errors must be clearly communicated.

### NFR-3: Lightweight Dependencies
- Only Python standard library allowed.
- No external frameworks or heavy libraries.

### NFR-4: Clean Architecture
- Follows clean Python architecture principles (separation of concerns, modularity).
- Recommended structure: `src/models.py`, `src/services.py`, `src/cli.py`, `src/main.py`

---

## Future Considerations (Out of Scope for Phase 1)

- Persistence (saving/loading tasks)
- Editing task descriptions
- Batch operations
- Task prioritization
- Due dates
- User accounts
