# Todo App Hackathon Requirements

![CI Pipeline](https://github.com/Dzuhaib/In-Memory-Python-Console-App/actions/workflows/ci.yml/badge.svg)
![Deploy Pipeline](https://github.com/Dzuhaib/In-Memory-Python-Console-App/actions/workflows/deploy.yml/badge.svg)

## Basic Level (Core Essentials)
These form the foundation - quick to build, essential for any MVP:
https://github.com/Dzuhaib/In-Memory-Python-Console-App.git
1. **Add Task** - Create new todo items
2. **Delete Task** - Remove tasks from the list
3. **Update Task** - Modify existing task details
4. **View Task List** - Display all tasks
5. **Mark as Complete** - Toggle task completion status

## Intermediate Level (Organization & Usability)
Add these to make the app feel polished and practical:

1. **Priorities & Tags/Categories** - Assign levels (high/medium/low) or labels (work/home)
2. **Search & Filter** - Search by keyword; filter by status, priority, or date
3. **Sort Tasks** - Reorder by due date, priority, or alphabetically

## Advanced Level (Intelligent Features)

1. **Recurring Tasks** - Auto-reschedule repeating tasks (e.g., "weekly meeting")

## Development Phases

### Phase 1: In-Memory Python Console App
- **Tech Stack**: Python, Claude Code, Spec-Kit Plus
- **Goal**: Basic functionality in a console environment
- **Status**: Current phase

### Phase 2: Full Stack Web Application
- **Tech Stack**: Next.js (frontend), FastAPI (backend), SQLModel (ORM), Neon DB (database)
- **Goal**: Web-based todo application with persistent storage

### Phase 3: AI-Powered Todo Chatbot
- **Tech Stack**: OpenAI ChatKit, Agents SDK, Official MCP SDK
- **Goal**: Natural language interface for todo management

### Phase 4: Local Kubernetes Deployment
- **Tech Stack**: Docker, Minikube, Helm, kubectl-ai, kagent
- **Goal**: Containerized deployment with Kubernetes orchestration

### Phase 5: Advanced Cloud Deployment
- **Tech Stack**: Kafka/Redpanda, Dapr, Kubernetes (Minikube + OKE/AKS/GKE), GitHub Actions CI/CD
- **Goal**: Event-driven microservices architecture with recurring tasks, due dates, reminders, Dapr integration, and production cloud deployment
- **Services**: Backend API, Frontend, 4 consumer microservices (audit, notification, recurring-task, websocket)
- **Architecture**: Dapr Pub/Sub (Kafka), Dapr Jobs API (reminders), Dapr Secrets (K8s), WebSocket real-time updates

## Bonus Features (Create when needed)

### Reusable Intelligence
- Create and use reusable intelligence via Claude Code subagents
- Create and use Cloud-Native blueprints via Agents Skills

### Multi-language Support
- Support Urdu in chatbot interface

### Voice Commands
- Add voice input for todo commands