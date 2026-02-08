# Data Model: ClawList Landing Page & Authentication

**Feature**: 005-clawlist-landing-auth
**Date**: 2026-02-08

## Entities

### User (managed by Better Auth)

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | string (UUID) | PK, auto-generated | Better Auth generates this |
| name | string | nullable | Display name (optional for email/password) |
| email | string | unique, not null | Primary identifier for login |
| emailVerified | boolean | default false | Email verification status |
| image | string | nullable | Profile image URL (unused for MVP) |
| createdAt | timestamp | auto-generated | Account creation time |
| updatedAt | timestamp | auto-updated | Last modification time |

### Session (managed by Better Auth)

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | string (UUID) | PK, auto-generated | |
| expiresAt | timestamp | not null | Session expiry (default 7 days) |
| token | string | unique, not null | Session token stored in cookie |
| createdAt | timestamp | auto-generated | |
| updatedAt | timestamp | auto-updated | |
| ipAddress | string | nullable | Client IP for security audit |
| userAgent | string | nullable | Browser user agent |
| userId | string | FK → user.id | Owner of the session |

### Account (managed by Better Auth)

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | string (UUID) | PK, auto-generated | |
| accountId | string | not null | Provider-specific account ID |
| providerId | string | not null | "credential" for email/password |
| userId | string | FK → user.id | |
| password | string | nullable | Hashed password (bcrypt) |
| accessToken | string | nullable | Not used for credential auth |
| refreshToken | string | nullable | Not used for credential auth |
| createdAt | timestamp | auto-generated | |
| updatedAt | timestamp | auto-updated | |

### Verification (managed by Better Auth)

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | string (UUID) | PK, auto-generated | |
| identifier | string | not null | What is being verified (email) |
| value | string | not null | Verification token |
| expiresAt | timestamp | not null | Token expiry |
| createdAt | timestamp | auto-generated | |
| updatedAt | timestamp | auto-updated | |

### Task (existing — no changes)

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | integer | PK, auto-increment | Existing field |
| title | string | not null | Existing field |
| completed | boolean | default false | Existing field |
| priority | enum (high/medium/low) | default medium | Existing field |
| tags | JSON array | default [] | Existing field |
| created_at | timestamp | auto-generated | Existing field |
| updated_at | timestamp | auto-updated | Existing field |

## Relationships

```
User 1 ──── * Session     (one user has many sessions)
User 1 ──── * Account     (one user has many auth providers)
User 1 ──── * Verification (one user has many verification tokens)

Task (no relationship to User for MVP — tasks are global)
```

## State Transitions

### User Authentication Flow

```
Visitor ──[register]──→ Registered User ──[auto-login]──→ Authenticated User
Visitor ──[login]──→ Authenticated User
Authenticated User ──[logout]──→ Visitor
Authenticated User ──[session expires]──→ Visitor
```

### Session Lifecycle

```
Created ──[valid token + not expired]──→ Active
Active ──[expiry reached]──→ Expired (auto-cleanup)
Active ──[user logs out]──→ Deleted
```

## Validation Rules

| Entity | Field | Rule |
|--------|-------|------|
| User | email | Valid email format, unique |
| Account | password | Minimum 8 characters, hashed with bcrypt |
| Session | expiresAt | Must be in the future at creation |
| Session | token | Cryptographically random, unique |

## Notes

- All auth tables are created and managed by Better Auth — no manual migration needed
- Better Auth auto-creates tables on first startup if they don't exist
- The Task table remains completely independent (managed by FastAPI/SQLModel)
- No per-user task ownership for MVP (all users share the same task list)
- Future: Add `userId` FK to Task table for per-user task isolation
