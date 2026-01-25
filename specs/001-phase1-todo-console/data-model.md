# Data Model: Phase 1 Todo Console App

**Date**: 2025-01-25
**Branch**: `001-phase1-todo-console`

## Entities

### Priority (Enum)

Represents task importance level with natural ordering for sorting.

| Value | Display | Sort Order |
|-------|---------|------------|
| HIGH | "high" | 1 (first) |
| MEDIUM | "medium" | 2 |
| LOW | "low" | 3 (last) |

**Default**: MEDIUM

### Task

Represents a single todo item.

| Field | Type | Required | Default | Validation |
|-------|------|----------|---------|------------|
| id | int | Yes | Auto-generated | Positive integer, unique, sequential |
| title | str | Yes | - | Non-empty after trimming whitespace |
| completed | bool | Yes | False | - |
| priority | Priority | Yes | MEDIUM | Must be valid Priority enum value |
| tags | list[str] | Yes | [] | Each tag non-empty after trimming |

**Constraints**:
- `id` is immutable after creation
- `title` cannot be set to empty string
- `tags` can be empty list (no tags)
- `completed` can be toggled freely

## State Transitions

### Task Lifecycle

```
                    ┌─────────────┐
    create()        │   CREATED   │
    ─────────────►  │ completed=F │
                    └──────┬──────┘
                           │
              complete()   │   uncomplete()
                    ┌──────▼──────┐
                    │  COMPLETED  │◄────────┐
                    │ completed=T │         │
                    └──────┬──────┘         │
                           │                │
              delete()     │    complete()  │
                    ┌──────▼──────┐         │
                    │   DELETED   │─────────┘
                    │  (removed)  │  (only if not deleted)
                    └─────────────┘
```

### Valid Operations by State

| Current State | Allowed Operations |
|--------------|-------------------|
| Created (incomplete) | view, update, delete, complete, add_tag, remove_tag |
| Completed | view, update, delete, uncomplete, add_tag, remove_tag |
| Deleted | (none - removed from storage) |

## Storage Schema

### In-Memory Structure

```python
# TaskService internal state
_tasks: dict[int, Task] = {}  # id -> Task mapping
_next_id: int = 1             # Sequential ID counter
```

### Operations Complexity

| Operation | Time Complexity | Notes |
|-----------|----------------|-------|
| Create | O(1) | Dict insertion |
| Get by ID | O(1) | Dict lookup |
| Update | O(1) | Dict lookup + mutation |
| Delete | O(1) | Dict removal |
| List all | O(n) | Iterate values |
| Search | O(n) | Linear scan of titles |
| Filter | O(n) | Linear scan with predicates |
| Sort | O(n log n) | Python sorted() |

## Relationships

### Entity Diagram

```
┌─────────────────────────────────────────────┐
│                    Task                      │
├─────────────────────────────────────────────┤
│ id: int (PK)                                │
│ title: str                                  │
│ completed: bool                             │
│ priority: Priority (FK → Priority enum)     │
│ tags: list[str]                             │
└─────────────────────────────────────────────┘
         │
         │ has-a
         ▼
┌─────────────────────────────────────────────┐
│                  Priority                    │
├─────────────────────────────────────────────┤
│ HIGH = 1                                    │
│ MEDIUM = 2                                  │
│ LOW = 3                                     │
└─────────────────────────────────────────────┘
```

## Validation Rules

### Task Creation

1. `title` MUST be non-empty after stripping whitespace
2. `priority` MUST be a valid Priority enum value (or default to MEDIUM)
3. `tags` MUST be a list (can be empty); each tag non-empty after stripping
4. `id` is auto-assigned (user cannot specify)

### Task Update

1. `title` if provided, MUST be non-empty after stripping
2. `priority` if provided, MUST be valid Priority enum value
3. `id` CANNOT be changed
4. `completed` can be changed via complete/uncomplete operations

### Tag Operations

1. Tag to add MUST be non-empty after stripping
2. Duplicate tags are ignored (set semantics)
3. Removing non-existent tag is a no-op (no error)

## Example Data

```python
from dataclasses import dataclass, field
from enum import IntEnum

class Priority(IntEnum):
    HIGH = 1
    MEDIUM = 2
    LOW = 3

@dataclass
class Task:
    id: int
    title: str
    completed: bool = False
    priority: Priority = Priority.MEDIUM
    tags: list[str] = field(default_factory=list)

# Example instances
task1 = Task(id=1, title="Buy groceries", priority=Priority.HIGH, tags=["shopping"])
task2 = Task(id=2, title="Review PR", completed=True, tags=["work", "code"])
task3 = Task(id=3, title="Call mom", priority=Priority.LOW)
```
