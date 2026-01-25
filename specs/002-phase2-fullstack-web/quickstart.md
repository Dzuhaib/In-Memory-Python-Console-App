# Quickstart: Phase 2 Full Stack Web Application

**Feature**: `002-phase2-fullstack-web`
**Date**: 2026-01-25

## Prerequisites

- Python 3.11+
- Node.js 18+ and npm
- Git
- Neon DB account (free tier: https://neon.tech)

## Setup Steps

### 1. Clone and Navigate

```bash
cd "C:\specify\new_session phase i ii 2"
git checkout 002-phase2-fullstack-web
```

### 2. Set Up Neon Database

1. Create a Neon account at https://neon.tech
2. Create a new project (e.g., "todo-app-phase2")
3. Copy the connection string from the dashboard
4. The connection string looks like:
   ```
   postgresql://username:password@ep-xxx.region.aws.neon.tech/neondb?sslmode=require
   ```

### 3. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env with your Neon DB connection string
# DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require
# CORS_ORIGINS=http://localhost:3000
# LOG_LEVEL=INFO
```

### 4. Initialize Database

```bash
# Run database migrations (creates tables)
python -c "from src.database import create_db_and_tables; create_db_and_tables()"
```

### 5. Start Backend Server

```bash
# Start FastAPI with uvicorn
uvicorn src.main:app --reload --port 8000

# Server runs at http://localhost:8000
# API docs at http://localhost:8000/docs
```

### 6. Frontend Setup (new terminal)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create .env.local file
cp .env.local.example .env.local

# The default API URL should work:
# NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

### 7. Start Frontend Server

```bash
# Start Next.js development server
npm run dev

# Server runs at http://localhost:3000
```

## Verification

### Check Backend Health

```bash
curl http://localhost:8000/api/v1/health
# Expected: {"status":"healthy","timestamp":"..."}
```

### Check API Docs

Open http://localhost:8000/docs in your browser to see Swagger UI.

### Test Task Creation (API)

```bash
# Create a task
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Buy groceries","priority":"high","tags":["shopping"]}'

# List tasks
curl http://localhost:8000/api/v1/tasks
```

### Test Web Interface

1. Open http://localhost:3000 in your browser
2. You should see the Todo App interface
3. Click "Add Task" to create a new task
4. Try completing, editing, and deleting tasks
5. Test search, filter, and sort functionality

## Common Issues

### CORS Errors

If you see CORS errors in the browser console:
- Ensure backend is running on port 8000
- Check that `CORS_ORIGINS` in backend `.env` includes `http://localhost:3000`

### Database Connection Failed

If database connection fails:
- Verify your Neon DB connection string is correct
- Ensure `?sslmode=require` is in the connection string
- Check that your Neon project is active (not suspended)

### Port Already in Use

If ports 3000 or 8000 are in use:
```bash
# Find process using port (Windows)
netstat -ano | findstr :8000
# Kill process
taskkill /PID <PID> /F

# Or use different ports:
uvicorn src.main:app --port 8001
npm run dev -- -p 3001
```

## Running Tests

### Backend Tests

```bash
cd backend
pytest
# With coverage
pytest --cov=src --cov-report=html
```

### Frontend Tests

```bash
cd frontend
# Unit tests
npm test
# E2E tests (requires both servers running)
npm run test:e2e
```

## Project Structure

```
backend/
├── src/
│   ├── main.py           # FastAPI entry point
│   ├── config.py         # Environment config
│   ├── database.py       # DB connection
│   ├── models/task.py    # SQLModel models
│   ├── schemas/task.py   # Pydantic schemas
│   ├── services/         # Business logic
│   └── api/tasks.py      # REST endpoints
└── tests/

frontend/
├── src/
│   ├── app/              # Next.js pages
│   ├── components/       # React components
│   ├── services/api.ts   # API client
│   └── hooks/            # Custom hooks
└── tests/
```

## Next Steps

After setup is complete:

1. Run `/sp.tasks` to generate implementation tasks
2. Follow TDD workflow: write tests first, then implement
3. Complete user stories in priority order (P1-P9)
