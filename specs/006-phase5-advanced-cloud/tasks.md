# Tasks: Phase 5 — Advanced Cloud Deployment

**Input**: Design documents from `specs/006-phase5-advanced-cloud/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/api-extensions.yaml, contracts/dapr-components.yaml, quickstart.md

**Organization**: Tasks grouped by user story. Agent tags indicate which specialized agent executes each task.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story (US1-US8)
- **Agent tags**: [Part-A-Features], [Part-A-Kafka], [Part-A-Dapr], [Part-B-Minikube], [Part-C-Cloud], [Part-C-CICD]

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Add shared dependencies and prepare project structure for Phase 5.

- [x] T001 Add `httpx` to backend/requirements.txt for Dapr HTTP client communication
- [x] T002 [P] Create `services/` directory at repo root with subdirectories: `notification-service/`, `recurring-task-service/`, `audit-service/`, `websocket-service/`
- [x] T003 [P] Create `dapr-components/` directory at repo root for Dapr component YAML files
- [x] T004 [P] Create `.github/workflows/` directory at repo root for CI/CD pipelines

**Checkpoint**: Project structure ready for feature implementation.

---

## Phase 2: Foundational (Task Model Extensions) [Part-A-Features]

**Purpose**: Extend the shared Task model with all new fields needed by US1, US2, and US3. MUST complete before any user story.

**CRITICAL**: No user story work can begin until this phase is complete.

- [x] T005 [Part-A-Features] Add `RecurrenceRule` string enum (daily, weekly, monthly, every_N_days) to backend/src/models/task.py
- [x] T006 [Part-A-Features] Add 4 nullable fields to Task model: `due_at` (Optional[datetime]), `remind_at` (Optional[datetime]), `recurrence_rule` (Optional[RecurrenceRule]), `recurrence_interval` (Optional[int]) in backend/src/models/task.py
- [x] T007 [Part-A-Features] Update `CreateTaskRequest` schema with `due_at`, `remind_at`, `recurrence_rule`, `recurrence_interval` optional fields in backend/src/schemas/task.py
- [x] T008 [Part-A-Features] Update `UpdateTaskRequest` schema with `due_at`, `remind_at`, `recurrence_rule`, `recurrence_interval` optional fields in backend/src/schemas/task.py
- [x] T009 [Part-A-Features] Add Pydantic model validators: remind_at <= due_at when both set, recurrence_interval >= 1 when rule is every_N_days, remind_at must be in future in backend/src/schemas/task.py
- [x] T010 [Part-A-Features] Update `task_to_dict()` to include new fields + computed `is_overdue` (due_at < now and not completed) in backend/src/api/tasks.py
- [x] T011 [Part-A-Features] Update database migration checker to expect new columns (due_at, remind_at, recurrence_rule, recurrence_interval) in backend/src/database.py
- [x] T012 [Part-A-Features] Update frontend TypeScript `Task` interface with `due_at`, `remind_at`, `recurrence_rule`, `recurrence_interval`, `is_overdue` fields in frontend/src/types/task.ts

**Checkpoint**: Task model extended — all new fields available across backend schemas, API serialization, and frontend types.

---

## Phase 3: User Story 2 — Due Dates & Reminders (Priority: P1) [Part-A-Features] MVP

**Goal**: Users can set due dates and reminders on tasks. Overdue tasks are visually flagged.

**Independent Test**: Create a task with `due_at = tomorrow`, verify it shows a due date. Create one with `due_at` in the past (via direct DB), verify `is_overdue = true`.

**Why US2 before US1**: Due dates are a prerequisite for recurring task scheduling (US1 needs `due_at` to compute next occurrence).

### Implementation for User Story 2

- [x] T013 [US2] [Part-A-Features] Update `TaskService.create_task()` to accept and persist `due_at` and `remind_at` in backend/src/services/task_service.py
- [x] T014 [US2] [Part-A-Features] Update `TaskService.update_task()` to accept and persist `due_at` and `remind_at` in backend/src/services/task_service.py
- [x] T015 [US2] [Part-A-Features] Update `create_task` API endpoint to pass `due_at` and `remind_at` from request to service in backend/src/api/tasks.py
- [x] T016 [US2] [Part-A-Features] Update `update_task` API endpoint to pass `due_at` and `remind_at` from request to service in backend/src/api/tasks.py
- [x] T017 [US2] [Part-A-Features] Update chatbot `create_task` tool to accept optional `due_at` and `remind_at` string parameters (ISO 8601) in backend/src/chatkit_server.py
- [x] T018 [US2] [Part-A-Features] Update chatbot `update_task` tool to accept optional `due_at` and `remind_at` parameters in backend/src/chatkit_server.py
- [x] T019 [US2] [Part-A-Features] Update chatbot `format_task()` to show due date and overdue indicator in backend/src/chatkit_server.py
- [x] T020 [P] [US2] [Part-A-Features] Add due date display and overdue visual indicator to task list items in frontend/src/components/ (task card or list row)
- [x] T021 [P] [US2] [Part-A-Features] Add date picker component for `due_at` and `remind_at` fields in task create/edit forms in frontend/src/components/
- [x] T022 [US2] [Part-A-Features] Update frontend API service to send `due_at` and `remind_at` in create/update requests in frontend/src/services/api.ts

**Checkpoint**: Users can set due dates and reminders. Overdue tasks visually flagged. Chatbot supports due dates.

---

## Phase 4: User Story 1 — Recurring Tasks (Priority: P1) [Part-A-Features]

**Goal**: Users create tasks with recurrence rules. Completing a recurring task spawns the next instance.

**Independent Test**: Create a task with `recurrence_rule = "daily"`, complete it, verify a new task appears with `due_at = tomorrow`.

**Depends on**: US2 (due dates must work first).

### Implementation for User Story 1

- [x] T023 [US1] [Part-A-Features] Update `TaskService.create_task()` to accept and persist `recurrence_rule` and `recurrence_interval` in backend/src/services/task_service.py
- [x] T024 [US1] [Part-A-Features] Add `calculate_next_due_date(current_due_at, rule, interval)` helper function in backend/src/services/task_service.py
- [x] T025 [US1] [Part-A-Features] Update `TaskService.toggle_complete()` to call recurrence spawning logic when task has recurrence_rule and is being marked complete in backend/src/services/task_service.py
- [x] T026 [US1] [Part-A-Features] Implement `TaskService.spawn_recurring_instance(task)` that creates a new task with same title/priority/tags/recurrence_rule and next due_at in backend/src/services/task_service.py
- [x] T027 [US1] [Part-A-Features] Update chatbot `create_task` tool to accept optional `recurrence_rule` and `recurrence_interval` parameters in backend/src/chatkit_server.py
- [x] T028 [P] [US1] [Part-A-Features] Add recurrence rule selector (dropdown: daily/weekly/monthly/custom) to task create/edit forms in frontend/src/components/
- [x] T029 [P] [US1] [Part-A-Features] Add recurrence indicator icon/badge to task list items in frontend/src/components/
- [x] T030 [US1] [Part-A-Features] Update frontend API service to send `recurrence_rule` and `recurrence_interval` in create/update requests in frontend/src/services/api.ts

**Checkpoint**: Recurring tasks work end-to-end. Completing spawns next instance. Chatbot and UI support recurrence.

---

## Phase 5: User Story 3 — Filter, Sort & Search Extensions (Priority: P2) [Part-A-Features]

**Goal**: Extend existing filter/sort/search with due-date range filtering and due-date sorting.

**Independent Test**: Create tasks with various due dates, filter by `due_before` and `overdue`, sort by `due_date`.

### Implementation for User Story 3

- [x] T031 [US3] [Part-A-Features] Add `due_before`, `due_after`, and `overdue` query parameters to `list_tasks` endpoint in backend/src/api/tasks.py
- [x] T032 [US3] [Part-A-Features] Add `sort_dir` query parameter (asc/desc) to `list_tasks` endpoint in backend/src/api/tasks.py
- [x] T033 [US3] [Part-A-Features] Implement due-date filtering logic in `TaskService.list_tasks()`: filter by due_before, due_after, overdue flag in backend/src/services/task_service.py
- [x] T034 [US3] [Part-A-Features] Add `due_date` and `created_at` sort options + `sort_dir` support to `TaskService.sort_tasks()` in backend/src/services/task_service.py
- [x] T035 [US3] [Part-A-Features] Update chatbot `list_tasks` tool to support `due_before`, `due_after`, and `overdue` filter params in backend/src/chatkit_server.py
- [x] T036 [P] [US3] [Part-A-Features] Add due-date filter controls (date range picker, overdue toggle) to task list UI in frontend/src/components/
- [x] T037 [P] [US3] [Part-A-Features] Add due-date sort option to sort dropdown in frontend task list in frontend/src/components/
- [x] T038 [US3] [Part-A-Features] Update frontend API service to send new query params (due_before, due_after, overdue, sort_dir) in frontend/src/services/api.ts

**Checkpoint**: Full filtering and sorting including due dates. All original filters (priority, tag, status, search) still work.

---

## Phase 6: User Story 4 — Event-Driven Architecture with Kafka (Priority: P2) [Part-A-Kafka]

**Goal**: All task mutations publish events. Four consumer microservices process events independently.

**Independent Test**: Create a task, check audit-service logs for `task.created` event. Complete a recurring task, check recurring-task-service creates a new instance.

### Event Publisher

- [x] T039 [US4] [Part-A-Kafka] Create `backend/src/services/event_publisher.py` with `EventPublisher` class that publishes TaskEvent JSON via HTTP POST to Dapr Pub/Sub endpoint
- [x] T040 [US4] [Part-A-Kafka] Define `TaskEvent` Pydantic model (event_id UUID, event_type, task_id, task_snapshot, actor, timestamp, metadata) in backend/src/schemas/task.py
- [x] T041 [US4] [Part-A-Kafka] Hook `EventPublisher.publish()` into `TaskService.create_task()` to publish `task.created` event in backend/src/services/task_service.py
- [x] T042 [US4] [Part-A-Kafka] Hook `EventPublisher.publish()` into `TaskService.update_task()` to publish `task.updated` event in backend/src/services/task_service.py
- [x] T043 [US4] [Part-A-Kafka] Hook `EventPublisher.publish()` into `TaskService.toggle_complete()` to publish `task.completed` event in backend/src/services/task_service.py
- [x] T044 [US4] [Part-A-Kafka] Hook `EventPublisher.publish()` into `TaskService.delete_task()` to publish `task.deleted` event in backend/src/services/task_service.py
- [x] T045 [US4] [Part-A-Kafka] Add Dapr Pub/Sub config settings (DAPR_HTTP_PORT, PUBSUB_NAME) to `Settings` class in backend/src/config.py

### Consumer Microservices

- [x] T046 [P] [US4] [Part-A-Kafka] Create `services/audit-service/main.py` — FastAPI app with `GET /dapr/subscribe` and `POST /api/events/task-events` that logs all events as structured JSON
- [x] T047 [P] [US4] [Part-A-Kafka] Create `services/audit-service/requirements.txt` (fastapi, uvicorn) and `services/audit-service/Dockerfile`
- [x] T048 [P] [US4] [Part-A-Kafka] Create `services/notification-service/main.py` — FastAPI app with `GET /dapr/subscribe` and `POST /api/events/reminders` that forwards notifications to websocket-service
- [x] T049 [P] [US4] [Part-A-Kafka] Create `services/notification-service/requirements.txt` and `services/notification-service/Dockerfile`
- [x] T050 [P] [US4] [Part-A-Kafka] Create `services/recurring-task-service/main.py` — FastAPI app with `GET /dapr/subscribe` and `POST /api/events/task-events` that spawns new task instances on `task.completed` events with recurrence_rule
- [x] T051 [P] [US4] [Part-A-Kafka] Create `services/recurring-task-service/requirements.txt` and `services/recurring-task-service/Dockerfile`
- [x] T052 [P] [US4] [Part-A-Kafka] Create `services/websocket-service/main.py` — FastAPI app with `GET /dapr/subscribe`, `POST /api/events/task-updates`, and `GET /ws` WebSocket endpoint that broadcasts to connected clients
- [x] T053 [P] [US4] [Part-A-Kafka] Create `services/websocket-service/requirements.txt` (fastapi, uvicorn, websockets) and `services/websocket-service/Dockerfile`

**Checkpoint**: Events published on all CRUD operations. All 4 consumers receive and process events. Audit-service logs every mutation.

---

## Phase 7: User Story 5 — Dapr Integration (Priority: P3) [Part-A-Dapr]

**Goal**: All infrastructure access goes through Dapr HTTP APIs. No direct Kafka client imports.

**Independent Test**: Publish event via Dapr Pub/Sub HTTP endpoint, verify consumer receives it. Schedule a Dapr Job, verify callback fires.

### Dapr Components

- [x] T054 [P] [US5] [Part-A-Dapr] Create `dapr-components/kafka-pubsub.yaml` — Dapr Pub/Sub component for Kafka (Redpanda) with brokers, consumer group, auth config
- [x] T055 [P] [US5] [Part-A-Dapr] Create `dapr-components/statestore.yaml` — Dapr State Store component for PostgreSQL with secretKeyRef for connection string
- [x] T056 [P] [US5] [Part-A-Dapr] Create `dapr-components/kubernetes-secrets.yaml` — Dapr Secrets Store component for Kubernetes Secrets

### Dapr Jobs for Reminders

- [x] T057 [US5] [Part-A-Dapr] Implement `schedule_reminder(task_id, remind_at)` function that creates a Dapr Job via `POST http://localhost:3500/v1.0-alpha1/jobs/reminder-task-{id}` in backend/src/services/event_publisher.py
- [x] T058 [US5] [Part-A-Dapr] Implement `cancel_reminder(task_id)` function that deletes a Dapr Job via `DELETE http://localhost:3500/v1.0-alpha1/jobs/reminder-task-{id}` in backend/src/services/event_publisher.py
- [x] T059 [US5] [Part-A-Dapr] Add `POST /api/jobs/trigger` callback endpoint in backend/src/main.py that receives Dapr Job callbacks and publishes `reminder.due` to reminders topic
- [x] T060 [US5] [Part-A-Dapr] Hook `schedule_reminder()` into task create/update when `remind_at` is set in backend/src/services/task_service.py
- [x] T061 [US5] [Part-A-Dapr] Hook `cancel_reminder()` into task delete and task complete (if already reminded) in backend/src/services/task_service.py

