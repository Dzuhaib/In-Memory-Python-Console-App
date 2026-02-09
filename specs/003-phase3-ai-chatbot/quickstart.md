# Quickstart: Phase 3 AI-Powered Todo Chatbot

**Feature**: 003-phase3-ai-chatbot
**Date**: 2026-01-26

## Prerequisites

1. Phase 2 backend running (FastAPI on port 8000)
2. Phase 2 frontend running (Next.js on port 3000)
3. OpenAI API key
4. Node.js 18+

## Setup

### 1. Install Dependencies

```bash
cd frontend
npm install ai openai
```

### 2. Configure Environment

```bash
# frontend/.env.local
OPENAI_API_KEY=sk-your-api-key-here
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

### 3. Start Development

```bash
# Terminal 1: Backend (if not already running)
cd backend
uvicorn src.main:app --reload

# Terminal 2: Frontend
cd frontend
npm run dev
```

### 4. Access Chat

Navigate to `http://localhost:3000/chat`

## Quick Test

1. Open chat page
2. Type: "Add a task to buy groceries with high priority"
3. See confirmation: "Created task: buy groceries (high priority)"
4. Type: "Show my tasks"
5. See formatted task list

## File Structure

```
frontend/
├── src/
│   ├── app/
│   │   └── chat/
│   │       └── page.tsx      # Chat page
│   │   └── api/
│   │       └── chat/
│   │           └── route.ts  # OpenAI API route
│   ├── components/
│   │   ├── ChatWindow.tsx
│   │   ├── ChatMessage.tsx
│   │   └── ChatInput.tsx
│   ├── services/
│   │   └── chat.ts
│   ├── hooks/
│   │   └── useChat.ts
│   └── types/
│       └── chat.ts
```

## Common Commands

| User Says | What Happens |
|-----------|--------------|
| "Add task buy milk" | Creates task with title "buy milk" |
| "Show my tasks" | Lists all tasks |
| "Show high priority tasks" | Lists filtered tasks |
| "Mark task 1 as done" | Toggles completion |
| "Delete task 2" | Removes task |
| "Help" | Shows available commands |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "API key not found" | Check OPENAI_API_KEY in .env.local |
| "Cannot reach backend" | Ensure FastAPI is running on port 8000 |
| "CORS error" | Check CORS settings in backend |
| "Rate limited" | Wait and try again, or check OpenAI usage |

## Next Steps

1. Run `/sp.tasks` to generate implementation tasks
2. Implement chat API route
3. Build chat components
4. Add tests
5. Deploy
