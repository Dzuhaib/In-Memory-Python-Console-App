# Tasks: Phase 1 Todo Console App

**Input**: Design documents from `/specs/001-phase1-todo-console/`
**Prerequisites**: plan.md (required), spec.md (required), data-model.md, contracts/cli-commands.md

**Tests**: Included per Constitution Principle II (Test-First Development - NON-NEGOTIABLE)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1-US9)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths follow plan.md structure

---

## Phase 1: Setup

**Purpose**: Project initialization and basic structure

- [x] T001 Create project directory structure per plan.md (src/, tests/, src/models/, src/services/, src/cli/, src/utils/)
- [x] T002 Create pyproject.toml with project metadata, Python 3.11+ requirement, and pytest dependencies
- [x] T003 [P] Create src/__init__.py with package initialization
- [x] T004 [P] Create src/models/__init__.py
- [x] T005 [P] Create src/services/__init__.py
- [x] T006 [P] Create src/cli/__init__.py
- [x] T007 [P] Create src/utils/__init__.py
- [x] T008 [P] Create tests/__init__.py
- [x] T009 [P] Create tests/unit/__init__.py
- [x] T010 [P] Create tests/integration/__init__.py

**Checkpoint**: Project structure ready - run `python -c "import src"` to verify

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T011 Create Priority enum (HIGH=1, MEDIUM=2, LOW=3) in src/models/task.py
- [x] T012 Create Task dataclass with id, title, completed, priority, tags fields in src/models/task.py
- [x] T013 Add Task validation in __post_init__ (title non-empty, priority valid) in src/models/task.py
- [x] T014 Create structured logging setup in src/utils/logger.py
- [x] T015 Create TaskService class with _tasks dict and _next_id counter in src/services/task_service.py
- [x] T016 Create display formatting functions (format_task, format_task_list) in src/cli/display.py
- [x] T017 Create CLI main loop with command dispatcher in src/cli/main.py
- [x] T018 Create command argument parser (handle quotes, --flags) in src/cli/commands.py
- [x] T019 Implement help command showing all available commands in src/cli/commands.py
- [x] T020 Implement exit/quit commands in src/cli/commands.py
- [x] T021 Implement unknown command error handler in src/cli/commands.py

**Checkpoint**: Foundation ready - run `python -m src.cli.main` shows prompt and help works

---

## Phase 3: User Story 1 - Create and View Tasks (Priority: P1) MVP

**Goal**: Users can add tasks and view the task list

**Independent Test**: Add tasks via CLI, view list, verify tasks appear with IDs

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T022 [P] [US1] Write unit test for TaskService.create_task() in tests/unit/test_task_service.py
- [x] T023 [P] [US1] Write unit test for TaskService.list_tasks() in tests/unit/test_task_service.py
- [x] T024 [P] [US1] Write unit test for Task creation validation in tests/unit/test_task_model.py
- [x] T025 [US1] Write integration test for add command in tests/integration/test_cli.py
- [x] T026 [US1] Write integration test for list command in tests/integration/test_cli.py

### Implementation for User Story 1

- [x] T027 [US1] Implement TaskService.create_task(title, priority, tags) in src/services/task_service.py
- [x] T028 [US1] Implement TaskService.list_tasks() returning all tasks in src/services/task_service.py
- [x] T029 [US1] Implement add command handler with --priority and --tags options in src/cli/commands.py
- [x] T030 [US1] Implement list command handler (basic, no filters yet) in src/cli/commands.py
- [x] T031 [US1] Add input validation for empty title in add command in src/cli/commands.py

**Checkpoint**: User Story 1 complete - can add and view tasks via CLI

---

## Phase 4: User Story 2 - Mark Tasks Complete (Priority: P2)

**Goal**: Users can mark tasks as complete and see completion status

**Independent Test**: Create task, mark complete, verify status changes in list

### Tests for User Story 2

- [x] T032 [P] [US2] Write unit test for TaskService.complete_task() in tests/unit/test_task_service.py
- [x] T033 [P] [US2] Write unit test for TaskService.uncomplete_task() in tests/unit/test_task_service.py
- [x] T034 [US2] Write integration test for complete command in tests/integration/test_cli.py

### Implementation for User Story 2

- [x] T035 [US2] Implement TaskService.get_task(id) in src/services/task_service.py
- [x] T036 [US2] Implement TaskService.complete_task(id) in src/services/task_service.py
- [x] T037 [US2] Implement TaskService.uncomplete_task(id) in src/services/task_service.py
- [x] T038 [US2] Implement complete command handler in src/cli/commands.py
- [x] T039 [US2] Implement uncomplete command handler in src/cli/commands.py
- [x] T040 [US2] Update display.format_task() to show [x]/[ ] status indicators in src/cli/display.py