### Dapr Secrets

- [x] T062 [US5] [Part-A-Dapr] Add optional Dapr Secrets retrieval for DATABASE_URL and OPENAI_API_KEY in backend/src/config.py (fallback to env vars when Dapr not available)

### Dapr Verification

- [x] T063 [US5] [Part-A-Dapr] Verify no direct Kafka client library imports (kafka-python, aiokafka, confluent-kafka) exist in any application code — search all Python files
- [x] T064 [US5] [Part-A-Dapr] Add Dapr subscription endpoint `GET /dapr/subscribe` to backend/src/main.py returning subscription config for topics the backend publishes to

**Checkpoint**: All infrastructure abstracted behind Dapr. No Kafka imports. Reminders scheduled via Dapr Jobs. Secrets via Dapr Secrets API.

---

## Phase 8: User Story 6 — Local Minikube Deployment (Priority: P3) [Part-B-Minikube]

**Goal**: Full stack deploys to Minikube with Dapr sidecars, Redpanda, and all consumer services.

**Independent Test**: `helm install`, wait for all pods Running, create task via frontend, verify audit-service logs the event.

### Helm Chart Extensions

- [x] T065 [US6] [Part-B-Minikube] Add Redpanda StatefulSet template (single-node, ephemeral storage, port 9092) in k8s/charts/todo-app/templates/redpanda-statefulset.yaml
- [x] T066 [US6] [Part-B-Minikube] Add Redpanda Service template (ClusterIP, port 9092) in k8s/charts/todo-app/templates/redpanda-service.yaml
- [x] T067 [P] [US6] [Part-B-Minikube] Add notification-service Deployment template with Dapr annotations in k8s/charts/todo-app/templates/notification-service-deployment.yaml
- [x] T068 [P] [US6] [Part-B-Minikube] Add notification-service Service template in k8s/charts/todo-app/templates/notification-service-service.yaml
- [x] T069 [P] [US6] [Part-B-Minikube] Add recurring-task-service Deployment template with Dapr annotations in k8s/charts/todo-app/templates/recurring-task-service-deployment.yaml
- [x] T070 [P] [US6] [Part-B-Minikube] Add recurring-task-service Service template in k8s/charts/todo-app/templates/recurring-task-service-service.yaml
- [x] T071 [P] [US6] [Part-B-Minikube] Add audit-service Deployment template with Dapr annotations in k8s/charts/todo-app/templates/audit-service-deployment.yaml
- [x] T072 [P] [US6] [Part-B-Minikube] Add audit-service Service template in k8s/charts/todo-app/templates/audit-service-service.yaml
- [x] T073 [P] [US6] [Part-B-Minikube] Add websocket-service Deployment template with Dapr annotations in k8s/charts/todo-app/templates/websocket-service-deployment.yaml
- [x] T074 [P] [US6] [Part-B-Minikube] Add websocket-service Service template in k8s/charts/todo-app/templates/websocket-service-service.yaml
- [x] T075 [US6] [Part-B-Minikube] Add Dapr component templates (kafka-pubsub, statestore, kubernetes-secrets) in k8s/charts/todo-app/templates/dapr-components.yaml
- [x] T076 [US6] [Part-B-Minikube] Add Dapr annotations to existing backend Deployment template (dapr.io/enabled, dapr.io/app-id, dapr.io/app-port) in k8s/charts/todo-app/templates/backend-deployment.yaml
- [x] T077 [US6] [Part-B-Minikube] Add Dapr annotations to existing frontend Deployment template in k8s/charts/todo-app/templates/frontend-deployment.yaml
- [x] T078 [US6] [Part-B-Minikube] Update values.yaml with new services config: image repos/tags, replicas, ports, resource limits for notification-service, recurring-task-service, audit-service, websocket-service, and Redpanda in k8s/charts/todo-app/values.yaml
- [x] T079 [US6] [Part-B-Minikube] Bump Chart version in k8s/charts/todo-app/Chart.yaml

