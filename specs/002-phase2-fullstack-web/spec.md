# Feature Specification: Phase 2 Full Stack Web Application

**Feature Branch**: `002-phase2-fullstack-web`
**Created**: 2026-01-25
**Status**: Draft
**Input**: User description: "Phase 2 Full Stack Web Application - Todo app with Next.js frontend, FastAPI backend, SQLModel ORM, and Neon DB for persistent storage. Migrate Phase 1 console features (CRUD, priorities, tags, search, filter, sort) to web interface with REST API."

## Overview

This phase migrates the Phase 1 in-memory console application to a full-stack web application with persistent storage. All existing features (CRUD operations, priorities, tags, search, filter, sort) will be accessible through a modern web interface backed by a REST API.

## User Scenarios & Testing

### User Story 1 - View and Add Tasks via Web UI (Priority: P1) MVP

Users can access a web interface to view their task list and add new tasks with titles, priorities, and tags.

**Why this priority**: Core functionality - without viewing and adding tasks, no other features are usable. This is the minimum viable web application.

**Independent Test**: User opens the web app in a browser, sees an empty task list (or existing tasks if any), clicks "Add Task", enters a title with optional priority/tags, submits, and sees the new task appear in the list. Data persists after page refresh.

**Acceptance Scenarios**:

1. **Given** a user opens the web app, **When** no tasks exist, **Then** the UI displays "No tasks found" message
2. **Given** a user is on the task list page, **When** they click "Add Task" and enter "Buy groceries" with priority "high", **Then** the task appears in the list with the correct priority badge
3. **Given** a user adds a task, **When** they refresh the page, **Then** the task is still visible (persisted in database)
4. **Given** a user adds a task with tags "work,urgent", **When** the task list loads, **Then** the tags are displayed with the task

---

### User Story 2 - Mark Tasks Complete/Incomplete (Priority: P2)

Users can toggle the completion status of tasks directly from the web interface.

**Why this priority**: Task completion is the primary purpose of a todo app - users need to track what they've done.

**Independent Test**: User clicks a checkbox or button next to a task to mark it complete, sees visual indication (strikethrough/checkmark), clicks again to uncomplete.

**Acceptance Scenarios**:

1. **Given** an incomplete task exists, **When** the user clicks the complete toggle, **Then** the task shows as completed with visual indicator
2. **Given** a completed task exists, **When** the user clicks the complete toggle, **Then** the task shows as incomplete
3. **Given** a user marks a task complete, **When** they refresh the page, **Then** the completion status persists

---

### User Story 3 - Update Task Details (Priority: P3)

Users can edit task titles and priorities through the web interface.

**Why this priority**: Users frequently need to correct typos or change priorities as circumstances change.

**Independent Test**: User clicks edit on a task, modifies the title or priority, saves changes, and sees updated information in the list.

**Acceptance Scenarios**:

1. **Given** a task exists, **When** the user clicks edit, changes the title to "Buy organic groceries", and saves, **Then** the updated title displays in the list
2. **Given** a task with medium priority, **When** the user changes priority to high, **Then** the priority badge updates accordingly
3. **Given** a user edits a task, **When** they try to save an empty title, **Then** an error message displays and the change is rejected

---

### User Story 4 - Delete Tasks (Priority: P4)

Users can remove tasks from the list permanently.

**Why this priority**: Users need to clean up completed or irrelevant tasks.

**Independent Test**: User clicks delete on a task, confirms deletion, and the task disappears from the list.

**Acceptance Scenarios**:

1. **Given** a task exists, **When** the user clicks delete and confirms, **Then** the task is removed from the list
2. **Given** a user deletes a task, **When** they refresh the page, **Then** the task remains deleted (not in database)

---

### User Story 5 - Manage Task Tags (Priority: P5)

Users can add and remove tags from existing tasks through the web interface.

**Why this priority**: Tags enable categorization which helps organize larger task lists.

**Independent Test**: User opens a task, adds a new tag, sees it appear, removes an existing tag, sees it disappear.

**Acceptance Scenarios**:

1. **Given** a task without tags, **When** the user adds tag "work", **Then** the tag appears on the task
2. **Given** a task with tag "work", **When** the user removes the tag, **Then** the tag is no longer displayed
3. **Given** a user adds a tag, **When** they refresh the page, **Then** the tag persists

---

### User Story 6 - Search Tasks (Priority: P6)

Users can search for tasks by keyword, with case-insensitive matching.

**Why this priority**: Search helps users quickly find specific tasks in longer lists.

**Independent Test**: User types a search term, list filters to show only matching tasks, clearing search shows all tasks.

**Acceptance Scenarios**:

1. **Given** tasks "Buy groceries" and "Call mom" exist, **When** the user searches "groceries", **Then** only "Buy groceries" is displayed
2. **Given** a task "Buy GROCERIES", **When** the user searches "groceries" (lowercase), **Then** the task is found (case-insensitive)
3. **Given** a search is active, **When** the user clears the search, **Then** all tasks are displayed

---

### User Story 7 - Filter Tasks (Priority: P7)

Users can filter tasks by status (complete/incomplete), priority level, or tag.

**Why this priority**: Filtering helps users focus on relevant subsets of their task list.

**Independent Test**: User selects filter criteria (e.g., "show only incomplete high priority tasks"), list updates to show matching tasks only.

**Acceptance Scenarios**:

