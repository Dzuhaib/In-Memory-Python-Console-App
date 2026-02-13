# Data Model: Phase 5 — Advanced Cloud Deployment

**Branch**: `006-phase5-advanced-cloud` | **Date**: 2026-02-12

---

## Entity: Task (Extended)

The existing Task entity is extended with 4 new optional fields. No existing fields are modified.

### Fields

| Field | Type | Required | Default | Constraints | Notes |
|-------|------|----------|---------|-------------|-------|
| id | integer | auto | auto-increment | PK | Existing — unchanged |
| title | string | yes | — | 1–500 chars | Existing — unchanged |
| completed | boolean | no | false | — | Existing — unchanged |
| priority | enum | no | medium | high, medium, low | Existing — unchanged |
| tags | list[string] | no | [] | stored as JSON | Existing — unchanged |
| created_at | datetime | auto | now | — | Existing — unchanged |
| updated_at | datetime | auto | now | updated on change | Existing — unchanged |
| **due_at** | datetime | no | null | must be in future at creation | **New** — optional due date |
| **remind_at** | datetime | no | null | must be <= due_at if both set; must be in future | **New** — optional reminder time |
| **recurrence_rule** | string | no | null | one of: daily, weekly, monthly, every_N_days | **New** — recurrence pattern |
| **recurrence_interval** | integer | no | null | >= 1; required only when recurrence_rule = every_N_days | **New** — custom interval in days |

### Validation Rules

1. If `remind_at` is set, it must be in the future at the time of creation/update.
2. If both `remind_at` and `due_at` are set, `remind_at` must be <= `due_at`.
3. If `recurrence_rule` is `every_N_days`, then `recurrence_interval` must be >= 1.
4. If `recurrence_rule` is `daily`, `weekly`, or `monthly`, `recurrence_interval` is ignored.
5. A task can have a `due_at` without `recurrence_rule` (one-time deadline).
6. A task can have `recurrence_rule` without `due_at` (the system sets the first due_at based on the rule).

### State Transitions

```
Created (completed=false)
    │
    ├─ complete ──► Completed (completed=true)
    │                  │
    │                  └─ [if recurrence_rule set] ──► New Task Created (next due_at calculated)
    │
    └─ delete ──► Deleted (no recurrence spawned)
```

### Recurrence Due Date Calculation

| Rule | Next due_at |
|------|-------------|
| daily | current due_at + 1 day |
| weekly | current due_at + 7 days |
| monthly | current due_at + 1 calendar month |
| every_N_days | current due_at + N days |

If the original task had no `due_at`, the next instance uses `now + interval` as the due date.

---

## Entity: TaskEvent (Virtual — Kafka Message)

Not persisted in the database. Published as JSON to Kafka topics.

### Fields

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| event_id | string (UUID) | yes | Unique event identifier |
| event_type | string | yes | One of: task.created, task.updated, task.completed, task.deleted |
| task_id | integer | yes | The task this event relates to |
| task_snapshot | object | yes | Full task state at the time of the event |
| actor | string | yes | "user" or "system" (for auto-spawned recurring tasks) |
| timestamp | datetime (ISO 8601) | yes | When the event occurred |
| metadata | object | no | Additional context (e.g., which fields changed for updates) |

### Topic Routing

| Event Type | Topic |
|------------|-------|
| task.created | task-events, task-updates |
| task.updated | task-events, task-updates |
| task.completed | task-events, task-updates |
| task.deleted | task-events, task-updates |
| reminder.due | reminders |

---

## Entity: AuditLog (Consumer-Side Storage)

Persisted by the audit-service consumer. Simple append-only log.

### Fields

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | integer | auto | PK, auto-increment |
| event_id | string (UUID) | yes | From TaskEvent |
| event_type | string | yes | From TaskEvent |
| task_id | integer | yes | From TaskEvent |
| actor | string | yes | From TaskEvent |
| timestamp | datetime | yes | From TaskEvent |
| payload | JSON | yes | Full event payload |

---

## Relationships

```
Task (1) ─────► (many) TaskEvent [via Kafka, not FK]
Task (1) ─────► (0..1) Scheduled Reminder [via Dapr Jobs API, not FK]
TaskEvent (1) ──► (1) AuditLog [consumed by audit-service]
```

---

## Compatibility Notes

- All new fields on Task are nullable → existing rows remain valid after schema update.
- No foreign keys or new tables are added to the primary database.
- AuditLog storage is within the audit-service's own scope (stdout JSON logs or optional SQLite).
- TaskEvent is a Kafka message schema, not a database table.