### Deployment Verification

- [x] T080 [US6] [Part-B-Minikube] Install Dapr on Minikube via `dapr init -k` and verify Dapr system pods are running - See minikube-deploy-guide.md
- [x] T081 [US6] [Part-B-Minikube] Build all Docker images (backend, frontend, 4 consumer services) in Minikube's Docker environment - See minikube-deploy-guide.md
- [x] T082 [US6] [Part-B-Minikube] Deploy full stack via `helm install todo-app ./k8s/charts/todo-app` with secrets and verify all pods (7+) reach Running status - See minikube-deploy-guide.md
- [x] T083 [US6] [Part-B-Minikube] Run smoke test: create task via frontend, verify event appears in audit-service pod logs - See minikube-deploy-guide.md

**Checkpoint**: Full stack running on Minikube. All pods healthy. Events flowing through Kafka/Dapr to all consumers.

---

## Phase 9: User Story 7 — Cloud Deployment (Priority: P4) [Part-C-Cloud]

**Goal**: Minikube-verified stack promoted to production cloud Kubernetes with TLS and ingress.

**Independent Test**: Access public HTTPS URL, create task, verify end-to-end flow.

### Cloud Cluster Setup

- [x] T084 [US7] [Part-C-Cloud] Provision Kubernetes cluster on OKE (or AKS/GKE) with at least 2 nodes
- [x] T085 [US7] [Part-C-Cloud] Configure kubectl context to connect to cloud cluster
- [x] T086 [US7] [Part-C-Cloud] Install Dapr on cloud cluster via `dapr init -k`

