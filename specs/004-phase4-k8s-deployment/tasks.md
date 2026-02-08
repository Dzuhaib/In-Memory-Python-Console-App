# Tasks: Local Kubernetes Deployment

**Input**: Design documents from `/specs/004-phase4-k8s-deployment/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Manual verification via kubectl commands, health endpoints, and Helm test hooks.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/` (FastAPI Python application)
- **Frontend**: `frontend/` (Next.js TypeScript application)
- **Kubernetes**: `k8s/base/` (raw manifests), `k8s/charts/` (Helm charts)
- **Root**: `docker-compose.yml`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and directory structure for Kubernetes deployment

- [x] T001 Create k8s directory structure: k8s/base/backend/, k8s/base/frontend/, k8s/charts/todo-app/templates/, k8s/charts/todo-app/tests/
- [x] T002 [P] Create .dockerignore file in backend/.dockerignore
- [x] T003 [P] Create .dockerignore file in frontend/.dockerignore
- [x] T004 Update .gitignore to exclude k8s secrets and local values

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Create backend Dockerfile with multi-stage build in backend/Dockerfile
- [x] T006 [P] Create frontend Dockerfile with Next.js standalone output in frontend/Dockerfile
- [ ] T007 Verify backend Dockerfile builds successfully: `docker build -t todo-backend:local ./backend`
- [ ] T008 [P] Verify frontend Dockerfile builds successfully: `docker build -t todo-frontend:local ./frontend`

**Checkpoint**: Docker images build successfully - containerization foundation ready

---

## Phase 3: User Story 1 - Container Build and Local Run (Priority: P1)

**Goal**: Run the entire application stack locally using Docker Compose

**Independent Test**: Run `docker-compose up` and verify todo application works end-to-end at localhost:3000

### Implementation for User Story 1

- [x] T009 [US1] Create docker-compose.yml with backend and frontend services at repository root
- [x] T010 [US1] Configure environment variables in docker-compose.yml for backend (DATABASE_URL, OPENAI_API_KEY)
- [x] T011 [US1] Configure environment variables in docker-compose.yml for frontend (NEXT_PUBLIC_API_URL)
- [x] T012 [US1] Add health check configuration to docker-compose.yml services
- [ ] T013 [US1] Test docker-compose up and verify frontend accessible at localhost:3000
- [ ] T014 [US1] Test todo creation via UI and verify persistence with external Neon DB
- [ ] T015 [US1] Test AI chatbot functionality via docker-compose deployment

**Checkpoint**: User Story 1 complete - application runs locally via docker-compose

---

## Phase 4: User Story 2 - Kubernetes Deployment on Minikube (Priority: P1)

**Goal**: Deploy containerized applications to local Minikube cluster using raw manifests

**Independent Test**: Run `kubectl apply -f k8s/base/` and access application via Minikube service URL

### Implementation for User Story 2

- [x] T016 [US2] Create namespace manifest in k8s/base/namespace.yaml
- [x] T017 [P] [US2] Create backend Deployment manifest in k8s/base/backend/deployment.yaml
- [x] T018 [P] [US2] Create backend Service manifest in k8s/base/backend/service.yaml
- [x] T019 [P] [US2] Create frontend Deployment manifest in k8s/base/frontend/deployment.yaml
- [x] T020 [P] [US2] Create frontend Service manifest (NodePort) in k8s/base/frontend/service.yaml
- [x] T021 [US2] Add imagePullPolicy: Never to deployments for local Minikube images
- [ ] T022 [US2] Test kubectl apply and verify all pods reach Running state
- [ ] T023 [US2] Test application access via minikube service command

**Checkpoint**: User Story 2 complete - application deploys to Minikube via kubectl

---

## Phase 5: User Story 3 - Helm Chart Deployment (Priority: P2)

**Goal**: Deploy application using Helm charts with configurable values

**Independent Test**: Run `helm install todo-app ./k8s/charts/todo-app` and verify deployment succeeds

### Implementation for User Story 3

