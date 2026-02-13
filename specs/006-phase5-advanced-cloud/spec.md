# Feature Specification: Phase 5 — Advanced Cloud Deployment

**Feature Branch**: `006-phase5-advanced-cloud`
**Created**: 2026-02-12
**Status**: Draft
**Input**: User description: "Phase 5: Advanced Cloud Deployment - Implement advanced features (Recurring Tasks, Due Dates & Reminders), intermediate features (Priorities, Tags, Search, Filter, Sort), event-driven architecture with Kafka, Dapr for distributed application runtime, local Minikube deployment, cloud deployment to AKS/GKE/OKE, and CI/CD pipeline with GitHub Actions."

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Recurring Tasks (Priority: P1)

A user creates a task that repeats on a schedule. The system automatically spawns a new instance of the task at the specified interval so the user never has to manually re-create routine work.

**Why this priority**: Recurring tasks are the most complex new domain feature. They require a rule engine, event-driven spawning, and touch every layer of the stack — making them the highest-risk item to validate first.

**Independent Test**: Can be fully tested by creating a task with `recurrence_rule = "daily"`, completing it, and verifying a new instance is automatically created within the configured interval.

**Acceptance Scenarios**:

1. **Given** a user creates a task with a daily recurrence rule, **When** the task is marked complete, **Then** a new task with the same title, priority, and tags is created with the next due date set to tomorrow.
2. **Given** a user creates a task with a weekly recurrence rule on Mondays, **When** the current Monday task is completed, **Then** a new task is created with a due date of next Monday.
3. **Given** a user creates a recurring task, **When** the user explicitly deletes (not completes) the task, **Then** no future instances are spawned.
4. **Given** a user modifies a recurring task's title, **When** the next recurrence fires, **Then** the new instance uses the updated title.

---

### User Story 2 — Due Dates and Reminders (Priority: P1)

A user assigns a due date to any task. Optionally, the user sets a reminder time before the due date. The system notifies the user at the reminder time.

**Why this priority**: Due dates and reminders are the most requested productivity features. They are also a prerequisite for recurring task scheduling.

**Independent Test**: Can be tested by creating a task with `due_at = tomorrow 9:00 AM` and `remind_at = tomorrow 8:30 AM`, then verifying the reminder fires at 8:30 AM.

**Acceptance Scenarios**:

1. **Given** a user creates a task with a due date, **When** the task list is viewed, **Then** the due date is displayed alongside the task.
2. **Given** a user sets a reminder 30 minutes before the due date, **When** the reminder time arrives, **Then** the user receives a notification with the task title.
3. **Given** a task's due date has passed without completion, **When** the user views the task list, **Then** the task is visually flagged as overdue.
4. **Given** a user completes a task before the reminder fires, **When** the reminder time arrives, **Then** no notification is sent.

---

### User Story 3 — Priorities, Tags, Search, Filter & Sort (Priority: P2)

A user organizes tasks using priority levels (high, medium, low), tags (arbitrary labels), full-text search across task titles, and filtering/sorting by any combination of priority, tag, status, and due date.

**Why this priority**: These features already partially exist (priorities and tags are in the model; basic search and filter exist in the API). This story extends them with due-date filtering, sort-by-due-date, and ensures the chatbot and event system support them.

**Independent Test**: Can be tested by creating several tasks with different priorities, tags, and due dates, then verifying that search, filter, and sort queries return correct results.

**Acceptance Scenarios**:

1. **Given** tasks with priorities high, medium, and low exist, **When** a user filters by priority = high, **Then** only high-priority tasks are returned.
2. **Given** tasks tagged "work" and "personal" exist, **When** a user filters by tag = "work", **Then** only work-tagged tasks are returned.
3. **Given** a user searches for "grocery", **When** a task titled "Buy groceries" exists, **Then** the search returns that task.
4. **Given** tasks with various due dates exist, **When** a user sorts by due date ascending, **Then** tasks are ordered from earliest to latest due date, with tasks without due dates listed last.

---

### User Story 4 — Event-Driven Architecture with Kafka (Priority: P2)

When a task is created, updated, completed, or deleted, the system publishes an event to a message broker. Specialized microservices consume these events to handle notifications, recurring task spawning, and activity auditing independently.

**Why this priority**: Kafka decouples services and enables the reminder, recurring task, and audit features to scale independently. It transforms the app from synchronous CRUD into an event-driven system.

**Independent Test**: Can be tested by creating a task and verifying that an event appears on the `task-events` topic, and that the audit consumer logs the event.

**Acceptance Scenarios**:

