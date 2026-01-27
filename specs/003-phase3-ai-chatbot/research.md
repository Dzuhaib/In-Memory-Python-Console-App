# Research: Phase 3 AI-Powered Todo Chatbot

**Feature**: 003-phase3-ai-chatbot
**Date**: 2026-01-26
**Purpose**: Resolve technical decisions for AI chatbot implementation

## Research Questions

### 1. OpenAI Integration Approach

**Question**: How should we integrate OpenAI for natural language understanding?

**Decision**: Use OpenAI Function Calling with Vercel AI SDK

**Rationale**:
- Function calling allows defining task operations as "tools" the AI can invoke
- Vercel AI SDK provides React hooks (`useChat`) that handle streaming, state, and tool execution
- Works directly from Next.js frontend with API routes for secure key handling
- No need for custom NLU parsing - OpenAI handles intent extraction

**Alternatives Considered**:
| Alternative | Rejected Because |
|-------------|------------------|
| Custom intent parsing | Complex, error-prone, requires training data |
| LangChain | Adds unnecessary abstraction, Vercel AI SDK is simpler |
| Direct OpenAI API calls | Vercel AI SDK handles streaming/state better |
| Backend-only AI | Adds latency, frontend streaming is better UX |

### 2. Architecture Pattern

**Question**: Where should the AI/chat logic live?

**Decision**: Hybrid - Next.js API route for OpenAI calls, frontend for state

**Rationale**:
- API route (`/api/chat`) keeps OpenAI key server-side (secure)
- Frontend `useChat` hook manages conversation state and streaming
- Task operations go directly to FastAPI backend via existing `api.ts`
- Clean separation: AI for NLU → Frontend for state → Backend for data

**Architecture Flow**:
```
User Input → Next.js API Route → OpenAI (function calling)
                                      ↓
                              Tool: createTask/getTasks/etc
                                      ↓
                              Frontend executes tool
                                      ↓
                              FastAPI Backend (existing)
                                      ↓
                              Result → OpenAI → Response → User
```

### 3. Function Definitions (Tools)

**Question**: What functions/tools should we expose to the AI?

**Decision**: 7 core functions mapping to existing API operations

| Function | Description | Parameters |
|----------|-------------|------------|
| `createTask` | Add a new task | title, priority?, tags? |
| `getTasks` | List tasks with filters | search?, status?, priority?, tag?, sort? |
| `getTask` | Get single task by ID | taskId |
| `updateTask` | Modify task | taskId, title?, priority? |
| `deleteTask` | Remove task | taskId |
| `toggleComplete` | Mark done/undone | taskId |
| `addTag` / `removeTag` | Manage tags | taskId, tag |

**Rationale**: Direct 1:1 mapping to existing FastAPI endpoints ensures consistency and reuses tested code.

### 4. Conversation Context

**Question**: How should conversation history be managed?

**Decision**: Client-side state with Vercel AI SDK's built-in history

**Rationale**:
- `useChat` hook maintains message history in React state
- History is automatically included in API calls for context
- Clears on page refresh (per spec: session-based, no persistence)
- Simple, no additional storage needed

### 5. UI Component Library

**Question**: Should we use a chat UI library or build custom?

**Decision**: Build minimal custom components with Tailwind CSS

**Rationale**:
- Only need 3 components: ChatWindow, ChatMessage, ChatInput
- Matches existing Phase 2 styling (Tailwind)
- Avoids dependency bloat
- Full control over UX

### 6. Error Handling Strategy

**Question**: How to handle AI/API errors gracefully?

**Decision**: Layered error handling with user-friendly messages

| Error Type | Handling |
|------------|----------|
| OpenAI API error | "I'm having trouble thinking. Try again." |
| Backend API error | "Couldn't reach task service. Try again." |
| Rate limit | "Too many requests. Wait a moment." |
| Invalid input | AI asks for clarification naturally |
| Network error | "Connection lost. Check your internet." |

### 7. MCP SDK Integration

**Question**: How does MCP SDK fit into the architecture?

**Decision**: MCP SDK provides the tool/function framework for Claude-compatible agents

**Rationale**:
- MCP (Model Context Protocol) standardizes how AI models interact with external tools
- For this phase, OpenAI function calling serves the same purpose
- MCP SDK can be added later for Claude integration or multi-model support
- Focus on OpenAI first for simplicity, architecture allows MCP addition

## Technology Stack Summary

| Component | Technology | Purpose |
|-----------|------------|---------|
| AI Provider | OpenAI GPT-4 | Natural language understanding |
| AI Integration | Vercel AI SDK | Streaming, hooks, tool execution |
| Frontend | Next.js + React | Chat UI, state management |
| Styling | Tailwind CSS | Consistent with Phase 2 |
| Backend | FastAPI (existing) | Task CRUD operations |
| Database | Neon PostgreSQL (existing) | Task persistence |

## Dependencies to Add

```json
// frontend/package.json
{
  "dependencies": {
    "ai": "^3.0.0",           // Vercel AI SDK
    "openai": "^4.0.0"        // OpenAI client
  }
}
```

## Environment Variables

```env
# frontend/.env.local
OPENAI_API_KEY=sk-...        # OpenAI API key (server-side only)
```

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| OpenAI API costs | Medium | Medium | Set usage limits, monitor |
| Rate limiting | Low | Medium | Implement backoff, user feedback |
| AI hallucinations | Medium | Low | Validate task IDs before operations |
| Slow responses | Low | Medium | Streaming UI shows progress |
