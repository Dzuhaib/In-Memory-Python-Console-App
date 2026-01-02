# Tasks: In-Memory Todo List Application

**Input**: Design documents from `specs/002-in-memory-todo-app/`
**Prerequisites**: plan.md, spec.md, data-model.md

**Tests**: Test tasks are included as per the project constitution (TDD).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel
- **[Story]**: Which user story this task belongs to

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root

---

## Phase 1: Setup

**Purpose**: Project initialization and basic structure.

- [ ] T001 [P] Create directory structure `src/todo_app/` and `tests/unit/`.
- [ ] T002 [P] Create empty files: `src/todo_app/__init__.py`, `src/todo_app/models.py`, `src/todo_app/service.py`, `src/todo_app/main.py`, `tests/unit/test_models.py`, `tests/unit/test_service.py`.

---

## Phase 2: Foundational (Task Model)

**Purpose**: Core data structure that all user stories depend on.

### Tests for Task Model

- [ ] T003 [P] In `tests/unit/test_models.py`, write a test to ensure a `Task` object can be created with an `id`, `description`, and defaults `completed` to `False`.

### Implementation for Task Model

- [ ] T004 In `src/todo_app/models.py`, implement the `Task` dataclass as defined in `data-model.md`. Ensure the test from T003 passes.

---

## Phase 3: User Story 1 - Add a Task (Priority: P1) 🎯 MVP

**Goal**: Allow a user to add a new task.
**Independent Test**: A user can add a task and it appears in the list.

### Tests for User Story 1

- [ ] T005 In `tests/unit/test_service.py`, write a test for a `TodoService` class that checks if `add_task("Buy milk")` correctly adds a new `Task` to its internal list. The list should have 1 item.
- [ ] T006 [P] In `tests/unit/test_service.py`, write another test to add a second task and verify the list contains 2 items.

### Implementation for User Story 1

- [ ] T007 In `src/todo_app/service.py`, create a `TodoService` class with an `__init__` method that initializes an empty list `self.tasks` and a `self.next_id`.
- [ ] T008 In `src/todo_app/service.py`, implement the `add_task(self, description)` method. It should create a new `Task` object with the next available ID and the given description, and add it to `self.tasks`. Ensure tests from T005 and T006 pass.

---

## Phase 4: User Story 2 - View All Tasks (Priority: P2)

**Goal**: Allow a user to see all current tasks.
**Independent Test**: After adding tasks, a user can view them all.

### Tests for User Story 2

- [ ] T009 In `tests/unit/test_service.py`, write a test for `view_tasks()` that adds a few tasks and verifies the method returns the complete list of tasks.
- [ ] T010 [P] In `tests/unit/test_service.py`, write a test for `view_tasks()` when the list is empty, ensuring it returns an empty list.

### Implementation for User Story 2

- [ ] T011 In `src/todo_app/service.py`, implement the `view_tasks(self)` method to return the `self.tasks` list. Ensure tests from T009 and T010 pass.

---

## Phase 5: User Story 3 - Mark a Task as Completed (Priority: P3)

**Goal**: Allow a user to mark a task as completed.
**Independent Test**: A user can mark a task as complete and its status is updated.

### Tests for User Story 3

- [ ] T012 In `tests/unit/test_service.py`, write a test for `complete_task(task_id)` that adds a task, calls `complete_task` with its ID, and verifies the task's `completed` status is now `True`.
- [ ] T013 [P] In `tests/unit/test_service.py`, write a test for `complete_task(task_id)` with a non-existent ID and verify it returns `False` or raises an error.

### Implementation for User Story 3

- [ ] T014 In `src/todo_app/service.py`, implement the `complete_task(self, task_id)` method. It should find the task with the given ID and set its `completed` status to `True`. It should handle cases where the ID doesn't exist. Ensure tests from T012 and T013 pass.

---

## Phase 6: User Story 4 - Clear Completed Tasks (Priority: P4)

**Goal**: Allow a user to remove all completed tasks.
**Independent Test**: Completed tasks are removed while uncompleted ones remain.

### Tests for User Story 4

- [ ] T015 In `tests/unit/test_service.py`, write a test that adds several tasks, completes some, calls `clear_completed_tasks()`, and verifies that only the uncompleted tasks remain.
- [ ] T016 [P] In `tests/unit/test_service.py`, write a test that calls `clear_completed_tasks()` when no tasks are complete and verifies the list is unchanged.

### Implementation for User Story 4

- [ ] T017 In `src/todo_app/service.py`, implement the `clear_completed_tasks(self)` method. It should remove all tasks from `self.tasks` where `completed` is `True`. Ensure tests from T015 and T016 pass.

---

## Phase 7: Polish & Console Integration

**Purpose**: Build the user-facing console interface and tie all service methods together.

- [ ] T018 In `src/todo_app/main.py`, create a `print_menu()` function that displays the main options to the user.
- [ ] T019 In `src/todo_app/main.py`, implement the main application loop (`while True:`).
- [ ] T020 [P] [US1] In `main.py`, integrate the `add_task` service method with the corresponding user menu choice.
- [ ] T021 [P] [US2] In `main.py`, integrate the `view_tasks` service method, including formatting the output for display.
- [ ] T022 [P] [US3] In `main.py`, integrate the `complete_task` service method.
- [ ] T023 [P] [US4] In `main.py`, integrate the `clear_completed_tasks` service method.
- [ ] T024 [P] In `main.py`, implement robust user input handling and error messages for invalid choices.
- [ ] T025 [P] In `main.py`, add a clear "exit" option to break the main loop.

## Dependencies & Execution Order

- **Phase 1 (Setup)** must be completed first.
- **Phase 2 (Foundational)** depends on Phase 1.
- **Phases 3-6 (User Stories)** depend on Phase 2. They can be implemented in any order after Phase 2 is done, but following the priority (P1-P4) is recommended.
- **Phase 7 (Polish)** depends on all previous phases being complete. It integrates all the service-level functionality into the final user-facing application.

## Implementation Strategy

### MVP First (User Story 1 Only)

1.  Complete Phase 1 & 2.
2.  Complete Phase 3 (Add a Task).
3.  Implement a minimal version of Phase 7 that only supports adding and viewing tasks to validate the MVP.
4.  This gives a testable, valuable slice of functionality.

### Incremental Delivery

1.  Complete Setup + Foundational.
2.  Add User Story 1 (Add) -> Test -> MVP is ready.
3.  Add User Story 2 (View) -> Test.
4.  Add User Story 3 (Complete) -> Test.
5.  Add User Story 4 (Clear) -> Test.
6.  Complete final integration in Phase 7.
