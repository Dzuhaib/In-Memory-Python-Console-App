# Data Model: Phase 3 AI-Powered Todo Chatbot

**Feature**: 003-phase3-ai-chatbot
**Date**: 2026-01-26

## Overview

Phase 3 primarily extends the UI layer and adds AI integration. It reuses the existing Task entity from Phase 2 and introduces new frontend-only types for chat functionality.

## Existing Entities (Phase 2 - No Changes)

### Task

The existing Task entity from Phase 2 remains unchanged. All task operations go through the existing FastAPI backend.

```typescript
// Already defined in frontend/src/types/task.ts
interface Task {
  id: number;
  title: string;
  completed: boolean;
  priority: 'high' | 'medium' | 'low';
  tags: string[];
  created_at: string;
  updated_at: string;
}
```

## New Entities (Frontend Only)

### ChatMessage

Represents a single message in the conversation.

```typescript
// frontend/src/types/chat.ts
interface ChatMessage {
  id: string;                    // Unique message ID (UUID)
  role: 'user' | 'assistant';    // Who sent the message
  content: string;               // Message text
  createdAt: Date;               // Timestamp
  toolInvocations?: ToolInvocation[]; // Actions taken (if any)
}
```

**Validation Rules**:
- `id`: Required, must be unique within session
- `role`: Required, must be 'user' or 'assistant'
- `content`: Required, 1-10000 characters
- `createdAt`: Required, valid timestamp

### ToolInvocation

Represents an AI tool/function call and its result.

```typescript
interface ToolInvocation {
  toolCallId: string;            // Unique call ID
  toolName: string;              // Function name (e.g., 'createTask')
  args: Record<string, unknown>; // Function arguments
  result?: unknown;              // Function result (after execution)
  state: 'pending' | 'result' | 'error'; // Execution state
}
```

**Validation Rules**:
- `toolName`: Must be one of: createTask, getTasks, getTask, updateTask, deleteTask, toggleComplete, addTag, removeTag
- `args`: Must match the schema for the given tool

### Conversation (Conceptual)

The conversation is managed by Vercel AI SDK's `useChat` hook and exists only in React state.

```typescript
// Conceptual - managed by useChat hook
interface Conversation {
  messages: ChatMessage[];       // Full message history
  input: string;                 // Current user input
  isLoading: boolean;            // AI is generating response
  error?: Error;                 // Last error (if any)
}
```

## Tool Schemas

These schemas define what the AI can do. They map to existing API operations.

### createTask

```typescript
interface CreateTaskArgs {
  title: string;                 // Task title (required)
  priority?: 'high' | 'medium' | 'low'; // Default: medium
  tags?: string[];               // Optional tags
}
```

### getTasks

```typescript
interface GetTasksArgs {
  search?: string;               // Keyword search
  status?: 'complete' | 'incomplete'; // Filter by status
  priority?: 'high' | 'medium' | 'low'; // Filter by priority
  tag?: string;                  // Filter by tag
  sort?: 'priority' | 'alpha' | 'id'; // Sort order
}
```

### getTask

```typescript
interface GetTaskArgs {
  taskId: number;                // Task ID to retrieve
}
```

### updateTask

```typescript
interface UpdateTaskArgs {
  taskId: number;                // Task ID to update
  title?: string;                // New title
  priority?: 'high' | 'medium' | 'low'; // New priority
}
```

### deleteTask

```typescript
interface DeleteTaskArgs {
  taskId: number;                // Task ID to delete
}
```

### toggleComplete

```typescript
interface ToggleCompleteArgs {
  taskId: number;                // Task ID to toggle
}
```

### addTag / removeTag

```typescript
interface TagOperationArgs {
  taskId: number;                // Task ID
  tag: string;                   // Tag to add/remove
}
```

## State Transitions

### Message States

```
User types → Input captured
           ↓
User submits → Message added (role: user)
             ↓
AI processing → isLoading: true
              ↓
Tool called → ToolInvocation added (state: pending)
            ↓
Tool executed → ToolInvocation updated (state: result/error)
              ↓
AI responds → Message added (role: assistant)
            ↓
Complete → isLoading: false
```

## Relationships

```
Conversation (1) ──contains──> (N) ChatMessage
ChatMessage (1) ──may have──> (N) ToolInvocation
ToolInvocation ──executes──> Task API (existing)
```

## No Database Changes

Phase 3 adds no new database tables. All chat state is ephemeral (browser session only). Task data continues to be managed by the Phase 2 backend.
