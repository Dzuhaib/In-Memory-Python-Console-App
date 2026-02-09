# Tasks: Phase 2 Full Stack Web Application

**Input**: Design documents from `/specs/002-phase2-fullstack-web/`
**Prerequisites**: plan.md (required), spec.md (required), data-model.md, contracts/api-openapi.yaml, research.md, quickstart.md

**Tests**: Included per Constitution Principle II (Test-First Development - NON-NEGOTIABLE)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1-US9)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/src/`, `backend/tests/`
- **Frontend**: `frontend/src/`, `frontend/tests/`
- Paths follow plan.md structure

---

## Phase 1: Setup

**Purpose**: Project initialization and basic structure for both backend and frontend

- [x] T001 Create backend directory structure per plan.md (backend/src/, backend/tests/, backend/src/models/, backend/src/services/, backend/src/api/, backend/src/schemas/, backend/src/utils/)
- [x] T002 Create frontend directory structure per plan.md (frontend/src/, frontend/src/app/, frontend/src/components/, frontend/src/services/, frontend/src/types/, frontend/src/hooks/, frontend/tests/)
- [x] T003 [P] Create backend/pyproject.toml with Python 3.11+, FastAPI, SQLModel, uvicorn, pytest dependencies
- [x] T004 [P] Create backend/requirements.txt with pinned versions
- [x] T005 [P] Create frontend/package.json with Next.js 14+, React 18+, TypeScript, Tailwind CSS dependencies
- [x] T006 [P] Create backend/.env.example with DATABASE_URL, LOG_LEVEL, CORS_ORIGINS placeholders
- [x] T007 [P] Create frontend/.env.local.example with NEXT_PUBLIC_API_URL placeholder
- [x] T008 [P] Create backend/src/__init__.py
- [x] T009 [P] Create backend/src/models/__init__.py
- [x] T010 [P] Create backend/src/services/__init__.py
- [x] T011 [P] Create backend/src/api/__init__.py
- [x] T012 [P] Create backend/src/schemas/__init__.py
- [x] T013 [P] Create backend/src/utils/__init__.py
- [x] T014 [P] Create backend/tests/__init__.py
- [x] T015 [P] Create backend/tests/unit/__init__.py
- [x] T016 [P] Create backend/tests/integration/__init__.py
- [x] T017 [P] Create frontend/tsconfig.json with strict TypeScript config
- [x] T018 [P] Create frontend/tailwind.config.js with content paths
- [x] T019 [P] Create frontend/next.config.js with basic configuration

**Checkpoint**: Project structure ready - run `python -c "import backend.src"` and `npm install` in frontend/ to verify

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T020 Create Priority enum (HIGH, MEDIUM, LOW) in backend/src/models/task.py
- [x] T021 Create SQLModel Task model with id, title, completed, priority, tags, created_at, updated_at in backend/src/models/task.py
- [x] T022 Add Task validation in model (title min_length=1, max_length=500) in backend/src/models/task.py
- [x] T023 Create database engine and session dependency in backend/src/database.py
- [x] T024 Create table initialization function create_db_and_tables() in backend/src/database.py
- [x] T025 Create environment configuration loader in backend/src/config.py
- [x] T026 Create structured logging setup in backend/src/utils/logger.py
- [x] T027 [P] Create Pydantic schemas (CreateTaskRequest, UpdateTaskRequest, AddTagRequest) in backend/src/schemas/task.py
- [x] T028 [P] Create TypeScript types (Task, Priority, CreateTaskRequest, UpdateTaskRequest, TaskQueryParams) in frontend/src/types/task.ts
- [x] T029 Create FastAPI app instance with CORS middleware in backend/src/main.py
- [x] T030 Create API router aggregation in backend/src/api/router.py
- [x] T031 Create base TaskService class with db session dependency in backend/src/services/task_service.py
- [x] T032 Create API client service with fetch wrapper in frontend/src/services/api.ts
- [x] T033 Create root layout with Tailwind CSS in frontend/src/app/layout.tsx
- [x] T034 Create global styles in frontend/src/app/globals.css
- [x] T035 Create pytest conftest.py with test database fixtures in backend/tests/conftest.py

**Checkpoint**: Foundation ready - backend runs with `uvicorn backend.src.main:app --reload` and frontend runs with `npm run dev`

---

## Phase 3: User Story 1 - View and Add Tasks (Priority: P1) MVP

**Goal**: Users can access a web interface to view their task list and add new tasks with titles, priorities, and tags

**Independent Test**: Open web app in browser, see empty list, add task with title/priority/tags, see it appear, refresh page and verify persistence

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T036 [P] [US1] Write unit test for TaskService.create_task() in backend/tests/unit/test_task_service.py
- [x] T037 [P] [US1] Write unit test for TaskService.list_tasks() in backend/tests/unit/test_task_service.py
- [x] T038 [P] [US1] Write unit test for Task model creation and validation in backend/tests/unit/test_models.py
- [x] T039 [US1] Write integration test for POST /tasks endpoint in backend/tests/integration/test_api.py
- [x] T040 [US1] Write integration test for GET /tasks endpoint in backend/tests/integration/test_api.py

### Implementation for User Story 1

- [x] T041 [US1] Implement TaskService.create_task(title, priority, tags) in backend/src/services/task_service.py
- [x] T042 [US1] Implement TaskService.list_tasks() returning all tasks in backend/src/services/task_service.py
- [x] T043 [US1] Implement POST /tasks endpoint in backend/src/api/tasks.py
- [x] T044 [US1] Implement GET /tasks endpoint (basic, no filters yet) in backend/src/api/tasks.py
- [x] T045 [US1] Create TaskForm component with title, priority, tags inputs in frontend/src/components/TaskForm.tsx
- [x] T046 [US1] Create TaskItem component displaying task details in frontend/src/components/TaskItem.tsx
- [x] T047 [US1] Create TaskList component with empty state message in frontend/src/components/TaskList.tsx
- [x] T048 [US1] Create useTasks hook with fetchTasks and createTask functions in frontend/src/hooks/useTasks.ts
- [x] T049 [US1] Implement main page with TaskList and TaskForm in frontend/src/app/page.tsx
- [x] T050 [US1] Add loading and error states to TaskList in frontend/src/components/TaskList.tsx

**Checkpoint**: User Story 1 complete - can add and view tasks via web UI with persistence

---

## Phase 4: User Story 2 - Mark Tasks Complete/Incomplete (Priority: P2)

**Goal**: Users can toggle the completion status of tasks directly from the web interface

**Independent Test**: Click checkbox/button on task to mark complete, see visual change, click again to uncomplete, refresh to verify persistence

### Tests for User Story 2

- [x] T051 [P] [US2] Write unit test for TaskService.toggle_complete() in backend/tests/unit/test_task_service.py
- [x] T052 [US2] Write integration test for PATCH /tasks/{id}/complete endpoint in backend/tests/integration/test_api.py

### Implementation for User Story 2

- [x] T053 [US2] Implement TaskService.get_task(id) in backend/src/services/task_service.py
- [x] T054 [US2] Implement TaskService.toggle_complete(id) in backend/src/services/task_service.py
- [x] T055 [US2] Implement PATCH /tasks/{id}/complete endpoint in backend/src/api/tasks.py
- [x] T056 [US2] Add completion toggle checkbox to TaskItem in frontend/src/components/TaskItem.tsx
- [x] T057 [US2] Add toggleComplete function to useTasks hook in frontend/src/hooks/useTasks.ts
- [x] T058 [US2] Add visual indicator (strikethrough/checkmark) for completed tasks in frontend/src/components/TaskItem.tsx

**Checkpoint**: User Story 2 complete - can toggle task completion status

---

## Phase 5: User Story 3 - Update Task Details (Priority: P3)

**Goal**: Users can edit task titles and priorities through the web interface

**Independent Test**: Click edit on task, modify title/priority, save, see updated info in list, verify empty title rejected

### Tests for User Story 3

- [x] T059 [P] [US3] Write unit test for TaskService.update_task() in backend/tests/unit/test_task_service.py
- [x] T060 [US3] Write integration test for PUT /tasks/{id} endpoint in backend/tests/integration/test_api.py

### Implementation for User Story 3

- [x] T061 [US3] Implement TaskService.update_task(id, title, priority) in backend/src/services/task_service.py
- [x] T062 [US3] Implement PUT /tasks/{id} endpoint in backend/src/api/tasks.py
- [x] T063 [US3] Add edit mode to TaskItem with inline form in frontend/src/components/TaskItem.tsx
- [x] T064 [US3] Add updateTask function to useTasks hook in frontend/src/hooks/useTasks.ts
- [x] T065 [US3] Add validation error display for empty title in frontend/src/components/TaskItem.tsx

**Checkpoint**: User Story 3 complete - can update task details

---

## Phase 6: User Story 4 - Delete Tasks (Priority: P4)

**Goal**: Users can remove tasks from the list permanently

**Independent Test**: Click delete on task, confirm deletion, verify task removed from list and database

### Tests for User Story 4

- [x] T066 [P] [US4] Write unit test for TaskService.delete_task() in backend/tests/unit/test_task_service.py
- [x] T067 [US4] Write integration test for DELETE /tasks/{id} endpoint in backend/tests/integration/test_api.py

### Implementation for User Story 4

- [x] T068 [US4] Implement TaskService.delete_task(id) in backend/src/services/task_service.py
- [x] T069 [US4] Implement DELETE /tasks/{id} endpoint in backend/src/api/tasks.py
- [x] T070 [US4] Add delete button with confirmation to TaskItem in frontend/src/components/TaskItem.tsx
- [x] T071 [US4] Add deleteTask function to useTasks hook in frontend/src/hooks/useTasks.ts

**Checkpoint**: User Story 4 complete - can delete tasks

---

## Phase 7: User Story 5 - Manage Task Tags (Priority: P5)

**Goal**: Users can add and remove tags from existing tasks through the web interface

**Independent Test**: Add tag to task, see it appear, remove tag, see it disappear, refresh to verify persistence

### Tests for User Story 5

- [x] T072 [P] [US5] Write unit test for TaskService.add_tag() in backend/tests/unit/test_task_service.py
- [x] T073 [P] [US5] Write unit test for TaskService.remove_tag() in backend/tests/unit/test_task_service.py
- [x] T074 [US5] Write integration test for POST /tasks/{id}/tags endpoint in backend/tests/integration/test_api.py
- [x] T075 [US5] Write integration test for DELETE /tasks/{id}/tags/{tag} endpoint in backend/tests/integration/test_api.py

### Implementation for User Story 5

- [x] T076 [US5] Implement TaskService.add_tag(id, tag) in backend/src/services/task_service.py
- [x] T077 [US5] Implement TaskService.remove_tag(id, tag) in backend/src/services/task_service.py
- [x] T078 [US5] Implement POST /tasks/{id}/tags endpoint in backend/src/api/tasks.py
- [x] T079 [US5] Implement DELETE /tasks/{id}/tags/{tag} endpoint in backend/src/api/tasks.py
- [x] T080 [US5] Add tag display with remove button to TaskItem in frontend/src/components/TaskItem.tsx
- [x] T081 [US5] Add tag input for adding new tags to TaskItem in frontend/src/components/TaskItem.tsx
- [x] T082 [US5] Add addTag and removeTag functions to useTasks hook in frontend/src/hooks/useTasks.ts

**Checkpoint**: User Story 5 complete - can manage task tags

---

## Phase 8: User Story 6 - Search Tasks (Priority: P6)

**Goal**: Users can search for tasks by keyword, with case-insensitive matching

**Independent Test**: Type search term, see list filter to matches only, clear search to see all tasks

### Tests for User Story 6

- [x] T083 [P] [US6] Write unit test for TaskService.search_tasks() case-insensitive in backend/tests/unit/test_task_service.py
- [x] T084 [US6] Write integration test for GET /tasks?search= in backend/tests/integration/test_api.py

### Implementation for User Story 6

- [x] T085 [US6] Implement TaskService.search_tasks(keyword) with case-insensitive ILIKE in backend/src/services/task_service.py
- [x] T086 [US6] Add search parameter to GET /tasks endpoint in backend/src/api/tasks.py
- [x] T087 [US6] Create SearchBar component with debounced input in frontend/src/components/SearchBar.tsx (integrated into page.tsx)
- [x] T088 [US6] Add search state and function to useTasks hook in frontend/src/hooks/useTasks.ts
- [x] T089 [US6] Integrate SearchBar into main page in frontend/src/app/page.tsx

**Checkpoint**: User Story 6 complete - search works case-insensitively

---

## Phase 9: User Story 7 - Filter Tasks (Priority: P7)

**Goal**: Users can filter tasks by status (complete/incomplete), priority level, or tag

**Independent Test**: Apply filters (status, priority, tag), see list update, apply multiple filters to verify AND logic

### Tests for User Story 7

- [x] T090 [P] [US7] Write unit test for TaskService.filter_tasks(status) in backend/tests/unit/test_task_service.py
- [x] T091 [P] [US7] Write unit test for TaskService.filter_tasks(priority) in backend/tests/unit/test_task_service.py
- [x] T092 [P] [US7] Write unit test for TaskService.filter_tasks(tag) in backend/tests/unit/test_task_service.py
- [x] T093 [US7] Write integration test for GET /tasks with filter params in backend/tests/integration/test_api.py

### Implementation for User Story 7

- [x] T094 [US7] Implement TaskService.filter_tasks(status, priority, tag) with AND logic in backend/src/services/task_service.py
- [x] T095 [US7] Add status, priority, tag filter parameters to GET /tasks endpoint in backend/src/api/tasks.py
- [x] T096 [US7] Create FilterPanel component with status/priority/tag dropdowns in frontend/src/components/FilterPanel.tsx (integrated into page.tsx)
- [x] T097 [US7] Add filter state and functions to useTasks hook in frontend/src/hooks/useTasks.ts
- [x] T098 [US7] Integrate FilterPanel into main page in frontend/src/app/page.tsx

**Checkpoint**: User Story 7 complete - can filter tasks by multiple criteria with AND logic

---

## Phase 10: User Story 8 - Sort Tasks (Priority: P8)

**Goal**: Users can sort tasks by priority, alphabetically by title, or by creation order

**Independent Test**: Select sort option, see list reorder, verify high priority first for priority sort

### Tests for User Story 8

- [x] T099 [P] [US8] Write unit test for TaskService.sort_tasks(by='priority') in backend/tests/unit/test_task_service.py
- [x] T100 [P] [US8] Write unit test for TaskService.sort_tasks(by='alpha') in backend/tests/unit/test_task_service.py
- [x] T101 [US8] Write integration test for GET /tasks?sort= in backend/tests/integration/test_api.py

### Implementation for User Story 8

- [x] T102 [US8] Implement TaskService.sort_tasks(tasks, sort_by) in backend/src/services/task_service.py
- [x] T103 [US8] Add sort parameter to GET /tasks endpoint in backend/src/api/tasks.py
- [x] T104 [US8] Create SortSelect component with priority/alpha/id options in frontend/src/components/SortSelect.tsx (integrated into page.tsx)
- [x] T105 [US8] Add sort state and function to useTasks hook in frontend/src/hooks/useTasks.ts
- [x] T106 [US8] Integrate SortSelect into main page in frontend/src/app/page.tsx

**Checkpoint**: User Story 8 complete - can sort tasks

---

## Phase 11: User Story 9 - API Health and Documentation (Priority: P9)

**Goal**: Developers can access API documentation and verify the backend is running

**Independent Test**: Navigate to /docs for Swagger UI, hit /health for status check

### Tests for User Story 9

- [x] T107 [P] [US9] Write integration test for GET /health endpoint in backend/tests/integration/test_api.py

### Implementation for User Story 9

- [x] T108 [US9] Implement GET /health endpoint returning status and timestamp in backend/src/api/tasks.py
- [x] T109 [US9] Verify FastAPI auto-generates /docs with OpenAPI from existing endpoints in backend/src/main.py

**Checkpoint**: User Story 9 complete - API docs and health check available

---

## Phase 12: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements that affect multiple user stories

- [x] T110 [P] Add comprehensive error messages for all edge cases in backend/src/api/tasks.py
- [x] T111 [P] Add logging calls for all operations in backend/src/services/task_service.py
- [x] T112 [P] Add responsive styling for mobile browsers in frontend/src/app/globals.css
- [x] T113 [P] Add loading spinners and disabled states during API calls in frontend/src/components/
- [x] T114 Run backend test suite and verify >80% coverage with pytest --cov (97% coverage achieved)
- [x] T115 Run frontend test suite with npm test (no frontend tests, but build passes with TypeScript type checking)
- [ ] T116 Run quickstart.md validation (manual walkthrough)
- [x] T117 Code cleanup: ensure PEP 8 compliance across backend files
- [x] T118 Code cleanup: ensure ESLint compliance across frontend files (build passes with linting)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies - start immediately
- **Phase 2 (Foundational)**: Depends on Phase 1 - BLOCKS all user stories
- **Phases 3-11 (User Stories)**: All depend on Phase 2 completion
  - US1 (P1): No dependencies on other stories - can start after Phase 2
  - US2 (P2): Can start after Phase 2 (independent of US1 for basic toggle)
  - US3 (P3): Can start after Phase 2
  - US4 (P4): Can start after Phase 2
  - US5 (P5): Can start after Phase 2
  - US6 (P6): Can start after Phase 2
  - US7 (P7): Can start after Phase 2
  - US8 (P8): Can start after Phase 2
  - US9 (P9): Can start after Phase 2
- **Phase 12 (Polish)**: Depends on all user stories complete

### Within Each User Story

- Tests MUST be written and FAIL before implementation (TDD)
- Backend before frontend (API must exist before UI calls it)
- Services before API endpoints
- Core implementation before UI integration

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T003-T019)
- Backend and frontend structure creation can run in parallel
- Within each user story, tests marked [P] can run in parallel
- Different user stories can be worked on in parallel by different developers

---

## Parallel Example: Setup Phase

```bash
# Launch all backend init files together:
Task: "Create backend/src/__init__.py"
Task: "Create backend/src/models/__init__.py"
Task: "Create backend/src/services/__init__.py"
Task: "Create backend/src/api/__init__.py"
Task: "Create backend/src/schemas/__init__.py"
Task: "Create backend/src/utils/__init__.py"