**Checkpoint**: User Story 2 complete - can mark tasks complete/incomplete

---

## Phase 5: User Story 3 - Update Task Details (Priority: P3)

**Goal**: Users can update task titles

**Independent Test**: Create task, update title, verify change in list

### Tests for User Story 3

- [x] T041 [P] [US3] Write unit test for TaskService.update_task() in tests/unit/test_task_service.py
- [x] T042 [US3] Write integration test for update command in tests/integration/test_cli.py

### Implementation for User Story 3

- [x] T043 [US3] Implement TaskService.update_task(id, title, priority) in src/services/task_service.py
- [x] T044 [US3] Implement update command handler with --title and --priority options in src/cli/commands.py
- [x] T045 [US3] Add validation for empty title in update command in src/cli/commands.py

**Checkpoint**: User Story 3 complete - can update task details

---

## Phase 6: User Story 4 - Delete Tasks (Priority: P4)

**Goal**: Users can delete tasks from the list

**Independent Test**: Create task, delete it, verify removed from list

### Tests for User Story 4

- [x] T046 [P] [US4] Write unit test for TaskService.delete_task() in tests/unit/test_task_service.py
- [x] T047 [US4] Write integration test for delete command in tests/integration/test_cli.py

### Implementation for User Story 4

- [x] T048 [US4] Implement TaskService.delete_task(id) in src/services/task_service.py
- [x] T049 [US4] Implement delete command handler in src/cli/commands.py

**Checkpoint**: User Story 4 complete - can delete tasks

---

## Phase 7: User Story 5 - Assign Priority Levels (Priority: P5)

**Goal**: Users can create tasks with priorities and update priorities

**Independent Test**: Create tasks with different priorities, verify display correctly

### Tests for User Story 5

- [x] T050 [P] [US5] Write unit test for priority validation in Task model in tests/unit/test_task_model.py
- [x] T051 [US5] Write integration test for add with --priority in tests/integration/test_cli.py

### Implementation for User Story 5

- [x] T052 [US5] Add priority display formatting in src/cli/display.py
- [x] T053 [US5] Add priority validation in add command (reject invalid values) in src/cli/commands.py
- [x] T054 [US5] Verify default priority is MEDIUM when not specified in src/cli/commands.py

**Checkpoint**: User Story 5 complete - priorities work in add/update/display

---

## Phase 8: User Story 6 - Categorize Tasks with Tags (Priority: P6)

**Goal**: Users can add and remove tags from tasks

**Independent Test**: Create task with tags, add/remove tags, verify in list

### Tests for User Story 6

- [x] T055 [P] [US6] Write unit test for TaskService.add_tag() in tests/unit/test_task_service.py
- [x] T056 [P] [US6] Write unit test for TaskService.remove_tag() in tests/unit/test_task_service.py
- [x] T057 [US6] Write integration test for tag command in tests/integration/test_cli.py

### Implementation for User Story 6

- [x] T058 [US6] Implement TaskService.add_tag(id, tag) in src/services/task_service.py
- [x] T059 [US6] Implement TaskService.remove_tag(id, tag) in src/services/task_service.py
- [x] T060 [US6] Implement tag command handler (add/remove actions) in src/cli/commands.py
- [x] T061 [US6] Update display.format_task() to show tags in src/cli/display.py

**Checkpoint**: User Story 6 complete - can manage task tags

---

## Phase 9: User Story 7 - Search Tasks (Priority: P7)

**Goal**: Users can search tasks by keyword

**Independent Test**: Create multiple tasks, search for keyword, verify only matches returned

### Tests for User Story 7

- [x] T062 [P] [US7] Write unit test for TaskService.search_tasks() case-insensitive in tests/unit/test_task_service.py
- [x] T063 [US7] Write integration test for search command in tests/integration/test_cli.py

### Implementation for User Story 7

- [x] T064 [US7] Implement TaskService.search_tasks(keyword) with case-insensitive matching in src/services/task_service.py
- [x] T065 [US7] Implement search command handler in src/cli/commands.py

**Checkpoint**: User Story 7 complete - search works case-insensitively

---

## Phase 10: User Story 8 - Filter Tasks (Priority: P8)

**Goal**: Users can filter tasks by status, priority, or tag

**Independent Test**: Create tasks with varying attributes, apply filters, verify correct subset

### Tests for User Story 8

- [x] T066 [P] [US8] Write unit test for TaskService.filter_tasks(status) in tests/unit/test_task_service.py
- [x] T067 [P] [US8] Write unit test for TaskService.filter_tasks(priority) in tests/unit/test_task_service.py
- [x] T068 [P] [US8] Write unit test for TaskService.filter_tasks(tag) in tests/unit/test_task_service.py
- [x] T069 [US8] Write integration test for list --status/--priority/--tag in tests/integration/test_cli.py

