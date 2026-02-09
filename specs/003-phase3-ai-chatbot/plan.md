# Implementation Plan: Phase 3 AI-Powered Todo Chatbot

**Branch**: `003-phase3-ai-chatbot` | **Date**: 2026-01-26 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-phase3-ai-chatbot/spec.md`

## Summary

Add an AI-powered conversational interface to the existing Todo application using OpenAI's API with function calling. Users can manage tasks through natural language commands (add, view, update, delete, complete, search) via a chat UI. The chatbot integrates with the existing Phase 2 FastAPI backend REST API.

## Technical Context

**Language/Version**: TypeScript 5.x (frontend), Python 3.11 (backend API route)
**Primary Dependencies**: OpenAI API (GPT-4), Vercel AI SDK, existing Next.js frontend, existing FastAPI backend
**Storage**: Existing Neon PostgreSQL via Phase 2 backend (no new storage needed)
**Testing**: Jest for frontend, pytest for backend integration tests
**Target Platform**: Web browser (desktop/mobile responsive)
**Project Type**: Web application (extending existing Phase 2 frontend)
**Performance Goals**: Chatbot response within 3 seconds, task operations within 500ms
**Constraints**: OpenAI API rate limits, session-based context (no persistence)
**Scale/Scope**: Single user, conversation context per browser session

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Phased Evolution | ✅ PASS | Phase 3 follows completed Phase 2 |
| II. Test-First Development | ✅ PASS | Tests planned for chat components and API integration |
| III. Smallest Viable Change | ✅ PASS | Adds only chat interface, reuses Phase 2 backend |
| IV. Clean Interfaces | ✅ PASS | Chat API with clear input/output, function calling for tools |
| V. Observability First | ✅ PASS | Structured logging for chat interactions |
| VI. Security by Default | ✅ PASS | OpenAI API key via env vars, no new auth needed |

**Gate Status**: PASSED - Proceed to Phase 0 Research

## Project Structure

### Documentation (this feature)

```text
specs/003-phase3-ai-chatbot/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (chat API contract)
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
# Extending existing Phase 2 web application structure

backend/
├── src/
│   ├── api/
│   │   ├── tasks.py          # Existing task endpoints
│   │   └── chat.py           # NEW: Chat completion endpoint (optional proxy)
│   └── ...existing...

frontend/
├── src/
│   ├── app/
│   │   ├── page.tsx          # Existing task list page
│   │   └── chat/
│   │       └── page.tsx      # NEW: Chat interface page
│   ├── components/
│   │   ├── ...existing...
│   │   ├── ChatWindow.tsx    # NEW: Main chat container
│   │   ├── ChatMessage.tsx   # NEW: Individual message component
│   │   └── ChatInput.tsx     # NEW: User input component
│   ├── services/
│   │   ├── api.ts            # Existing API client
│   │   └── chat.ts           # NEW: Chat/AI service
│   ├── hooks/
│   │   └── useChat.ts        # NEW: Chat state management hook
│   └── types/
│       └── chat.ts           # NEW: Chat-related types
└── tests/
    └── chat/                 # NEW: Chat component tests
```

**Structure Decision**: Extend existing Phase 2 web application by adding a `/chat` route with dedicated chat components. The chat service calls OpenAI directly from the frontend (using Vercel AI SDK) and uses existing `api.ts` for task operations.

## Complexity Tracking

> No violations requiring justification. Design follows constitution principles.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | - | - |
