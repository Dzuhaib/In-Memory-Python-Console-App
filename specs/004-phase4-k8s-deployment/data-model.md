# Data Model: Kubernetes Resources

**Feature**: 004-phase4-k8s-deployment
**Date**: 2026-01-28

## Overview

This document defines the Kubernetes resources for deploying the Todo application. The model follows Kubernetes resource patterns and defines relationships between Deployments, Services, ConfigMaps, and Secrets.

## Resource Hierarchy

```
Namespace: todo-app
├── Backend
│   ├── Deployment (todo-backend)
│   ├── Service (backend-service)
│   ├── ConfigMap (backend-config)
│   └── Secret (backend-secrets)
└── Frontend
    ├── Deployment (todo-frontend)
    ├── Service (frontend-service)
    └── ConfigMap (frontend-config)
```

## Resource Definitions

### Namespace

| Field | Value | Description |
|-------|-------|-------------|
| name | todo-app | Isolates all Todo app resources |
| labels.app | todo-app | Common label for all resources |

---

### Backend Deployment

| Field | Value | Description |
|-------|-------|-------------|
| name | todo-backend | Deployment identifier |
| replicas | 1 (dev) / 2-3 (prod) | Number of pod instances |
| image | todo-backend:local | Container image |
| port | 8000 | Container port |
| envFrom | backend-config, backend-secrets | Environment sources |

**Pod Template Labels**:
- app: todo-app
- component: backend
- tier: api

**Probes**:
| Probe | Path | Port | Initial Delay | Period |
|-------|------|------|---------------|--------|
| liveness | /health | 8000 | 30s | 10s |
| readiness | /health | 8000 | 10s | 5s |

**Resources**:
| Type | Memory | CPU |
|------|--------|-----|
| requests | 128Mi | 100m |
| limits | 512Mi | 500m |

---

### Backend Service

| Field | Value | Description |
|-------|-------|-------------|
| name | backend-service | Service identifier |
| type | ClusterIP | Internal-only access |
| port | 8000 | Service port |
| targetPort | 8000 | Container port |
| selector | component: backend | Pod selector |

---

### Backend ConfigMap

| Key | Example Value | Description |
|-----|---------------|-------------|
| LOG_LEVEL | INFO | Logging verbosity |
| PORT | 8000 | Server port |
| HOST | 0.0.0.0 | Bind address |
| CORS_ORIGINS | http://frontend-service:3000 | Allowed origins |

---

### Backend Secret

| Key | Source | Description |
|-----|--------|-------------|
| DATABASE_URL | .env file | PostgreSQL connection string |
| OPENAI_API_KEY | .env file | OpenAI API key for chatbot |

**Note**: Secrets are base64 encoded when stored in Kubernetes.

---

### Frontend Deployment

| Field | Value | Description |
|-------|-------|-------------|
| name | todo-frontend | Deployment identifier |
| replicas | 1 (dev) / 2-3 (prod) | Number of pod instances |
| image | todo-frontend:local | Container image |
| port | 3000 | Container port |
| envFrom | frontend-config | Environment sources |

**Pod Template Labels**:
- app: todo-app
- component: frontend
- tier: web

**Probes**:
| Probe | Path | Port | Initial Delay | Period |
|-------|------|------|---------------|--------|
| liveness | / | 3000 | 30s | 10s |
| readiness | / | 3000 | 10s | 5s |

**Resources**:
| Type | Memory | CPU |
|------|--------|-----|
| requests | 128Mi | 100m |
| limits | 512Mi | 500m |

---

### Frontend Service

| Field | Value | Description |
|-------|-------|-------------|
| name | frontend-service | Service identifier |
| type | NodePort | External access via Minikube |
| port | 3000 | Service port |
| targetPort | 3000 | Container port |
| nodePort | 30000 (optional) | Fixed external port |
| selector | component: frontend | Pod selector |

---

### Frontend ConfigMap

| Key | Example Value | Description |
|-----|---------------|-------------|
| NEXT_PUBLIC_API_URL | http://backend-service:8000/api/v1 | Backend API URL (internal) |

**Note**: NEXT_PUBLIC_* variables are embedded at build time for client-side use.

---

## Helm Values Schema

The Helm chart uses a values.yaml file with the following structure:

```yaml
# Global settings
namespace: todo-app
environment: development

# Backend configuration
backend:
  name: todo-backend
  replicas: 1
  image:
    repository: todo-backend
    tag: local
    pullPolicy: Never  # For local Minikube
  service:
    type: ClusterIP
    port: 8000
  resources:
    requests:
      memory: "128Mi"
      cpu: "100m"
    limits:
      memory: "512Mi"
      cpu: "500m"
  config:
    LOG_LEVEL: INFO
    PORT: "8000"
    HOST: "0.0.0.0"
  # secrets provided via --set or external secret management

# Frontend configuration
frontend:
  name: todo-frontend
  replicas: 1
  image:
    repository: todo-frontend
    tag: local
    pullPolicy: Never
  service:
    type: NodePort
    port: 3000
    nodePort: 30000
  resources:
    requests:
      memory: "128Mi"
      cpu: "100m"
    limits:
      memory: "512Mi"
      cpu: "500m"
  config:
    NEXT_PUBLIC_API_URL: "http://backend-service:8000/api/v1"
```

---

## Resource Relationships

```
┌─────────────────────────────────────────────────────────────┐
│                    Namespace: todo-app                       │
│                                                              │
│  ┌─────────────────────┐      ┌─────────────────────┐       │
│  │  frontend-service   │      │  backend-service    │       │
│  │  (NodePort:30000)   │      │  (ClusterIP:8000)   │       │
│  └──────────┬──────────┘      └──────────┬──────────┘       │
│             │                            │                   │
│             ▼                            ▼                   │
│  ┌─────────────────────┐      ┌─────────────────────┐       │
│  │  todo-frontend      │─────▶│  todo-backend       │       │
│  │  Deployment         │ HTTP │  Deployment         │       │
│  │  (replicas: 1)      │      │  (replicas: 1)      │       │
│  └──────────┬──────────┘      └──────────┬──────────┘       │
│             │                            │                   │
│             ▼                            ▼                   │
│  ┌─────────────────────┐      ┌─────────────────────┐       │
│  │  frontend-config    │      │  backend-config     │       │
│  │  (ConfigMap)        │      │  (ConfigMap)        │       │
│  └─────────────────────┘      └──────────┬──────────┘       │
│                                          │                   │
│                               ┌──────────▼──────────┐       │
│                               │  backend-secrets    │       │
│                               │  (Secret)           │       │
│                               └─────────────────────┘       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                                          │
                                          ▼
                               ┌─────────────────────┐
                               │  External: Neon DB  │
                               │  (PostgreSQL)       │
                               └─────────────────────┘
```

---

## Labels and Selectors

All resources use consistent labeling:

| Label | Purpose | Values |
|-------|---------|--------|
| app | Application identifier | todo-app |
| component | Service identifier | frontend, backend |
| tier | Architecture layer | web, api |
| environment | Deployment environment | development, staging, production |
| version | Release version | v1.0.0, local |

**Selector Pattern**:
```yaml
selector:
  matchLabels:
    app: todo-app
    component: <component-name>
```
