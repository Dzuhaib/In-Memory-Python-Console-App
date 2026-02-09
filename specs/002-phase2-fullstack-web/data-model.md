# Data Model: Phase 2 Full Stack Web Application

**Feature**: `002-phase2-fullstack-web`
**Date**: 2026-01-25
**Database**: PostgreSQL (Neon DB)

## Entity Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                          TASK                                │
├─────────────────────────────────────────────────────────────┤
│ id          : INTEGER (PK, AUTO)                            │
│ title       : VARCHAR(500) NOT NULL                         │
│ completed   : BOOLEAN DEFAULT FALSE                         │
│ priority    : VARCHAR(10) DEFAULT 'medium'                  │
│ tags        : JSON DEFAULT '[]'                             │
│ created_at  : TIMESTAMP DEFAULT NOW()                       │
│ updated_at  : TIMESTAMP DEFAULT NOW()                       │
└─────────────────────────────────────────────────────────────┘
```

## Entity: Task

### Fields

| Field | Type | Constraints | Default | Description |
|-------|------|-------------|---------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO INCREMENT | auto | Unique identifier |
| title | VARCHAR(500) | NOT NULL, MIN LENGTH 1 | - | Task description |
| completed | BOOLEAN | NOT NULL | FALSE | Completion status |
| priority | VARCHAR(10) | CHECK IN ('high','medium','low') | 'medium' | Priority level |
| tags | JSON | - | '[]' | Array of tag strings |
| created_at | TIMESTAMP | NOT NULL | NOW() | Creation timestamp |
| updated_at | TIMESTAMP | NOT NULL | NOW() | Last update timestamp |

### Validation Rules

1. **title**:
   - Required (non-null)
   - Minimum length: 1 character
   - Maximum length: 500 characters
   - Whitespace-only titles rejected

2. **priority**:
   - Must be one of: 'high', 'medium', 'low'
   - Case-insensitive on input, stored lowercase
   - Default: 'medium'

3. **tags**:
   - Array of strings
   - Each tag: 1-50 characters
   - No duplicate tags per task
   - Maximum 20 tags per task

4. **timestamps**:
   - created_at: Set once at creation, never modified
   - updated_at: Updated on every modification

### SQLModel Definition

```python
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, JSON
from typing import Optional, List
from datetime import datetime
from enum import Enum

class Priority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class Task(SQLModel, table=True):
    """Task entity for the todo application."""

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(min_length=1, max_length=500)
    completed: bool = Field(default=False)
    priority: Priority = Field(default=Priority.MEDIUM)
    tags: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        use_enum_values = True
```

### TypeScript Type Definition

```typescript
// types/task.ts

export type Priority = 'high' | 'medium' | 'low';

export interface Task {
  id: number;
  title: string;
  completed: boolean;
  priority: Priority;
  tags: string[];
  created_at: string;  // ISO 8601 datetime
  updated_at: string;  // ISO 8601 datetime
}

export interface CreateTaskRequest {
  title: string;
  priority?: Priority;
  tags?: string[];
}

export interface UpdateTaskRequest {
  title?: string;
  priority?: Priority;
}

export interface TaskQueryParams {
  search?: string;
  status?: 'complete' | 'incomplete';
  priority?: Priority;
  tag?: string;
  sort?: 'priority' | 'alpha' | 'id';
}
```

## Database Schema (SQL)

```sql
-- Create enum type for priority (PostgreSQL)
CREATE TYPE priority_enum AS ENUM ('high', 'medium', 'low');

-- Create tasks table
CREATE TABLE task (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL CHECK (length(trim(title)) > 0),
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    priority VARCHAR(10) NOT NULL DEFAULT 'medium'
        CHECK (priority IN ('high', 'medium', 'low')),
    tags JSON NOT NULL DEFAULT '[]',
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Index for common queries
CREATE INDEX idx_task_completed ON task(completed);
CREATE INDEX idx_task_priority ON task(priority);
CREATE INDEX idx_task_created_at ON task(created_at);

-- Trigger for updating updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_task_updated_at
    BEFORE UPDATE ON task
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

## State Transitions

```
                    ┌─────────────────────┐
                    │                     │
    create()        │    INCOMPLETE       │◄────┐
    ─────────────►  │  (completed=false)  │     │
                    │                     │     │ uncomplete()
                    └──────────┬──────────┘     │
                               │                │
                    complete() │                │
                               ▼                │
                    ┌──────────────────────┐    │
                    │                      │    │
                    │     COMPLETE         │────┘
                    │  (completed=true)    │
                    │                      │
                    └──────────────────────┘
```

### Allowed State Transitions

| From State | Action | To State | Validation |
|------------|--------|----------|------------|
| (none) | create | INCOMPLETE | title required |
| INCOMPLETE | complete | COMPLETE | - |
| COMPLETE | uncomplete | INCOMPLETE | - |
| ANY | update | (same) | title required if changed |
| ANY | delete | (none) | - |
| ANY | add_tag | (same) | tag not already present |
| ANY | remove_tag | (same) | tag must exist |

## Query Patterns

### List Tasks (with filters)

```sql
-- Base query
SELECT * FROM task;

-- With status filter
SELECT * FROM task WHERE completed = false;  -- incomplete
SELECT * FROM task WHERE completed = true;   -- complete

-- With priority filter
SELECT * FROM task WHERE priority = 'high';

-- With tag filter (JSON array contains)
SELECT * FROM task WHERE tags @> '["work"]';

-- With search (case-insensitive)
SELECT * FROM task WHERE title ILIKE '%groceries%';

-- Combined filters (AND logic)
SELECT * FROM task
WHERE completed = false
  AND priority = 'high'
  AND tags @> '["work"]'
  AND title ILIKE '%urgent%';

-- Sorting
SELECT * FROM task ORDER BY
  CASE priority
    WHEN 'high' THEN 1
    WHEN 'medium' THEN 2
    WHEN 'low' THEN 3
  END;  -- by priority

SELECT * FROM task ORDER BY title ASC;  -- alphabetical
SELECT * FROM task ORDER BY id ASC;     -- creation order
```

### CRUD Operations

```sql
-- Create
INSERT INTO task (title, priority, tags)
VALUES ('Buy groceries', 'high', '["shopping"]')
RETURNING *;

-- Read single
SELECT * FROM task WHERE id = 1;

-- Update
UPDATE task
SET title = 'Buy organic groceries', priority = 'medium', updated_at = NOW()
WHERE id = 1
RETURNING *;

-- Delete
DELETE FROM task WHERE id = 1;

-- Toggle complete
UPDATE task SET completed = NOT completed, updated_at = NOW()
WHERE id = 1
RETURNING *;

-- Add tag
UPDATE task
SET tags = tags || '"newtag"'::jsonb, updated_at = NOW()
WHERE id = 1 AND NOT tags @> '["newtag"]'
RETURNING *;

-- Remove tag
UPDATE task
SET tags = tags - 'oldtag', updated_at = NOW()
WHERE id = 1
RETURNING *;
```

## Migration Notes

### From Phase 1

The Phase 1 in-memory Task model maps directly:

| Phase 1 Field | Phase 2 Field | Notes |
|---------------|---------------|-------|
| id: int | id: INTEGER | Same, now persisted |
| title: str | title: VARCHAR(500) | Same validation |
| completed: bool | completed: BOOLEAN | Same |
| priority: Priority | priority: VARCHAR(10) | Enum stored as string |
| tags: List[str] | tags: JSON | Array stored as JSON |
| (none) | created_at | New - auto-populated |
| (none) | updated_at | New - auto-populated |

No data migration needed as Phase 1 is in-memory only.
