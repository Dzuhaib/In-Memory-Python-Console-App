# Auth API Contracts

**Feature**: 005-clawlist-landing-auth
**Date**: 2026-02-08
**Base Path**: `/api/auth` (Next.js API route, handled by Better Auth)

All endpoints below are managed by Better Auth's built-in route handler. They are documented here for reference — no custom implementation is needed.

---

## POST /api/auth/sign-up/email

**Description**: Register a new user with email and password

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "name": "John Doe"
}
```

**Success Response** (200):
```json
{
  "user": {
    "id": "uuid-string",
    "email": "user@example.com",
    "name": "John Doe",
    "emailVerified": false,
    "createdAt": "2026-02-08T00:00:00.000Z",
    "updatedAt": "2026-02-08T00:00:00.000Z"
  },
  "session": {
    "id": "uuid-string",
    "token": "session-token",
    "expiresAt": "2026-02-15T00:00:00.000Z",
    "userId": "uuid-string"
  }
}
```

**Error Responses**:
- `400`: Invalid email format or password too short (< 8 chars)
- `422`: Email already registered

**Side Effects**: Sets `better-auth.session_token` HTTP-only cookie

---

## POST /api/auth/sign-in/email

**Description**: Authenticate an existing user

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "rememberMe": true
}
```

**Success Response** (200):
```json
{
  "user": { ... },
  "session": { ... }
}
```

**Error Responses**:
- `401`: Invalid credentials (generic message — does not reveal which field is wrong)

**Side Effects**: Sets `better-auth.session_token` HTTP-only cookie

---

## POST /api/auth/sign-out

**Description**: End the current session

**Request**: No body required (session identified by cookie)

**Success Response** (200):
```json
{
  "success": true
}
```

**Side Effects**: Clears session cookie, deletes session from database

---

## GET /api/auth/get-session

**Description**: Get the current user's session (used by `useSession` hook)

**Request**: No body (session identified by cookie)

**Success Response** (200):
```json
{
  "user": {
    "id": "uuid-string",
    "email": "user@example.com",
    "name": "John Doe"
  },
  "session": {
    "id": "uuid-string",
    "expiresAt": "2026-02-15T00:00:00.000Z"
  }
}
```

**No Session Response** (200):
```json
null
```

---

## Client-Side Usage

### Sign Up
```ts
const { data, error } = await authClient.signUp.email({
  email: "user@example.com",
  password: "securepassword123",
  name: "John Doe",
});
```

### Sign In
```ts
const { data, error } = await authClient.signIn.email({
  email: "user@example.com",
  password: "securepassword123",
});
```

### Sign Out
```ts
await authClient.signOut();
```

### Get Session (React Hook)
```ts
const { data: session, isPending, error } = authClient.useSession();
```

---

## Existing Task API (Unchanged)

The following endpoints remain unchanged. They are served by the FastAPI backend at `NEXT_PUBLIC_API_URL/api/v1/`.

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v1/tasks | List tasks with filters |
| POST | /api/v1/tasks | Create task |
| GET | /api/v1/tasks/{id} | Get task |
| PUT | /api/v1/tasks/{id} | Update task |
| DELETE | /api/v1/tasks/{id} | Delete task |
| PATCH | /api/v1/tasks/{id}/complete | Toggle complete |
| POST | /api/v1/tasks/{id}/tags | Add tag |
| DELETE | /api/v1/tasks/{id}/tags/{tag} | Remove tag |
| POST | /api/v1/chat | Chat with AI assistant |
| GET | /api/v1/health | Health check |

No authentication is added to these endpoints for MVP. Access is controlled at the frontend route level via middleware.
