# Tasks: ClawList Landing Page & Authentication

**Input**: Design documents from `/specs/005-clawlist-landing-auth/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/auth-api.md, quickstart.md

**Tests**: Not explicitly requested in the feature specification. Test tasks are omitted. Integration testing is covered in the Polish phase.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `frontend/src/` for Next.js frontend
- **Backend**: No changes — existing FastAPI backend at `backend/src/` is unchanged

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Install dependencies and configure environment for Better Auth

- [x] T001 Install `better-auth` package in `frontend/package.json` via `npm install better-auth`
- [x] T002 Update `frontend/.env.local.example` with new env vars: `DATABASE_URL`, `BETTER_AUTH_SECRET`, `BETTER_AUTH_URL`
- [x] T003 Update `frontend/next.config.js` to add `serverExternalPackages` for `better-auth` if needed for PostgreSQL driver compatibility

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core auth infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Create Better Auth server instance in `frontend/src/lib/auth.ts` — configure with PostgreSQL database adapter (using `DATABASE_URL`), enable `emailAndPassword`, set `trustedOrigins` from env
- [x] T005 Create Better Auth client instance in `frontend/src/lib/auth-client.ts` — export `authClient` using `createAuthClient()` from `better-auth/react`
- [x] T006 Create Better Auth API route handler in `frontend/src/app/api/auth/[...all]/route.ts` — export `GET` and `POST` using `toNextJsHandler(auth)`
- [x] T007 Create route protection middleware in `frontend/src/middleware.ts` — protect `/app` routes (redirect to `/login`), redirect authenticated users from `/login` and `/register` to `/app`
- [x] T008 Update root layout in `frontend/src/app/layout.tsx` — remove the existing app chrome (header with "Todo App" title, container constraints), make it a minimal shell for both landing and app pages

**Checkpoint**: Auth infrastructure ready — Better Auth tables auto-created on first request, middleware protecting routes, API handler serving auth endpoints

---

## Phase 3: User Story 1 — Landing Page Experience (Priority: P1) MVP

**Goal**: Visitors see an attractive landing page with glassmorphism header, hero, benefits, CTA sections, and footer

**Independent Test**: Visit `http://localhost:3000/` and verify all four sections render, header is sticky with blur effect, CTA buttons link to `/register`, footer displays brand and links

### Implementation for User Story 1

- [x] T009 [P] [US1] Create glassmorphism header component in `frontend/src/components/Header.tsx` — sticky nav with `backdrop-blur-md bg-white/70`, ClawList logo/brand name, Login and Sign Up nav links, auth-aware state (show user name + Logout when authenticated using `authClient.useSession()`)
- [x] T010 [P] [US1] Create hero section component in `frontend/src/components/landing/HeroSection.tsx` — bold headline, descriptive subtext, primary CTA button linking to `/register`
- [x] T011 [P] [US1] Create benefits section component in `frontend/src/components/landing/BenefitsSection.tsx` — 3-4 benefit cards with SVG icons (task management, AI chatbot, priorities/tags, clean interface)
- [x] T012 [P] [US1] Create CTA section component in `frontend/src/components/landing/CTASection.tsx` — final call-to-action with heading and button linking to `/register`
- [x] T013 [P] [US1] Create footer component in `frontend/src/components/landing/Footer.tsx` — ClawList brand name, copyright year, relevant links
- [x] T014 [US1] Replace `frontend/src/app/page.tsx` with landing page composition — import and render Header, HeroSection, BenefitsSection, CTASection, Footer in order

**Checkpoint**: Landing page fully functional at `/` with all sections, glassmorphism header, and CTA buttons pointing to `/register`

---

## Phase 4: User Story 2 — User Registration (Priority: P1)

**Goal**: New visitors can create an account with email and password and are redirected to the todo list

**Independent Test**: Navigate to `/register`, fill in email and password, submit form, verify account is created, user is auto-logged in, and redirected to `/app`

### Implementation for User Story 2

- [x] T015 [P] [US2] Create registration form component in `frontend/src/components/auth/RegisterForm.tsx` — email input, password input (min 8 chars), submit button, link to login page, inline error display, loading state, calls `authClient.signUp.email()`, redirects to `/app` on success
- [x] T016 [US2] Create registration page in `frontend/src/app/register/page.tsx` — render RegisterForm centered on page with ClawList branding, clean minimal layout

**Checkpoint**: Registration flow works end-to-end — new user can sign up and is redirected to `/app`

---

## Phase 5: User Story 3 — User Login (Priority: P1)

**Goal**: Registered users can log in with email and password and are redirected to the todo list

**Independent Test**: Navigate to `/login`, enter valid credentials, submit form, verify user is logged in and redirected to `/app`

### Implementation for User Story 3

- [x] T017 [P] [US3] Create login form component in `frontend/src/components/auth/LoginForm.tsx` — email input, password input, submit button, link to registration page, inline error display (generic message for invalid credentials), loading state, calls `authClient.signIn.email()`, redirects to `/app` on success
- [x] T018 [US3] Create login page in `frontend/src/app/login/page.tsx` — render LoginForm centered on page with ClawList branding, clean minimal layout

**Checkpoint**: Login flow works end-to-end — existing user can log in and is redirected to `/app`

---

## Phase 6: User Story 4 — Protected Routes and Session Management (Priority: P2)

**Goal**: Todo list is protected behind authentication; sessions persist; logout works

**Independent Test**: Try accessing `/app` while logged out (expect redirect to `/login`), log in, verify todo list loads with all features (task CRUD, AI chatbot), click logout, verify redirect to landing page

### Implementation for User Story 4

