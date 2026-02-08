---
description: "Task list for Authentication & API Security feature implementation"
---

# Tasks: Authentication & API Security (Better Auth + JWT)

**Input**: Design documents from `/specs/002-auth-jwt-security/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- Backend: Python FastAPI with existing structure
- Frontend: Next.js 16+ App Router (new)

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization for frontend and backend auth dependencies

- [X] T001 Create frontend project structure with Next.js App Router in frontend/
- [X] T002 Initialize Next.js project with TypeScript and Better Auth dependencies in frontend/package.json
- [X] T003 [P] Add PyJWT dependency to backend/requirements.txt
- [X] T004 [P] Create frontend environment template in frontend/.env.local.example
- [X] T005 Update backend environment template with JWT settings in backend/.env.example

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core authentication infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T006 Configure Better Auth server instance in frontend/lib/auth.ts
- [X] T007 Create Better Auth API route handler in frontend/app/api/auth/[...all]/route.ts
- [X] T008 [P] Create Better Auth client configuration in frontend/lib/auth-client.ts
- [X] T009 [P] Update backend settings with JWT configuration in backend/src/config/settings.py
- [X] T010 Create JWT verification dependency in backend/src/api/deps.py
- [X] T011 Create OAuth2PasswordBearer security scheme in backend/src/api/deps.py
- [X] T012 Update backend CORS configuration in backend/src/main.py

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - User Sign Up (Priority: P1) 🎯 MVP

**Goal**: Enable new users to create accounts with email and password, receiving JWT tokens upon successful registration

**Independent Test**: Can be fully tested by navigating to the sign-up page, entering valid credentials, and verifying the account is created and user receives authentication tokens.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T013 [P] [US1] Contract test for sign-up endpoint in frontend/tests/auth/test_signup.ts
- [ ] T014 [P] [US1] Integration test for sign-up user journey in frontend/tests/integration/test_signup_flow.ts

### Implementation for User Story 1

- [X] T015 [P] [US1] Create sign-up form component in frontend/components/auth/sign-up-form.tsx
- [X] T016 [US1] Create sign-up page with form integration in frontend/app/(auth)/sign-up/page.tsx
- [X] T017 [US1] Add email validation to sign-up form in frontend/components/auth/sign-up-form.tsx
- [X] T018 [US1] Add password requirements validation (min 8 chars) in frontend/components/auth/sign-up-form.tsx
- [X] T019 [US1] Handle sign-up errors (duplicate email, validation) in frontend/components/auth/sign-up-form.tsx
- [X] T020 [US1] Redirect to dashboard on successful sign-up in frontend/app/(auth)/sign-up/page.tsx

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - User Sign In (Priority: P1) 🎯 MVP

**Goal**: Enable returning users to sign in with email and password, receiving JWT tokens for API access

**Independent Test**: Can be fully tested by signing in with valid credentials and verifying the JWT token is returned and stored for subsequent API requests.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T021 [P] [US2] Contract test for sign-in endpoint in frontend/tests/auth/test_signin.ts
- [ ] T022 [P] [US2] Integration test for sign-in user journey in frontend/tests/integration/test_signin_flow.ts

### Implementation for User Story 2

- [X] T023 [P] [US2] Create sign-in form component in frontend/components/auth/sign-in-form.tsx
- [X] T024 [US2] Create sign-in page with form integration in frontend/app/(auth)/sign-in/page.tsx
- [X] T025 [US2] Handle sign-in errors (invalid credentials) in frontend/components/auth/sign-in-form.tsx
- [X] T026 [US2] Redirect to dashboard on successful sign-in in frontend/app/(auth)/sign-in/page.tsx
- [X] T027 [US2] Store session and enable JWT token retrieval in frontend/lib/auth-client.ts

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Authenticated API Requests (Priority: P1) 🎯 MVP

**Goal**: Enable authenticated users to make API requests with JWT tokens attached, with backend verification

**Independent Test**: Can be fully tested by making API requests with a valid JWT token and verifying the request succeeds, then making requests without a token and verifying they are rejected with 401.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T028 [P] [US3] Unit test for JWT verification dependency in backend/tests/unit/test_jwt_verification.py
- [ ] T029 [P] [US3] Integration test for protected endpoints in backend/tests/integration/test_protected_routes.py

### Implementation for User Story 3

- [X] T030 [P] [US3] Create API client with JWT attachment in frontend/lib/api-client.ts
- [X] T031 [US3] Implement token retrieval from Better Auth session in frontend/lib/api-client.ts
- [X] T032 [US3] Add Authorization: Bearer header to all API requests in frontend/lib/api-client.ts
- [X] T033 [US3] Update task routes to require JWT authentication in backend/src/api/routes/tasks.py
- [X] T034 [US3] Extract user_id from JWT token in route handlers in backend/src/api/routes/tasks.py
- [X] T035 [US3] Return 401 Unauthorized for missing/invalid tokens in backend/src/api/deps.py
- [X] T036 [US3] Return 401 Unauthorized for expired tokens in backend/src/api/deps.py
- [X] T037 [US3] Handle auth errors and redirect to sign-in in frontend/lib/api-client.ts

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work - full auth flow operational

---

## Phase 6: User Story 4 - User-Scoped Data Access (Priority: P2)

**Goal**: Ensure authenticated users can only access their own tasks based on JWT token identity

**Independent Test**: Can be fully tested by creating tasks as User A, then authenticating as User B and verifying User B cannot see or modify User A's tasks.

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [ ] T038 [P] [US4] Integration test for cross-user access prevention in backend/tests/integration/test_user_isolation.py

### Implementation for User Story 4

- [X] T039 [US4] Validate URL user_id matches JWT token user_id in backend/src/api/routes/tasks.py
- [X] T040 [US4] Return 404 for cross-user task access attempts in backend/src/api/routes/tasks.py
- [X] T041 [US4] Update create task to use user_id from JWT token in backend/src/api/routes/tasks.py
- [X] T042 [US4] Update task queries to filter by JWT user_id in backend/src/services/task_service.py
- [X] T043 [US4] Remove user_id from request body validation in backend/src/api/routes/tasks.py

**Checkpoint**: At this point, User Stories 1-4 should all work - full security in place

---

## Phase 7: User Story 5 - User Sign Out (Priority: P3)

**Goal**: Enable users to sign out, clearing their JWT token and preventing further API access

**Independent Test**: Can be fully tested by signing in, verifying API access works, signing out, and verifying API access is denied.

### Tests for User Story 5 (OPTIONAL - only if tests requested) ⚠️

- [ ] T044 [P] [US5] Integration test for sign-out flow in frontend/tests/integration/test_signout_flow.ts

### Implementation for User Story 5

- [X] T045 [P] [US5] Create sign-out button component in frontend/components/auth/sign-out-button.tsx
- [X] T046 [US5] Implement sign-out action calling Better Auth in frontend/components/auth/sign-out-button.tsx
- [X] T047 [US5] Clear stored JWT token on sign-out in frontend/lib/auth-client.ts
- [X] T048 [US5] Redirect to sign-in page after sign-out in frontend/components/auth/sign-out-button.tsx
- [X] T049 [US5] Add auth state check to protected pages in frontend/app/layout.tsx

**Checkpoint**: All user stories should now be independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T050 [P] Update frontend root layout with auth provider in frontend/app/layout.tsx
- [X] T051 [P] Create protected route wrapper component in frontend/components/auth/protected-route.tsx
- [X] T052 [P] Documentation updates in backend/README.md
- [X] T053 [P] Documentation updates in frontend/README.md
- [X] T054 Code cleanup and error message standardization
- [X] T055 Security hardening review (CORS, headers, secrets)
- [X] T056 Run quickstart validation with full auth flow

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - US1 (Sign Up) and US2 (Sign In) can run in parallel
  - US3 (API Auth) depends on US1 or US2 being complete (need a way to get tokens)
  - US4 (User Isolation) depends on US3 (need auth working first)
  - US5 (Sign Out) can run in parallel with US3/US4
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

```
US1 (Sign Up) ─────────────┐
                           ├──► US3 (API Auth) ──► US4 (User Isolation)
