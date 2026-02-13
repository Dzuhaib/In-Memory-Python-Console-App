# Implementation Plan: Phase 5 — Advanced Cloud Deployment

**Branch**: `006-phase5-advanced-cloud` | **Date**: 2026-02-12 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/006-phase5-advanced-cloud/spec.md`

---

## Summary

Extend the existing todo application with advanced features (recurring tasks, due dates, reminders), event-driven architecture (Kafka via Redpanda, 4 consumer microservices), Dapr integration (Pub/Sub, Jobs, Secrets, Service Invocation), Minikube local deployment, cloud Kubernetes deployment (OKE/AKS/GKE), and CI/CD pipeline (GitHub Actions). All infrastructure is abstracted behind Dapr HTTP APIs so the application code remains vendor-agnostic.

---

## Technical Context

**Language/Version**: Python 3.11+ (backend, all microservices), TypeScript 5.3+ (frontend)
**Primary Dependencies**: FastAPI 0.109+, SQLModel 0.0.14+, httpx (Dapr HTTP client), Pydantic 2.6+, Next.js 14.1
**Storage**: PostgreSQL (Neon DB) for tasks; Kafka/Redpanda for events; Dapr state store (optional)
**Testing**: pytest (Python), Jest (TypeScript), Playwright (e2e)
**Target Platform**: Kubernetes (Minikube local, OKE/AKS/GKE cloud)
**Project Type**: Web application with microservices
**Performance Goals**: API < 200ms p95, reminder delivery < 60s of scheduled time, Helm deploy < 5min
**Constraints**: Free-tier cloud providers; no direct Kafka library imports after Dapr integration
**Scale/Scope**: Single-user to small-team usage; 7 pods (frontend, backend, 4 consumers, Redpanda)

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Phased Evolution | PASS | Phase 5 builds on completed Phase 4 K8s infrastructure |
| II. Test-First Development | PASS | Tests required for all new model fields, API extensions, and consumer logic |
| III. Smallest Viable Change | PASS with justification | Adding 4 microservices is significant, but each is <100 lines and required by the hackathon brief |
| IV. Clean Interfaces | PASS | All services communicate via Dapr HTTP API; contracts defined in OpenAPI |
| V. Observability First | PASS | Structured logging in all services; audit-service provides event trail |
| VI. Security by Default | PASS | Secrets via Dapr/K8s Secrets; no hardcoded credentials; input validation on new fields |

### Post-Design Re-Check

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Phased Evolution | PASS | Extends Phase 4 Helm charts; no Phase 4 rework needed |
| II. Test-First Development | PASS | Unit tests for model validation, service logic, API endpoints; integration tests for event flow |
| III. Smallest Viable Change | PASS with justification | 4 new services justified: each handles a distinct concern (see Complexity Tracking) |
| IV. Clean Interfaces | PASS | OpenAPI contract covers all new endpoints; Dapr component contracts defined |
| V. Observability First | PASS | All events logged; audit-service captures complete mutation history |
| VI. Security by Default | PASS | All secrets in K8s Secrets accessed via Dapr; no env vars with plaintext credentials |

---

## Project Structure

### Documentation (this feature)

```text
specs/006-phase5-advanced-cloud/
├── plan.md              # This file
├── research.md          # Phase 0: Technology decisions
├── data-model.md        # Phase 1: Entity definitions
├── quickstart.md        # Phase 1: Developer setup guide
├── contracts/
│   ├── api-extensions.yaml    # OpenAPI contract for new/modified endpoints
│   └── dapr-components.yaml   # Dapr component contracts
├── checklists/
│   └── requirements.md        # Spec quality checklist
└── tasks.md             # Phase 2 output (created by /sp.tasks)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/task.py           # Extended: +due_at, +remind_at, +recurrence_rule, +recurrence_interval
│   ├── schemas/task.py          # Extended: new fields in Create/Update/Response
│   ├── services/
│   │   ├── task_service.py      # Extended: due-date filtering, sorting, recurrence
│   │   └── event_publisher.py   # New: publish TaskEvents via Dapr Pub/Sub
│   ├── api/
│   │   └── tasks.py             # Extended: new query params, event publishing hooks
│   ├── chatkit_server.py        # Extended: new tool params for due_at, remind_at, recurrence
│   ├── config.py                # Extended: Dapr settings
│   ├── database.py              # Extended: migration checker for new columns
│   └── main.py                  # Extended: Dapr subscription endpoint, jobs callback
├── tests/
│   ├── unit/
│   │   ├── test_models.py       # Tests for new field validation
│   │   ├── test_task_service.py # Tests for due-date filter, recurrence logic
│   │   └── test_event_publisher.py  # Tests for event publishing
│   └── integration/
│       └── test_api.py          # Tests for new API params and responses
├── requirements.txt             # +httpx
└── Dockerfile                   # Unchanged

frontend/
├── src/
│   ├── types/task.ts            # Extended: new fields
│   ├── components/              # Extended: due date picker, reminder UI, recurrence selector
│   └── services/api.ts          # Extended: new query params
└── Dockerfile                   # Unchanged