### Kafka/Redpanda Cloud

- [x] T087 [US7] [Part-C-Cloud] Set up Kafka broker: Redpanda Cloud Serverless (free tier), Strimzi operator, or other Dapr-compatible Pub/Sub — create topics: task-events, reminders, task-updates
- [x] T088 [US7] [Part-C-Cloud] Update Dapr kafka-pubsub component YAML with cloud broker credentials (SASL_SSL, bootstrap servers)

### Production Helm Values

- [x] T089 [US7] [Part-C-Cloud] Create k8s/charts/todo-app/values-production.yaml with: cloud image registry paths, production resource limits, cloud Kafka config, ingress enabled, TLS enabled
- [x] T090 [US7] [Part-C-Cloud] Add Ingress template with TLS and Let's Encrypt cert-manager annotations in k8s/charts/todo-app/templates/ingress.yaml
- [x] T091 [US7] [Part-C-Cloud] Install cert-manager on cloud cluster for automated TLS certificate provisioning
- [x] T092 [US7] [Part-C-Cloud] Install nginx-ingress controller on cloud cluster

### Cloud Deployment

- [x] T093 [US7] [Part-C-Cloud] Build and push all Docker images to GHCR (ghcr.io/dzuhaib/*)
- [x] T094 [US7] [Part-C-Cloud] Create Kubernetes Secrets for DATABASE_URL, OPENAI_API_KEY, and Kafka credentials on cloud cluster
- [x] T095 [US7] [Part-C-Cloud] Deploy full stack to cloud via `helm upgrade --install todo-app ./k8s/charts/todo-app -f values-production.yaml`
- [x] T096 [US7] [Part-C-Cloud] Verify all pods Running with Dapr sidecars injected on cloud cluster
- [x] T097 [US7] [Part-C-Cloud] Verify HTTPS access via public URL with valid TLS certificate

**Checkpoint**: Full stack live on cloud. TLS secured. All events flowing through cloud Kafka to consumers.

---

## Phase 10: User Story 8 — CI/CD Pipeline (Priority: P4) [Part-C-CICD]

**Goal**: Automated CI (lint + test) on every push and CD (build + deploy) on push to main.

**Independent Test**: Push a commit, verify GitHub Actions runs lint/test/build/deploy stages.

### CI Workflow

- [x] T098 [P] [US8] [Part-C-CICD] Create `.github/workflows/ci.yml` — trigger on push/PR, jobs: Python lint (ruff), TS lint (eslint), Python tests (pytest), TS tests (jest)
- [x] T099 [P] [US8] [Part-C-CICD] Create `.github/workflows/deploy.yml` — trigger on push to main, jobs: build Docker images, push to GHCR, Helm upgrade on cloud cluster, rollback on failure

### Pipeline Configuration

- [x] T100 [US8] [Part-C-CICD] Document all required GitHub Secrets (KUBE_CONFIG, GHCR_TOKEN, DATABASE_URL, OPENAI_API_KEY, KAFKA_CREDENTIALS) in a SECRETS.md or README section
- [x] T101 [US8] [Part-C-CICD] Add Helm rollback step in deploy workflow: if health check fails after deploy, run `helm rollback`
- [x] T102 [US8] [Part-C-CICD] Verify CI workflow runs successfully on a test push
- [x] T103 [US8] [Part-C-CICD] Verify deploy workflow builds images, pushes to GHCR, and deploys to cloud cluster

**Checkpoint**: Full CI/CD pipeline operational. Automated lint/test/build/deploy with rollback.

---

## Phase 11: Polish & Cross-Cutting Concerns

**Purpose**: Final cleanup, documentation, and validation.

- [x] T104 [P] Update README.md with Phase 5 documentation: architecture diagram, deployment instructions, environment variables
- [x] T105 [P] Update DEPLOYMENT.md with Minikube + Cloud deployment steps for Phase 5
- [x] T106 Verify all acceptance scenarios from spec.md pass end-to-end
- [x] T107 Run quickstart.md validation: follow all steps, verify each works
- [x] T108 Verify no hardcoded secrets in any file (grep for API keys, passwords, connection strings)

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1: Setup ──────────────────────────────────────────► (no dependencies)
Phase 2: Foundational (Task Model) ──────────────────────► depends on Phase 1
Phase 3: US2 Due Dates (P1) ─────────────────────────────► depends on Phase 2
Phase 4: US1 Recurring Tasks (P1) ───────────────────────► depends on Phase 3 (needs due_at)
Phase 5: US3 Filter/Sort (P2) ──────────────────────────► depends on Phase 2 (can parallel with US1)
Phase 6: US4 Kafka Events (P2) ─────────────────────────► depends on Phase 4 (needs recurrence in events)
Phase 7: US5 Dapr Integration (P3) ──────────────────────► depends on Phase 6 (replaces Kafka clients)
Phase 8: US6 Minikube Deploy (P3) ──────────────────────► depends on Phase 7 (needs Dapr components)
Phase 9: US7 Cloud Deploy (P4) ─────────────────────────► depends on Phase 8 (Minikube validated first)
Phase 10: US8 CI/CD (P4) ───────────────────────────────► depends on Phase 9 (needs cloud cluster)
Phase 11: Polish ────────────────────────────────────────► depends on all above
```

### User Story Dependencies

| Story | Depends On | Can Parallel With |
|-------|-----------|-------------------|
| US2 Due Dates (P1) | Foundational only | — |
| US1 Recurring (P1) | US2 (needs due_at) | US3 |
| US3 Filter/Sort (P2) | Foundational only | US1, US4 |
| US4 Kafka (P2) | US1 + US2 (full feature set) | US3 (partially) |
| US5 Dapr (P3) | US4 (replaces Kafka clients) | — |
| US6 Minikube (P3) | US5 (needs Dapr components) | — |
| US7 Cloud (P4) | US6 (local validation first) | — |
| US8 CI/CD (P4) | US7 (needs cloud cluster) | — |

### Within Each User Story

- Models/schemas before services
- Services before API endpoints
- Backend before frontend
- Core logic before integration

### Parallel Opportunities

- **Phase 1**: All T001-T004 are independent, run in parallel
- **Phase 2**: T005-T006 sequential (enum then fields), T007-T012 parallelizable after T006
- **Phase 3 (US2)**: T020-T021 (frontend) parallel with T013-T019 (backend)
- **Phase 4 (US1)**: T028-T029 (frontend) parallel with T023-T027 (backend)
- **Phase 5 (US3)**: T036-T037 (frontend) parallel with T031-T035 (backend)
- **Phase 6 (US4)**: All consumer services (T046-T053) parallel with each other
- **Phase 7 (US5)**: Dapr component YAMLs (T054-T056) parallel
- **Phase 8 (US6)**: All consumer Helm templates (T067-T074) parallel
- **Phase 9 (US7)**: T090-T092 (TLS/ingress setup) after T084 (cluster provision)
- **Phase 10 (US8)**: CI and deploy workflows (T098-T099) parallel

---

## Parallel Example: Phase 6 (Kafka Consumers)

```bash
# All consumer services can be built simultaneously (different directories):
Task T046: "Create audit-service/main.py"
Task T048: "Create notification-service/main.py"
Task T050: "Create recurring-task-service/main.py"
Task T052: "Create websocket-service/main.py"

# Their Dockerfiles can also be created in parallel:
Task T047: "Create audit-service/Dockerfile"
Task T049: "Create notification-service/Dockerfile"
Task T051: "Create recurring-task-service/Dockerfile"
Task T053: "Create websocket-service/Dockerfile"
```

---

## Implementation Strategy

### MVP First (Phases 1-4: Due Dates + Recurring Tasks)

1. Complete Phase 1: Setup (T001-T004)
2. Complete Phase 2: Foundational model extensions (T005-T012)
3. Complete Phase 3: US2 Due Dates & Reminders (T013-T022)
4. Complete Phase 4: US1 Recurring Tasks (T023-T030)
5. **STOP and VALIDATE**: Both P1 stories work independently
6. Deploy/demo — this is the MVP

### Incremental Delivery

1. MVP (above) → Due dates + Recurring tasks working
2. Add Phase 5: US3 Filter/Sort → Enhanced querying
3. Add Phase 6: US4 Kafka → Event-driven architecture
4. Add Phase 7: US5 Dapr → Infrastructure abstraction
5. Add Phase 8: US6 Minikube → Local K8s deployment
6. Add Phase 9: US7 Cloud → Production deployment
7. Add Phase 10: US8 CI/CD → Automation
8. Phase 11: Polish → Final documentation

### Agent Execution Strategy

Each agent handles its tagged tasks:

| Agent | Tags | Phases | Task Count |
|-------|------|--------|------------|
| **feature-implementer** | [Part-A-Features] | 2, 3, 4, 5 | 34 tasks |
| **kafka-architect** | [Part-A-Kafka] | 6 | 15 tasks |
| **dapr-integrator** | [Part-A-Dapr] | 7 | 11 tasks |
| **minikube-deployer** | [Part-B-Minikube] | 8 | 19 tasks |
| **cloud-deployer** | [Part-C-Cloud] | 9 | 14 tasks |
| **cicd-engineer** | [Part-C-CICD] | 10 | 6 tasks |

---

## Summary

| Metric | Value |
|--------|-------|
| **Total tasks** | 108 |
| **Setup tasks** | 4 |
| **Foundational tasks** | 8 |
| **US1 Recurring Tasks** | 8 |
| **US2 Due Dates** | 10 |
| **US3 Filter/Sort** | 8 |
| **US4 Kafka Events** | 15 |
| **US5 Dapr** | 11 |
| **US6 Minikube** | 19 |
| **US7 Cloud** | 14 |
| **US8 CI/CD** | 6 |
| **Polish** | 5 |
| **Parallel opportunities** | 40+ tasks marked [P] |
| **MVP scope** | Phases 1-4 (30 tasks) |

---

## Notes

- [P] tasks = different files, no dependencies on incomplete tasks
- [Story] label maps task to specific user story
- Agent tags map tasks to specialized agents
- Commit after each phase or logical group
- Stop at any checkpoint to validate independently
- The recurring-task-service (US4) eventually replaces the synchronous spawning in US1 — US1 implements sync first, US4 makes it async via events
