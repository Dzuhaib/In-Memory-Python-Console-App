# Research: Phase 5 — Advanced Cloud Deployment

**Branch**: `006-phase5-advanced-cloud` | **Date**: 2026-02-12

---

## R-001: Recurring Task Rule Engine

**Decision**: Use a `recurrence_rule` string enum field on the Task model with values: `daily`, `weekly`, `monthly`, `every_N_days`. A `recurrence_interval` integer field stores the custom N value. The recurring-task-service consumes `task.completed` events and creates new instances.

**Rationale**: Simple string enum avoids the complexity of RFC 5545 RRULE parsing while covering the four required patterns. The spawning logic lives in a consumer microservice, keeping the main API stateless.

**Alternatives considered**:
- RFC 5545 RRULE format (e.g., `RRULE:FREQ=DAILY`): Too complex for 4 patterns; overkill for a hackathon.
- Cron expressions: Powerful but unintuitive for end users; harder to validate.
- Separate RecurrenceRule table: Adds a join; unnecessary when the rule is a simple enum.

---

## R-002: Reminder Scheduling Mechanism

**Decision**: Use Dapr Jobs API to schedule one-shot reminders at exact times. Each reminder is a Dapr job with `dueTime` set to the task's `remind_at` timestamp. When the job fires, Dapr calls a callback endpoint on the backend, which publishes to the `reminders` Kafka topic.

**Rationale**: Dapr Jobs API provides exact-time scheduling without polling overhead. It eliminates the need for a cron-based scanner that queries the database every minute.

**Alternatives considered**:
- Cron Binding (poll every minute): Wasteful; doesn't scale well; 0-60s latency.
- APScheduler (Python in-process): Not Kubernetes-native; lost on pod restart.
- Celery + Redis: Adds 2 dependencies; heavier than Dapr Jobs for this use case.

---

## R-003: Kafka Topic Design

**Decision**: Three topics:
1. `task-events` — All CRUD mutations (created, updated, completed, deleted). Consumed by recurring-task-service and audit-service.
2. `reminders` — Reminder-due notifications. Consumed by notification-service.
3. `task-updates` — Real-time state changes for UI sync. Consumed by websocket-service.

**Rationale**: Separating topics by consumer purpose avoids complex filtering logic. Each consumer subscribes to exactly the topic it needs.

**Alternatives considered**:
- Single `tasks` topic with event-type filtering: Simpler config but all consumers process all messages; wasteful.
- Per-event topics (`task-created`, `task-updated`, etc.): Too many topics; harder to manage.

---

## R-004: Dapr Building Blocks Selection

**Decision**: Use 5 Dapr building blocks:
1. **Pub/Sub** (`pubsub.kafka`): Abstract Kafka publishing and subscribing.
2. **State Management** (`state.postgresql`): Optional; conversation state for chatbot. May keep direct SQLModel for primary task storage.
3. **Service Invocation**: Frontend-to-backend discovery with retries.
4. **Jobs API**: Schedule reminders at exact times.
5. **Secrets** (`secretstores.kubernetes`): Retrieve DATABASE_URL, OPENAI_API_KEY from K8s secrets.

**Rationale**: These five blocks cover all infrastructure abstractions needed. Primary task storage stays in PostgreSQL via SQLModel (not Dapr state) because the app already has a working ORM layer.

**Alternatives considered**:
- Dapr State for task storage: Would require rewriting the entire data layer; not worth it.
- Skip Service Invocation: Lose automatic retries and mTLS.

---

## R-005: Consumer Microservice Architecture

**Decision**: Four consumer microservices, each a separate FastAPI application with its own Dockerfile:
1. **notification-service**: Consumes `reminders`, broadcasts via websocket-service.
2. **recurring-task-service**: Consumes `task-events` (completed), creates new task instances via backend API.
3. **audit-service**: Consumes `task-events`, logs to stdout (structured JSON) for K8s log aggregation.
4. **websocket-service**: Consumes `task-updates`, broadcasts to connected WebSocket clients.

**Rationale**: Separate services allow independent scaling and failure isolation. Each service is a thin Python app (~50-100 lines) with a Dapr subscription endpoint.

**Alternatives considered**:
- Single monolith consumer: Violates the event-driven microservice pattern; single point of failure.
- Serverless functions: Not applicable in self-hosted K8s; adds FaaS complexity.

---

## R-006: Database Migration Strategy

**Decision**: Add new nullable columns (`due_at`, `remind_at`, `recurrence_rule`, `recurrence_interval`) to the existing `task` table using SQLModel's `create_all()` with `checkfirst=True`. Existing data is unaffected since all new fields are optional.

**Rationale**: The existing migration logic in `database.py` uses `create_all()` which only adds missing tables/columns. Since all new fields are nullable with defaults, existing rows remain valid.

**Alternatives considered**:
- Alembic migrations: More robust for production but adds tooling overhead; the existing `create_all()` + migration checker pattern works for this project's scale.
- Recreate table: Destructive; loses existing data.

---

## R-007: Kafka Broker for Local and Cloud

**Decision**:
- **Local (Minikube)**: Deploy Redpanda as a single-node StatefulSet within the cluster. No Zookeeper needed.
- **Cloud**: Redpanda Cloud Serverless (free tier) or Strimzi operator (self-hosted, free).

**Rationale**: Redpanda is Kafka-compatible, simpler to operate (no Zookeeper), and has a free serverless tier. Strimzi is the fallback for self-hosted.

**Alternatives considered**:
- Confluent Cloud: $400 credit expires; no permanent free tier.
- CloudKarafka: 5 topics free but limited throughput.
- Apache Kafka (direct): Requires Zookeeper; more complex to deploy.

---

## R-008: Cloud Kubernetes Provider

**Decision**: OKE (Oracle Cloud) as primary target. Always-free tier includes 4 OCPUs and 24GB RAM — sufficient for the full stack with no time limit. AKS and GKE documented as alternatives.

**Rationale**: OKE's always-free tier eliminates cost pressure. AKS ($200/30 days) and GKE ($300/90 days) are time-limited.

**Alternatives considered**:
- AKS: Good docs, 30-day credit limit.
- GKE: Best Kubernetes implementation, 90-day credit limit.
- DigitalOcean DOKS: $200/60 days; referenced in constitution but OKE is more sustainable.

---

## R-009: CI/CD Pipeline Design

**Decision**: Two GitHub Actions workflows:
1. **ci.yml**: Triggers on push/PR to any branch. Runs linting (ruff, eslint), tests (pytest, jest), and type checking.
2. **deploy.yml**: Triggers on push to main branch only. Builds Docker images, pushes to GHCR, deploys via Helm upgrade, with rollback on failure.

**Rationale**: Separating CI from CD allows PRs to be tested without triggering deployments. GHCR is free for public repos and integrates natively with GitHub Actions.

**Alternatives considered**:
- Single workflow with conditional stages: Harder to maintain and debug.
- Docker Hub: Requires separate account; GHCR is integrated.
- ArgoCD for GitOps: Overkill for this project; adds another operator.

---

## R-010: Notification Delivery Mechanism

**Decision**: In-app WebSocket notifications. The websocket-service maintains persistent connections with browser clients and broadcasts reminder notifications as JSON messages.

**Rationale**: WebSocket is already needed for real-time task sync (FR-021). Using the same channel for reminders avoids adding email/SMS providers.

**Alternatives considered**:
- Email (SendGrid/SES): Requires third-party account; outside project scope.
- Push notifications: Requires service worker setup; complex for a hackathon.
- Polling: Adds latency; WebSocket is already implemented for task-updates.
