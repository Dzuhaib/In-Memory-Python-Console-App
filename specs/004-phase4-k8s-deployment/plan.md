# Implementation Plan: Local Kubernetes Deployment

**Branch**: `004-phase4-k8s-deployment` | **Date**: 2026-01-28 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/004-phase4-k8s-deployment/spec.md`

## Summary

Containerize the existing Todo application (Next.js frontend and FastAPI backend with AI chatbot) using Docker, create Kubernetes manifests and Helm charts, and deploy to a local Minikube cluster. This enables consistent deployments and validates the infrastructure before cloud deployment in Phase 5.

## Technical Context

**Language/Version**: Python 3.11+ (backend), Node.js 20+ (frontend), YAML (manifests)
**Primary Dependencies**: Docker, Kubernetes (Minikube), Helm 3.x, kubectl
**Storage**: PostgreSQL via Neon DB (external), ConfigMaps/Secrets for config
**Testing**: Manual verification via kubectl, helm test hooks, health endpoints
**Target Platform**: Local Kubernetes (Minikube) on Linux/macOS/Windows
**Project Type**: Web application (frontend + backend + infra)
**Performance Goals**: Pods ready within 60 seconds, app accessible within 3 minutes of deployment
**Constraints**: Local development only, no external registry required, minimal resource usage for dev machines
**Scale/Scope**: 2 services (frontend, backend), single namespace, 1-3 replicas each

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Phased Evolution | PASS | Phase 4 follows completed Phase 3 (AI Chatbot) |
| II. Test-First Development | PASS | Health checks, Helm test hooks, manual verification scripts |
| III. Smallest Viable Change | PASS | Minimal manifests, no over-engineering |
| IV. Clean Interfaces | PASS | Services expose clear endpoints, ConfigMaps externalize config |
| V. Observability First | PASS | Health endpoints, liveness/readiness probes, structured logging |
| VI. Security by Default | PASS | Secrets for sensitive data, no hardcoded credentials |

## Project Structure

### Documentation (this feature)

```text
specs/004-phase4-k8s-deployment/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output (K8s resource model)
├── quickstart.md        # Phase 1 output (local setup guide)
├── contracts/           # Phase 1 output (Helm values schema)
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
# Existing application structure (from Phase 2/3)
backend/
├── src/
│   ├── models/
│   ├── services/
│   ├── api/
│   └── chatkit_server.py
├── tests/
├── pyproject.toml
└── Dockerfile              # NEW - Phase 4

frontend/
├── src/
│   ├── components/
│   ├── hooks/
│   └── services/
├── package.json
└── Dockerfile              # NEW - Phase 4

# NEW - Kubernetes infrastructure (Phase 4)
k8s/
├── base/                   # Raw Kubernetes manifests
│   ├── namespace.yaml
│   ├── backend/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   ├── configmap.yaml
│   │   └── secret.yaml
│   └── frontend/
│       ├── deployment.yaml
│       ├── service.yaml
│       └── configmap.yaml
└── charts/                 # Helm charts
    └── todo-app/
        ├── Chart.yaml
        ├── values.yaml
        ├── values-dev.yaml
        ├── templates/
        │   ├── _helpers.tpl
        │   ├── backend-deployment.yaml
        │   ├── backend-service.yaml
        │   ├── backend-configmap.yaml
        │   ├── backend-secret.yaml
        │   ├── frontend-deployment.yaml
        │   ├── frontend-service.yaml
        │   └── frontend-configmap.yaml
        └── tests/
            └── test-connection.yaml

docker-compose.yml          # NEW - Local multi-container development
```

**Structure Decision**: Web application structure with added infrastructure layer (k8s/). The existing backend/ and frontend/ directories gain Dockerfiles. New k8s/ directory contains both raw manifests (for kubectl) and Helm charts (for templated deployments).

## Complexity Tracking

No constitution violations - all complexity is justified by the Phase 4 requirements.
