# Research: ClawList Landing Page & Authentication

**Feature**: 005-clawlist-landing-auth
**Date**: 2026-02-08
**Status**: Complete

## R1: Authentication Library — Better Auth with Next.js

**Decision**: Use Better Auth with email/password authentication in the Next.js frontend

**Rationale**:
- Better Auth is explicitly requested by the user as a product requirement
- It provides a framework-agnostic TypeScript auth library with first-class Next.js support
- It handles user management, session management, and password hashing out of the box
- It runs entirely in the Next.js app (server-side), using its own database tables — no separate auth server needed
- The existing FastAPI backend remains unchanged; it only handles task CRUD and chatbot

**Alternatives considered**:
- NextAuth.js: Mature but being replaced by Auth.js; Better Auth was explicitly requested
- Clerk/Auth0: Third-party SaaS services, not self-hosted
- Custom auth: Too much effort, insecure by default

**Key findings from Better Auth docs**:

1. **Server instance** (`lib/auth.ts`): `betterAuth({ database, emailAndPassword: { enabled: true } })`
2. **Client instance** (`lib/auth-client.ts`): `createAuthClient()` from `better-auth/react`
3. **Route handler**: `/app/api/auth/[...all]/route.ts` using `toNextJsHandler(auth)`
4. **Middleware**: `getSessionCookie(request)` for lightweight route protection
5. **Session hook**: `authClient.useSession()` for client-side session state
6. **Database**: Better Auth manages its own tables (user, session, account, verification) — can use the same Neon PostgreSQL instance as the task backend

## R2: Database Strategy — Shared PostgreSQL, Separate Concerns

**Decision**: Better Auth uses the same Neon PostgreSQL database but manages its own tables independently from the FastAPI task tables

**Rationale**:
- Better Auth creates and manages its own tables (user, session, account, verification)
- The FastAPI backend's task table is completely separate
- No schema conflicts — Better Auth tables have distinct names
- Single database reduces infrastructure complexity
- Better Auth connects directly from Next.js server-side, not through FastAPI

**Alternatives considered**:
- Separate database for auth: Unnecessary complexity, extra cost
- Auth through FastAPI: Would require duplicating Better Auth's session management in Python; Better Auth is a JS/TS library and runs natively in Next.js

**Database tables managed by Better Auth**:
- `user`: id, name, email, emailVerified, image, createdAt, updatedAt
- `session`: id, expiresAt, token, createdAt, updatedAt, ipAddress, userAgent, userId
- `account`: id, accountId, providerId, userId, accessToken, refreshToken, idToken, accessTokenExpiresAt, refreshTokenExpiresAt, scope, password, createdAt, updatedAt
- `verification`: id, identifier, value, expiresAt, createdAt, updatedAt

## R3: Route Architecture — Landing vs App

**Decision**: Restructure routes so `/` is the landing page and `/app` is the protected todo list

**Rationale**:
- The landing page is the first thing visitors see — it belongs at the root URL
- The existing todo app moves to `/app` (protected route)
- Clean separation: public pages (/, /login, /register) vs protected pages (/app)
- Middleware protects `/app` routes; redirects unauthenticated users to `/login`

**Route map**:
| Route | Access | Purpose |
|-------|--------|---------|
| `/` | Public | Landing page (hero, benefits, CTA, footer) |
| `/login` | Public | Login form |
| `/register` | Public | Registration form |
| `/app` | Protected | Todo list + AI chatbot (existing functionality) |

**Alternatives considered**:
- `/dashboard` for the app: `/app` is shorter and aligns with common SaaS patterns
- Keep todo at `/` and landing at `/landing`: Bad UX — visitors should see the landing page first

## R4: Landing Page Design — Glassmorphism & Minimal Aesthetic

**Decision**: Clean, minimalist design with glassmorphism header using Tailwind CSS

**Rationale**:
- User explicitly requested "clean and minimalist" with "beautiful blur header"
- Glassmorphism achieved via Tailwind's `backdrop-blur` and semi-transparent backgrounds
- No additional UI libraries needed — Tailwind CSS is already installed
- Four sections: Hero, Benefits (3-4 items), CTA, Footer

**Design tokens** (Tailwind utility classes):
- Header: `backdrop-blur-md bg-white/70 border-b border-white/20 sticky top-0 z-50`
- Brand colors: Indigo/purple gradient for CTAs, neutral grays for text
- Typography: System font stack (already in Tailwind defaults), large bold hero text
- Spacing: Generous padding (py-20+ for sections), max-w-6xl container

**Alternatives considered**:
- shadcn/ui: Adds complexity; the landing page is simple enough with raw Tailwind
- Framer Motion animations: Nice-to-have but not in scope for MVP

## R5: Auth Integration with Existing Backend

**Decision**: Better Auth handles authentication independently; FastAPI backend requires no auth changes for MVP

**Rationale**:
- The existing FastAPI backend has no authentication — all task endpoints are open
- For MVP, Better Auth protects access at the frontend route level (middleware)
- The task API remains accessible to authenticated frontend users via the same fetch calls
- Future enhancement: Add API-level auth tokens if needed (out of scope)

**Alternatives considered**:
- Add JWT validation to FastAPI: Significant backend changes, not needed for MVP
- Proxy task API through Next.js API routes: Adds latency and complexity

**Trade-off accepted**: Task API endpoints are not individually authenticated at the backend level. Route-level protection in Next.js middleware ensures only logged-in users can reach the `/app` page that calls these endpoints. This is acceptable for a hackathon project but would need API-level auth for production.

## R6: Session Persistence & Logout

**Decision**: Use Better Auth's built-in cookie-based session management

**Rationale**:
- Better Auth stores sessions in the database with secure HTTP-only cookies
- Sessions persist across browser refreshes (spec requirement: 24+ hours)
- `authClient.signOut()` clears session and redirects to landing page
- No custom session management code needed

**Key configuration**:
- Session expiry: Better Auth default (7 days) exceeds the 24-hour spec requirement
- Cookie: Secure, HttpOnly, SameSite=Lax (Better Auth defaults)

## Summary of Decisions

| Area | Decision | Risk Level |
|------|----------|------------|
| Auth library | Better Auth (email/password) | Low — well-documented, user-requested |
| Database | Shared Neon PostgreSQL | Low — separate tables, no conflicts |
| Route structure | / landing, /app protected | Low — standard SaaS pattern |
| Landing design | Tailwind glassmorphism | Low — no new dependencies |
| Backend auth | Frontend-only protection (MVP) | Medium — acceptable for hackathon |
| Sessions | Better Auth cookies | Low — built-in, battle-tested |
