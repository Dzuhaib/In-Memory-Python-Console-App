# Implementation Plan: ClawList Landing Page & Authentication

**Branch**: `005-clawlist-landing-auth` | **Date**: 2026-02-08 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/005-clawlist-landing-auth/spec.md`

## Summary

Add a public landing page at `/` with hero, benefits, CTA, and footer sections styled with glassmorphism and minimal aesthetics. Integrate Better Auth for email/password authentication (login, registration, session management). Move the existing todo list to a protected `/app` route. The FastAPI backend remains unchanged — auth runs entirely in the Next.js server using the same Neon PostgreSQL database.

## Technical Context

**Language/Version**: TypeScript 5.3+ (Next.js), Python 3.11+ (existing backend — unchanged)
**Primary Dependencies**: Next.js 14.1, Better Auth (new), Tailwind CSS 3.4 (existing), React 18.2 (existing)
**Storage**: Neon PostgreSQL (existing — Better Auth adds user/session/account/verification tables)
**Testing**: Jest + React Testing Library (existing), Playwright (existing)
**Target Platform**: Web (Vercel deployment for frontend, Railway for backend)
**Project Type**: Web application (Next.js frontend + FastAPI backend)
**Performance Goals**: Landing page loads in <3s, auth redirects in <1s, Lighthouse >80
**Constraints**: No social login providers, no backend auth changes, min 8-char passwords
**Scale/Scope**: Single-user hackathon project, ~15 new/modified files

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Phased Evolution | PASS | This is a Phase 3 enhancement — Phases 1-3 are complete |
| II. Test-First Development | PASS | Tests will be written for auth flow and landing page components |
| III. Smallest Viable Change | PASS | Minimal auth (email/password only), no social login, no API-level auth |
| IV. Clean Interfaces | PASS | Better Auth provides well-defined API contracts; landing page uses standard component composition |
| V. Observability First | PASS | Better Auth logs auth events; structured error messages for auth failures |
| VI. Security by Default | PASS | Better Auth handles password hashing (bcrypt), HTTP-only cookies, CSRF protection; secrets in env vars |

**Post-Phase 1 Re-check**:

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Phased Evolution | PASS | Building on Phase 3 codebase, no Phase 4/5 dependencies |
| II. Test-First Development | PASS | Component tests for landing, integration tests for auth flow |
| III. Smallest Viable Change | PASS | Only 1 new dependency (better-auth), reuses existing Tailwind/components |
| IV. Clean Interfaces | PASS | Auth API contract documented; route handler pattern is standard |
| V. Observability First | PASS | Auth errors surfaced with actionable messages |
| VI. Security by Default | PASS | No secrets in code; passwords hashed; sessions expire; cookies secure |

## Project Structure

### Documentation (this feature)

```text
specs/005-clawlist-landing-auth/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Phase 0 research output
├── data-model.md        # Phase 1 data model
├── quickstart.md        # Phase 1 setup guide
├── contracts/
│   └── auth-api.md      # Auth API contracts
├── checklists/
│   └── requirements.md  # Spec quality checklist
└── tasks.md             # Phase 2 output (created by /sp.tasks)
```

### Source Code (repository root)

```text
frontend/
├── src/
│   ├── lib/
│   │   ├── auth.ts                    # Better Auth server instance (NEW)
│   │   └── auth-client.ts             # Better Auth React client (NEW)
│   ├── app/
│   │   ├── layout.tsx                 # Root layout (MODIFIED — minimal, no app chrome)
│   │   ├── page.tsx                   # Landing page (REPLACED — was todo list)
│   │   ├── not-found.tsx              # 404 page (existing)
│   │   ├── globals.css                # Global styles (MODIFIED — add landing page styles)
│   │   ├── login/
│   │   │   └── page.tsx               # Login page (NEW)
│   │   ├── register/
│   │   │   └── page.tsx               # Registration page (NEW)
│   │   ├── app/
│   │   │   ├── layout.tsx             # Protected layout with header/chat (NEW)
│   │   │   └── page.tsx               # Todo list (MOVED from root page.tsx)
│   │   └── api/
│   │       └── auth/
│   │           └── [...all]/
│   │               └── route.ts       # Better Auth handler (NEW)
│   ├── components/
│   │   ├── Header.tsx                 # Glassmorphism nav header (NEW)
│   │   ├── landing/
│   │   │   ├── HeroSection.tsx        # Hero section (NEW)
│   │   │   ├── BenefitsSection.tsx    # Benefits section (NEW)
│   │   │   ├── CTASection.tsx         # CTA section (NEW)
│   │   │   └── Footer.tsx             # Footer (NEW)
│   │   ├── auth/
│   │   │   ├── LoginForm.tsx          # Login form (NEW)
│   │   │   └── RegisterForm.tsx       # Registration form (NEW)
│   │   ├── ClientProviders.tsx        # Client providers (existing)
│   │   ├── ChatWidget.tsx             # AI chatbot (existing — moved to /app layout)
│   │   ├── TaskForm.tsx               # Task creation (existing)
│   │   ├── TaskItem.tsx               # Task item (existing)
│   │   └── TaskList.tsx               # Task list (existing)
│   ├── hooks/
│   │   └── useTasks.ts               # Task management hook (existing)
│   ├── services/
│   │   └── api.ts                    # FastAPI client (existing)
│   ├── types/
│   │   ├── task.ts                   # Task types (existing)
│   │   └── chat.ts                   # Chat types (existing)
│   └── middleware.ts                  # Route protection (NEW)
├── package.json                       # Add better-auth dependency (MODIFIED)
├── .env.local                         # Add DATABASE_URL, BETTER_AUTH_SECRET, BETTER_AUTH_URL (MODIFIED)
└── next.config.js                     # May need serverExternalPackages for pg (MODIFIED)

