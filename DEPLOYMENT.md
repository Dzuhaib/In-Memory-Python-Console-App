# Todo App Deployment Guide

This guide covers deploying the Todo App to local Kubernetes using Minikube.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Kubernetes Cluster                        │
│                    (Minikube / DOKS)                        │
│                                                              │
│  ┌─────────────────────┐      ┌─────────────────────┐       │
│  │  frontend-service   │      │  backend-service    │       │
│  │  (NodePort:30000)   │      │  (ClusterIP:8000)   │       │
│  └──────────┬──────────┘      └──────────┬──────────┘       │
│             │                            │                   │
│             ▼                            ▼                   │
│  ┌─────────────────────┐      ┌─────────────────────┐       │
│  │  todo-frontend      │─────▶│  todo-backend       │       │
│  │  (Next.js)          │ HTTP │  (FastAPI + OpenAI) │       │
│  └─────────────────────┘      └──────────┬──────────┘       │
│                                          │                   │
└──────────────────────────────────────────┼───────────────────┘
                                           │
                                           ▼
                                ┌─────────────────────┐
                                │  Neon PostgreSQL    │
                                │  (External)         │
                                └─────────────────────┘
```

## Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| Docker | 24.0+ | Container runtime |
| Minikube | 1.32+ | Local Kubernetes |
| kubectl | 1.28+ | Kubernetes CLI |
| Helm | 3.13+ | Package manager |

## Quick Start

### 1. Start Minikube

```bash
minikube start --memory=4096 --cpus=2
```

### 2. Build Images in Minikube

```bash
# Use Minikube's Docker daemon
eval $(minikube docker-env)  # Linux/macOS
# OR
minikube docker-env --shell powershell | Invoke-Expression  # Windows

# Build images
docker build -t todo-backend:local ./backend
docker build -t todo-frontend:local ./frontend
```

### 3. Deploy with kubectl

```bash
# Create namespace and secrets
kubectl apply -f k8s/base/namespace.yaml
kubectl create secret generic backend-secrets \
  --namespace todo-app \
  --from-literal=DATABASE_URL='your-db-url' \
  --from-literal=OPENAI_API_KEY='your-api-key'

# Deploy application
kubectl apply -f k8s/base/backend/
kubectl apply -f k8s/base/frontend/

# Access the app
minikube service frontend-service -n todo-app
```

### 4. Deploy with Helm (Alternative)

```bash
helm install todo-app ./k8s/charts/todo-app \
  --set backend.secrets.DATABASE_URL='your-db-url' \
  --set backend.secrets.OPENAI_API_KEY='your-api-key'
```

## Local Development with Docker Compose

For local development without Kubernetes:

```bash
# Copy environment file
cp .env.example .env
# Edit .env with your values

# Start services
docker-compose up --build

# Access
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

## Directory Structure

```
.
├── backend/
│   ├── Dockerfile          # Multi-stage Python build
│   └── src/                # FastAPI application
├── frontend/
│   ├── Dockerfile          # Multi-stage Node.js build
│   └── src/                # Next.js application
├── k8s/
│   ├── base/               # Raw Kubernetes manifests
│   │   ├── namespace.yaml
│   │   ├── backend/        # Backend resources
│   │   └── frontend/       # Frontend resources
│   └── charts/
│       └── todo-app/       # Helm chart
├── docker-compose.yml      # Local development
└── DEPLOYMENT.md           # This file
```

## Configuration

### Environment Variables

| Variable | Location | Description |
|----------|----------|-------------|
| DATABASE_URL | Secret | PostgreSQL connection string |
| OPENAI_API_KEY | Secret | OpenAI API key for chatbot |
| LOG_LEVEL | ConfigMap | Logging level (INFO/DEBUG) |
| CORS_ORIGINS | ConfigMap | Allowed CORS origins |
| NEXT_PUBLIC_API_URL | ConfigMap | Backend API URL |

### Resource Limits

| Component | Memory Request | Memory Limit | CPU Request | CPU Limit |
|-----------|----------------|--------------|-------------|-----------|
| Backend | 128Mi | 512Mi | 100m | 500m |
| Frontend | 128Mi | 512Mi | 100m | 500m |

## Operations

### View Logs

```bash
kubectl logs -l component=backend -n todo-app -f
kubectl logs -l component=frontend -n todo-app -f
```

### Scale

```bash
kubectl scale deployment todo-backend --replicas=3 -n todo-app
```

### Rolling Update

