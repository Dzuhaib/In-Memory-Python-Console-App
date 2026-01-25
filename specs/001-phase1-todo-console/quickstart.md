# Quickstart: Phase 1 Todo Console App

**Date**: 2025-01-25
**Branch**: `001-phase1-todo-console`

## Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

## Installation

```bash
# Clone the repository (if not already done)
cd "new_session phase i ii 2"

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install development dependencies
pip install pytest pytest-cov
```

## Running the Application

```bash
# From repository root
python -m src.cli.main
```

You'll see the prompt:
```
Todo App v1.0.0
Type "help" for available commands.

todo>
```

## Quick Tutorial

### 1. Create Tasks

```
todo> add "Buy groceries"
Created task #1: "Buy groceries" [medium]

todo> add "Finish report" --priority high --tags work,urgent
Created task #2: "Finish report" [high] (tags: work, urgent)

todo> add "Call mom" --priority low
Created task #3: "Call mom" [low]
```

### 2. View Tasks

```
todo> list
Tasks (3):
  [ ] #1 Buy groceries [medium]
  [ ] #2 Finish report [high] (tags: work, urgent)
  [ ] #3 Call mom [low]
```

### 3. Complete a Task

```
todo> complete 1
Completed task #1: "Buy groceries"

todo> list
Tasks (3):
  [x] #1 Buy groceries [medium]
  [ ] #2 Finish report [high] (tags: work, urgent)
  [ ] #3 Call mom [low]
```

### 4. Filter Tasks

```
todo> list --status incomplete
Tasks (2):
  [ ] #2 Finish report [high] (tags: work, urgent)
  [ ] #3 Call mom [low]

todo> list --priority high
Tasks (1):
  [ ] #2 Finish report [high] (tags: work, urgent)

todo> list --tag work
Tasks (1):
  [ ] #2 Finish report [high] (tags: work, urgent)
```

### 5. Sort Tasks

```
todo> list --sort priority
Tasks (3):
  [ ] #2 Finish report [high] (tags: work, urgent)
  [x] #1 Buy groceries [medium]
  [ ] #3 Call mom [low]

todo> list --sort alpha
Tasks (3):
  [x] #1 Buy groceries [medium]
  [ ] #3 Call mom [low]
  [ ] #2 Finish report [high] (tags: work, urgent)
```

### 6. Search Tasks

```
todo> search report
Search results for "report" (1):
  [ ] #2 Finish report [high] (tags: work, urgent)
```

### 7. Update a Task

```
todo> update 3 --title "Call mom and dad" --priority medium
Updated task #3: "Call mom and dad" [medium]
```

### 8. Manage Tags

```
todo> tag 1 add shopping
Added tag "shopping" to task #1

todo> tag 1 remove shopping
Removed tag "shopping" from task #1
```

### 9. Delete a Task

```
todo> delete 3
Deleted task #3: "Call mom and dad"
```

### 10. Exit

```
todo> exit
Goodbye!
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_task_model.py

# Run with verbose output
pytest -v
```

## Project Structure

```
.
├── src/
│   ├── models/
│   │   └── task.py          # Task dataclass
│   ├── services/
│   │   └── task_service.py  # Business logic
│   ├── cli/
│   │   ├── main.py          # Entry point
│   │   ├── commands.py      # Command handlers
│   │   └── display.py       # Output formatting
│   └── utils/
│       └── logger.py        # Logging setup
├── tests/
│   ├── unit/
│   └── integration/
├── specs/                    # Design documents
└── pyproject.toml           # Project config
```

## Common Issues

### "ModuleNotFoundError: No module named 'src'"

Make sure you're running from the repository root:
```bash
python -m src.cli.main
```

### Tests not finding modules

Ensure you're in the virtual environment:
```bash
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

## Next Steps

After completing Phase 1:
- All tasks are stored in memory (lost on exit)
- Phase 2 will add persistent storage with a database
- See `specs/001-phase1-todo-console/spec.md` for full requirements
