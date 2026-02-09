# Research: Phase 1 Todo Console App

**Date**: 2025-01-25
**Branch**: `001-phase1-todo-console`

## Research Questions

### RQ-001: Python CLI Architecture Patterns

**Question**: What is the best pattern for building a Python console application with interactive commands?

**Decision**: Use a simple command-loop pattern with dictionary-based command dispatch

**Rationale**:
- Standard library only (no argparse for interactive mode complexity)
- Simple `while True` loop with `input()` for user commands
- Dictionary mapping command names to handler functions
- Easy to test and extend

**Alternatives Considered**:
- `cmd` module: Overkill for this scope; adds complexity without benefit
- `argparse`: Better for single-command CLI tools, not interactive sessions
- Third-party (click, typer): Violates "no external dependencies" constraint

### RQ-002: Data Model Design

**Question**: How should the Task entity be structured in Python?

**Decision**: Use `dataclass` with `field()` defaults and validation methods

**Rationale**:
- `dataclass` provides clean structure with minimal boilerplate
- Built into Python 3.7+ (standard library)
- Easy to add validation via `__post_init__`
- Serialization-ready for future phases

**Alternatives Considered**:
- Plain dict: No type hints, no validation, hard to maintain
- NamedTuple: Immutable (problematic for updates)
- Pydantic: External dependency not justified for Phase 1

### RQ-003: In-Memory Storage Pattern

**Question**: How should tasks be stored in memory for efficient CRUD, search, and filter operations?

**Decision**: Dictionary with integer ID as key, plus ID counter

**Rationale**:
- O(1) lookup by ID for CRUD operations
- Sequential ID generation via counter
- Easy iteration for search/filter/sort
- Natural fit for Python patterns

**Alternatives Considered**:
- List with index as ID: Deletion creates gaps, ID reuse issues
- SQLite in-memory: Over-engineering for Phase 1; adds dependency complexity

### RQ-004: Search and Filter Implementation

**Question**: How to implement case-insensitive search and multi-criteria filtering?

**Decision**: Generator-based filtering with chained predicates

**Rationale**:
- Memory efficient for large lists (lazy evaluation)
- Composable: multiple filters chain naturally
- Case-insensitive via `.lower()` comparison
- Clean functional style

**Implementation Pattern**:
```python
def filter_tasks(tasks, status=None, priority=None, tag=None, search=None):
    results = tasks.values()
    if status is not None:
        results = (t for t in results if t.completed == (status == 'complete'))
    if priority:
        results = (t for t in results if t.priority == priority)
    if tag:
        results = (t for t in results if tag in t.tags)
    if search:
        search_lower = search.lower()
        results = (t for t in results if search_lower in t.title.lower())
    return list(results)
```

### RQ-005: Sort Implementation

**Question**: How to implement sorting by priority and alphabetically?

**Decision**: Use `sorted()` with key functions and enum for priority ordering

**Rationale**:
- Python's `sorted()` is stable and efficient
- Priority enum provides natural ordering (high=1, medium=2, low=3)
- Alphabetical sort via `key=lambda t: t.title.lower()`

**Implementation Pattern**:
```python
from enum import IntEnum

class Priority(IntEnum):
    HIGH = 1
    MEDIUM = 2
    LOW = 3

def sort_by_priority(tasks):
    return sorted(tasks, key=lambda t: t.priority.value)

def sort_alphabetically(tasks):
    return sorted(tasks, key=lambda t: t.title.lower())
```

### RQ-006: Input Validation Strategy

**Question**: Where and how should input validation occur?

**Decision**: Validate at CLI layer (boundary) with clear error messages

**Rationale**:
- Constitution principle VI (Security by Default) requires boundary validation
- Fail fast with user-friendly messages
- Service layer assumes valid input (already validated)
- Centralized validation in command handlers

**Validation Rules**:
- Title: Non-empty string, strip whitespace
- Priority: Must be "high", "medium", or "low"
- ID: Must be positive integer
- Tags: Any non-empty strings, strip whitespace

### RQ-007: Logging Strategy

**Question**: How to implement structured logging for observability?

**Decision**: Python `logging` module with custom formatter

**Rationale**:
- Standard library (no external dependencies)
- Configurable log levels
- Can output to console and/or file
- Structured format: `[LEVEL] [TIMESTAMP] [MODULE] message`

**Implementation Pattern**:
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s [%(module)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)
```

### RQ-008: Testing Strategy

**Question**: How to structure tests for TDD workflow?

**Decision**: pytest with unit tests for model/service and integration tests for CLI

**Rationale**:
- pytest is the Python standard for testing
- Fixtures for test data setup
- Parametrized tests for multiple scenarios
- Coverage via pytest-cov

**Test Structure**:
- `tests/unit/test_task_model.py`: Task creation, validation, equality
- `tests/unit/test_task_service.py`: CRUD, search, filter, sort logic
- `tests/integration/test_cli.py`: End-to-end command testing

## Summary

All technical decisions use Python standard library to minimize dependencies while following constitution principles. The architecture is:

1. **Model Layer** (`src/models/task.py`): Task dataclass with Priority enum
2. **Service Layer** (`src/services/task_service.py`): Business logic with in-memory storage
3. **CLI Layer** (`src/cli/`): Command parsing, validation, display formatting
4. **Tests**: pytest with unit and integration coverage

No external runtime dependencies required. pytest is the only development dependency.
