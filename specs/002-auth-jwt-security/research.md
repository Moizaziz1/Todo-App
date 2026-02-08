# Research: Authentication & API Security (Better Auth + JWT)

**Date**: 2026-02-07
**Feature**: 002-auth-jwt-security

## Research Summary

This document consolidates research findings for implementing JWT-based authentication using Better Auth in the Next.js frontend and JWT verification in the FastAPI backend.

---

## Decision 1: Better Auth Configuration

**Decision**: Use Better Auth with JWT plugin for token issuance

**Rationale**:
- Better Auth is a framework-agnostic TypeScript authentication library
- Native support for Next.js App Router
- Built-in JWT plugin for issuing access tokens
- Uses JWKS (JSON Web Key Set) for token verification
- Supports both session-based and JWT authentication

**Alternatives Considered**:
- NextAuth.js: More complex, heavier setup
- Auth0: External service, cost implications
- Custom implementation: More work, security risks

**Configuration Details**:
```typescript
// auth.ts
import { betterAuth } from "better-auth"
import { jwt } from "better-auth/plugins"

export const auth = betterAuth({
  emailAndPassword: { enabled: true },
  plugins: [jwt()]
})
```

**Environment Variables Required**:
- `BETTER_AUTH_SECRET`: 32+ character cryptographic key (generate with `openssl rand -base64 32`)
- `BETTER_AUTH_URL`: Application base URL (e.g., `http://localhost:3000`)

---

## Decision 2: JWT Token Strategy

**Decision**: Use HS256 symmetric algorithm with shared secret for JWT signing

**Rationale**:
- Simpler implementation than asymmetric keys (EdDSA/RSA)
- Better Auth supports HS256 through its JWT plugin
- Shared secret can be configured via environment variables
- Sufficient security for hackathon scope
- Easier backend verification without JWKS endpoint calls

**Token Structure**:
- **Header**: `{"alg": "HS256", "typ": "JWT"}`
- **Payload**: `{"sub": "<user_id>", "email": "<email>", "iat": <timestamp>, "exp": <timestamp>}`
- **Signature**: HMAC-SHA256 of header.payload with secret

**Expiration**: 24 hours (configurable via `expirationTime` in JWT plugin)

**Alternatives Considered**:
- EdDSA (asymmetric): More secure but requires JWKS verification
- JWE (encrypted): Overkill for this use case
- Session-only: Doesn't work for cross-service API calls

---

## Decision 3: Frontend Token Handling

**Decision**: Store JWT in memory and attach via Authorization header

**Rationale**:
- Better Auth client provides `authClient.token()` to retrieve JWT
- Token attached to requests as `Authorization: Bearer <token>`
- Memory storage avoids XSS risks of localStorage
- Better Auth manages session cookies separately for frontend state

**Implementation Pattern**:
```typescript
// Get token from Better Auth
const { data } = await authClient.token()
const jwtToken = data.token

// Attach to API requests
fetch('/api/v1/tasks', {
  headers: {
    'Authorization': `Bearer ${jwtToken}`
  }
})
```

---

## Decision 4: FastAPI JWT Verification

**Decision**: Use PyJWT library with FastAPI dependency injection

**Rationale**:
- PyJWT is lightweight and actively maintained
- FastAPI's dependency injection makes it easy to protect routes
- OAuth2PasswordBearer handles Authorization header extraction
- Consistent with FastAPI official documentation patterns

**Alternatives Considered**:
- python-jose: More features but larger dependency
- Authlib: Overkill for simple JWT verification
- Custom header parsing: Error-prone

**Implementation Pattern**:
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return {"user_id": user_id, "email": payload.get("email")}
    except InvalidTokenError:
        raise credentials_exception
```

---

## Decision 5: User Data Model

**Decision**: Create User model in backend database for user storage

**Rationale**:
- Better Auth manages users on frontend with its own database adapter
- Backend needs to store user references for task ownership
- User ID from JWT used as foreign key in tasks
- Email stored for reference but authentication handled by frontend

**User Model Fields**:
- `id`: String (UUID from Better Auth)
- `email`: String (unique)
- `created_at`: DateTime

**Alternatives Considered**:
- No backend user table: Would require JWT-only user identification
- Full user management in backend: Duplicates Better Auth functionality

---

## Decision 6: Error Handling Strategy

**Decision**: Return standard HTTP status codes with JSON error bodies

**Status Codes**:
| Code | Scenario |
|------|----------|
| 401 Unauthorized | Missing, invalid, or expired token |
| 403 Forbidden | User attempting to access another user's resource |
| 404 Not Found | Resource not found (also used for access control to avoid enumeration) |

**Error Response Format**:
```json
{
  "detail": "Human-readable error message",
  "error_code": "INVALID_TOKEN"
}
```

---

## Technology Summary

### Frontend Stack
- **Framework**: Next.js 16+ (App Router)
- **Auth Library**: Better Auth with JWT plugin
- **Token Storage**: In-memory via Better Auth client
- **API Client**: fetch with Authorization header

### Backend Stack
- **Framework**: FastAPI (Python 3.11)
- **JWT Library**: PyJWT
- **Token Verification**: FastAPI dependency with OAuth2PasswordBearer
- **Secret Configuration**: Environment variables via pydantic-settings

### Shared Configuration
- **JWT Algorithm**: HS256
- **Secret Key**: Shared via `BETTER_AUTH_SECRET` (frontend) and `SECRET_KEY` (backend)
- **Token Expiration**: 24 hours

---

## References

- [Better Auth Documentation](https://www.better-auth.com/docs)
- [Better Auth JWT Plugin](https://www.better-auth.com/docs/plugins/jwt)
- [FastAPI Security Tutorial](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)
- [PyJWT Documentation](https://pyjwt.readthedocs.io/)
