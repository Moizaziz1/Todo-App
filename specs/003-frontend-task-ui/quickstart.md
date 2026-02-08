# Quickstart Guide: Frontend Web Application (UI + API Integration)

## Prerequisites

- Node.js 18+
- Backend API running (Spec 1)
- Better Auth configured (Spec 2)
- Database accessible from both frontend and backend

## Setup Instructions

### 1. Navigate to Frontend Directory

```bash
cd frontend
```

### 2. Install Dependencies

```bash
npm install
```

This installs:
- Next.js 14+
- React 18+
- Better Auth
- Tailwind CSS
- TypeScript

### 3. Environment Configuration

Create `.env.local` from the example:

```bash
cp .env.local.example .env.local
```

Required variables:
```env
BETTER_AUTH_SECRET=<your-32-character-secret>
BETTER_AUTH_URL=http://localhost:3000
DATABASE_URL=<your-neon-postgresql-url>
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

**CRITICAL**: `BETTER_AUTH_SECRET` must match `SECRET_KEY` in backend.

### 4. Run Database Migrations

Initialize Better Auth tables:

```bash
npx @better-auth/cli migrate
```

### 5. Start Development Server

```bash
npm run dev
```

The frontend will be available at http://localhost:3000

---

## Testing the Complete Flow

### 1. Sign Up

1. Navigate to http://localhost:3000
2. Click "Sign Up"
3. Enter email and password (min 8 characters)
4. Submit form
5. You should be redirected to dashboard

### 2. View Dashboard

1. After signing in, you'll see the task dashboard
2. If no tasks exist, you'll see an empty state message
3. If tasks exist, you'll see your task list

### 3. Create a Task

1. Click "Create Task" button
2. Enter a task title (required)
3. Optionally enter description
4. Click "Create"
5. Task appears in list immediately

### 4. Toggle Task Completion

1. Click the checkbox next to a task
2. Task appearance changes (strikethrough for completed)
3. Change persists after page refresh

### 5. Edit a Task

1. Click "Edit" button on a task
2. Modify title or description
3. Click "Save"
4. Changes appear immediately in list

### 6. Delete a Task

1. Click "Delete" button on a task
2. Confirm deletion in dialog
3. Task is removed from list

### 7. Sign Out

1. Click "Sign Out" in header
2. Redirected to sign-in page
3. Dashboard is no longer accessible without signing in

---

## Verification Checklist

- [ ] Sign-up creates account and redirects to dashboard
- [ ] Sign-in authenticates and redirects to dashboard
- [ ] Dashboard shows loading state while fetching tasks
- [ ] Dashboard shows empty state when no tasks exist
- [ ] Dashboard shows task list when tasks exist
- [ ] Create task form validates required fields
- [ ] New tasks appear immediately in list
- [ ] Completion toggle updates task status visually
- [ ] Edit modal pre-fills with current task data
- [ ] Edit saves update and refreshes list
- [ ] Delete shows confirmation dialog
- [ ] Delete removes task from list
- [ ] All API errors show user-friendly messages
- [ ] Interface is usable on mobile (320px+ width)
- [ ] Sign-out clears session and redirects

---

## Common Issues

### 1. API Connection Errors

**Symptom**: "Failed to load tasks" or similar errors

**Solutions**:
- Verify backend is running on correct port (8000)
- Check `NEXT_PUBLIC_API_URL` in `.env.local`
- Verify CORS is configured in backend to allow `http://localhost:3000`
- Check browser console for detailed error messages

### 2. Authentication Failures

**Symptom**: Constant redirects to sign-in, 401 errors

**Solutions**:
- Verify `BETTER_AUTH_SECRET` matches `SECRET_KEY` in backend
- Check JWT token is being sent in Authorization header (browser DevTools → Network)
- Verify Better Auth database tables exist
- Confirm user signed in successfully (check browser cookies)

### 3. Tasks Not Appearing

**Symptom**: Empty state shows even after creating tasks

**Solutions**:
- Check browser console for API errors
- Verify JWT token contains correct user_id
- Check backend database for tasks with that user_id
- Confirm frontend is calling correct API endpoint

### 4. Styling Issues

**Symptom**: Layout broken or not responsive

**Solutions**:
- Verify Tailwind CSS is configured in `tailwind.config.js`
- Check `globals.css` includes Tailwind directives
- Clear `.next` cache and restart dev server
- Test on different screen sizes using browser DevTools

---

## Project Structure After Setup

```
frontend/
├── app/
│   ├── api/auth/[...all]/route.ts    # Better Auth handler (Spec 2)
│   ├── (auth)/
│   │   ├── sign-in/page.tsx          # Sign-in page (Spec 2)
│   │   └── sign-up/page.tsx          # Sign-up page (Spec 2)
│   ├── dashboard/
│   │   └── page.tsx                  # Task dashboard (NEW)
│   ├── layout.tsx                    # Root layout with auth provider
│   ├── globals.css                   # Tailwind imports
│   └── page.tsx                      # Landing page
├── components/
│   ├── auth/                         # Auth components (Spec 2)
│   └── tasks/                        # Task UI components (NEW)
│       ├── task-list.tsx
│       ├── task-item.tsx
│       ├── create-task-form.tsx
│       ├── edit-task-modal.tsx
│       └── delete-confirmation.tsx
├── lib/
│   ├── auth.ts                       # Better Auth config (Spec 2)
│   ├── auth-client.ts                # Auth client (Spec 2)
│   └── api-client.ts                 # API client with JWT (Spec 2)
├── package.json
├── tsconfig.json
├── tailwind.config.js
└── .env.local
```

---

## Development Workflow

1. **Start backend**: `cd backend && uvicorn src.main:app --reload`
2. **Start frontend**: `cd frontend && npm run dev`
3. **Open browser**: http://localhost:3000
4. **Test flow**: Sign up → Dashboard → Create task → Manage tasks → Sign out

---

## Performance Expectations

- Dashboard load: < 3 seconds
- Task creation: < 30 seconds end-to-end
- Completion toggle: < 1 second response
- All actions: Visual feedback within 200ms