```bash
# Build new image
docker build -t todo-backend:v2 ./backend

# Update deployment
kubectl set image deployment/todo-backend backend=todo-backend:v2 -n todo-app
```

### Rollback

```bash
kubectl rollout undo deployment/todo-backend -n todo-app
# OR with Helm
helm rollback todo-app
```

## Troubleshooting

### Pods not starting

```bash
kubectl describe pod <pod-name> -n todo-app
kubectl get events -n todo-app --sort-by='.lastTimestamp'
```

### Image not found

Ensure you're using Minikube's Docker daemon:
```bash
eval $(minikube docker-env)
docker images | grep todo
```

### Health check failures

Check the health endpoints work:
```bash
kubectl exec -it <pod-name> -n todo-app -- curl http://localhost:8000/health
```

## Phase 5: Event-Driven Microservices Deployment

### Architecture (Phase 5)

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
│  │  Task API  │  Chat API  │  Event Publisher  │  Jobs Callback   │ │
│  └────────────┴────────────┴──────────────────┴───────────────────┘ │
└──────────────────────────────────────────────────────────────────────┘
                                    │
                    Kafka/Redpanda Topics
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
            ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
            │ task-events  │ │  reminders   │ │ task-updates  │
            └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
          ┌────────┴────────┐      │                │
          ▼                 ▼      ▼                ▼
  ┌───────────────┐ ┌───────────┐ ┌──────────────┐ ┌──────────────┐
  │ recurring-    │ │ audit-    │ │ notification-│ │ websocket-   │
  │ task-service  │ │ service   │ │ service      │ │ service      │
  └───────────────┘ └───────────┘ └──────────────┘ └──────────────┘
```

### Phase 5 Services

| Service | Port | Purpose |
|---------|------|---------|
| Backend (FastAPI) | 8000 | Task API + Event Publisher + Jobs Callback |
| Frontend (Next.js) | 3000 | Web UI + WebSocket client |
| audit-service | 8001 | Logs all task events as structured JSON |
| notification-service | 8002 | Processes reminders, forwards to WebSocket |
| recurring-task-service | 8003 | Spawns new task instances on completion |
| websocket-service | 8004 | Broadcasts real-time updates via WebSocket |
| Redpanda | 9092 | Kafka-compatible message broker |

### Phase 5 Minikube Deployment

```bash
# Start Minikube with sufficient resources
minikube start --memory=6144 --cpus=4

# Install Dapr on cluster
dapr init -k

# Use Minikube's Docker daemon
eval $(minikube docker-env)

# Build all images
docker build -t todo-backend:local ./backend
docker build -t todo-frontend:local ./frontend
docker build -t audit-service:local ./services/audit-service
docker build -t notification-service:local ./services/notification-service
docker build -t recurring-task-service:local ./services/recurring-task-service
docker build -t websocket-service:local ./services/websocket-service

# Deploy with Helm
helm install todo-app ./k8s/charts/todo-app \
  --set backend.secrets.DATABASE_URL='your-db-url' \
  --set backend.secrets.OPENAI_API_KEY='your-api-key'

# Verify all pods are running (expect 7+ pods: backend, frontend, 4 consumers, redpanda + Dapr sidecars)
kubectl get pods -n default

# Smoke test
minikube service frontend-service
```

### Phase 5 Cloud Deployment

```bash
# Deploy to cloud with production values
helm upgrade --install todo-app ./k8s/charts/todo-app \
  -f k8s/charts/todo-app/values-production.yaml

# Verify
kubectl get pods
kubectl get ingress
```

See `specs/006-phase5-advanced-cloud/cloud-deploy-guide.md` for comprehensive cloud deployment instructions.

### Phase 5 Environment Variables

| Variable | Location | Description |
|----------|----------|-------------|
| DATABASE_URL | Secret | PostgreSQL connection string |
| OPENAI_API_KEY | Secret | OpenAI API key for chatbot |
| DAPR_HTTP_PORT | Env | Dapr sidecar HTTP port (default: 3500) |
| PUBSUB_NAME | Env | Dapr Pub/Sub component name (default: kafka-pubsub) |
| KAFKA_BROKERS | Secret | Kafka/Redpanda broker address |

### CI/CD Pipeline

- **CI** (`.github/workflows/ci.yml`): Runs on push/PR — Python lint (ruff), TS lint (eslint), pytest, jest, Docker builds, Helm lint
- **Deploy** (`.github/workflows/deploy.yml`): Runs on push to main — builds/pushes images to GHCR, Helm deploys to cloud, rollback on failure