# Launch all frontend config together:
Task: "Create frontend/tsconfig.json"
Task: "Create frontend/tailwind.config.js"
Task: "Create frontend/next.config.js"
```

## Parallel Example: User Story 1 Tests

```bash
# Launch all US1 tests together:
Task: "Write unit test for TaskService.create_task()"
Task: "Write unit test for TaskService.list_tasks()"
Task: "Write unit test for Task model creation and validation"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1 (View and Add Tasks)
4. **STOP and VALIDATE**: Can add tasks and view them in web browser
5. Deploy/demo if ready - this is a working web todo app!

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add US1 → Test → **MVP!** (add/view via web)
3. Add US2 → Test → Can track completion
4. Add US3 → Test → Can edit tasks
5. Add US4 → Test → Can delete tasks
6. Add US5 → Test → Can manage tags
7. Add US6 → Test → Can search tasks
8. Add US7 → Test → Can filter tasks
9. Add US8 → Test → Can sort tasks
10. Add US9 → Test → API docs available
11. Polish → Production ready

### Recommended Execution Order (Solo Developer)

1. T001-T035 (Setup + Foundational)
2. T036-T050 (US1 - MVP)
3. T051-T058 (US2 - Complete/Uncomplete)
4. T059-T065 (US3 - Update)
5. T066-T071 (US4 - Delete)
6. T072-T082 (US5 - Tags)
7. T083-T089 (US6 - Search)
8. T090-T098 (US7 - Filter)
9. T099-T106 (US8 - Sort)
10. T107-T109 (US9 - Health/Docs)
11. T110-T118 (Polish)

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable
- TDD: Write tests first, verify they FAIL, then implement
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Backend tests use pytest with test database
- Frontend tests use Jest/React Testing Library