1. **Given** a user creates a task, **When** the create operation completes, **Then** a `task.created` event is published to the `task-events` topic containing the task ID, title, and timestamp.
2. **Given** a task completion event is published, **When** the recurring-task-service consumes it, **Then** a new recurring instance is created if the task has a recurrence rule.
3. **Given** a reminder is due, **When** the notification-service consumes the `reminders` topic, **Then** it delivers the notification to the user.
4. **Given** any task mutation occurs, **When** the audit-service consumes the event, **Then** it logs the event with actor, action, and timestamp.

---

### User Story 5 — Dapr Integration (Priority: P3)

The application communicates with Kafka, state stores, and secrets through Dapr's HTTP API rather than importing vendor-specific libraries directly. Infrastructure can be swapped (e.g., Kafka to RabbitMQ) by changing YAML configuration without code changes.

**Why this priority**: Dapr abstracts infrastructure. It is layered on top of the working Kafka integration, so it depends on Kafka being functional first.

**Independent Test**: Can be tested by publishing a task event via Dapr's Pub/Sub HTTP endpoint and verifying it reaches the consumer, without any Kafka client library imported in the application code.

**Acceptance Scenarios**:

1. **Given** Dapr is initialized on the cluster, **When** the backend publishes an event via Dapr Pub/Sub, **Then** consumers receive the event.
2. **Given** Dapr Secrets API is configured, **When** the application requests a secret, **Then** it retrieves it without hardcoded credentials in the codebase.
3. **Given** a reminder is scheduled via Dapr Jobs API, **When** the scheduled time arrives, **Then** Dapr calls the application's callback endpoint to trigger the reminder.
4. **Given** the frontend calls the backend via Dapr Service Invocation, **When** the backend is healthy, **Then** the request is routed with built-in retries and mTLS.

---

### User Story 6 — Local Minikube Deployment (Priority: P3)

A developer deploys the entire stack (frontend, backend, Kafka/Redpanda, Dapr sidecars, consumer microservices) to a local Minikube cluster using Helm charts and verifies all services communicate correctly.

**Why this priority**: Local deployment validates the full architecture before committing to cloud costs. It also serves as the developer inner-loop environment.

**Independent Test**: Can be tested by running `helm install` on Minikube, creating a task via the frontend, and verifying the event flows through Kafka to the audit consumer.

**Acceptance Scenarios**:

1. **Given** Minikube is running with Dapr installed, **When** the Helm chart is applied, **Then** all pods (frontend, backend, Redpanda, notification-service, recurring-task-service, audit-service, websocket-service) reach Running status.
2. **Given** all pods are running, **When** a user creates a task through the frontend, **Then** the task is persisted and an event is visible on the Kafka topic.
3. **Given** Dapr sidecars are attached, **When** a service publishes via Dapr Pub/Sub, **Then** the message reaches the consumer without direct Kafka client code.

---

### User Story 7 — Cloud Deployment (Priority: P4)

The Minikube-verified stack is promoted to a production-grade managed Kubernetes cluster (AKS, GKE, or OKE) with TLS, ingress, Dapr, and Kafka (Redpanda Cloud or Strimzi).

**Why this priority**: Cloud deployment is the final deliverable. It depends on all previous stories being complete and working locally.

**Independent Test**: Can be tested by accessing the public URL over HTTPS, creating a task, and verifying end-to-end flow (frontend to backend to Kafka to consumer).

**Acceptance Scenarios**:

1. **Given** the cloud cluster is provisioned, **When** the Helm chart is deployed with production values, **Then** all pods reach Running status with Dapr sidecars injected.
2. **Given** TLS is configured via cert-manager, **When** a user accesses the application URL, **Then** the connection is secured with a valid certificate.
3. **Given** Kafka is connected (Redpanda Cloud or Strimzi), **When** a task event is published, **Then** all consumer services process it successfully.

---

### User Story 8 — CI/CD Pipeline (Priority: P4)

Every push to the main branch triggers an automated pipeline that lints, tests, builds container images, pushes them to a registry, and deploys to the cloud cluster.

**Why this priority**: CI/CD is the final operational requirement. It automates what was previously done manually.

**Independent Test**: Can be tested by pushing a commit and verifying that the pipeline runs all stages (lint, test, build, push, deploy) and the updated application is live.

**Acceptance Scenarios**:

