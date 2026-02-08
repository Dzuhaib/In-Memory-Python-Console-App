# Research: Local Kubernetes Deployment

**Feature**: 004-phase4-k8s-deployment
**Date**: 2026-01-28
**Status**: Complete

## Research Questions

### 1. Docker Best Practices for Next.js Applications

**Decision**: Multi-stage build with standalone output mode

**Rationale**:
- Multi-stage builds reduce final image size by separating build dependencies from runtime
- Next.js standalone output mode creates a minimal production server (~50MB vs full node_modules)
- Alpine-based Node image further reduces size

**Alternatives Considered**:
- Single-stage build: Larger images, includes dev dependencies
- nginx static export: Loses SSR capabilities and API routes

**Implementation**:
```dockerfile
# Stage 1: Install dependencies
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Stage 2: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# Stage 3: Production
FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public
EXPOSE 3000
CMD ["node", "server.js"]
```

---

### 2. Docker Best Practices for FastAPI Applications

**Decision**: Multi-stage build with uvicorn production server

**Rationale**:
- Python slim image reduces size vs full Python image
- pip install with --no-cache-dir reduces layer size
- Non-root user for security

**Alternatives Considered**:
- Full Python image: Larger, includes unnecessary tools
- gunicorn: More complex config, uvicorn sufficient for our scale

**Implementation**:
```dockerfile
FROM python:3.11-slim AS builder
WORKDIR /app
COPY pyproject.toml ./
RUN pip install --no-cache-dir build && python -m build

FROM python:3.11-slim AS runner
WORKDIR /app
RUN useradd -m appuser
COPY --from=builder /app/dist/*.whl ./
RUN pip install --no-cache-dir *.whl && rm *.whl
COPY src/ ./src/
USER appuser
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

### 3. Kubernetes Resource Configuration

**Decision**: Standard Deployment + Service pattern with ClusterIP for backend, LoadBalancer/NodePort for frontend

**Rationale**:
- Deployments provide declarative updates, rollback, and scaling
- ClusterIP for backend (internal only, accessed by frontend)
- NodePort for frontend (accessible outside cluster in Minikube)
- LoadBalancer would work but requires cloud provider or metallb

**Alternatives Considered**:
- StatefulSets: Not needed, our apps are stateless
- DaemonSets: Not applicable
- Ingress: Good for production, adds complexity for local dev

**Key Configuration**:
- Replica count: 1 for development, configurable via Helm values
- Resource requests: 128Mi memory, 100m CPU (minimal for local dev)
- Resource limits: 512Mi memory, 500m CPU
- Liveness probe: HTTP GET /health
- Readiness probe: HTTP GET /health

---

### 4. Kubernetes Health Probes Configuration

**Decision**: HTTP probes with conservative timeouts for local development

**Rationale**:
- Both services have /health endpoints (backend: /health and /api/v1/health)
- HTTP probes are simpler than TCP or exec probes
- Conservative timeouts (30s initial delay) allow for slow container starts on dev machines

**Configuration**:
```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3

readinessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 5
  timeoutSeconds: 3
  failureThreshold: 3
```

---

### 5. ConfigMaps and Secrets Strategy

**Decision**: Separate ConfigMaps for non-sensitive config, Secrets for API keys

**Rationale**:
- ConfigMaps for: API URLs, log levels, CORS origins
- Secrets for: DATABASE_URL, OPENAI_API_KEY
- Environment variables injected via envFrom
- Secrets created from .env files or kubectl create secret

**Environment Variables Mapping**:

| Service | ConfigMap | Secret |
|---------|-----------|--------|
| Backend | LOG_LEVEL, CORS_ORIGINS, PORT | DATABASE_URL, OPENAI_API_KEY |
| Frontend | NEXT_PUBLIC_API_URL | N/A |

---

### 6. Helm Chart Structure

**Decision**: Single chart with subcharts pattern (simplified to templates)

**Rationale**:
- Single chart manages both services together
- values.yaml provides environment-specific configuration
- Template helpers (_helpers.tpl) reduce duplication
- Test hooks verify deployment success

**Chart Structure**:
```
charts/todo-app/
├── Chart.yaml          # Chart metadata
├── values.yaml         # Default values
├── values-dev.yaml     # Development overrides
├── templates/
│   ├── _helpers.tpl    # Template helpers
│   ├── backend-*.yaml  # Backend resources
│   ├── frontend-*.yaml # Frontend resources
│   └── NOTES.txt       # Post-install instructions
└── tests/
    └── test-connection.yaml
```

---

### 7. Minikube Deployment Strategy

**Decision**: Use minikube docker-env to build images directly in Minikube's Docker

**Rationale**:
- Avoids need for external registry
- Images are immediately available to Kubernetes
- Faster iteration than pushing to registry

**Workflow**:
```bash
# Point Docker CLI to Minikube's Docker daemon
eval $(minikube docker-env)

# Build images
docker build -t todo-backend:local ./backend
docker build -t todo-frontend:local ./frontend

# Deploy with imagePullPolicy: Never
kubectl apply -f k8s/base/
# OR
helm install todo-app ./k8s/charts/todo-app
```

---

### 8. Service Discovery Pattern

**Decision**: Kubernetes DNS for inter-service communication

**Rationale**:
- Frontend connects to backend via service name: `http://backend-service:8000`
- Kubernetes DNS automatically resolves service names
- Environment variable NEXT_PUBLIC_API_URL set at build time for client-side calls

**Implementation Notes**:
- Backend service: `backend-service.default.svc.cluster.local` (or just `backend-service`)
- Frontend needs API URL at build time for SSR, runtime for client
- For client-side, frontend uses relative URLs or public endpoint

---

## Dependencies Summary

| Tool | Version | Purpose |
|------|---------|---------|
| Docker | 24.0+ | Container runtime |
| Minikube | 1.32+ | Local Kubernetes |
| kubectl | 1.28+ | Kubernetes CLI |
| Helm | 3.13+ | Package manager |

## Open Questions (Resolved)

1. **Image registry**: Resolved - use Minikube's Docker directly
2. **Database in cluster**: Resolved - continue using external Neon DB
3. **Ingress vs NodePort**: Resolved - NodePort for simplicity in local dev
4. **Secret management**: Resolved - kubectl create secret from .env files
