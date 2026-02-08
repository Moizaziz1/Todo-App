# Quickstart Guide: Backend API & Database (Core CRUD)

## Prerequisites

- Python 3.11+
- Poetry or pip for dependency management
- Access to Neon Serverless PostgreSQL database
- Environment variables configured for database connection

## Setup Instructions

### 1. Clone and Navigate
```bash
# Already in the project directory
cd D:/hackathon II/Phase II/
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
# Or if using poetry:
poetry install
```

### 3. Environment Configuration
Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
# Edit .env with your database connection details
```

Required environment variables:
- `DATABASE_URL`: Connection string for Neon PostgreSQL database
- `SECRET_KEY`: Secret key for security (JWT if implemented later)

### 4. Database Setup
Initialize the database tables:
```bash
# Using Alembic migrations
alembic upgrade head
```

### 5. Run the Application
```bash
# Using uvicorn
uvicorn backend.src.main:app --host 0.0.0.0 --port 8000 --reload

# Or using Python directly
python -m backend.src.main
```

## API Usage Examples

### Create a Task
```bash
curl -X POST http://localhost:8000/api/v1/users/1/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Sample Task", "description": "This is a sample task", "user_id": "1"}'
```

### Get All Tasks for User
```bash
curl http://localhost:8000/api/v1/users/1/tasks
```

### Get Specific Task
```bash
curl http://localhost:8000/api/v1/users/1/tasks/1
```

### Update a Task
```bash
curl -X PUT http://localhost:8000/api/v1/users/1/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Task", "description": "Updated description", "completed": true}'
```

### Delete a Task
```bash
curl -X DELETE http://localhost:8000/api/v1/users/1/tasks/1
```

### Complete a Task
```bash
curl -X PATCH http://localhost:8000/api/v1/users/1/tasks/1/complete \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

## Testing

### Run Unit Tests
```bash
pytest tests/unit/
```

### Run Integration Tests
```bash
pytest tests/integration/
```

### Run All Tests
```bash
pytest
```

## Project Structure
```
backend/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py            # SQLModel Task model definition
│   ├── services/
│   │   ├── __init__.py
│   │   └── database.py        # Database connection and session management
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py            # Dependency injection functions
│   │   └── routes/
│   │       ├── __init__.py
│   │       └── tasks.py       # Task CRUD endpoint implementations
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py        # Configuration and environment variables
│   └── main.py                # FastAPI app initialization
├── tests/
│   ├── conftest.py            # Pytest fixtures
│   ├── unit/
│   │   └── test_models.py     # Model-level tests
│   ├── integration/
│   │   └── test_tasks_api.py  # API endpoint tests
│   └── contract/              # API contract tests
└── requirements.txt           # Python dependencies
```

## Common Issues

1. **Database Connection Error**: Verify DATABASE_URL in your .env file
2. **Alembic Migration Error**: Ensure your database server is running
3. **Import Errors**: Run `pip install -r requirements.txt` again
4. **Port Already in Use**: Change port in the uvicorn command or kill the existing process