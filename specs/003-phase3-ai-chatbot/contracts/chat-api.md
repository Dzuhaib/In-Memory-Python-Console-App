# Chat API Contract

**Feature**: 003-phase3-ai-chatbot
**Date**: 2026-01-26
**Type**: Next.js API Route (Server-side)

## Overview

The chat API route handles communication with OpenAI. It receives user messages, calls OpenAI with function definitions, and streams responses back to the client.

## Endpoint

### POST /api/chat

Process a chat message and stream the AI response.

**Request**:
```typescript
interface ChatRequest {
  messages: {
    role: 'user' | 'assistant';
    content: string;
  }[];
}
```

**Response**: Server-Sent Events (SSE) stream

The Vercel AI SDK handles the streaming format automatically. The stream includes:
- Text chunks as they're generated
- Tool calls when the AI wants to execute a function
- Tool results after execution

**Headers**:
```
Content-Type: text/event-stream
Cache-Control: no-cache
Connection: keep-alive
```

**Error Responses**:

| Status | Error | Description |
|--------|-------|-------------|
| 400 | `invalid_request` | Malformed request body |
| 401 | `unauthorized` | Missing or invalid API key |
| 429 | `rate_limited` | Too many requests |
| 500 | `internal_error` | Server error |

## Tool Definitions

These are the functions exposed to the AI:

### createTask

```json
{
  "name": "createTask",
  "description": "Create a new task with a title and optional priority and tags",
  "parameters": {
    "type": "object",
    "properties": {
      "title": {
        "type": "string",
        "description": "The task title/description"
      },
      "priority": {
        "type": "string",
        "enum": ["high", "medium", "low"],
        "description": "Task priority level"
      },
      "tags": {
        "type": "array",
        "items": { "type": "string" },
        "description": "Tags to categorize the task"
      }
    },
    "required": ["title"]
  }
}
```

### getTasks

```json
{
  "name": "getTasks",
  "description": "Get a list of tasks, optionally filtered by status, priority, tag, or search term",
  "parameters": {
    "type": "object",
    "properties": {
      "search": {
        "type": "string",
        "description": "Search term to filter tasks by title"
      },
      "status": {
        "type": "string",
        "enum": ["complete", "incomplete"],
        "description": "Filter by completion status"
      },
      "priority": {
        "type": "string",
        "enum": ["high", "medium", "low"],
        "description": "Filter by priority level"
      },
      "tag": {
        "type": "string",
        "description": "Filter by tag"
      },
      "sort": {
        "type": "string",
        "enum": ["priority", "alpha", "id"],
        "description": "Sort order"
      }
    }
  }
}
```

### getTask

```json
{
  "name": "getTask",
  "description": "Get a single task by its ID",
  "parameters": {
    "type": "object",
    "properties": {
      "taskId": {
        "type": "number",
        "description": "The task ID"
      }
    },
    "required": ["taskId"]
  }
}
```

### updateTask

```json
{
  "name": "updateTask",
  "description": "Update an existing task's title or priority",
  "parameters": {
    "type": "object",
    "properties": {
      "taskId": {
        "type": "number",
        "description": "The task ID to update"
      },
      "title": {
        "type": "string",
        "description": "New task title"
      },
      "priority": {
        "type": "string",
        "enum": ["high", "medium", "low"],
        "description": "New priority level"
      }
    },
    "required": ["taskId"]
  }
}
```

### deleteTask

```json
{
  "name": "deleteTask",
  "description": "Delete a task by its ID",
  "parameters": {
    "type": "object",
    "properties": {
      "taskId": {
        "type": "number",
        "description": "The task ID to delete"
      }
    },
    "required": ["taskId"]
  }
}
```

### toggleComplete

```json
{
  "name": "toggleComplete",
  "description": "Toggle a task's completion status (mark as done or undone)",
  "parameters": {
    "type": "object",
    "properties": {
      "taskId": {
        "type": "number",
        "description": "The task ID to toggle"
      }
    },
    "required": ["taskId"]
  }
}
```

### addTag

```json
{
  "name": "addTag",
  "description": "Add a tag to an existing task",
  "parameters": {
    "type": "object",
    "properties": {
      "taskId": {
        "type": "number",
        "description": "The task ID"
      },
      "tag": {
        "type": "string",
        "description": "The tag to add"
      }
    },
    "required": ["taskId", "tag"]
  }
}
```

### removeTag

```json
{
  "name": "removeTag",
  "description": "Remove a tag from an existing task",
  "parameters": {
    "type": "object",
    "properties": {
      "taskId": {
        "type": "number",
        "description": "The task ID"
      },
      "tag": {
        "type": "string",
        "description": "The tag to remove"
      }
    },
    "required": ["taskId", "tag"]
  }
}
```

## System Prompt

```text
You are a helpful todo assistant. You help users manage their tasks through natural conversation.

When users want to:
- Add tasks: Use createTask with the title, priority (if mentioned), and tags (if mentioned)
- View tasks: Use getTasks with appropriate filters based on what they ask for
- Complete tasks: Use toggleComplete with the task ID
- Delete tasks: Use deleteTask with the task ID
- Update tasks: Use updateTask with the task ID and changes
- Add/remove tags: Use addTag or removeTag

Always confirm what you did after completing an action. If a user's request is unclear, ask for clarification.

Format task lists nicely with:
- Task ID, title, and status (✓ for complete, ○ for incomplete)
- Priority indicator (🔴 high, 🟡 medium, 🟢 low)
- Tags in brackets [tag1, tag2]

Be friendly and helpful!
```

## Existing Backend API

The tool implementations call the existing Phase 2 FastAPI endpoints:

| Tool | Backend Endpoint | Method |
|------|------------------|--------|
| createTask | `/api/v1/tasks` | POST |
| getTasks | `/api/v1/tasks` | GET |
| getTask | `/api/v1/tasks/{id}` | GET |
| updateTask | `/api/v1/tasks/{id}` | PUT |
| deleteTask | `/api/v1/tasks/{id}` | DELETE |
| toggleComplete | `/api/v1/tasks/{id}/complete` | PATCH |
| addTag | `/api/v1/tasks/{id}/tags` | POST |
| removeTag | `/api/v1/tasks/{id}/tags/{tag}` | DELETE |
