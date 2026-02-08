# Task Manager - Full-Stack Web Application

A modern, secure task management application built with spec-driven development using the Agentic Dev Stack.

## Features

- User authentication with Better Auth (email/password)
- JWT-secured API communication
- Full CRUD operations for tasks
- Responsive UI (desktop and mobile)
- Real-time task completion toggling
- User data isolation and security

## Technology Stack

| Layer | Technology |
|-------|------------|
| Frontend | Next.js 16+ (App Router), React 18, TypeScript, Tailwind CSS |
| Authentication | Better Auth with JWT plugin |
| Backend | Python FastAPI |
| ORM | SQLModel |
| Database | Neon Serverless PostgreSQL |
| Spec-Driven | Claude Code + Spec-Kit Plus |

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                    Frontend (Next.js)               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────┐ │
│  │  Auth Pages  │  │  Dashboard   │  │Task CRUD │ │
│  │ (Better Auth)│  │   (React)    │  │   UI     │ │
│  └──────┬───────┘  └──────┬───────┘  └─────┬────┘ │
│         │                 │                 │      │
│         └─────────────────┴─────────────────┘      │
│                           │                        │
│                      JWT Token                     │
│                     (HS256 signed)                 │
└───────────────────────────┼─────────────────────────┘
                            │
                   Authorization: Bearer
                            │
┌───────────────────────────▼─────────────────────────┐
│              Backend (FastAPI)                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────┐ │
│  │ JWT Verify   │  │ Task Routes  │  │  Models  │ │
│  │ (PyJWT)      │  │  (Protected) │  │(SQLModel)│ │
│  └──────┬───────┘  └──────┬───────┘  └─────┬────┘ │
│         │                 │                 │      │
│         └─────────────────┴─────────────────┘      │
│                           │                        │
└───────────────────────────┼─────────────────────────┘
                            │
                     SQL Queries
                            │
┌───────────────────────────▼─────────────────────────┐
│         Database (Neon PostgreSQL)                  │
│  ┌──────────────┐        ┌──────────────┐          │
│  │   Users      │        │    Tasks     │          │
│  │ (Better Auth)│◄───────┤ (user_id FK) │          │
│  └──────────────┘        └──────────────┘          │
└─────────────────────────────────────────────────────┘
```

## Project Structure

```
Phase II/
├── backend/                    # FastAPI backend (Spec 1 & 2)
│   ├── src/
│   │   ├── models/            # SQLModel entities
│   │   ├── services/          # Business logic
│   │   ├── api/               # REST endpoints
│   │   └── config/            # Settings
│   └── tests/                 # Backend tests
│
├── frontend/                  # Next.js frontend (Spec 2 & 3)
│   ├── app/
│   │   ├── api/auth/          # Better Auth routes
│   │   ├── (auth)/            # Sign-in/sign-up pages
│   │   └── dashboard/         # Task management UI
│   ├── components/
│   │   ├── auth/              # Auth components
│   │   └── tasks/             # Task UI components
│   └── lib/                   # Auth & API clients
│
└── specs/                     # Specifications
    ├── 1-backend-task-crud/   # Spec 1: Backend API
    ├── 002-auth-jwt-security/ # Spec 2: Authentication
    └── 003-frontend-task-ui/  # Spec 3: Frontend UI
```

## Quick Start

### Prerequisites

- Node.js 18+
- Python 3.11+
- PostgreSQL database (Neon recommended)

### 1. Generate Shared Secret

```bash
openssl rand -base64 32
```

Save this value - it will be used in both frontend and backend.

### 2. Configure Backend

```bash
cd backend
cp .env.example .env
# Edit .env and set:
# - DATABASE_URL (your PostgreSQL connection string)
# - SECRET_KEY (the shared secret from step 1)
```

### 3. Install Backend Dependencies

```bash
pip install -r requirements.txt
```

### 4. Start Backend

```bash
uvicorn src.main:app --reload --port 8000
```

Backend runs at http://localhost:8000

### 5. Configure Frontend

```bash
cd frontend
cp .env.local.example .env.local
# Edit .env.local and set:
# - DATABASE_URL (same as backend)
# - BETTER_AUTH_SECRET (same as backend SECRET_KEY)
# - NEXT_PUBLIC_API_URL (http://localhost:8000/api/v1)
```

### 6. Install Frontend Dependencies

```bash
npm install
```

### 7. Run Better Auth Migrations

```bash
npx @better-auth/cli migrate
```

### 8. Start Frontend

```bash
npm run dev
```

Frontend runs at http://localhost:3000

### 9. Test the Application

1. Navigate to http://localhost:3000
2. Click "Sign Up" and create an account
3. You'll be redirected to the dashboard
4. Create, complete, edit, and delete tasks
5. Test on mobile by resizing browser window

## API Endpoints

### Authentication (Better Auth)
- `POST /api/auth/sign-up/email` - Create account
- `POST /api/auth/sign-in/email` - Sign in
- `GET /api/auth/token` - Get JWT token
- `POST /api/auth/sign-out` - Sign out

### Tasks (FastAPI - JWT Required)
- `GET /api/v1/users/{user_id}/tasks` - List tasks
- `POST /api/v1/users/{user_id}/tasks` - Create task
- `GET /api/v1/users/{user_id}/tasks/{task_id}` - Get task
- `PUT /api/v1/users/{user_id}/tasks/{task_id}` - Update task
- `DELETE /api/v1/users/{user_id}/tasks/{task_id}` - Delete task
- `PATCH /api/v1/users/{user_id}/tasks/{task_id}/complete` - Toggle completion

## Security Features

- JWT-based authentication
- HS256 token signing with shared secret
- Token verification on all protected routes
- User data isolation (users can only access their own tasks)
- 401 responses for unauthenticated requests
- 404 responses for cross-user access attempts (prevents enumeration)
- CORS configured for frontend origin only

## Development Workflow

This project was built using Spec-Driven Development:

1. **Spec 1**: Backend API & Database (Core CRUD)
2. **Spec 2**: Authentication & API Security (Better Auth + JWT)
3. **Spec 3**: Frontend Web Application (UI + API Integration)

Each spec followed: `spec → plan → tasks → implement` workflow using Claude Code.

## Documentation

- **Specs**: See `specs/` directory for detailed specifications
- **Backend**: See `backend/README.md`
- **Frontend**: See `frontend/README.md`
- **Quickstart Guides**: Each spec has a `quickstart.md`
- **Prompt History**: See `history/prompts/` for development records

## Troubleshooting

### "Could not validate credentials" (401)
- Verify `SECRET_KEY` (backend) matches `BETTER_AUTH_SECRET` (frontend)
- Check JWT token is being sent in Authorization header

### "Failed to load tasks"
- Ensure backend is running on port 8000
- Verify `NEXT_PUBLIC_API_URL` in frontend `.env.local`
- Check CORS configuration in backend

### UI not loading
- Run `npm install` in frontend directory
- Clear `.next` cache: `rm -rf .next`
- Check browser console for errors

## Contributing

All features must follow the Spec-Driven Development workflow:

1. Create specification with `/sp.specify`
2. Generate plan with `/sp.plan`
3. Break into tasks with `/sp.tasks`
4. Implement with `/sp.implement`

See `.specify/memory/constitution.md` for project principles.

## License

Hackathon Project - Phase II