1. **Given** complete and incomplete tasks exist, **When** the user filters by "incomplete", **Then** only incomplete tasks are shown
2. **Given** tasks with different priorities exist, **When** the user filters by "high" priority, **Then** only high priority tasks are shown
3. **Given** tasks with various tags, **When** the user filters by tag "work", **Then** only tasks with that tag are shown
4. **Given** multiple filters are applied, **When** filtering by "incomplete" AND "high priority", **Then** only tasks matching both criteria are shown (AND logic)

---

### User Story 8 - Sort Tasks (Priority: P8)

Users can sort tasks by priority, alphabetically by title, or by creation order.

**Why this priority**: Sorting helps users view tasks in their preferred order for better planning.

**Independent Test**: User selects sort option, list reorders according to selection.

**Acceptance Scenarios**:

1. **Given** tasks with different priorities, **When** sorting by priority, **Then** high priority tasks appear first, then medium, then low
2. **Given** tasks "Zebra task" and "Apple task", **When** sorting alphabetically, **Then** "Apple task" appears before "Zebra task"
3. **Given** sort by ID selected, **When** viewing the list, **Then** tasks appear in creation order

---

### User Story 9 - API Health and Documentation (Priority: P9)

Developers can access API documentation and verify the backend is running.

**Why this priority**: Essential for development, debugging, and API consumers.

**Independent Test**: Developer navigates to API docs endpoint, sees interactive documentation; health endpoint returns OK status.

**Acceptance Scenarios**:

1. **Given** the backend is running, **When** accessing /docs endpoint, **Then** interactive API documentation (Swagger/OpenAPI) is displayed
2. **Given** the backend is running, **When** accessing /health endpoint, **Then** a 200 OK response with status "healthy" is returned

---

### Edge Cases

- What happens when database connection fails? Display user-friendly error message, not technical details
- What happens when user submits empty task title? Validation error prevents submission
- What happens when user tries to delete a non-existent task? 404 error handled gracefully
- What happens when search/filter returns no results? Display "No tasks match your criteria" message
- What happens with very long task titles? Truncate display with ellipsis, show full on hover/click
- What happens with special characters in titles/tags? Properly escaped and stored
- What happens when user loses internet connection? Show offline indicator, queue operations if possible

## Requirements

### Functional Requirements

**Task Management (Core)**
- **FR-001**: System MUST allow users to create tasks with title (required), priority (optional, default: medium), and tags (optional)
- **FR-002**: System MUST allow users to view all tasks in a list format
- **FR-003**: System MUST allow users to mark tasks as complete or incomplete
- **FR-004**: System MUST allow users to update task title and priority
- **FR-005**: System MUST allow users to delete tasks permanently
- **FR-006**: System MUST validate that task titles are non-empty

**Tags**
- **FR-007**: System MUST allow users to add tags to existing tasks
- **FR-008**: System MUST allow users to remove tags from tasks
- **FR-009**: System MUST display tags visually with each task

**Search and Filter**
- **FR-010**: System MUST support case-insensitive keyword search across task titles
- **FR-011**: System MUST support filtering by completion status (complete/incomplete)
- **FR-012**: System MUST support filtering by priority level (high/medium/low)
- **FR-013**: System MUST support filtering by tag
- **FR-014**: System MUST apply multiple filters with AND logic

**Sort**
- **FR-015**: System MUST support sorting by priority (high first)
- **FR-016**: System MUST support sorting alphabetically by title
- **FR-017**: System MUST support sorting by task ID (creation order)

**Persistence**
- **FR-018**: System MUST persist all task data to a PostgreSQL database
- **FR-019**: System MUST maintain data integrity across browser sessions

**API**
- **FR-020**: System MUST provide REST API endpoints for all task operations
- **FR-021**: System MUST provide interactive API documentation
- **FR-022**: System MUST provide a health check endpoint

**UI**
- **FR-023**: System MUST provide a responsive web interface
- **FR-024**: System MUST display appropriate loading states during operations
- **FR-025**: System MUST display user-friendly error messages

### Key Entities

- **Task**: Core entity representing a todo item
  - ID (unique identifier)
  - Title (text, required)
  - Completed (boolean, default: false)
  - Priority (enum: high/medium/low, default: medium)
  - Tags (list of strings)
  - Created timestamp
  - Updated timestamp

## Success Criteria

### Measurable Outcomes

- **SC-001**: Users can complete the full CRUD cycle (create, read, update, delete) for a task in under 30 seconds
- **SC-002**: Page load time is under 2 seconds on standard broadband connection
- **SC-003**: All Phase 1 features (9 user stories) are accessible via web interface
- **SC-004**: Data persists correctly across browser sessions and page refreshes
- **SC-005**: API responds to requests in under 500ms for typical operations
- **SC-006**: System handles concurrent users without data corruption
- **SC-007**: All form inputs have appropriate validation with clear error messages
- **SC-008**: Application is usable on both desktop and mobile browsers

## Assumptions

- Users have modern web browsers (Chrome, Firefox, Safari, Edge - latest 2 versions)
- Users have internet connectivity to access the web application
- Single-user application (no authentication required for Phase 2)
- Neon DB free tier is sufficient for development and initial deployment
- Next.js App Router will be used for the frontend
- FastAPI will handle all backend logic and database operations

## Out of Scope

- User authentication and multi-user support (Phase 3+)
- Real-time collaboration features
- Mobile native applications
- Offline-first functionality
- Task due dates and reminders
- Task subtasks or hierarchies
- File attachments
- Email notifications
