# Quickstart: ClawList Landing Page & Authentication

**Feature**: 005-clawlist-landing-auth
**Date**: 2026-02-08

## Prerequisites

- Node.js 18+ installed
- Existing frontend running (`npm run dev` in `frontend/`)
- Existing backend running (`uvicorn main:app` in `backend/src/`)
- Neon PostgreSQL database accessible (same DATABASE_URL as backend)

## New Dependencies

### Frontend (npm)

```bash
cd frontend
npm install better-auth
```

**Package**: `better-auth` — handles both server-side auth instance and client-side React hooks.

No other new dependencies needed. Tailwind CSS is already installed for the landing page styling.

## New Environment Variables

### Frontend (.env.local)

```env
# Existing
NEXT_PUBLIC_API_URL=https://your-backend.railway.app/api/v1

# New — Better Auth
DATABASE_URL=postgresql://user:pass@host/dbname    # Same Neon DB as backend
BETTER_AUTH_SECRET=your-random-secret-min-32-chars  # Session signing secret
BETTER_AUTH_URL=http://localhost:3000               # Base URL for auth callbacks
```

### Backend (no changes)

The FastAPI backend requires no new environment variables. Better Auth runs entirely in the Next.js server.

## File Structure (New Files)

```
frontend/
├── src/
│   ├── lib/
│   │   ├── auth.ts                    # Better Auth server instance
│   │   └── auth-client.ts             # Better Auth React client
│   ├── app/
│   │   ├── page.tsx                   # Landing page (replaces current todo list)
│   │   ├── layout.tsx                 # Updated root layout (remove old header)
│   │   ├── login/
│   │   │   └── page.tsx               # Login form
│   │   ├── register/
│   │   │   └── page.tsx               # Registration form
│   │   ├── app/
│   │   │   ├── layout.tsx             # Protected app layout (with ChatWidget)
│   │   │   └── page.tsx               # Todo list (moved from root page.tsx)
│   │   └── api/
│   │       └── auth/
│   │           └── [...all]/
│   │               └── route.ts       # Better Auth route handler
│   ├── components/
│   │   ├── Header.tsx                 # Glassmorphism header (new)
│   │   ├── landing/
│   │   │   ├── HeroSection.tsx        # Hero section component
│   │   │   ├── BenefitsSection.tsx    # Benefits section component
│   │   │   ├── CTASection.tsx         # CTA section component
│   │   │   └── Footer.tsx            # Footer component
│   │   └── auth/
│   │       ├── LoginForm.tsx          # Login form component
│   │       └── RegisterForm.tsx       # Registration form component
│   └── middleware.ts                  # Route protection middleware (new)
```

## Setup Steps

1. **Install Better Auth**: `npm install better-auth`
2. **Add environment variables** to `.env.local`
3. **Create auth server instance** (`lib/auth.ts`)
4. **Create auth client** (`lib/auth-client.ts`)
5. **Create API route handler** (`api/auth/[...all]/route.ts`)
6. **Create middleware** (`middleware.ts`) for route protection
7. **Build landing page** components (Hero, Benefits, CTA, Footer)
8. **Build auth pages** (Login, Register)
9. **Move todo list** from `/` to `/app`
10. **Update layouts** (root layout for landing, app layout for protected area)
11. **Add Header** component with glassmorphism effect
12. **Test full flow**: Landing → Register → Redirect to /app → Logout → Landing

## Verification

```bash
# 1. Start dev server
cd frontend && npm run dev

# 2. Visit landing page
open http://localhost:3000

# 3. Click "Get Started" CTA → should go to /register
# 4. Register with email/password → should redirect to /app (todo list)
# 5. Visit /app directly while logged in → should show todo list
# 6. Logout → should redirect to landing page
# 7. Visit /app while logged out → should redirect to /login
```