- [x] T019 [US4] Create protected app layout in `frontend/src/app/app/layout.tsx` — wrap children with ClientProviders, include ChatWidget, add app-specific container styling (max-w-4xl, padding), include Header component with logout button
- [x] T020 [US4] Create app page in `frontend/src/app/app/page.tsx` — move existing todo list code from `frontend/src/app/page.tsx` (TaskForm, TaskList, search/filter controls, useTasks hook) to this new protected route
- [x] T021 [US4] Add logout functionality to Header component in `frontend/src/components/Header.tsx` — when user is authenticated, show user email and Logout button that calls `authClient.signOut()` and redirects to `/`
- [x] T022 [US4] Verify ChatWidget renders and functions correctly in the `/app` route — ensure AI chatbot works from the new protected layout
- [x] T023 [US4] Verify all task CRUD operations work from `/app` — create, read, update, delete, toggle complete, add/remove tags, search, filter, sort

**Checkpoint**: Protected app route fully functional — unauthenticated users redirected to login, authenticated users see full todo app with chatbot, logout works

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: End-to-end verification and responsive design

- [x] T024 [P] Update `frontend/src/app/globals.css` to add any landing-page-specific styles (smooth scrolling `html { scroll-behavior: smooth }`)
- [x] T025 [P] Update `frontend/src/app/not-found.tsx` to include link back to landing page and consistent ClawList branding
- [x] T026 Verify mobile responsiveness — all landing page sections stack vertically, auth forms are full-width on mobile, header hamburger menu or responsive nav
- [x] T027 Run `quickstart.md` full verification flow — landing → register → app → logout → login → app → logout
- [x] T028 Update `frontend/.env.local.example` with final list of all required environment variables and comments

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user stories
- **US1 Landing Page (Phase 3)**: Depends on Foundational (needs Header with auth state from T005)
- **US2 Registration (Phase 4)**: Depends on Foundational (needs auth client from T005, route handler from T006)
- **US3 Login (Phase 5)**: Depends on Foundational (needs auth client from T005, route handler from T006)
- **US4 Protected Routes (Phase 6)**: Depends on Foundational (needs middleware from T007) and US1 (needs Header from T009)
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **US1 (Landing Page)**: Can start after Foundational — no dependencies on other stories
- **US2 (Registration)**: Can start after Foundational — no dependencies on other stories
- **US3 (Login)**: Can start after Foundational — no dependencies on other stories
- **US4 (Protected Routes)**: Depends on US1 (Header component) — can start after US1 is complete

### Within Each User Story

- Components (marked [P]) can be built in parallel within a story
- Page composition depends on all components being ready
- Integration/verification depends on page being ready

### Parallel Opportunities

- T001, T002, T003 (Setup) can run in parallel
- T004, T005 can run in parallel (separate files)
- T009, T010, T011, T012, T013 (US1 components) can ALL run in parallel
- T015 and T017 (US2 + US3 forms) can run in parallel since they're separate files and stories
- US1, US2, US3 can start in parallel after Foundational phase (if team capacity allows)

---

## Parallel Example: User Story 1 (Landing Page)

```bash
# Launch all landing page components together (all [P] — separate files):
Task: "Create Header component in frontend/src/components/Header.tsx"
Task: "Create HeroSection in frontend/src/components/landing/HeroSection.tsx"
Task: "Create BenefitsSection in frontend/src/components/landing/BenefitsSection.tsx"
Task: "Create CTASection in frontend/src/components/landing/CTASection.tsx"
Task: "Create Footer in frontend/src/components/landing/Footer.tsx"

# Then compose the landing page (depends on all above):
Task: "Replace frontend/src/app/page.tsx with landing page composition"
```

## Parallel Example: US2 + US3 (Registration + Login)

```bash
# Build both auth forms in parallel (separate files, separate stories):
Task: "Create RegisterForm in frontend/src/components/auth/RegisterForm.tsx"
Task: "Create LoginForm in frontend/src/components/auth/LoginForm.tsx"

# Then create pages (each depends on its own form):
Task: "Create registration page in frontend/src/app/register/page.tsx"
Task: "Create login page in frontend/src/app/login/page.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 + 2 + 3)

1. Complete Phase 1: Setup (install better-auth)
2. Complete Phase 2: Foundational (auth server, client, route handler, middleware, layout update)
3. Complete Phase 3: US1 Landing Page — **VALIDATE**: landing page renders with all sections
4. Complete Phase 4: US2 Registration — **VALIDATE**: new user can register and reach /app
5. Complete Phase 5: US3 Login — **VALIDATE**: existing user can log in
6. **STOP and DEMO**: Core auth + landing page working

### Full Delivery

7. Complete Phase 6: US4 Protected Routes — **VALIDATE**: todo list protected, logout works
8. Complete Phase 7: Polish — responsive design, end-to-end verification
9. Deploy to Vercel and test with production database

### Incremental Delivery

Each user story adds testable value:
- After US1: Visitors see a professional landing page
- After US2: New users can register
- After US3: Returning users can log in
- After US4: App is fully protected with session management

---

## Summary

| Metric | Value |
|--------|-------|
| Total tasks | 28 |
| Setup tasks | 3 (T001-T003) |
| Foundational tasks | 5 (T004-T008) |
| US1 Landing Page tasks | 6 (T009-T014) |
| US2 Registration tasks | 2 (T015-T016) |
| US3 Login tasks | 2 (T017-T018) |
| US4 Protected Routes tasks | 5 (T019-T023) |
| Polish tasks | 5 (T024-T028) |
| Parallelizable tasks | 14 (marked [P]) |
| New files | ~15 |
| Modified files | ~4 |

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable after Foundational phase
- No backend changes — all work is in the Next.js frontend
- Better Auth auto-creates database tables on first auth request
- Commit after each task or logical group for clean git history