services/                        # New directory for consumer microservices
├── notification-service/
│   ├── main.py                  # FastAPI app: Dapr subscription for reminders topic
│   ├── requirements.txt
│   └── Dockerfile
├── recurring-task-service/
│   ├── main.py                  # FastAPI app: Dapr subscription for task-events topic
│   ├── requirements.txt
│   └── Dockerfile
├── audit-service/
│   ├── main.py                  # FastAPI app: Dapr subscription for task-events topic
│   ├── requirements.txt
│   └── Dockerfile
└── websocket-service/
    ├── main.py                  # FastAPI app: Dapr subscription for task-updates topic + WebSocket
    ├── requirements.txt
    └── Dockerfile

dapr-components/                 # New: Dapr component YAML files
├── kafka-pubsub.yaml
├── statestore.yaml
└── kubernetes-secrets.yaml

k8s/
├── charts/todo-app/
│   ├── values.yaml              # Extended: consumer services, Redpanda config
│   ├── values-production.yaml   # New: cloud-specific values (TLS, ingress, resources)
│   └── templates/
│       ├── notification-service-*.yaml    # New
│       ├── recurring-task-service-*.yaml  # New
│       ├── audit-service-*.yaml           # New
│       ├── websocket-service-*.yaml       # New
│       ├── redpanda-*.yaml                # New
│       ├── dapr-components.yaml           # New
│       └── ingress.yaml                   # New (cloud)
└── base/                        # Unchanged (raw manifests from Phase 4)

.github/workflows/               # New: CI/CD pipelines
├── ci.yml
└── deploy.yml
```

**Structure Decision**: Web application with microservices. The existing `backend/` and `frontend/` directories are extended. A new `services/` directory at root level houses the 4 consumer microservices, each with its own FastAPI app and Dockerfile. Infrastructure config lives in `dapr-components/` and extended `k8s/charts/`.

---

## Complexity Tracking

> Constitution Principle III (Smallest Viable Change) requires justification for 4 new microservices.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| 4 new microservices | Hackathon Phase 5 explicitly requires event-driven architecture with consumer services | Putting all consumers in the backend would create tight coupling and violate the event-driven architecture requirement |
| Dapr abstraction layer | Required by hackathon brief to demonstrate distributed application runtime | Direct Kafka client code would work but misses the Dapr learning objective |
| Redpanda deployment | Kafka-compatible broker needed for Pub/Sub | In-memory event bus wouldn't demonstrate real message brokering |

---

## Architecture Overview

### Service Communication Flow

```
                                    ┌─────────────────────────┐
                                    │       Frontend          │
                                    │    (Next.js + WS)       │
                                    └─────────┬───────────────┘
                                              │ HTTP / WebSocket
                                              ▼
┌──────────────────────────────────────────────────────────────────────┐
│                         Dapr Sidecar                                 │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │                     Backend (FastAPI)                            │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────────┐ │ │
│  │  │ Task API │  │ Chat API │  │ Event    │  │ Jobs Callback  │ │ │
│  │  │          │  │          │  │ Publisher│  │ /api/jobs/     │ │ │
│  │  └────┬─────┘  └──────────┘  └────┬─────┘  └────────────────┘ │ │
│  │       │                            │                            │ │
│  │       ▼                            ▼                            │ │
│  │  PostgreSQL                 Dapr Pub/Sub                        │ │
│  │  (Neon DB)                  (HTTP → Kafka)                      │ │
│  └─────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────┘
                                    │
                    Kafka/Redpanda Topics
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
            ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
            │ task-events  │ │  reminders   │ │ task-updates  │
            └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
                   │                │                │
          ┌────────┴────────┐      │                │
          ▼                 ▼      ▼                ▼
  ┌───────────────┐ ┌───────────┐ ┌──────────────┐ ┌──────────────┐
  │ recurring-    │ │ audit-    │ │ notification-│ │ websocket-   │
  │ task-service  │ │ service   │ │ service      │ │ service      │
  └───────────────┘ └───────────┘ └──────────────┘ └──────────────┘
