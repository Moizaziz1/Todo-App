# Data Model: Authentication & API Security

## Entity: User

**Description**: Represents an authenticated account holder in the system. Users are created via the Better Auth signup flow and stored in both the frontend (Better Auth database) and backend (for task ownership reference).

**Fields**:
- `id`: String (UUID), Primary Key - Matches Better Auth user ID
- `email`: String (max 255), Required, Unique - User's email address
- `name`: String (max 255), Optional - User's display name
- `created_at`: DateTime, Auto-generated - Account creation timestamp
- `updated_at`: DateTime, Auto-generated - Last profile update timestamp

**Validation Rules**:
- Email must be valid format (validated by Better Auth)
- Email must be unique across all users
- ID must match the ID issued by Better Auth

**State Transitions**:
- Created when user signs up via Better Auth
- Email cannot be changed after creation (in this scope)

---

## Entity: JWT Token (Transient)

**Description**: Represents authentication credentials issued by Better Auth. Not stored in database - exists only in transit between frontend and backend.

**Claims (Payload)**:
- `sub`: String - User ID (subject claim)
- `email`: String - User's email address
- `iat`: Integer - Issued-at timestamp (Unix epoch)
- `exp`: Integer - Expiration timestamp (Unix epoch)
- `iss`: String - Issuer (Better Auth URL)

**Validation Rules**:
- Token must be signed with correct secret key
- Token must not be expired (`exp` > current time)
- Subject (`sub`) must be present and non-empty
- Signature must verify with HS256 algorithm

---

## Entity: Task (Updated)

**Description**: Existing task entity from Spec 1, updated to enforce user ownership via authenticated user ID from JWT token.

**Relationship Change**:
- `user_id` field now references authenticated user from JWT
- No longer accepted as request body parameter
- Extracted from JWT token claims on each request

**Access Control**:
- Create: User ID set from JWT token, not from request
- Read: Only tasks where `task.user_id == token.sub`
- Update: Only tasks where `task.user_id == token.sub`
- Delete: Only tasks where `task.user_id == token.sub`

---

## Relationships

### User → Task (One-to-Many)
- One user can have many tasks
- Tasks are always associated with exactly one user
- User ID derived from JWT token, not request parameters

### Better Auth User → Backend User (One-to-One)
- Better Auth manages authentication and stores user credentials
- Backend stores user reference for task ownership
- IDs are synchronized between systems

---

## Indexes

- Index on `User.email` for unique constraint enforcement
- Index on `User.id` for quick user lookup during token validation
- Existing index on `Task.user_id` supports user-scoped queries

---

## Sequence Diagram: Authentication Flow

```
User        Frontend        Better Auth      Backend API
 │              │                │                │
 │──Sign Up────►│                │                │
 │              │──Create User──►│                │
 │              │◄──Session──────│                │
 │              │──Sync User────────────────────►│
 │              │◄──────────────────────OK───────│
 │              │                │                │
 │──Sign In────►│                │                │
 │              │──Authenticate─►│                │
 │              │◄──Session+JWT──│                │
 │◄─JWT Token───│                │                │
 │              │                │                │
 │──API Request─┼─────────────────────Bearer────►│
 │              │                │      │        │
 │              │                │      │Verify  │
 │              │                │      │JWT     │
 │              │                │      ▼        │
 │◄─────────────┼────────────────────Response────│
```
