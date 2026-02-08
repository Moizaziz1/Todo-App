# Data Model: Frontend Web Application (UI + API Integration)

## Entity: Task (UI Model)

**Description**: Represents a task as displayed and manipulated in the frontend UI. Maps to the Task entity from backend API (Spec 1).

**Fields**:
- `id`: Number - Task primary key from backend
- `external_id`: String (UUID) - External identifier
- `title`: String (max 255) - Task title displayed in list
- `description`: String (optional, max 1000) - Task details
- `completed`: Boolean - Completion status, visually indicated
- `user_id`: String - User identifier (from JWT token)
- `priority`: String (optional) - Priority level (low/normal/high)
- `due_date`: String (optional) - ISO date string
- `created_at`: String - ISO timestamp
- `updated_at`: String - ISO timestamp

**Display Rules**:
- Completed tasks: Show with strikethrough, muted color, checkmark icon
- Incomplete tasks: Show with normal styling, empty checkbox
- Long titles: Truncate with ellipsis on mobile
- Empty description: Hide description field in display

---

## Entity: UI State

**Description**: Represents the various states the UI can be in during data operations.

**States**:
- **Loading**: Fetching data from API
  - Display: Skeleton screens or loading spinner
  - User actions: Disabled
- **Error**: API call failed
  - Display: Error message with retry option
  - User actions: Limited to retry
- **Empty**: No tasks exist
  - Display: Empty state message with create prompt
  - User actions: Can create new task
- **Success**: Data loaded and displayed
  - Display: Task list with all actions available
  - User actions: Full CRUD operations available
- **Pending**: Operation in progress (save, delete)
  - Display: Loading indicator on affected element
  - User actions: Disabled for that element

**Transitions**:
```
Initial → Loading → (Success | Error | Empty)
Success → Pending → (Success | Error)
Error → Loading (on retry)
Empty → Success (after create)
```

---

## Entity: Form State

**Description**: Represents the state of task creation and editing forms.

**Fields**:
- `title`: String - Current title input value
- `description`: String - Current description input value
- `priority`: String (optional) - Selected priority
- `errors`: Object - Validation errors by field
- `isSubmitting`: Boolean - Whether form is being submitted

**Validation Rules**:
- Title must not be empty (trimmed)
- Title must be ≤ 255 characters
- Description must be ≤ 1000 characters if provided
- Validate on blur and on submit

---

## Entity: Modal State

**Description**: Represents the state of confirmation dialogs and modals.

**Types**:
- **Delete Confirmation**: Shown before deleting a task
  - Data: Task ID and title being deleted
  - Actions: Confirm, Cancel
- **Edit Form**: Shown when editing a task
  - Data: Current task details
  - Actions: Save, Cancel

**State Management**:
```typescript
const [deleteDialogOpen, setDeleteDialogOpen] = useState(false)
const [taskToDelete, setTaskToDelete] = useState<number | null>(null)
const [editingTask, setEditingTask] = useState<Task | null>(null)
```

---

## Component Hierarchy

```
App (layout)
├── AuthProvider (from Spec 2)
└── Routes
    ├── /dashboard (protected)
    │   └── TaskDashboard
    │       ├── TaskList
    │       │   └── TaskItem (multiple)
    │       │       ├── CompletionToggle
    │       │       ├── EditButton
    │       │       └── DeleteButton
    │       ├── CreateTaskForm
    │       ├── EditTaskModal
    │       └── DeleteConfirmationDialog
    ├── /sign-in (from Spec 2)
    └── /sign-up (from Spec 2)
```

---

## Data Flow

### Task List Load
```
User navigates to dashboard
  → Check authentication (redirect if needed)
  → Show loading skeleton
  → Fetch tasks from API (with JWT)
  → Update state with tasks
  → Render task list
```

### Task Creation
```
User clicks "Create Task"
  → Show create form
  → User enters title & description
  → Validate input
  → Submit to API (with JWT)
  → Add new task to state
  → Close form
  → Show success feedback
```

### Task Completion Toggle
```
User clicks completion checkbox
  → Optimistically update UI
  → Call API to update task (with JWT)
  → On success: Keep optimistic update
  → On failure: Revert UI + show error
```

### Task Deletion
```
User clicks delete button
  → Show confirmation dialog
  → User confirms
  → Call API to delete task (with JWT)
  → Remove from state
  → Close dialog
  → Show success feedback
```

---

## API Integration Points

All API calls use the `taskApi` client from Spec 2:

| UI Action | API Method | Endpoint |
|-----------|------------|----------|
| Load tasks | `taskApi.getTasks(userId)` | GET /users/{id}/tasks |
| Create task | `taskApi.createTask(userId, data)` | POST /users/{id}/tasks |
| Update task | `taskApi.updateTask(userId, taskId, data)` | PUT /users/{id}/tasks/{taskId} |
| Toggle complete | `taskApi.completeTask(userId, taskId, completed)` | PATCH /users/{id}/tasks/{taskId}/complete |
| Delete task | `taskApi.deleteTask(userId, taskId)` | DELETE /users/{id}/tasks/{taskId} |

**Authentication**:
- JWT token automatically attached by API client
- 401 responses trigger redirect to sign-in
- User ID obtained from Better Auth session