backend/                               # NO CHANGES — existing FastAPI backend
```

**Structure Decision**: Web application pattern. Frontend receives all new code (landing page, auth). Backend is unchanged. Better Auth runs server-side within Next.js, connecting directly to the shared Neon PostgreSQL database.

## Complexity Tracking

> No constitution violations detected. No complexity justifications needed.

## Implementation Phases

### Phase A: Auth Infrastructure (Foundation)

**Goal**: Set up Better Auth with email/password in the Next.js app

**Tasks**:
1. Install `better-auth` package
2. Create `lib/auth.ts` — Better Auth server instance with PostgreSQL adapter and email/password enabled
3. Create `lib/auth-client.ts` — Client-side auth client with `createAuthClient()`
4. Create `app/api/auth/[...all]/route.ts` — Route handler using `toNextJsHandler(auth)`
5. Create `middleware.ts` — Protect `/app` routes, redirect logic for `/login` and `/register`
6. Update `.env.local` with `DATABASE_URL`, `BETTER_AUTH_SECRET`, `BETTER_AUTH_URL`
7. Update `next.config.js` if needed for PostgreSQL driver compatibility

**Dependencies**: None (foundation work)

### Phase B: Auth Pages (Login & Registration)

**Goal**: Build login and registration UI

**Tasks**:
1. Create `components/auth/LoginForm.tsx` — Email/password form with error handling
2. Create `components/auth/RegisterForm.tsx` — Email/password form with validation
3. Create `app/login/page.tsx` — Login page with form, link to register
4. Create `app/register/page.tsx` — Registration page with form, link to login
5. Handle auth errors (duplicate email, invalid credentials, weak password)
6. Redirect to `/app` after successful login/registration

**Dependencies**: Phase A (auth infrastructure must exist)

### Phase C: Landing Page

**Goal**: Build the public landing page with glassmorphism header

**Tasks**:
1. Create `components/Header.tsx` — Sticky glassmorphism header with logo, nav links (Login, Sign Up), and auth-aware state (show user name + Logout when authenticated)
2. Create `components/landing/HeroSection.tsx` — Headline, subtext, CTA button
3. Create `components/landing/BenefitsSection.tsx` — 3-4 benefit cards with icons
4. Create `components/landing/CTASection.tsx` — Final CTA with button
5. Create `components/landing/Footer.tsx` — Brand, copyright, links
6. Replace `app/page.tsx` with landing page composition
7. Update `app/layout.tsx` — Remove old app chrome (header, container constraints)

**Dependencies**: Phase A (header needs auth state)

### Phase D: Protected App Route

**Goal**: Move existing todo list to protected `/app` route

**Tasks**:
1. Create `app/app/layout.tsx` — Protected layout with ChatWidget, app-specific header/container
2. Create `app/app/page.tsx` — Move existing todo list code from root page.tsx
3. Add logout button to Header when on `/app` routes
4. Verify ChatWidget works in the new location
5. Verify all task CRUD operations work from `/app`
6. Update `ClientProviders.tsx` if needed for new route structure

**Dependencies**: Phase A (middleware), Phase C (header component)

### Phase E: Integration Testing & Polish

**Goal**: Verify full auth flow works end-to-end

**Tasks**:
1. Test: Visitor sees landing page at `/`
2. Test: CTA buttons redirect to `/register`
3. Test: Registration creates user and redirects to `/app`
4. Test: Login authenticates and redirects to `/app`
5. Test: `/app` redirects to `/login` when not authenticated
6. Test: Logout redirects to `/`
7. Test: Logged-in user visiting `/login` redirects to `/app`
8. Test: Mobile responsiveness of landing page and auth forms
9. Fix any issues discovered during testing

**Dependencies**: All previous phases

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Auth library | Better Auth | User requirement; TypeScript-native; built-in Next.js support |
| Auth scope | Frontend-only (middleware) | Smallest viable change; backend unchanged for MVP |
| Database | Shared Neon PostgreSQL | Reduces infra; Better Auth tables don't conflict with task table |
| Protected route path | `/app` | Short, standard SaaS convention |
| Landing page at | `/` (root) | First impression for visitors; industry standard |
| UI library for landing | Raw Tailwind CSS | Already installed; no new dependencies needed |
| Password hashing | Better Auth default (bcrypt) | Industry standard, secure |
| Session storage | Database + HTTP-only cookie | Better Auth default; secure and persistent |

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Better Auth PostgreSQL adapter compatibility | Could block auth setup | Test early in Phase A; fallback to SQLite adapter for dev |
| Next.js 14 middleware limitations | Route protection gaps | Use cookie-based check (lightweight); full session validation on pages |
| Task API has no auth | Endpoints accessible without login | Acceptable for hackathon; mitigated by frontend route protection |

## Generated Artifacts

- [research.md](research.md) — Phase 0 research findings
- [data-model.md](data-model.md) — Entity definitions and relationships
- [contracts/auth-api.md](contracts/auth-api.md) — Auth API contracts
- [quickstart.md](quickstart.md) — Setup and verification guide