1. **Given** a developer pushes to the main branch, **When** GitHub Actions triggers, **Then** linting and tests run and must pass before proceeding.
2. **Given** tests pass, **When** the build stage runs, **Then** Docker images are built and pushed to GitHub Container Registry (GHCR).
3. **Given** images are pushed, **When** the deploy stage runs, **Then** the Helm chart is upgraded on the cloud cluster with the new image tags.
4. **Given** a deployment fails, **When** health checks report unhealthy, **Then** the pipeline triggers a Helm rollback to the previous release.

---

### Edge Cases

- What happens when a recurring task's recurrence rule is invalid (e.g., "every 0 days")? The system rejects with a validation error.
- What happens when a reminder is set for a time in the past? The system rejects with a validation error indicating the reminder time must be in the future.
- What happens when Kafka is temporarily unavailable? Events are retried with exponential backoff; the main API continues serving requests (eventual consistency).
- What happens when a user deletes a task that has a pending reminder? The scheduled reminder job is cancelled.
- What happens when the cloud cluster runs out of resources during deployment? The pipeline reports the failure and does not mark the deployment as successful.

---

## Requirements *(mandatory)*

### Functional Requirements

**Part A — Advanced Features**

- **FR-001**: System MUST allow users to set a due date (`due_at`) on any task as an optional datetime field.
- **FR-002**: System MUST allow users to set a reminder time (`remind_at`) on any task, constrained to be before or equal to the `due_at` value.
- **FR-003**: System MUST visually indicate overdue tasks (tasks past their `due_at` that are not completed).
- **FR-004**: System MUST deliver a notification to the user when the `remind_at` time is reached for an incomplete task.
- **FR-005**: System MUST support recurring tasks with the following recurrence rules: daily, weekly, monthly, and custom interval (every N days).
- **FR-006**: System MUST automatically create the next instance of a recurring task when the current instance is completed.
- **FR-007**: System MUST stop recurring task generation when the user explicitly deletes (not completes) the task.
- **FR-008**: System MUST support filtering tasks by due date range (e.g., "due this week").
- **FR-009**: System MUST support sorting tasks by due date (ascending and descending).

**Part A — Intermediate Features (Extensions)**

- **FR-010**: System MUST continue to support priority levels (high, medium, low) as already implemented.
- **FR-011**: System MUST continue to support tagging tasks with arbitrary string labels as already implemented.
- **FR-012**: System MUST support full-text search across task titles (already implemented; extend to search descriptions if added).
- **FR-013**: System MUST support combined filtering by priority, tag, status, and due date simultaneously.
- **FR-014**: System MUST support sorting by priority, due date, creation date, and alphabetical order.

**Part A — Event-Driven Architecture (Kafka)**

- **FR-015**: System MUST publish events to a `task-events` topic when a task is created, updated, completed, or deleted.
- **FR-016**: System MUST publish reminder-due events to a `reminders` topic when a reminder time is reached.
- **FR-017**: System MUST publish task state changes to a `task-updates` topic for real-time client synchronization.
- **FR-018**: A notification-service MUST consume from the `reminders` topic and deliver notifications.
- **FR-019**: A recurring-task-service MUST consume from `task-events` and spawn new task instances on completion of recurring tasks.
- **FR-020**: An audit-service MUST consume from `task-events` and log all task mutations with actor, action, and timestamp.
- **FR-021**: A websocket-service MUST consume from `task-updates` and broadcast changes to connected clients.

**Part A — Dapr Integration**

- **FR-022**: System MUST publish events via Dapr Pub/Sub HTTP API instead of direct Kafka client libraries.
- **FR-023**: System MUST consume events via Dapr Pub/Sub subscription endpoints.
- **FR-024**: System MUST schedule reminders via Dapr Jobs API (exact time scheduling, not polling).
- **FR-025**: System MUST retrieve secrets (database URL, API keys) via Dapr Secrets API or Kubernetes Secrets.
- **FR-026**: Frontend-to-backend communication MAY use Dapr Service Invocation for discovery and retries.
- **FR-027**: System MUST NOT import any direct Kafka client libraries (e.g., `kafka-python`, `aiokafka`) in application code after Dapr integration.

**Part B — Local Deployment**

- **FR-028**: System MUST deploy to a local Minikube cluster using Helm charts.
- **FR-029**: System MUST include Dapr sidecars on all application pods.
- **FR-030**: System MUST deploy Redpanda (or equivalent) as the local Kafka-compatible broker within Minikube.
- **FR-031**: System MUST include Dapr component YAML files for Pub/Sub, State, Secrets, and Bindings.

**Part C — Cloud Deployment**

