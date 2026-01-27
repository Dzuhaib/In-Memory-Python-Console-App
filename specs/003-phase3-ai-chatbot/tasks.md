# Tasks: Phase 3 AI-Powered Todo Chatbot

**Input**: Design documents from `/specs/003-phase3-ai-chatbot/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/chat-api.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Frontend**: `frontend/src/`
- **Backend**: `backend/src/` (existing, minimal changes)
- Paths based on plan.md structure

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Install dependencies and create base structure for chat feature

- [x] T001 Install Vercel AI SDK and OpenAI packages in frontend/package.json
- [x] T002 [P] Add OPENAI_API_KEY to frontend/.env.local and frontend/.env.example
- [x] T003 [P] Create chat types in frontend/src/types/chat.ts
- [x] T004 [P] Create chat directory structure frontend/src/app/chat/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core chat infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Create Next.js API route for OpenAI in frontend/src/app/api/chat/route.ts
- [x] T006 Define tool schemas (all 8 functions) in frontend/src/app/api/chat/tools.ts
- [x] T007 Implement tool executor that calls existing api.ts in frontend/src/app/api/chat/executor.ts
- [x] T008 [P] Create ChatMessage component in frontend/src/components/ChatMessage.tsx
- [x] T009 [P] Create ChatInput component in frontend/src/components/ChatInput.tsx
- [x] T010 Create ChatWindow component in frontend/src/components/ChatWindow.tsx
- [x] T011 Create chat page in frontend/src/app/chat/page.tsx
- [x] T012 Add navigation link to chat page in frontend/src/app/layout.tsx

**Checkpoint**: Basic chat UI renders, API route responds (without tools working)

---

## Phase 3: User Story 1 - Add Tasks via Natural Language (Priority: P1) 🎯 MVP

**Goal**: Users can create new tasks by typing natural language commands like "Add a task to buy groceries"

**Independent Test**: Type "Add a high priority task to buy groceries" → See confirmation with task details

### Implementation for User Story 1

- [x] T013 [US1] Implement createTask tool execution in frontend/src/app/api/chat/executor.ts
- [x] T014 [US1] Add system prompt for task creation guidance in frontend/src/app/api/chat/route.ts
- [x] T015 [US1] Handle createTask tool response formatting (confirmation message)
- [ ] T016 [US1] Test: Add task with title only ("Add task buy milk")
- [ ] T017 [US1] Test: Add task with priority ("Add high priority task to call mom")
- [ ] T018 [US1] Test: Add task with tags ("Add task meeting, tags work, urgent")

**Checkpoint**: User Story 1 complete - can add tasks via chat

---

## Phase 4: User Story 2 - View Tasks via Natural Language (Priority: P2)

**Goal**: Users can see their task list by asking in natural language

**Independent Test**: Type "Show me my tasks" → See formatted list of all tasks

### Implementation for User Story 2

- [x] T019 [US2] Implement getTasks tool execution in frontend/src/app/api/chat/executor.ts
- [x] T020 [US2] Implement getTask tool execution in frontend/src/app/api/chat/executor.ts
- [x] T021 [US2] Format task list response with emojis (✓/○, priority colors) in tool response
- [x] T022 [US2] Handle empty task list case ("You don't have any tasks yet")
- [ ] T023 [US2] Test: Show all tasks
- [ ] T024 [US2] Test: Show filtered tasks ("Show high priority tasks", "Show incomplete tasks")

**Checkpoint**: User Stories 1 AND 2 complete - can add and view tasks

---

## Phase 5: User Story 3 - Mark Tasks Complete (Priority: P3)

**Goal**: Users can mark tasks complete/incomplete via natural language

**Independent Test**: Type "Mark task 1 as done" → See confirmation of status change

### Implementation for User Story 3

- [x] T025 [US3] Implement toggleComplete tool execution in frontend/src/app/api/chat/executor.ts
- [x] T026 [US3] Handle task not found error gracefully
- [ ] T027 [US3] Test: Mark task complete by ID ("Mark task 1 as done")
- [ ] T028 [US3] Test: Mark task incomplete ("Unmark task 1")

**Checkpoint**: User Stories 1-3 complete - can add, view, and complete tasks

---

## Phase 6: User Story 4 - Delete Tasks (Priority: P4)

**Goal**: Users can delete tasks via natural language

**Independent Test**: Type "Delete task 2" → See confirmation task was removed

### Implementation for User Story 4

- [x] T029 [US4] Implement deleteTask tool execution in frontend/src/app/api/chat/executor.ts
- [x] T030 [US4] Handle task not found error gracefully
- [ ] T031 [US4] Test: Delete task by ID ("Delete task 2")
- [ ] T032 [US4] Test: Delete non-existent task (error handling)

**Checkpoint**: User Stories 1-4 complete - full CRUD minus update

---

## Phase 7: User Story 5 - Update Tasks (Priority: P5)

**Goal**: Users can modify task title, priority, and tags via natural language

**Independent Test**: Type "Change task 1 priority to high" → See confirmation

### Implementation for User Story 5

- [x] T033 [US5] Implement updateTask tool execution in frontend/src/app/api/chat/executor.ts
- [x] T034 [US5] Implement addTag tool execution in frontend/src/app/api/chat/executor.ts
- [x] T035 [US5] Implement removeTag tool execution in frontend/src/app/api/chat/executor.ts
- [ ] T036 [US5] Test: Update priority ("Change task 1 priority to high")
- [ ] T037 [US5] Test: Update title ("Rename task 1 to 'Buy organic groceries'")
- [ ] T038 [US5] Test: Add/remove tags ("Add tag urgent to task 1")

**Checkpoint**: User Stories 1-5 complete - full CRUD with updates

---

## Phase 8: User Story 6 - Search and Filter (Priority: P6)

**Goal**: Users can find specific tasks using natural language queries

**Independent Test**: Type "Find tasks about groceries" → See matching tasks

### Implementation for User Story 6

- [ ] T039 [US6] Enhance getTasks tool to support search parameter
- [ ] T040 [US6] Test: Search by keyword ("Find tasks about groceries")
- [ ] T041 [US6] Test: Filter by tag ("Show tasks tagged work")
- [ ] T042 [US6] Test: Combined filters ("Show incomplete high priority tasks")

**Checkpoint**: User Stories 1-6 complete - all task operations via chat

---

## Phase 9: User Story 7 - Help and Guidance (Priority: P7)

**Goal**: Users can ask for help and receive guidance

**Independent Test**: Type "Help" → See list of available commands

### Implementation for User Story 7

- [ ] T043 [US7] Add help handling in system prompt
- [ ] T044 [US7] Add graceful unknown command handling
- [ ] T045 [US7] Test: Help command shows examples
- [ ] T046 [US7] Test: Unknown command gives helpful suggestions

**Checkpoint**: All user stories complete

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T047 [P] Add loading state animation to ChatMessage component
- [ ] T048 [P] Add error boundary for chat page
- [ ] T049 [P] Style chat interface with Tailwind (match Phase 2 design)
- [ ] T050 [P] Add mobile responsive styles to chat components
- [ ] T051 Verify all quickstart.md scenarios work end-to-end
- [ ] T052 Update frontend README with chat feature documentation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-9)**: All depend on Foundational phase completion
  - Can proceed sequentially in priority order (P1 → P2 → ... → P7)
- **Polish (Phase 10)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational - No dependencies on other stories (MVP)
- **User Story 2 (P2)**: Can start after Foundational - Independent of US1
- **User Story 3 (P3)**: Can start after Foundational - Independent
- **User Story 4 (P4)**: Can start after Foundational - Independent
- **User Story 5 (P5)**: Can start after Foundational - Independent
- **User Story 6 (P6)**: Builds on US2 (getTasks) but independently testable
- **User Story 7 (P7)**: Can start after Foundational - Independent

### Within Each User Story

- Tool implementation before testing
- Core implementation before edge cases
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (T008, T009)
- Multiple user stories could be parallelized if team capacity allows
- All Polish tasks marked [P] can run in parallel

---

## Parallel Example: Foundational Phase

```bash
# These can run in parallel:
Task: "Create ChatMessage component in frontend/src/components/ChatMessage.tsx"
Task: "Create ChatInput component in frontend/src/components/ChatInput.tsx"