```

### Event Flow: Task Completion with Recurrence

```
1. User completes task via API
2. Backend toggles completed=true, persists to DB
3. Backend publishes task.completed to task-events + task-updates via Dapr Pub/Sub
4. recurring-task-service receives task.completed event
5. Checks if task has recurrence_rule
6. If yes: calls Backend API to create new task with next due_at
7. Backend creates new task, publishes task.created
8. websocket-service broadcasts the new task to all connected clients
```

### Event Flow: Reminder

```
1. User creates task with remind_at via API
2. Backend persists task, then schedules Dapr Job with dueTime=remind_at
3. At remind_at, Dapr calls /api/jobs/trigger on the backend
4. Backend publishes reminder.due to reminders topic via Dapr Pub/Sub
5. notification-service receives reminder.due
6. notification-service publishes to task-updates for websocket delivery
7. websocket-service broadcasts reminder notification to connected clients
```

---

## Implementation Phases

### Part A: Features (Steps 1-6)

**Goal**: Extend the Task model, API, and UI with due dates, reminders, and recurrence.

**Approach**:
- Add 4 nullable columns to Task model (`due_at`, `remind_at`, `recurrence_rule`, `recurrence_interval`)
- Extend Pydantic schemas with new fields + validation (remind_at <= due_at)
- Add due-date filtering (`due_before`, `due_after`, `overdue` params) and sorting (`due_date` option)
- Update chatbot tools to accept new parameters
- Update frontend TypeScript types and add UI components

**Key Files Modified**: `backend/src/models/task.py`, `backend/src/schemas/task.py`, `backend/src/services/task_service.py`, `backend/src/api/tasks.py`, `backend/src/chatkit_server.py`, `frontend/src/types/task.ts`

### Part A: Kafka Event Publishing (Steps 7-11)

**Goal**: Publish events on all task mutations; build 4 consumer microservices.

**Approach**:
- Create `event_publisher.py` that publishes TaskEvent JSON via Dapr Pub/Sub HTTP endpoint
- Hook event publishing into TaskService (after create, update, complete, delete)
- Build each consumer as a minimal FastAPI app with a Dapr subscription endpoint
- Each consumer has its own Dockerfile based on `python:3.11-slim`

**Key Files Created**: `backend/src/services/event_publisher.py`, `services/notification-service/`, `services/recurring-task-service/`, `services/audit-service/`, `services/websocket-service/`

### Part A: Dapr Integration (Steps 12-15)

**Goal**: Replace direct Kafka imports with Dapr HTTP API; add Jobs and Secrets.

**Approach**:
- Event publisher uses `httpx.post("http://localhost:3500/v1.0/publish/kafka-pubsub/{topic}", json=event)`
- Consumers expose `GET /dapr/subscribe` returning their subscription config
- Reminder scheduling uses `httpx.post("http://localhost:3500/v1.0-alpha1/jobs/{job-name}", json={dueTime, data})`
- Secrets retrieved via `httpx.get("http://localhost:3500/v1.0/secrets/kubernetes-secrets/{key}")`
- Create Dapr component YAML files in `dapr-components/`

**Key Files Created**: `dapr-components/*.yaml`
**Key Files Modified**: `backend/src/config.py`, `backend/src/main.py`

### Part B: Minikube Deployment (Steps 16-21)

**Goal**: Deploy entire stack to local Minikube with Dapr sidecars.

**Approach**:
- Add Helm templates for 4 consumer services (deployment + service each)
- Add Helm template for Redpanda StatefulSet
- Add Dapr annotations to all pod templates (`dapr.io/enabled: "true"`, `dapr.io/app-id`, `dapr.io/app-port`)
- Deploy Dapr on Minikube via `dapr init -k`
- Smoke test: create task via frontend, verify event in audit-service logs

**Key Files Modified**: `k8s/charts/todo-app/values.yaml`, `k8s/charts/todo-app/Chart.yaml`
**Key Files Created**: `k8s/charts/todo-app/templates/` (8+ new template files)

### Part C: Cloud Deployment (Steps 22-26)

**Goal**: Promote Minikube stack to production cloud Kubernetes.

**Approach**:
- Provision OKE cluster (or AKS/GKE)
- Install Dapr on cloud cluster
- Configure Kafka (Redpanda Cloud serverless or Strimzi)
- Create `values-production.yaml` with TLS, ingress, resource limits, cloud Kafka credentials
- Deploy via `helm upgrade --install`

**Key Files Created**: `k8s/charts/todo-app/values-production.yaml`, `k8s/charts/todo-app/templates/ingress.yaml`

### Part C: CI/CD Pipeline (Steps 27-30)

**Goal**: Automate lint/test/build/deploy with GitHub Actions.

**Approach**:
- CI workflow: trigger on push/PR, run ruff (Python lint), eslint (TS lint), pytest, jest
- Deploy workflow: trigger on push to main, build Docker images, push to GHCR, Helm upgrade, rollback on failure
- Document required GitHub Secrets

**Key Files Created**: `.github/workflows/ci.yml`, `.github/workflows/deploy.yml`

---

## Risk Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| Dapr Jobs API in alpha | Reminder scheduling may have bugs | Fallback: use Dapr Cron Binding to poll every minute |
| Redpanda Cloud rate limits | Free tier may throttle during testing | Fallback: self-hosted Redpanda in cluster |
| Cloud cluster provisioning failure | Cannot deploy to production | Document manual steps for all 3 providers (OKE, AKS, GKE) |
| Consumer pod restarts | Missed events | Kafka consumer groups handle offset tracking; Dapr retries failed deliveries |

---

## Definition of Done

- [ ] All 4 new Task fields work in API (create, read, update, filter, sort)
- [ ] Recurring tasks spawn new instances on completion
- [ ] Reminders fire within 60s of scheduled time
- [ ] All 4 consumer microservices process events correctly
- [ ] No direct Kafka library imports in application code
- [ ] Full stack deploys to Minikube with all pods healthy
- [ ] Full stack deploys to cloud with TLS and ingress
- [ ] CI/CD pipeline passes all stages
- [ ] All tests pass (unit + integration)