- [x] T024 [US3] Create Chart.yaml with metadata in k8s/charts/todo-app/Chart.yaml
- [x] T025 [US3] Create values.yaml with default configuration in k8s/charts/todo-app/values.yaml
- [x] T026 [US3] Create _helpers.tpl with template helpers in k8s/charts/todo-app/templates/_helpers.tpl
- [x] T027 [P] [US3] Create backend deployment template in k8s/charts/todo-app/templates/backend-deployment.yaml
- [x] T028 [P] [US3] Create backend service template in k8s/charts/todo-app/templates/backend-service.yaml
- [x] T029 [P] [US3] Create frontend deployment template in k8s/charts/todo-app/templates/frontend-deployment.yaml
- [x] T030 [P] [US3] Create frontend service template in k8s/charts/todo-app/templates/frontend-service.yaml
- [x] T031 [US3] Create NOTES.txt with post-install instructions in k8s/charts/todo-app/templates/NOTES.txt
- [x] T032 [US3] Create values-dev.yaml with development overrides in k8s/charts/todo-app/values-dev.yaml
- [ ] T033 [US3] Test helm install and verify application deploys successfully
- [ ] T034 [US3] Test helm upgrade with modified replica count and verify changes apply
- [ ] T035 [US3] Test helm rollback and verify application reverts correctly

**Checkpoint**: User Story 3 complete - application deploys via Helm with configurable values

---

## Phase 6: User Story 4 - Service Discovery and Communication (Priority: P2)

**Goal**: Frontend and backend services discover each other via Kubernetes DNS

**Independent Test**: Verify frontend calls backend using service DNS name (backend-service:8000)

### Implementation for User Story 4

- [x] T036 [US4] Update frontend ConfigMap to use Kubernetes DNS URL for backend in k8s/base/frontend/configmap.yaml
- [x] T037 [US4] Update frontend deployment to use ConfigMap environment in k8s/base/frontend/deployment.yaml
- [x] T038 [US4] Update Helm frontend template to use service discovery URL in k8s/charts/todo-app/templates/frontend-configmap.yaml
- [ ] T039 [US4] Test service discovery by deploying and verifying frontend-to-backend communication
- [ ] T040 [US4] Test backend pod restart and verify frontend reconnects automatically
- [ ] T041 [US4] Test scaling backend to 2 replicas and verify load balancing

**Checkpoint**: User Story 4 complete - services communicate via Kubernetes DNS

---

## Phase 7: User Story 5 - Environment Configuration Management (Priority: P2)

**Goal**: Manage configuration via ConfigMaps and Secrets

**Independent Test**: Deploy with ConfigMaps/Secrets and verify application uses correct values

### Implementation for User Story 5

- [x] T042 [US5] Create backend ConfigMap manifest in k8s/base/backend/configmap.yaml
- [x] T043 [US5] Create backend Secret template manifest in k8s/base/backend/secret.yaml
- [x] T044 [US5] Update backend deployment to use envFrom for ConfigMap and Secret in k8s/base/backend/deployment.yaml
- [x] T045 [P] [US5] Create Helm backend ConfigMap template in k8s/charts/todo-app/templates/backend-configmap.yaml
- [x] T046 [P] [US5] Create Helm backend Secret template in k8s/charts/todo-app/templates/backend-secret.yaml
- [ ] T047 [US5] Document secret creation command in quickstart.md
- [ ] T048 [US5] Test ConfigMap configuration by verifying LOG_LEVEL is read from ConfigMap
- [ ] T049 [US5] Test Secret configuration by verifying database and API key are read from Secret
- [ ] T050 [US5] Test ConfigMap update by changing value and restarting pods

**Checkpoint**: User Story 5 complete - configuration externalized via ConfigMaps and Secrets

---

## Phase 8: User Story 6 - Health Checks and Resource Management (Priority: P3)

**Goal**: Kubernetes monitors health and manages resources efficiently

**Independent Test**: Kill application process in pod and verify Kubernetes restarts it within 60 seconds

### Implementation for User Story 6

- [x] T051 [US6] Add liveness probe to backend deployment in k8s/base/backend/deployment.yaml
- [x] T052 [US6] Add readiness probe to backend deployment in k8s/base/backend/deployment.yaml
- [x] T053 [P] [US6] Add liveness probe to frontend deployment in k8s/base/frontend/deployment.yaml
- [x] T054 [P] [US6] Add readiness probe to frontend deployment in k8s/base/frontend/deployment.yaml
- [x] T055 [US6] Add resource requests and limits to backend deployment
- [x] T056 [P] [US6] Add resource requests and limits to frontend deployment
- [x] T057 [US6] Update Helm templates with probe and resource configurations
- [x] T058 [US6] Create Helm test connection job in k8s/charts/todo-app/tests/test-connection.yaml
- [ ] T059 [US6] Test liveness probe by killing backend process and verifying pod restart
- [ ] T060 [US6] Test readiness probe by checking pod receives traffic only after ready
- [ ] T061 [US6] Run helm test to verify deployment connectivity

