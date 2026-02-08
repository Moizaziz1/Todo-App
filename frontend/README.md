# Task Manager Frontend

Next.js frontend for the Task Management application with Better Auth authentication.

## Features

- User sign-up and sign-in with email/password
- JWT token-based authentication
- Protected routes and API calls
- Task management interface

## Setup

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Environment Variables

Copy the example environment file and configure:

```bash
cp .env.local.example .env.local
```

Required variables:
- `BETTER_AUTH_SECRET`: 32+ character secret key (must match backend SECRET_KEY)
- `BETTER_AUTH_URL`: Application URL (default: http://localhost:3000)
- `DATABASE_URL`: PostgreSQL connection string for Better Auth
- `NEXT_PUBLIC_API_URL`: Backend API URL (default: http://localhost:8000/api/v1)

### 3. Run Development Server

```bash
npm run dev
```

The frontend will be available at http://localhost:3000

## Project Structure

```
frontend/
├── app/
│   ├── api/auth/[...all]/route.ts  # Better Auth API handler
│   ├── (auth)/
│   │   ├── sign-in/page.tsx        # Sign-in page
│   │   └── sign-up/page.tsx        # Sign-up page
│   ├── layout.tsx                  # Root layout
│   └── page.tsx                    # Home page
├── components/
│   └── auth/
│       ├── sign-in-form.tsx        # Sign-in form component
│       ├── sign-up-form.tsx        # Sign-up form component
│       ├── sign-out-button.tsx     # Sign-out button component
│       └── protected-route.tsx     # Protected route wrapper
├── lib/
│   ├── auth.ts                     # Better Auth server config
│   ├── auth-client.ts              # Better Auth client
│   └── api-client.ts               # API client with JWT
└── package.json
```

## Authentication Flow

1. User signs up/in via Better Auth
2. Better Auth issues session cookie and JWT token
3. API client retrieves JWT token for backend requests
4. Backend verifies JWT and processes request

## Important Notes

- `BETTER_AUTH_SECRET` must match `SECRET_KEY` in backend for JWT verification
- All API requests automatically include JWT token in Authorization header
- Unauthenticated requests to protected endpoints redirect to sign-in