US2 (Sign In) ────────────┘           │
                                       │
US5 (Sign Out) ◄───────────────────────┘
```

### Parallel Execution Opportunities

**Within Setup Phase:**
- T003, T004 can run in parallel (different projects)

**Within Foundational Phase:**
- T008, T009 can run in parallel (frontend vs backend)

**Within User Story Phases:**
- T015-T020 (US1) and T023-T027 (US2) can run in parallel
- T030-T037 (US3) and T045-T049 (US5) can run in parallel after US1/US2

---

## Implementation Strategy

### MVP Scope (Recommended First Delivery)

**Phases 1-5 (US1 + US2 + US3)**: Complete authentication flow
- Users can sign up
- Users can sign in
- API requests are authenticated
- Unauthenticated requests return 401

### Incremental Delivery

1. **Increment 1**: Setup + Foundational (T001-T012)
2. **Increment 2**: Sign Up (T015-T020)
3. **Increment 3**: Sign In (T023-T027)
4. **Increment 4**: API Auth (T030-T037)
5. **Increment 5**: User Isolation (T039-T043)
6. **Increment 6**: Sign Out + Polish (T045-T056)

### File Touch Summary

| File | Tasks |
|------|-------|
| frontend/lib/auth.ts | T006 |
| frontend/lib/auth-client.ts | T008, T027, T047 |
| frontend/lib/api-client.ts | T030, T031, T032, T037 |
| frontend/app/api/auth/[...all]/route.ts | T007 |
| frontend/components/auth/sign-up-form.tsx | T015, T017, T018, T019 |
| frontend/components/auth/sign-in-form.tsx | T023, T025 |
| frontend/components/auth/sign-out-button.tsx | T045, T046, T048 |
| frontend/app/(auth)/sign-up/page.tsx | T016, T020 |
| frontend/app/(auth)/sign-in/page.tsx | T024, T026 |
| frontend/app/layout.tsx | T049, T050 |
| backend/src/api/deps.py | T010, T011, T035, T036 |
| backend/src/api/routes/tasks.py | T033, T034, T039, T040, T041, T043 |
| backend/src/services/task_service.py | T042 |
| backend/src/config/settings.py | T009 |
| backend/src/main.py | T012 |