- **FR-032**: System MUST deploy to a managed Kubernetes service (AKS, GKE, or OKE).
- **FR-033**: System MUST configure TLS termination with a valid certificate (cert-manager + Let's Encrypt or equivalent).
- **FR-034**: System MUST configure ingress for external HTTPS access.
- **FR-035**: System MUST connect to Kafka via Redpanda Cloud, Confluent Cloud, Strimzi, or any Dapr-compatible Pub/Sub provider.
- **FR-036**: System MUST deploy Dapr on the cloud cluster with full building blocks (Pub/Sub, State, Bindings, Secrets, Service Invocation).

**Part C — CI/CD**

- **FR-037**: System MUST have a GitHub Actions CI workflow that runs linting and tests on every push/PR.
- **FR-038**: System MUST have a GitHub Actions deploy workflow that builds Docker images, pushes to GHCR, and deploys via Helm.
- **FR-039**: System MUST support rollback on failed deployments (Helm rollback).
- **FR-040**: System MUST document all required GitHub Secrets for the pipeline.

### Key Entities

- **Task** (extended): The core entity. Extended with `due_at` (optional datetime), `remind_at` (optional datetime), `recurrence_rule` (optional string — "daily", "weekly", "monthly", or "every_N_days"), and `recurrence_interval` (optional integer for custom intervals).
- **TaskEvent**: An event record representing a task mutation. Contains event type, task ID, task snapshot, actor, and timestamp. Published to Kafka topics.
- **Reminder**: A scheduled job that fires at a specific time to notify a user about an upcoming task. Managed via Dapr Jobs API.
- **AuditLog**: An immutable record of every task mutation, consumed from `task-events` by the audit-service.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can create, view, and manage recurring tasks with at least 4 recurrence patterns (daily, weekly, monthly, custom interval).
- **SC-002**: Users receive reminders within 60 seconds of the scheduled `remind_at` time for incomplete tasks.
- **SC-003**: Users can filter and sort tasks by any combination of priority, tag, status, and due date, with results returned in under 2 seconds.
- **SC-004**: Task events (create, update, complete, delete) are published and consumed by all 4 microservices (notification, recurring-task, audit, websocket) without message loss under normal operation.
- **SC-005**: The full stack deploys to Minikube with all pods healthy within 5 minutes of running the Helm install command.
- **SC-006**: The full stack deploys to a cloud Kubernetes cluster with TLS-secured HTTPS access and all pods healthy.
- **SC-007**: The CI/CD pipeline completes a full cycle (lint, test, build, push, deploy) within 15 minutes of a push to the main branch.
- **SC-008**: Failed deployments automatically roll back to the previous healthy release.
- **SC-009**: No direct Kafka client library imports exist in application code after Dapr integration is complete.
- **SC-010**: All infrastructure secrets are managed through Dapr Secrets API or Kubernetes Secrets — zero hardcoded credentials.

---

## Assumptions

- The existing Phase 4 Kubernetes infrastructure (Dockerfiles, Helm charts, base manifests) is functional and will be extended, not rewritten.
- The existing Task model fields (id, title, completed, priority, tags, created_at, updated_at) remain unchanged; new fields are additive.
- PostgreSQL (Neon DB) remains the primary relational database for task storage.
- The AI chatbot (Phase 3) will be updated to support new fields (due_at, remind_at, recurrence) via tool invocations.
- Redpanda is used as the Kafka-compatible broker for both local (container) and cloud (Redpanda Cloud serverless) deployments, unless the user opts for Strimzi or another provider.
- OKE (Oracle Cloud) is the primary cloud target due to its always-free tier, with AKS and GKE as alternatives.
- The notification delivery mechanism is in-app (websocket broadcast) rather than email/SMS, unless the user specifies otherwise.

---

## Dependencies

- Phase 4 (Kubernetes deployment) must be complete and the Helm chart must be functional.
- A Kafka-compatible broker (Redpanda) must be available locally and in the cloud.
- Dapr CLI and runtime must be installable on the target Kubernetes clusters.
- A cloud Kubernetes provider account (OKE, AKS, or GKE) with sufficient credits/quota.
- GitHub repository configured for GitHub Actions with appropriate secrets.

---

## Risks

- **Kafka complexity**: Running a message broker adds operational overhead. Mitigated by using Redpanda (simpler, no Zookeeper) and Dapr (abstracts the broker).
- **Cloud cost overruns**: Managed Kubernetes and Kafka services may exceed free-tier limits. Mitigated by using OKE always-free tier and Redpanda Cloud serverless free tier.
- **Dapr maturity**: Some Dapr features (Jobs API) are in alpha. Mitigated by having fallback implementations and keeping Dapr optional for core functionality.