# This depends on both above:
Task: "Create ChatWindow component in frontend/src/components/ChatWindow.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (4 tasks)
2. Complete Phase 2: Foundational (8 tasks)
3. Complete Phase 3: User Story 1 (6 tasks)
4. **STOP and VALIDATE**: Test adding tasks via chat
5. Deploy/demo if ready - Users can add tasks via chat!

### Incremental Delivery

1. Setup + Foundational → Chat UI renders (12 tasks)
2. Add User Story 1 → Can add tasks (6 tasks) → Deploy (MVP!)
3. Add User Story 2 → Can view tasks (6 tasks) → Deploy
4. Add User Story 3 → Can complete tasks (4 tasks) → Deploy
5. Continue through remaining stories...

### Single Developer Strategy

Execute phases sequentially in order:
1. Phase 1-2: Get chat infrastructure working
2. Phase 3: MVP - add tasks
3. Phase 4-9: Add remaining features in priority order
4. Phase 10: Polish

---

## Summary

| Phase | Tasks | Description |
|-------|-------|-------------|
| Setup | 4 | Dependencies, types, structure |
| Foundational | 8 | API route, components, tools |
| US1 (P1) | 6 | Add tasks via chat (MVP) |
| US2 (P2) | 6 | View tasks via chat |
| US3 (P3) | 4 | Complete tasks via chat |
| US4 (P4) | 4 | Delete tasks via chat |
| US5 (P5) | 6 | Update tasks via chat |
| US6 (P6) | 4 | Search/filter via chat |
| US7 (P7) | 4 | Help and guidance |
| Polish | 6 | Styling, errors, docs |
| **Total** | **52** | |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- All tool implementations call existing frontend/src/services/api.ts functions
