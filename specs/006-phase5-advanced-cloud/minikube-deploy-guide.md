# Minikube Deployment Guide - Phase 5 Todo App

This guide covers deployment verification tasks T080-T083 for the full event-driven todo application stack on Minikube.

## Prerequisites

Ensure the following tools are installed:

- **Minikube**: v1.30.0 or later
- **kubectl**: v1.27.0 or later
- **Dapr CLI**: v1.11.0 or later
- **Helm**: v3.12.0 or later
- **Docker**: v24.0.0 or later

### Version Verification

```bash
minikube version
kubectl version --client
dapr version
helm version
docker --version
```

## Step-by-Step Deployment

### Step 1: Start Minikube (if not already running)

```bash
# Start Minikube with sufficient resources for the full stack
minikube start --memory=4096 --cpus=2

# Verify Minikube is running
minikube status
kubectl cluster-info
```

### Step 2: T080 - Install Dapr on Minikube

```bash
# Initialize Dapr on Kubernetes cluster
dapr init -k

# Wait for Dapr system pods to be ready
kubectl wait --for=condition=ready pod -l app.kubernetes.io/part-of=dapr -n dapr-system --timeout=300s

# Verify Dapr installation
dapr status -k

# Expected output: 3 Dapr system components running (dapr-operator, dapr-placement, dapr-sidecar-injector)
kubectl get pods -n dapr-system
```

### Step 3: T081 - Build Docker Images in Minikube's Docker Environment

```bash
# Point Docker CLI to Minikube's Docker daemon
eval $(minikube docker-env)

# Build backend image
cd backend
docker build -t todo-backend:local .
cd ..

# Build frontend image
cd frontend
docker build -t todo-frontend:local .
cd ..

# Build notification-service image
cd services/notification-service
docker build -t notification-service:local .
cd ../..

# Build recurring-task-service image
cd services/recurring-task-service
docker build -t recurring-task-service:local .
cd ../..

# Build audit-service image
cd services/audit-service
docker build -t audit-service:local .
cd ../..

# Build websocket-service image
cd services/websocket-service
docker build -t websocket-service:local .
cd ../..

# Verify all images are built in Minikube's Docker
docker images | grep -E "(todo-backend|todo-frontend|notification-service|recurring-task-service|audit-service|websocket-service)"

# Expected: 6 images with 'local' tag
```

**CRITICAL**: All Helm deployment templates use `imagePullPolicy: Never`, which requires images to exist in Minikube's Docker daemon. Never skip this step.

### Step 4: T082 - Deploy Full Stack via Helm

#### Create Kubernetes Secrets

```bash
# Create secrets for backend (replace with your actual values)
kubectl create secret generic todo-backend-secrets \
  --from-literal=DATABASE_URL="postgresql://user:password@host:5432/dbname" \
  --from-literal=OPENAI_API_KEY="sk-your-openai-api-key" \
  --namespace=todo-app \
  --dry-run=client -o yaml | kubectl apply -f -
```

**Note**: For local testing, you may use a SQLite DATABASE_URL or run PostgreSQL in Minikube. Update the connection string accordingly.

#### Install the Helm Chart

```bash
# Install the full stack
helm install todo-app ./k8s/charts/todo-app --create-namespace --namespace todo-app

# Wait for all pods to reach Running status
kubectl wait --for=condition=ready pod --all -n todo-app --timeout=300s

# Check deployment status
kubectl get pods -n todo-app
```

**Expected Pods (7+ total)**:

- `todo-backend-*` (1 pod + Dapr sidecar)
- `todo-frontend-*` (1 pod + Dapr sidecar)
- `notification-service-*` (1 pod + Dapr sidecar)
- `recurring-task-service-*` (1 pod + Dapr sidecar)
- `audit-service-*` (1 pod + Dapr sidecar)
- `websocket-service-*` (1 pod + Dapr sidecar)
- `redpanda-0` (1 pod - StatefulSet)

#### Verify Dapr Sidecars

