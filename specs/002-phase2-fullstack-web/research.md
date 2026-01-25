# Research: Phase 2 Full Stack Web Application

**Feature**: `002-phase2-fullstack-web`
**Date**: 2026-01-25
**Status**: Complete

## Research Tasks

### R1: FastAPI + SQLModel Best Practices

**Question**: How to structure FastAPI application with SQLModel for a todo app?

**Decision**: Use layered architecture with dependency injection

**Rationale**:
- Separation of concerns: models → services → API routes
- SQLModel allows single class for both DB model and Pydantic schema
- Dependency injection for database sessions enables testing
- Async endpoints for better performance (though sync is acceptable for this scale)

**Alternatives Considered**:
- Direct DB access in routes: Rejected - harder to test, violates SRP
- Repository pattern: Rejected - over-engineering for single-entity app

**Key Implementation Details**:
```python
# SQLModel combines SQLAlchemy + Pydantic
from sqlmodel import SQLModel, Field
from typing import Optional, List
from datetime import datetime

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(min_length=1)
    completed: bool = False
    priority: str = Field(default="medium")  # high/medium/low
    tags: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

---

### R2: Neon DB Connection with SQLModel

**Question**: How to connect SQLModel to Neon DB (serverless PostgreSQL)?

**Decision**: Use standard PostgreSQL connection string with connection pooling

**Rationale**:
- Neon uses standard PostgreSQL protocol
- Connection string format: `postgresql://user:password@host/dbname?sslmode=require`
- SQLModel/SQLAlchemy handles connection pooling
- SSL required for Neon connections

**Alternatives Considered**:
- Direct psycopg3: Lower level than needed
- asyncpg with async SQLAlchemy: Added complexity not needed for Phase 2

**Key Implementation Details**:
```python
from sqlmodel import create_engine, Session
import os

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session
```

---

### R3: Next.js App Router with External API

**Question**: How to integrate Next.js App Router with external FastAPI backend?

**Decision**: Use client components for interactive features, fetch API for data

**Rationale**:
- Task list requires interactivity (complete toggle, edit, delete) - client components
- Search/filter/sort are client-side operations on fetched data
- No need for Next.js API routes - FastAPI handles all backend logic
- Environment variable `NEXT_PUBLIC_API_URL` for API base URL

**Alternatives Considered**:
- Server components with server actions: Complex for CRUD operations
- Next.js API routes as proxy: Unnecessary layer of indirection

**Key Implementation Details**:
```typescript
// services/api.ts
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export async function getTasks(params?: TaskQueryParams): Promise<Task[]> {
  const query = new URLSearchParams(params as any).toString();
  const response = await fetch(`${API_URL}/tasks?${query}`);
  if (!response.ok) throw new Error('Failed to fetch tasks');
  return response.json();
}
```

---

### R4: Tags Storage Strategy

**Question**: How to store task tags in PostgreSQL?

**Decision**: JSON array column in tasks table

**Rationale**:
- Tags are simple strings with no metadata
- PostgreSQL JSON supports array operations and indexing
- Single query to get task with all tags
- SQLModel/Pydantic handles serialization automatically
- Appropriate for <1000 tasks with <10 tags each

**Alternatives Considered**:
- Separate tags table with many-to-many: Over-engineered, adds query complexity
- Array column (PostgreSQL ARRAY type): JSON more portable, easier in SQLModel
- Comma-separated string: Hard to query and validate

**Key Implementation Details**:
```python
from sqlalchemy import Column, JSON

class Task(SQLModel, table=True):
    # ... other fields
    tags: List[str] = Field(default_factory=list, sa_column=Column(JSON))
```

---

### R5: CORS Configuration for Local Development

**Question**: How to handle CORS between Next.js (port 3000) and FastAPI (port 8000)?

**Decision**: FastAPI CORS middleware with configurable origins

**Rationale**:
- Development requires cross-origin requests (different ports)
- Production may have same-origin or different CORS needs
- Environment variable for flexibility

**Key Implementation Details**:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### R6: Frontend State Management

**Question**: How to manage task state in React/Next.js?

**Decision**: React hooks with fetch + local state, no external state library

**Rationale**:
- Single page app with one main data type (tasks)
- React 18 hooks (useState, useEffect, useCallback) sufficient
- SWR or React Query would be overkill for this scale
- Keep it simple - can add complexity in later phases if needed

**Alternatives Considered**:
- Redux: Heavy for single-entity CRUD app
- Zustand: Lightweight but still unnecessary
- SWR/React Query: Good for caching but adds dependency

**Key Implementation Details**:
```typescript
// hooks/useTasks.ts
export function useTasks() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchTasks = useCallback(async () => {
    setLoading(true);
    try {
      const data = await api.getTasks();
      setTasks(data);
      setError(null);
    } catch (err) {
      setError('Failed to load tasks');
    } finally {
      setLoading(false);
    }
  }, []);

  // ... CRUD operations
  return { tasks, loading, error, fetchTasks, createTask, ... };
}
```

---

### R7: UI Component Library

**Question**: What UI approach for the frontend?

**Decision**: Tailwind CSS with custom components (no component library)

**Rationale**:
- Tailwind provides utility classes for rapid styling
- Custom components maintain full control
- No external dependency on component library versions
- Good for learning and hackathon context
- Responsive design built-in with Tailwind

**Alternatives Considered**:
- shadcn/ui: Good but adds complexity
- Material UI: Heavy, opinionated styling
- Chakra UI: Nice but another dependency

---

### R8: Error Handling Strategy

**Question**: How to handle errors consistently across frontend and backend?

**Decision**: Structured error responses with HTTP status codes

**Rationale**:
- FastAPI HTTPException for backend errors
- Consistent error shape: `{ "detail": "message" }`
- Frontend displays user-friendly messages
- Logging for debugging

**Key Implementation Details**:
```python
# Backend error response
from fastapi import HTTPException

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = service.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
```

```typescript
// Frontend error handling
try {
  await api.deleteTask(id);
} catch (error) {
  setError('Failed to delete task. Please try again.');
}
```

---

## Summary

All research questions resolved. Key decisions:

1. **Backend**: FastAPI + SQLModel with layered architecture
2. **Database**: Neon DB via standard PostgreSQL connection
3. **Tags**: JSON array column (simple, sufficient for scale)
4. **Frontend**: Next.js App Router with client components
5. **State**: React hooks (no external library)
6. **Styling**: Tailwind CSS
7. **CORS**: FastAPI middleware with configurable origins
8. **Errors**: Structured responses, user-friendly messages

No NEEDS CLARIFICATION items remain. Ready for Phase 1 design.
