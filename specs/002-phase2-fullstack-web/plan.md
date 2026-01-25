# Implementation Plan: Phase 2 Full Stack Web Application

**Branch**: `002-phase2-fullstack-web` | **Date**: 2026-01-25 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-phase2-fullstack-web/spec.md`

## Summary

Migrate Phase 1 in-memory console application to a full-stack web application with persistent PostgreSQL storage. The backend will use FastAPI with SQLModel ORM connecting to Neon DB, while the frontend will use Next.js App Router. All 9 user stories (CRUD, complete/uncomplete, tags, search, filter, sort) will be accessible via REST API and responsive web interface.

## Technical Context

**Language/Version**: Python 3.11+ (backend), TypeScript 5.x (frontend)
**Primary Dependencies**:
- Backend: FastAPI, SQLModel, psycopg2-binary, uvicorn, pydantic
- Frontend: Next.js 14+, React 18+, TypeScript, Tailwind CSS
**Storage**: PostgreSQL (Neon DB - serverless)
**Testing**:
- Backend: pytest, pytest-asyncio, httpx (for API testing)
- Frontend: Jest, React Testing Library, Playwright (e2e)
**Target Platform**: Web browsers (Chrome, Firefox, Safari, Edge - latest 2 versions)
**Project Type**: Web application (separate frontend + backend)
**Performance Goals**:
- API: <200ms p95 response time
- Frontend: Lighthouse >80, <2s page load
**Constraints**:
- <500ms API response for typical operations
- Single-user (no authentication in Phase 2)
- Must work on desktop and mobile browsers
**Scale/Scope**: Single user, ~1000 tasks maximum, development/demo scale

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Phased Evolution | PASS | Phase 1 complete (82 tests passing), Phase 2 is next in sequence |
| II. Test-First Development | PASS | TDD will be followed - tests before implementation |
| III. Smallest Viable Change | PASS | Only migrating existing features + persistence, no new features |
| IV. Clean Interfaces | PASS | REST API contracts defined, clear separation frontend/backend |
| V. Observability First | PASS | Structured logging carried from Phase 1, API logging added |
| VI. Security by Default | PASS | No hardcoded secrets (env vars), input validation at API boundaries |

**Gate Status**: PASS - Proceed to Phase 0

## Project Structure

### Documentation (this feature)

```text
specs/002-phase2-fullstack-web/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── api-openapi.yaml # REST API contract
├── checklists/          # Validation checklists
│   └── requirements.md  # Spec quality checklist
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Environment configuration
│   ├── database.py          # Database connection/session
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py          # SQLModel Task model
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── task.py          # Pydantic request/response schemas
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_service.py  # Business logic
│   ├── api/
│   │   ├── __init__.py
│   │   ├── router.py        # API router aggregation
│   │   └── tasks.py         # Task endpoints
│   └── utils/
│       ├── __init__.py
│       └── logger.py        # Structured logging
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Pytest fixtures
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_models.py
│   │   └── test_services.py
│   └── integration/
│       ├── __init__.py
│       └── test_api.py      # API endpoint tests
├── pyproject.toml
├── requirements.txt
└── .env.example

frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx       # Root layout
│   │   ├── page.tsx         # Home page (task list)
│   │   └── globals.css      # Global styles
│   ├── components/
│   │   ├── TaskList.tsx     # Task list display
│   │   ├── TaskItem.tsx     # Single task row
│   │   ├── TaskForm.tsx     # Add/Edit task form
│   │   ├── SearchBar.tsx    # Search input
│   │   ├── FilterPanel.tsx  # Filter controls
│   │   └── SortSelect.tsx   # Sort dropdown
│   ├── services/
│   │   └── api.ts           # API client
│   ├── types/
│   │   └── task.ts          # TypeScript types
│   └── hooks/
│       └── useTasks.ts      # Task data hook
├── tests/
│   ├── components/          # Component tests
│   └── e2e/                 # Playwright tests
├── package.json
├── tsconfig.json
├── tailwind.config.js
├── next.config.js
└── .env.local.example
```

**Structure Decision**: Web application with separate `backend/` and `frontend/` directories at repository root. This enables independent development, testing, and deployment of each tier while maintaining a monorepo structure for simplicity.

## Complexity Tracking

> No Constitution violations - no entries needed.

## Architecture Decisions

### AD-001: Monorepo with Separate Backend/Frontend

**Decision**: Keep backend and frontend in same repository as sibling directories.

**Rationale**:
- Simplifies development workflow (single git clone)
- Shared documentation and specs
- Easier to maintain consistency between API contract and frontend types
- Appropriate for single-developer hackathon context

**Alternatives Rejected**:
- Separate repositories: Overhead of managing multiple repos not justified for Phase 2 scope

### AD-002: SQLModel for ORM

**Decision**: Use SQLModel (Pydantic + SQLAlchemy) for database models.

**Rationale**:
- Single model definition for both DB and API validation
- Built-in Pydantic integration with FastAPI
- Type safety with Python type hints
- Simpler than raw SQLAlchemy for this use case

**Alternatives Rejected**:
- Raw SQLAlchemy: More boilerplate, separate Pydantic models needed
- Tortoise ORM: Less mature, smaller community

### AD-003: Tags as JSON Array

**Decision**: Store tags as a PostgreSQL JSON array column rather than separate table.

**Rationale**:
- Simpler schema - single table for tasks
- Tags are simple strings, no metadata needed
- Good enough for <1000 tasks, ~10 tags per task
- Neon DB supports PostgreSQL JSON operations

**Alternatives Rejected**:
- Separate tags table with many-to-many: Over-engineered for current scale
- Comma-separated string: Harder to query and validate

### AD-004: Next.js App Router with Server Components

**Decision**: Use Next.js 14+ App Router with React Server Components where appropriate.

**Rationale**:
- Modern React patterns (server components)
- Built-in API route handling (though we use separate FastAPI backend)
- File-based routing simplifies structure
- Good TypeScript support

**Alternatives Rejected**:
- Pages Router: Legacy pattern, App Router is the future
- Create React App: No longer maintained, less features
- Vite + React: Requires more configuration for SSR

## API Design Overview

Base URL: `http://localhost:8000/api/v1`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /tasks | List all tasks (with filters, search, sort) |
| POST | /tasks | Create new task |
| GET | /tasks/{id} | Get single task |
| PUT | /tasks/{id} | Update task |
| DELETE | /tasks/{id} | Delete task |
| PATCH | /tasks/{id}/complete | Toggle completion |
| POST | /tasks/{id}/tags | Add tag |
| DELETE | /tasks/{id}/tags/{tag} | Remove tag |
| GET | /health | Health check |
| GET | /docs | OpenAPI documentation |

## Testing Strategy

### Backend Testing

1. **Unit Tests** (pytest)
   - Model validation (Task creation, priority enum)
   - Service layer logic (CRUD, search, filter, sort)

2. **Integration Tests** (pytest + httpx)
   - Full API endpoint testing
   - Database operations
   - Error handling

### Frontend Testing

1. **Component Tests** (Jest + React Testing Library)
   - TaskList, TaskItem, TaskForm rendering
   - User interactions (click, type, submit)

2. **E2E Tests** (Playwright)
   - Full user flows (add task, complete, delete)
   - Cross-browser verification

### Test Coverage Target

- Backend: >80% coverage
- Frontend: >70% coverage (components)
- E2E: All 9 user stories covered

## Deployment Architecture (Development)

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Browser       │────▶│  Next.js        │────▶│  FastAPI        │
│   (User)        │     │  (localhost:3000)│     │  (localhost:8000)│
└─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                         │
                                                         ▼
                                                ┌─────────────────┐
                                                │   Neon DB       │
                                                │   (PostgreSQL)  │
                                                └─────────────────┘
```

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://user:password@neon-host/dbname
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:3000
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

## Migration from Phase 1

The Phase 1 console app provides the reference implementation for business logic:

| Phase 1 Component | Phase 2 Equivalent |
|-------------------|-------------------|
| `src/models/task.py` | `backend/src/models/task.py` (SQLModel) |
| `src/services/task_service.py` | `backend/src/services/task_service.py` |
| `src/cli/commands.py` | `backend/src/api/tasks.py` (REST endpoints) |
| `src/cli/display.py` | `frontend/src/components/*.tsx` |

The business logic (validation, search, filter, sort algorithms) can be largely preserved; only the I/O layer changes from CLI to HTTP/HTML.
