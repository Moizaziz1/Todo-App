# Task Management Backend API

FastAPI-based backend service with JWT authentication, user-scoped task management, and PostgreSQL persistence.

## Features

- Full CRUD operations for tasks
- JWT authentication (Better Auth compatible)
- User-scoped data isolation
- REST API conventions
- Data persistence in Neon PostgreSQL
- Proper error handling and validation

## Authentication

All task endpoints require JWT authentication:
- Token must be provided in `Authorization: Bearer <token>` header
- Token is verified using shared secret (must match frontend BETTER_AUTH_SECRET)
- User can only access their own tasks

## Endpoints

### Health Check
- `GET /health` - Health check (no auth required)

### Protected Task Endpoints (JWT required)
- `POST /api/v1/users/{user_id}/tasks` - Create a new task
- `GET /api/v1/users/{user_id}/tasks` - Get all tasks for user
- `GET /api/v1/users/{user_id}/tasks/{task_id}` - Get a specific task
- `PUT /api/v1/users/{user_id}/tasks/{task_id}` - Update a task
- `DELETE /api/v1/users/{user_id}/tasks/{task_id}` - Delete a task
- `PATCH /api/v1/users/{user_id}/tasks/{task_id}/complete` - Update completion status

## Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Required variables:
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT secret (MUST match BETTER_AUTH_SECRET in frontend)
- `ALGORITHM`: JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration (default: 1440 = 24 hours)
- `ALLOWED_ORIGINS`: CORS origins (default: http://localhost:3000)

### 3. Run the Application

```bash
uvicorn src.main:app --reload --port 8000
```

The API will be available at http://localhost:8000

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Error Responses

| Status | Meaning |
|--------|---------|
| 401 | Missing or invalid JWT token |
| 404 | Resource not found (or access denied to prevent enumeration) |
| 422 | Validation error |
| 500 | Server error |

## Security Notes

- SECRET_KEY must match BETTER_AUTH_SECRET in the frontend
- All task operations use the user_id from the JWT token, not from requests
- Cross-user access attempts return 404 (not 403) to prevent enumeration
- CORS is configured to allow only specified frontend origins
