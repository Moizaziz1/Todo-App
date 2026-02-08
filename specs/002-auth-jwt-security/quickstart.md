# Quickstart Guide: Authentication & API Security

## Prerequisites

- Node.js 18+ (for Next.js frontend)
- Python 3.11+ (for FastAPI backend)
- Access to Neon Serverless PostgreSQL database
- Backend from Spec 1 (Backend API & Database) operational

## Setup Instructions

### 1. Generate Shared Secret

Generate a secure secret key that will be shared between frontend and backend:

```bash
openssl rand -base64 32
```

Save this value - you'll use it in both frontend and backend configuration.

### 2. Frontend Setup (Next.js + Better Auth)

#### Install Dependencies
```bash
cd frontend
npm install better-auth
```

#### Environment Configuration
Create `.env.local` in the frontend directory:
```env
BETTER_AUTH_SECRET=<your-generated-secret>
BETTER_AUTH_URL=http://localhost:3000
DATABASE_URL=<your-neon-postgresql-url>
```

#### Create Auth Configuration
Create `lib/auth.ts`:
```typescript
import { betterAuth } from "better-auth"
import { jwt } from "better-auth/plugins"

export const auth = betterAuth({
  database: {
    // Neon PostgreSQL adapter configuration
  },
  emailAndPassword: {
    enabled: true,
  },
  plugins: [
    jwt({
      expirationTime: "24h",
    })
  ]
})
```

#### Create API Route Handler
Create `app/api/auth/[...all]/route.ts`:
```typescript
import { auth } from "@/lib/auth"
import { toNextJsHandler } from "better-auth/next-js"

export const { POST, GET } = toNextJsHandler(auth)
```

#### Create Auth Client
Create `lib/auth-client.ts`:
```typescript
import { createAuthClient } from "better-auth/react"

export const authClient = createAuthClient({
  baseURL: process.env.BETTER_AUTH_URL
})
```

### 3. Backend Setup (FastAPI + JWT Verification)

#### Install Dependencies
```bash
cd backend
pip install PyJWT
```

Or add to `requirements.txt`:
```
PyJWT==2.8.0
```

#### Environment Configuration
Update `.env` in the backend directory:
```env
SECRET_KEY=<same-secret-as-frontend>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
DATABASE_URL=<your-neon-postgresql-url>
```

#### Update Settings
The `backend/src/config/settings.py` already has JWT settings configured.

#### Create JWT Authentication Dependency
Update `backend/src/api/deps.py` with actual JWT verification (see implementation tasks).

### 4. Database Migrations

#### Frontend (Better Auth)
```bash
cd frontend
npx @better-auth/cli migrate
```

#### Backend (Alembic)
```bash
cd backend
alembic upgrade head
```

### 5. Run the Application

#### Start Backend
```bash
cd backend
uvicorn src.main:app --reload --port 8000
```

#### Start Frontend
```bash
cd frontend
npm run dev
```

## Testing Authentication Flow

### 1. Sign Up
```bash
curl -X POST http://localhost:3000/api/auth/sign-up/email \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123", "name": "Test User"}'
```

### 2. Sign In
```bash
curl -X POST http://localhost:3000/api/auth/sign-in/email \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'
```

### 3. Get JWT Token
```bash
# After signing in, get the token (requires session cookie)
curl http://localhost:3000/api/auth/token \
  -H "Cookie: <session-cookie>"
```

### 4. Access Protected Backend API
```bash
# Use the JWT token to access backend
curl http://localhost:8000/api/v1/users/{user_id}/tasks \
  -H "Authorization: Bearer <jwt-token>"
```

### 5. Test Unauthorized Access
```bash
# Should return 401
curl http://localhost:8000/api/v1/users/{user_id}/tasks
```

## Verification Checklist

- [ ] Frontend sign-up creates user account
- [ ] Frontend sign-in returns session
- [ ] JWT token can be retrieved after sign-in
- [ ] Backend accepts requests with valid JWT
- [ ] Backend rejects requests without JWT (401)
- [ ] Backend rejects requests with invalid JWT (401)
- [ ] Backend rejects cross-user access attempts (404)
- [ ] Sign-out clears session and prevents API access

## Common Issues

1. **"Could not validate credentials" (401)**
   - Verify SECRET_KEY matches BETTER_AUTH_SECRET
   - Check token hasn't expired
   - Ensure Authorization header format is correct: `Bearer <token>`

2. **Token verification fails**
   - Confirm both services use the same algorithm (HS256)
   - Check for trailing spaces in environment variables

3. **CORS errors**
   - Verify CORS middleware allows frontend origin
   - Check preflight requests are handled

4. **Database connection errors**
   - Verify DATABASE_URL is correct in both services
   - Check network connectivity to Neon database

## Project Structure After Setup

```
frontend/
├── app/
│   ├── api/
│   │   └── auth/
│   │       └── [...all]/
│   │           └── route.ts    # Better Auth handler
│   ├── (auth)/
│   │   ├── sign-in/
│   │   └── sign-up/
│   └── layout.tsx
├── lib/
│   ├── auth.ts                 # Better Auth config
│   └── auth-client.ts          # Client-side auth
└── .env.local

backend/
├── src/
│   ├── api/
│   │   ├── deps.py             # JWT verification dependency
│   │   └── routes/
│   │       └── tasks.py        # Protected endpoints
│   └── config/
│       └── settings.py         # JWT settings
└── .env
```