```bash
# List all Dapr-enabled apps
dapr list -k -n todo-app

# Expected output: 6 services with Dapr sidecars
# - todo-backend
# - todo-frontend
# - notification-service
# - recurring-task-service
# - audit-service
# - websocket-service
```

#### Verify Dapr Components

```bash
# Check Dapr components are registered
kubectl get components -n todo-app

# Expected components:
# - kafka-pubsub (pubsub.kafka)
# - statestore (state.postgresql)
# - kubernetes-secrets (secretstores.kubernetes)
```

### Step 5: T083 - Run Smoke Test

#### Access the Frontend

```bash
# Get frontend service URL
minikube service todo-frontend --namespace=todo-app --url

# Expected output: http://192.168.xx.xx:30000 (or similar)
# Open this URL in your browser
```

#### Create a Task via API

```bash
# Port-forward backend service
kubectl port-forward -n todo-app svc/backend-service 8000:8000 &

# Wait 2 seconds for port-forward to establish
sleep 2

# Create a test task
curl -X POST http://localhost:8000/api/v1/tasks \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "Minikube Smoke Test Task",
    "description": "E2E verification for Phase 5 deployment",
    "priority": "high"
  }'

# Expected: 201 Created with task JSON response including task_id
```

#### Verify Event Propagation in Audit Service

```bash
# Wait 5-10 seconds for event propagation through Kafka/Dapr
sleep 10

# Check audit-service logs for the task.created event
kubectl logs -n todo-app -l component=audit-service --tail=50

# Expected log entry (structured JSON):
# {
#   "event_type": "task.created",
#   "task_id": "<UUID>",
#   "timestamp": "<ISO-8601>",
#   "task_snapshot": {...}
# }
```

**Smoke Test Success Criteria**:
1. Task creation API returns 201 with valid task JSON
2. Audit-service logs show `task.created` event within 10 seconds
3. Event contains correct task_id and snapshot data

### Troubleshooting

#### ImagePullBackOff Errors

```bash
# If pods are in ImagePullBackOff, verify images are in Minikube's Docker daemon
eval $(minikube docker-env)
docker images | grep -E "(todo-backend|todo-frontend|notification-service|recurring-task-service|audit-service|websocket-service)"

# Rebuild any missing images (see Step 3)
```

#### Dapr Sidecar Not Injecting

```bash
# Verify Dapr is installed
dapr status -k

# Check pod annotations
kubectl describe pod <pod-name> -n todo-app | grep dapr.io

# Expected annotations:
# dapr.io/enabled: "true"
# dapr.io/app-id: "<service-name>"
# dapr.io/app-port: "<port>"
```

#### Redpanda Connectivity Issues

```bash
# Check Redpanda pod status
kubectl get pods -n todo-app -l component=redpanda

# Check Redpanda logs
kubectl logs -n todo-app redpanda-0 --tail=100

# Test Kafka connectivity from a pod
kubectl run -it --rm --restart=Never kafka-test --image=docker.redpanda.com/redpandadata/redpanda:v24.2.4 -n todo-app -- \
  rpk cluster info --brokers redpanda:9092
```

#### Pod CrashLoopBackOff

```bash
# Get pod details
kubectl describe pod <pod-name> -n todo-app

# Check logs
kubectl logs <pod-name> -c <container-name> -n todo-app --tail=100

# Common issues:
# - Missing DATABASE_URL or invalid connection string
# - Missing OPENAI_API_KEY
# - Redpanda not ready (wait for redpanda-0 to be Running first)
```

#### Events Not Appearing in Audit Service

```bash
# Verify kafka-pubsub component is registered
kubectl get component kafka-pubsub -n todo-app -o yaml

# Check backend pod can reach Dapr sidecar
kubectl exec -it <backend-pod> -c backend -n todo-app -- curl -v http://localhost:3500/v1.0/publish/kafka-pubsub/task-events

# Check audit-service subscription
kubectl logs -n todo-app -l component=audit-service | grep "subscribe"

# Verify Redpanda has topic created
kubectl exec -it redpanda-0 -n todo-app -- rpk topic list
```

## Service Access

### Frontend (UI)