**Checkpoint**: User Story 6 complete - health monitoring and resource management operational

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Documentation and final validation

- [x] T062 [P] Update quickstart.md with complete deployment instructions
- [x] T063 [P] Create DEPLOYMENT.md in repository root with full deployment guide
- [ ] T064 Run full deployment test: build images → kubectl apply → verify app
- [ ] T065 Run full Helm deployment test: build images → helm install → verify app
- [ ] T066 Validate all success criteria from spec.md are met
- [ ] T067 Clean up any temporary test resources

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational (Dockerfiles)
- **User Story 2 (Phase 4)**: Depends on User Story 1 (working containers)
- **User Story 3 (Phase 5)**: Depends on User Story 2 (working K8s manifests)
- **User Story 4-6 (Phase 6-8)**: Can proceed after User Story 2, independent of each other
- **Polish (Phase 9)**: Depends on all desired user stories being complete

### User Story Dependencies

```
Phase 1: Setup
    ↓
Phase 2: Foundational (Dockerfiles)
    ↓
Phase 3: US1 - Docker Compose
    ↓
Phase 4: US2 - Kubernetes Manifests ←────────────────┐
    ↓                                                 │
Phase 5: US3 - Helm Charts                           │
    ↓                                                 │
┌───┴───────────────┬────────────────┐               │
↓                   ↓                ↓               │
US4: Service        US5: Config      US6: Health     │
Discovery           Management       Checks          │
(independent)       (independent)    (independent)   │
└───────────────────┴────────────────┘               │
    ↓                                                 │
Phase 9: Polish ──────────────────────────────────────┘
```

### Parallel Opportunities

**Within Phase 1 (Setup)**:
- T002, T003 can run in parallel (different .dockerignore files)

**Within Phase 2 (Foundational)**:
- T006 (frontend Dockerfile) can run parallel to T005 (backend Dockerfile)
- T007, T008 can run in parallel (build verification)

**Within Phase 4 (US2)**:
- T017, T018, T019, T020 can all run in parallel (different manifest files)

**Within Phase 5 (US3)**:
- T027, T028, T029, T030 can all run in parallel (different template files)

**Within Phase 7 (US5)**:
- T045, T046 can run in parallel (different Helm templates)

**Within Phase 8 (US6)**:
- T053, T054 can run in parallel (frontend probes)
- T056 can run parallel to T055 (different deployments)

**Cross-Story Parallelism** (after US2 complete):
- US4, US5, US6 can proceed in parallel (independent concerns)

---

## Parallel Example: User Story 2

```bash
# Launch all K8s manifests in parallel:
Task: "Create backend Deployment manifest in k8s/base/backend/deployment.yaml"
Task: "Create backend Service manifest in k8s/base/backend/service.yaml"
Task: "Create frontend Deployment manifest in k8s/base/frontend/deployment.yaml"
Task: "Create frontend Service manifest in k8s/base/frontend/service.yaml"
```

---

## Implementation Strategy

### MVP First (User Story 1 + 2)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (Dockerfiles)
3. Complete Phase 3: User Story 1 (docker-compose works)
4. Complete Phase 4: User Story 2 (kubectl apply works)
5. **STOP and VALIDATE**: Application runs on Minikube
6. Deploy/demo if ready

### Incremental Delivery

1. Setup + Foundational → Dockerfiles ready
2. Add User Story 1 → Test docker-compose → Demo (containers work!)
3. Add User Story 2 → Test kubectl → Demo (K8s works!)
4. Add User Story 3 → Test helm → Demo (Helm works!)
5. Add User Stories 4-6 → Polish deployment → Full Phase 4 complete
6. Each story adds infrastructure capability independently

### Suggested MVP Scope

**Minimum Viable Deployment**: User Stories 1 + 2
- Dockerfiles that build successfully
- docker-compose for local development
- Basic Kubernetes manifests for Minikube
- Application accessible via NodePort

This provides a working local K8s deployment foundation for Phase 5.

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Use `minikube docker-env` to build images directly in Minikube's Docker
- All secrets should be created via kubectl create secret, not committed to repo
- Test health endpoints before adding probes to avoid restart loops
