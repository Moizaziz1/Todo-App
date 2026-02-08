# Authentication API Quick Reference

## Base URL
```
http://localhost:8000
```

## Endpoints

### 1. Sign Up (Create Account)

**Endpoint:** `POST /api/v1/auth/signup`

**Request:**
```json
{
  "email": "user@example.com",
  "password": "mypassword123"
}
```

**Success Response (201 Created):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "external_id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "created_at": "2024-01-15T10:30:00"
  }
}
```

**Error Response (400 Bad Request):**
```json
{
  "detail": "Email already registered"
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "mypassword123"}'
```

---

### 2. Sign In (Login)

**Endpoint:** `POST /api/v1/auth/signin`

**Request:**
```json
{
  "email": "user@example.com",
  "password": "mypassword123"
}
```

**Success Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "external_id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "created_at": "2024-01-15T10:30:00"
  }
}
```

**Error Response (401 Unauthorized):**
```json
{
  "detail": "Invalid email or password"
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/signin \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "mypassword123"}'
```

---

### 3. Access Protected Endpoints

**Example:** Get user's tasks

**Endpoint:** `GET /api/v1/users/{user_id}/tasks`

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Success Response (200 OK):**
```json
[
  {
    "id": 1,
    "title": "My Task",
    "description": "Task description",
    "completed": false,
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "created_at": "2024-01-15T10:30:00"
  }
]
```

**Error Response (401 Unauthorized):**
```json
{
  "detail": "Could not validate credentials"
}
```

**cURL Example:**
```bash
curl -X GET http://localhost:8000/api/v1/users/550e8400-e29b-41d4-a716-446655440000/tasks \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

---

## JavaScript/TypeScript Examples

### Sign Up
```javascript
async function signUp(email, password) {
  const response = await fetch('http://localhost:8000/api/v1/auth/signup', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail);
  }

  const data = await response.json();
  // Store the token
  localStorage.setItem('access_token', data.access_token);
  localStorage.setItem('user', JSON.stringify(data.user));

  return data;
}
```

### Sign In
```javascript
async function signIn(email, password) {
  const response = await fetch('http://localhost:8000/api/v1/auth/signin', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail);
  }

  const data = await response.json();
  // Store the token
  localStorage.setItem('access_token', data.access_token);
  localStorage.setItem('user', JSON.stringify(data.user));

  return data;
}
```

### Make Authenticated Request
```javascript
async function getTasks(userId) {
  const token = localStorage.getItem('access_token');

  const response = await fetch(
    `http://localhost:8000/api/v1/users/${userId}/tasks`,
    {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    }
  );

  if (response.status === 401) {
    // Token expired or invalid - redirect to login
    window.location.href = '/login';
    return;
  }

  if (!response.ok) {
    throw new Error('Failed to fetch tasks');
  }

  return await response.json();
}
```

### Create Task (Authenticated)
```javascript
async function createTask(userId, taskData) {
  const token = localStorage.getItem('access_token');

  const response = await fetch(
    `http://localhost:8000/api/v1/users/${userId}/tasks`,
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(taskData),
    }
  );

  if (response.status === 401) {
    // Token expired or invalid - redirect to login
    window.location.href = '/login';
    return;
  }

  if (!response.ok) {
    throw new Error('Failed to create task');
  }

  return await response.json();
}
```

---

## Python Examples (using requests)

### Sign Up
```python
import requests

def sign_up(email, password):
    response = requests.post(
        'http://localhost:8000/api/v1/auth/signup',
        json={'email': email, 'password': password}
    )

    if response.status_code == 201:
        data = response.json()
        return data['access_token'], data['user']
    else:
        raise Exception(response.json()['detail'])
```

### Sign In
```python
def sign_in(email, password):
    response = requests.post(
        'http://localhost:8000/api/v1/auth/signin',
        json={'email': email, 'password': password}
    )

    if response.status_code == 200:
        data = response.json()
        return data['access_token'], data['user']
    else:
        raise Exception(response.json()['detail'])
```

### Make Authenticated Request
```python
def get_tasks(user_id, token):
    response = requests.get(
        f'http://localhost:8000/api/v1/users/{user_id}/tasks',
        headers={'Authorization': f'Bearer {token}'}
    )

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(response.json()['detail'])
```

---

## Token Information

- **Algorithm:** HS256 (HMAC with SHA-256)
- **Expiration:** 24 hours (1440 minutes)
- **Claims:**
  - `sub`: User's external_id (UUID)
  - `email`: User's email address
  - `exp`: Expiration timestamp
  - `iat`: Issued at timestamp

---

## Error Codes

| Status Code | Description |
|------------|-------------|
| 200 | OK - Request successful |
| 201 | Created - User successfully registered |
| 400 | Bad Request - Invalid input or email already exists |
| 401 | Unauthorized - Invalid or expired token |
| 404 | Not Found - Resource not found or access denied |
| 500 | Internal Server Error - Server error |

---

## Password Requirements

- Minimum length: 8 characters
- No maximum length restriction
- All characters allowed

---

## Email Requirements

- Must be a valid email format
- Must be unique (no duplicate emails)
- Case-insensitive for comparison

---

## Best Practices

1. **Store tokens securely:**
   - Use httpOnly cookies (preferred)
   - Or secure localStorage with XSS protection

2. **Handle token expiration:**
   - Check for 401 responses
   - Redirect to login page
   - Optionally implement token refresh

3. **Never store passwords:**
   - Only store the JWT token
   - Clear token on logout

4. **Include token in all protected requests:**
   - Use Authorization header
   - Format: `Bearer <token>`

5. **Validate responses:**
   - Check status codes
   - Handle errors gracefully
   - Show user-friendly messages