```bash
minikube service todo-frontend --namespace=todo-app
```

### Backend API

```bash
kubectl port-forward -n todo-app svc/backend-service 8000:8000
# Access at http://localhost:8000/api/v1
```

### Redpanda Admin

```bash
kubectl port-forward -n todo-app svc/redpanda 8082:8082
# Access at http://localhost:8082
```

## Teardown

### Uninstall Helm Release

```bash
helm uninstall todo-app --namespace=todo-app
```

### Delete Namespace

```bash
kubectl delete namespace todo-app
```

### Uninstall Dapr (optional)

```bash
dapr uninstall -k
```

### Stop Minikube (optional)

```bash
minikube stop
```

### Delete Minikube Cluster (complete cleanup)

```bash
minikube delete
```

## Deployment Summary

### Architecture

```
            ┌─────────────────────────────────────────────────────────────┐
            │                     Minikube Cluster                        │
            │                                                              │
            │  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐ │
            │  │  Frontend   │      │   Backend   │      │  Redpanda   │ │
            │  │  (Next.js)  │─────▶│  (FastAPI)  │◀─────│  (Kafka)    │ │
            │  │  + Dapr     │      │  + Dapr     │      │             │ │
            │  └─────────────┘      └─────────────┘      └─────────────┘ │
            │                              │                               │
            │                              │ (publishes task events)       │
            │                              ▼                               │
            │                       kafka-pubsub                           │
            │                              │                               │
            │         ┌────────────────────┼────────────────────┐         │
            │         ▼                    ▼                    ▼          │
            │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
            │  │ Audit Service│  │ Notification │  │ Recurring    │       │
            │  │  + Dapr      │  │  Service     │  │ Task Service │       │
            │  └──────────────┘  │  + Dapr      │  │  + Dapr      │       │
            │                    └──────────────┘  └──────────────┘       │
            │         │                    │                               │
            │         └────────────────────┼───────────────────┐          │
            │                              ▼                    ▼          │
            │                       ┌──────────────┐   ┌──────────────┐   │
            │                       │  WebSocket   │   │   Backend    │   │
            │                       │   Service    │   │   (create    │   │
            │                       │   + Dapr     │   │   new task)  │   │
            │                       └──────────────┘   └──────────────┘   │
            └─────────────────────────────────────────────────────────────┘
            ```

### Resource Requirements

- **Memory**: 4GB minimum (Minikube + 7 pods + Dapr sidecars)
- **CPU**: 2 cores minimum
- **Disk**: 10GB minimum (Docker images + ephemeral storage)

### Ports

| Service                | Port | Type      | Access                          |
|------------------------|------|-----------|---------------------------------|
| Frontend               | 3000 | NodePort  | `minikube service todo-frontend`|
| Backend                | 8000 | ClusterIP | Port-forward                    |
| Notification Service   | 8002 | ClusterIP | Internal only                   |
| Recurring Task Service | 8003 | ClusterIP | Internal only                   |
| Audit Service          | 8001 | ClusterIP | Internal only                   |
| WebSocket Service      | 8004 | ClusterIP | Internal only                   |
| Redpanda (Kafka)       | 9092 | ClusterIP | Internal only                   |
| Redpanda (Admin)       | 8082 | ClusterIP | Port-forward                    |

## Next Steps

After successful Minikube deployment:

1. **Phase 9: Cloud Deployment** - Promote to production Kubernetes cluster (OKE/AKS/GKE)
2. **Phase 10: CI/CD Pipeline** - Automate build, test, and deployment
3. **Monitoring & Observability** - Add Prometheus, Grafana, Jaeger for distributed tracing
4. **Scaling** - Increase replicas for consumer services based on load
5. **Production Hardening** - Add resource quotas, network policies, pod security policies

## References

- [Dapr on Kubernetes](https://docs.dapr.io/operations/hosting/kubernetes/)
- [Redpanda Documentation](https://docs.redpanda.com/)
- [Helm Charts Best Practices](https://helm.sh/docs/chart_best_practices/)
- [Minikube Documentation](https://minikube.sigs.k8s.io/docs/)
