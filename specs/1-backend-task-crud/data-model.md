# Data Model: Backend API & Database (Core CRUD)

## Entity: Task

**Description**: Represents a unit of work or activity to be completed, associated with a specific user for data isolation.

**Fields**:
- `id`: Integer, Primary Key, Auto-increment
- `title`: String (max 255), Required, Task title
- `description`: String (optional, max 1000), Task description/details
- `completed`: Boolean, Default False, Completion status
- `user_id`: Integer, Required, Foreign Key reference to User
- `created_at`: DateTime, Auto-generated, Timestamp when task was created
- `updated_at`: DateTime, Auto-generated, Timestamp when task was last updated

**Validation Rules**:
- Title must not be empty
- Title must be between 1-255 characters
- Description must be under 1000 characters if provided
- user_id must reference an existing user (when user system is implemented)
- completed field must be boolean value

**State Transitions**:
- Created with `completed=False`
- Can be updated to `completed=True` or `completed=False`
- Cannot change `user_id` after creation

## Entity: User (Reference)

**Description**: Represents a system user, identified by user_id which serves as the primary mechanism for data isolation and access control.

**Fields**:
- `id`: Integer, Primary Key, Auto-increment

**Note**: Full user entity details are out of scope for this specification but referenced for relationship mapping.

## Relationships

- **One-to-Many**: User (1) → Task (Many)
  - One user can have many tasks
  - Tasks are always associated with exactly one user

## Constraints

- All tasks must have an associated user_id
- Users can only access/modify tasks associated with their user_id
- Task titles must be unique within the context of a single user (optional constraint)

## Indexes

- Index on `user_id` for efficient filtering
- Composite index on `(user_id, created_at)` for efficient querying
- Index on `completed` for efficient filtering of completed/incomplete tasks