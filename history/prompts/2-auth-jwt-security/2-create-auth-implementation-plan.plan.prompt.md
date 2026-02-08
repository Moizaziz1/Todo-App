---
id: 2
title: Create Auth Implementation Plan
stage: plan
date: 2026-02-07
surface: agent
model: claude-sonnet-4-5-20250929
feature: 2-auth-jwt-security
branch: 002-auth-jwt-security
user: user
command: /sp.plan
labels: ["authentication", "jwt", "planning", "better-auth", "fastapi"]
links:
  spec: specs/002-auth-jwt-security/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-auth-jwt-security/plan.md
  - specs/002-auth-jwt-security/research.md
  - specs/002-auth-jwt-security/data-model.md
  - specs/002-auth-jwt-security/quickstart.md
  - specs/002-auth-jwt-security/contracts/auth-api-contract.yaml
tests:
  - null
---

## Prompt

/sp.plan Spec 2 — Authentication & API Security (Better Auth + JWT)

Objective:
Secure the existing backend API by integrating Better Auth on the frontend and JWT verification on the FastAPI backend.

Milestones:

1. Better Auth Setup (Frontend)
   - Install and configure Better Auth in Next.js
   - Implement signup and signin flows
   - Enable JWT plugin to issue tokens
   - Store JWT token in client session

2. Shared Secret Configuration
   - Define BETTER_AUTH_SECRET in frontend environment
   - Define the same secret in backend environment
   - Ensure both services use the same signing key

3. Frontend API Client Update
   - Modify API client to attach JWT token to all requests
   - Add Authorization: Bearer <token> header
   - Handle missing or expired tokens

4. FastAPI JWT Verification
   - Add middleware or dependency to:
     - Extract Authorization header
     - Decode and verify JWT signature
     - Reject invalid or expired tokens
   - Extract user identity from decoded token

5. API Route Enforcement
   - Protect all task endpoints with JWT validation
   - Remove trust in user_id from request alone
   - Match token user ID with request user_id parameter
   - Reject mismatched user access attempts

6. Error Handling
   - Return 401 Unauthorized for missing or invalid tokens
   - Return 403 Forbidden for user mismatch
   - Return clear error messages for auth failures

7. Testing & Verification
   - Test login and token issuance from frontend
   - Test API access with valid token
   - Test API access without token (expect 401)
   - Test cross-user access attempts (expect rejection)

Deliverables:
- Better Auth configured with JWT support
- Frontend API client sending JWT tokens
- FastAPI backend verifying JWT tokens
- Fully protected task API routes

Out of scope:
- Frontend task UI
- Database schema changes
- Advanced security features (refresh tokens, RBAC)
- OAuth or social login providers

Completion criteria:
- All API endpoints reject unauthenticated requests
- JWT tokens are correctly verified

## Response snapshot

Created complete implementation plan for Authentication & API Security:

**Artifacts Generated:**
1. `plan.md` - Implementation plan with 6 phases, constitution check, project structure
2. `research.md` - 6 key decisions on Better Auth, JWT strategy, token handling, verification
3. `data-model.md` - User entity, JWT token structure, relationship updates
4. `contracts/auth-api-contract.yaml` - Auth endpoints, JWT structure, protected routes
5. `quickstart.md` - Step-by-step setup guide for frontend and backend

**Key Technical Decisions:**
- JWT Algorithm: HS256 symmetric with shared secret
- Token Storage: Better Auth managed (session cookies + on-demand JWT)
- User ID Source: JWT token claims (not URL parameters)
- Error Strategy: 404 for unauthorized resource access (prevents enumeration)

**Implementation Phases:**
1. Backend JWT Verification (PyJWT dependency)
2. Backend Route Protection
3. Frontend Better Auth Setup
4. Frontend Auth UI (sign-in/sign-up)
5. Frontend API Client
6. Integration Testing

**Constitution Check:** All 6 principles PASSED

## Outcome

- ✅ Impact: Complete implementation plan ready for task generation
- 🧪 Tests: Test strategy defined in plan
- 📁 Files: 5 artifacts created
- 🔁 Next prompts: Run `/sp.tasks` to generate task breakdown
- 🧠 Reflection: Research on Better Auth JWT plugin was key to design decisions

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Constitution check PASS (6/6)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
