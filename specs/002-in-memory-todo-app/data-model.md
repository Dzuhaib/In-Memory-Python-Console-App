# Data Model: In-Memory Todo List Application

This document defines the data structures used in the application.

## Task

Represents a single to-do item.

### Attributes

-   **id** (`int`): A unique identifier for the task. This will be generated sequentially.
-   **description** (`str`): The text content of the task (e.g., "Buy milk").
-   **completed** (`bool`): The completion status of the task. Defaults to `False`.

### Example Representation

In Python, a task could be represented by a simple dictionary or a `dataclass`/`namedtuple`.

**As a dictionary:**
```python
{
    "id": 1,
    "description": "Walk the dog",
    "completed": False
}
```

**As a `dataclass` (preferred for clarity):**
```python
from dataclasses import dataclass

@dataclass
class Task:
    id: int
    description: str
    completed: bool = False
```

The main application will manage a list of these `Task` objects.
```python
tasks: list[Task] = []
```
