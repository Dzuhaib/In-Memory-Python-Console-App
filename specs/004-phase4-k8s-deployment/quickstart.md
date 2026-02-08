# Quickstart: Local Kubernetes Deployment

**Feature**: 004-phase4-k8s-deployment
**Date**: 2026-01-28

## Prerequisites

Before starting, ensure you have the following installed:

| Tool | Version | Installation |
|------|---------|--------------|
| Docker Desktop | 24.0+ | https://docs.docker.com/get-docker/ |
| Minikube | 1.32+ | https://minikube.sigs.k8s.io/docs/start/ |
| kubectl | 1.28+ | https://kubernetes.io/docs/tasks/tools/ |
| Helm | 3.13+ | https://helm.sh/docs/intro/install/ |

## Quick Start (5 minutes)

### 1. Start Minikube

```bash
# Start Minikube with sufficient resources
minikube start --memory=4096 --cpus=2

# Verify cluster is running
kubectl cluster-info
```

### 2. Configure Docker to use Minikube

```bash
# Point Docker CLI to Minikube's Docker daemon
# Linux/macOS:
eval $(minikube docker-env)

# Windows PowerShell:
minikube docker-env --shell powershell | Invoke-Expression

# Verify (should show Minikube's Docker info)
docker info | grep -i name
```

### 3. Build Container Images

```bash
# From repository root
cd "C:\specify\new_session phase i ii 2"

# Build backend image
docker build -t todo-backend:local ./backend

# Build frontend image
docker build -t todo-frontend:local ./frontend

# Verify images exist
docker images | grep todo
```

### 4. Create Secrets

```bash
# Create secrets from environment files
kubectl create secret generic backend-secrets \
  --from-env-file=backend/.env

# Or create manually
kubectl create secret generic backend-secrets \
  --from-literal=DATABASE_URL='your-neon-db-url' \
  --from-literal=OPENAI_API_KEY='your-openai-key'
```

### 5. Deploy with kubectl

```bash
# Apply base manifests
kubectl apply -f k8s/base/namespace.yaml
kubectl apply -f k8s/base/backend/
kubectl apply -f k8s/base/frontend/

# Check deployment status
kubectl get pods -n todo-app
kubectl get services -n todo-app
```

### 6. Access the Application

```bash
# Get the frontend URL
minikube service frontend-service -n todo-app --url

# Or use port-forward
kubectl port-forward svc/frontend-service 3000:3000 -n todo-app
```

Open http://localhost:3000 in your browser.

---

## Alternative: Deploy with Helm

```bash
# Install the Helm chart
helm install todo-app ./k8s/charts/todo-app \
  --set backend.secrets.DATABASE_URL="your-neon-db-url" \
  --set backend.secrets.OPENAI_API_KEY="your-openai-key"

# Check release status
helm status todo-app

# Upgrade with new values
helm upgrade todo-app ./k8s/charts/todo-app -f ./k8s/charts/todo-app/values-dev.yaml

# Uninstall
helm uninstall todo-app
```

---

## Useful Commands

### Viewing Logs

```bash
# Backend logs
kubectl logs -l component=backend -n todo-app -f

# Frontend logs
kubectl logs -l component=frontend -n todo-app -f

# All pods
kubectl logs -l app=todo-app -n todo-app -f
```

### Debugging

```bash
# Describe pod for events and status
kubectl describe pod <pod-name> -n todo-app

# Shell into a pod
kubectl exec -it <pod-name> -n todo-app -- /bin/sh

# Check service endpoints
kubectl get endpoints -n todo-app
```

### Scaling

```bash
# Scale backend to 3 replicas
kubectl scale deployment todo-backend --replicas=3 -n todo-app

# Or with Helm
helm upgrade todo-app ./k8s/charts/todo-app --set backend.replicas=3
```

### Cleanup

```bash
# Delete all resources
kubectl delete namespace todo-app

# Or with Helm
helm uninstall todo-app

# Stop Minikube
minikube stop
```

---

## Troubleshooting

### Pods not starting

1. Check pod events: `kubectl describe pod <pod-name> -n todo-app`
2. Check image exists: `docker images | grep todo`
3. Verify imagePullPolicy is `Never` for local images

### Database connection errors

1. Verify secret exists: `kubectl get secret backend-secrets -n todo-app`
2. Check DATABASE_URL format in secret
3. Ensure Neon DB allows connections from any IP

### Frontend can't reach backend

1. Verify backend service exists: `kubectl get svc backend-service -n todo-app`
2. Check backend pods are Ready: `kubectl get pods -n todo-app`
3. Test connectivity: `kubectl exec -it <frontend-pod> -- curl http://backend-service:8000/health`

### Health check failures

1. Increase initialDelaySeconds in deployment
2. Check container logs for startup errors
3. Verify health endpoints work locally before containerizing

---

## Environment Variables Reference

### Backend

| Variable | ConfigMap/Secret | Description |
|----------|------------------|-------------|
| LOG_LEVEL | ConfigMap | Logging level (INFO, DEBUG) |
| PORT | ConfigMap | Server port (8000) |
| HOST | ConfigMap | Bind address (0.0.0.0) |
| CORS_ORIGINS | ConfigMap | Allowed CORS origins |
| DATABASE_URL | Secret | PostgreSQL connection string |
| OPENAI_API_KEY | Secret | OpenAI API key |

### Frontend

| Variable | ConfigMap/Secret | Description |
|----------|------------------|-------------|
| NEXT_PUBLIC_API_URL | ConfigMap | Backend API URL |

---

## Creating Secrets

**IMPORTANT**: Never commit secrets to git. Use one of these methods:

### Method 1: kubectl create secret (Recommended)

```bash
# Create namespace first
kubectl apply -f k8s/base/namespace.yaml

# Create secret from literal values
kubectl create secret generic backend-secrets \
  --namespace todo-app \
  --from-literal=DATABASE_URL='postgresql://user:password@host:5432/dbname?sslmode=require' \
  --from-literal=OPENAI_API_KEY='sk-your-openai-api-key-here'
```

### Method 2: From environment file

```bash
# Create a .env file (not committed to git)
echo "DATABASE_URL=postgresql://user:password@host:5432/dbname?sslmode=require" > backend/.env.secrets
echo "OPENAI_API_KEY=sk-your-openai-api-key-here" >> backend/.env.secrets

# Create secret from env file
kubectl create secret generic backend-secrets \
  --namespace todo-app \
  --from-env-file=backend/.env.secrets

# Delete the temp file
rm backend/.env.secrets
```

### Method 3: With Helm values

```bash
helm install todo-app ./k8s/charts/todo-app \
  --set backend.secrets.DATABASE_URL="postgresql://user:password@host:5432/dbname?sslmode=require" \
  --set backend.secrets.OPENAI_API_KEY="sk-your-openai-api-key-here"
```

---

## Next Steps

After successful local deployment:

1. Validate all features work (todos, AI chatbot)
2. Test scaling and rolling updates
3. Proceed to Phase 5 (Cloud Deployment on DigitalOcean DOKS)
