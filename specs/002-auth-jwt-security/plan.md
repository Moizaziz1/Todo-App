# Implementation Plan: Authentication & API Security

**Branch**: `002-auth-jwt-security` | **Date**: 2026-02-07 | **Spec**: [specs/002-auth-jwt-security/spec.md](spec.md)
**Input**: Feature specification from `/specs/002-auth-jwt-security/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement JWT-based authentication by integrating Better Auth in the Next.js frontend for user management and token issuance, and adding JWT verification middleware to the FastAPI backend to protect all task endpoints. Users will sign up/sign in via Better Auth, receive JWT tokens, and use these tokens to access their task data through the protected API.

## Technical Context

**Language/Version**: Python 3.11 (Backend), TypeScript/Node.js 18+ (Frontend)
**Primary Dependencies**: Better Auth, PyJWT, FastAPI, Next.js 16+ App Router
**Storage**: Neon Serverless PostgreSQL (shared between frontend auth and backend tasks)
**Testing**: pytest (backend), Jest/Playwright (frontend)
**Target Platform**: Web application (cross-platform browsers)
**Project Type**: web (frontend + backend)
**Performance Goals**: Token verification under 100ms, authentication flows under 10 seconds
**Constraints**: HS256 symmetric JWT, shared secret via environment variables, no session-based auth on backend
**Scale/Scope**: 100 concurrent authenticated users

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Spec-Driven Development**: Following spec → plan → tasks → Claude Code workflow (PASSED)
- **Full-Stack Architecture**: Frontend handles auth UI and token storage, backend verifies tokens (PASSED)
- **Security-First Design**: JWT verification on all protected routes, user data isolation enforced (PASSED)
- **REST API Conventions**: Standard Authorization: Bearer header, proper HTTP status codes (PASSED)
- **Data Persistence Requirement**: Users and tasks stored in Neon PostgreSQL (PASSED)
- **Frontend-Backend Separation**: Better Auth on frontend, PyJWT verification on backend (PASSED)

## Project Structure

### Documentation (this feature)

```text
specs/002-auth-jwt-security/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   └── auth-api-contract.yaml
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── task.py           # Existing task model
│   │   └── user.py           # NEW: User model for backend reference
│   ├── services/
│   │   ├── __init__.py
│   │   ├── database.py       # Existing database connection
│   │   └── task_service.py   # Existing task service
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py           # UPDATED: JWT verification dependency
│   │   ├── schemas/
│   │   │   └── task.py       # Existing schemas
│   │   └── routes/
│   │       └── tasks.py      # UPDATED: Protected with JWT auth
│   ├── config/
│   │   └── settings.py       # UPDATED: JWT configuration
│   └── main.py               # Existing FastAPI app
├── tests/
│   ├── unit/
│   │   └── test_auth.py      # NEW: JWT verification tests
│   └── integration/
│       └── test_protected_routes.py  # NEW: Auth integration tests
├── requirements.txt          # UPDATED: Add PyJWT
└── .env.example             # UPDATED: Add JWT settings

frontend/
├── app/
│   ├── api/
│   │   └── auth/
│   │       └── [...all]/
│   │           └── route.ts  # NEW: Better Auth handler
│   ├── (auth)/
│   │   ├── sign-in/
│   │   │   └── page.tsx      # NEW: Sign-in page
│   │   └── sign-up/
│   │       └── page.tsx      # NEW: Sign-up page
│   ├── layout.tsx            # UPDATED: Auth provider
│   └── page.tsx              # Existing/placeholder
├── lib/
│   ├── auth.ts               # NEW: Better Auth server config
│   ├── auth-client.ts        # NEW: Better Auth client
│   └── api-client.ts         # NEW: API client with JWT attachment
├── components/
│   └── auth/
│       ├── sign-in-form.tsx  # NEW: Sign-in form component
│       └── sign-up-form.tsx  # NEW: Sign-up form component
├── package.json              # UPDATED: Add better-auth
└── .env.local.example        # NEW: Frontend env template
```

**Structure Decision**: Web application structure with existing backend from Spec 1 and new frontend directory. Backend receives JWT verification middleware; frontend handles all authentication UI and token management via Better Auth.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |

## Key Design Decisions

### 1. JWT Algorithm: HS256 (Symmetric)

**Decision**: Use HS256 with shared secret instead of asymmetric algorithms (EdDSA/RSA)

**Rationale**:
- Simpler configuration - single secret shared between services
- Sufficient security for hackathon scope
- No JWKS endpoint required for verification
- Faster verification than asymmetric algorithms

**Trade-off**: Requires secure secret distribution; both services must have access to the same secret.

### 2. Token Storage: Better Auth Managed

**Decision**: Let Better Auth manage token storage and retrieval

**Rationale**:
- Better Auth handles session cookies securely
- JWT retrieved on-demand via `authClient.token()`
- Avoids XSS risks of localStorage
- Follows library best practices

### 3. User ID Source: JWT Token Only

**Decision**: Extract user_id from JWT token, not from URL parameters

**Rationale**:
- URL user_id can be spoofed without auth
- Token-based identity is cryptographically verified
- Enables strict user isolation
- URL user_id validated against token for defense-in-depth

### 4. Error Response Strategy

**Decision**: Return 404 for unauthorized access to specific resources

**Rationale**:
- Prevents resource enumeration attacks
- User cannot determine if resource exists vs. access denied
- 401 reserved for missing/invalid tokens only
- Standard security practice

## Implementation Phases

### Phase 1: Backend JWT Verification
- Add PyJWT dependency
- Create JWT verification dependency
- Update settings with JWT configuration
- Add authentication middleware

### Phase 2: Backend Route Protection
- Protect all task endpoints
- Validate user_id matches token
- Update error handling

### Phase 3: Frontend Better Auth Setup
- Install and configure Better Auth
- Create auth API routes
- Set up database adapter

### Phase 4: Frontend Auth UI
- Create sign-up page and form
- Create sign-in page and form
- Add sign-out functionality

### Phase 5: Frontend API Client
- Create API client with JWT attachment
- Handle token retrieval
- Handle auth errors

### Phase 6: Integration Testing
- Test complete auth flow
- Test cross-user access prevention
- Verify error handling

## Dependencies

### External Dependencies
- Better Auth: ^1.0.0 (npm)
- PyJWT: ^2.8.0 (pip)

### Internal Dependencies
- Spec 1 (Backend CRUD): Task endpoints must exist to protect
- Database: Neon PostgreSQL must be accessible from both services

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| Secret key mismatch | High - All auth fails | Document in quickstart, validate during setup |
| Token expiration UX | Medium - Users logged out | Set 24h expiration, clear error messages |
| CORS configuration | Medium - Frontend blocked | Configure in backend CORS middleware |
| Database schema conflicts | Low - Migration issues | Run Better Auth migrations first |

## Success Metrics

- [ ] 401 returned for all unauthenticated requests
- [ ] 404 returned for cross-user access attempts
- [ ] Token verification under 100ms
- [ ] Sign-up completes in under 30 seconds
- [ ] Sign-in completes in under 10 seconds
- [ ] Sign-out clears credentials and prevents API access