### Implementation for User Story 8

- [x] T070 [US8] Implement TaskService.filter_tasks(status, priority, tag) with AND logic in src/services/task_service.py
- [x] T071 [US8] Add --status filter option to list command in src/cli/commands.py
- [x] T072 [US8] Add --priority filter option to list command in src/cli/commands.py
- [x] T073 [US8] Add --tag filter option to list command in src/cli/commands.py

**Checkpoint**: User Story 8 complete - can filter tasks by multiple criteria

---

## Phase 11: User Story 9 - Sort Tasks (Priority: P9)

**Goal**: Users can sort tasks by priority or alphabetically

**Independent Test**: Create tasks with different priorities/titles, sort, verify order

### Tests for User Story 9

- [x] T074 [P] [US9] Write unit test for TaskService.sort_tasks(by='priority') in tests/unit/test_task_service.py
- [x] T075 [P] [US9] Write unit test for TaskService.sort_tasks(by='alpha') in tests/unit/test_task_service.py
- [x] T076 [US9] Write integration test for list --sort in tests/integration/test_cli.py

### Implementation for User Story 9

- [x] T077 [US9] Implement TaskService.sort_tasks(tasks, sort_by) in src/services/task_service.py
- [x] T078 [US9] Add --sort option to list command (priority/alpha/id) in src/cli/commands.py

**Checkpoint**: User Story 9 complete - can sort tasks

---

## Phase 12: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements that affect multiple user stories

- [x] T079 [P] Add comprehensive error messages for all edge cases in src/cli/commands.py
- [x] T080 [P] Add logging calls for all operations in src/services/task_service.py
- [x] T081 Run full test suite and verify >80% coverage with pytest --cov
- [ ] T082 Run quickstart.md validation (manual walkthrough)
- [x] T083 Code cleanup: ensure PEP 8 compliance across all files

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies - start immediately
- **Phase 2 (Foundational)**: Depends on Phase 1 - BLOCKS all user stories
- **Phases 3-11 (User Stories)**: All depend on Phase 2 completion
  - US1 (P1): No dependencies on other stories - can start after Phase 2
  - US2 (P2): Can start after Phase 2 (uses get_task from US2 but that's within US2)
  - US3 (P3): Can start after Phase 2
  - US4 (P4): Can start after Phase 2
  - US5 (P5): Can start after Phase 2 (priority is in Task model from Phase 2)
  - US6 (P6): Can start after Phase 2
  - US7 (P7): Can start after Phase 2
  - US8 (P8): Can start after Phase 2
  - US9 (P9): Can start after Phase 2
- **Phase 12 (Polish)**: Depends on all user stories complete

### Within Each User Story

- Tests MUST be written and FAIL before implementation (TDD)
- Models before services (already done in Phase 2)
- Services before CLI commands
- Core implementation before validation/edge cases

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T003-T010)
- Within each user story, tests marked [P] can run in parallel
- Different user stories can be worked on in parallel by different developers

---

## Parallel Example: Setup Phase

```bash
# Launch all init files together:
Task: "Create src/__init__.py"
Task: "Create src/models/__init__.py"
Task: "Create src/services/__init__.py"
Task: "Create src/cli/__init__.py"
Task: "Create src/utils/__init__.py"
Task: "Create tests/__init__.py"
Task: "Create tests/unit/__init__.py"
Task: "Create tests/integration/__init__.py"
```

## Parallel Example: User Story 1 Tests

```bash
# Launch all US1 unit tests together:
Task: "Write unit test for TaskService.create_task()"
Task: "Write unit test for TaskService.list_tasks()"
Task: "Write unit test for Task creation validation"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1 (Create and View)
4. **STOP and VALIDATE**: Can add tasks and view them
5. Deploy/demo if ready - this is a working todo app!

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add US1 → Test → **MVP!** (add/view)
3. Add US2 → Test → Can track completion
4. Add US3 → Test → Can edit tasks
5. Add US4 → Test → Can delete tasks
6. Add US5-US9 → Test → Full intermediate features
7. Polish → Production ready

### Recommended Execution Order (Solo Developer)

1. T001-T021 (Setup + Foundational)
2. T022-T031 (US1 - MVP)
3. T032-T040 (US2 - Complete)
4. T041-T045 (US3 - Update)
5. T046-T049 (US4 - Delete)
6. T050-T054 (US5 - Priority)
7. T055-T061 (US6 - Tags)
8. T062-T065 (US7 - Search)
9. T066-T073 (US8 - Filter)
10. T074-T078 (US9 - Sort)
11. T079-T083 (Polish)

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable
- TDD: Write tests first, verify they FAIL, then implement
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
