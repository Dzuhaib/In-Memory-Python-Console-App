# Quickstart: Phase 5 — Advanced Cloud Deployment

**Branch**: `006-phase5-advanced-cloud` | **Date**: 2026-02-12

---

## Prerequisites

- Docker Desktop running
- Minikube v1.32+ installed
- kubectl v1.28+ configured
- Helm v3.13+ installed
- Dapr CLI v1.13+ installed
- GitHub account with repository access
- Python 3.11+ (for local development)
- Node.js 18+ (for frontend)

## Implementation Order

### Part A: Features + Kafka + Dapr

```
Step 1: Extend Task model (add due_at, remind_at, recurrence_rule, recurrence_interval)
Step 2: Update Pydantic schemas (CreateTaskRequest, UpdateTaskRequest, TaskResponse)
Step 3: Update TaskService (new fields in CRUD, due-date filtering, sorting)
Step 4: Update API endpoints (new query params, validation)
Step 5: Update chatbot tools (support new fields)
Step 6: Update frontend (due date picker, reminder UI, recurrence selector)
Step 7: Add event publisher (publish TaskEvents on CRUD operations)
Step 8: Build notification-service (consume reminders topic)
Step 9: Build recurring-task-service (consume task-events, spawn new instances)
Step 10: Build audit-service (consume task-events, log mutations)
Step 11: Build websocket-service (consume task-updates, broadcast to clients)
Step 12: Replace Kafka client with Dapr Pub/Sub HTTP calls
Step 13: Add Dapr Jobs API for reminder scheduling
Step 14: Add Dapr Secrets API for credential retrieval
Step 15: Create Dapr component YAML files
```

### Part B: Local Deployment

```
Step 16: Update Helm chart with new services (4 consumers + Redpanda)
Step 17: Install Dapr on Minikube
Step 18: Deploy Redpanda to Minikube
Step 19: Apply Dapr components
Step 20: Deploy full stack via Helm
Step 21: Verify all pods healthy + smoke test
```

### Part C: Cloud Deployment + CI/CD

```
Step 22: Provision cloud K8s cluster (OKE/AKS/GKE)
Step 23: Install Dapr on cloud cluster
Step 24: Configure Kafka (Redpanda Cloud or Strimzi)
Step 25: Update Helm values for production (TLS, ingress, resources)
Step 26: Deploy to cloud
Step 27: Create GitHub Actions CI workflow (lint + test)
Step 28: Create GitHub Actions deploy workflow (build + push + Helm upgrade)
Step 29: Configure GitHub Secrets
Step 30: End-to-end verification
```

## Local Development Quick Start

```bash
# 1. Start Minikube
minikube start --memory=4096 --cpus=2

# 2. Install Dapr
dapr init -k

# 3. Build images (point Docker to Minikube)
eval $(minikube docker-env)
docker build -t todo-backend:local ./backend
docker build -t todo-frontend:local ./frontend
docker build -t notification-service:local ./services/notification-service
docker build -t recurring-task-service:local ./services/recurring-task-service
docker build -t audit-service:local ./services/audit-service
docker build -t websocket-service:local ./services/websocket-service

# 4. Deploy
kubectl apply -f dapr-components/
helm install todo-app ./k8s/charts/todo-app \
  --set backend.secrets.DATABASE_URL='...' \
  --set backend.secrets.OPENAI_API_KEY='...'

# 5. Access
minikube service todo-frontend -n todo-app
```

## Key Files to Modify/Create

### Modify (existing)
- `backend/src/models/task.py` — Add new fields
- `backend/src/schemas/task.py` — Extend request/response schemas
- `backend/src/services/task_service.py` — Add filtering, recurrence logic
- `backend/src/api/tasks.py` — New query params, event publishing
- `backend/src/chatkit_server.py` — Support new fields in tools
- `backend/src/config.py` — Add Dapr config settings
- `backend/src/database.py` — Update migration checker for new columns
- `backend/Dockerfile` — Add httpx dependency
- `k8s/charts/todo-app/values.yaml` — Add consumer services, Redpanda
- `k8s/charts/todo-app/Chart.yaml` — Version bump
- `frontend/src/types/task.ts` — Add new fields to TypeScript interface

### Create (new)
- `services/notification-service/` — FastAPI consumer app
- `services/recurring-task-service/` — FastAPI consumer app
- `services/audit-service/` — FastAPI consumer app
- `services/websocket-service/` — FastAPI consumer app
- `dapr-components/` — Dapr component YAML files
- `.github/workflows/ci.yml` — CI pipeline
- `.github/workflows/deploy.yml` — CD pipeline
- `k8s/charts/todo-app/templates/` — New Helm templates for consumers

## Environment Variables (New)

| Variable | Service | Description |
|----------|---------|-------------|
| DAPR_HTTP_PORT | all | Dapr sidecar HTTP port (default: 3500) |
| PUBSUB_NAME | backend | Dapr Pub/Sub component name |
| BACKEND_URL | recurring-task-service | URL to call backend API for creating tasks |
