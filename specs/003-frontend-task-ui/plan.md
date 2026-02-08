# Implementation Plan: Frontend Web Application (UI + API Integration)

**Branch**: `003-frontend-task-ui` | **Date**: 2026-02-07 | **Spec**: [specs/003-frontend-task-ui/spec.md](spec.md)
**Input**: Feature specification from `/specs/003-frontend-task-ui/spec.md`

## Summary

Build a responsive Next.js task management dashboard that allows authenticated users to view, create, update, delete, and complete tasks through a JWT-secured backend API. The UI handles loading, error, and empty states while providing visual feedback for all operations. The interface adapts seamlessly to desktop and mobile devices using Tailwind CSS.

## Technical Context

**Language/Version**: TypeScript 5.0+, Node.js 18+
**Primary Dependencies**: Next.js 14+, React 18, Better Auth (from Spec 2), Tailwind CSS
**Storage**: Client-side state management with React hooks, API client from Spec 2
**Testing**: Jest, React Testing Library (optional)
**Target Platform**: Modern web browsers (Chrome, Firefox, Safari, Edge)
**Project Type**: web (frontend only - extends Spec 2 foundation)
**Performance Goals**: Dashboard load < 3s, task operations < 1s, visual feedback < 200ms
**Constraints**: Client-side rendering, JWT token from Better Auth, API from Spec 1, mobile-first responsive
**Scale/Scope**: Single-user dashboard view, 100+ tasks displayable

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Spec-Driven Development**: Following spec → plan → tasks → Claude Code workflow (PASSED)
- **Full-Stack Architecture**: Frontend UI layer cleanly separated from backend API (PASSED)
- **Security-First Design**: Uses JWT authentication from Spec 2, redirects unauthenticated users (PASSED)
- **REST API Conventions**: Integrates with existing REST API endpoints from Spec 1 (PASSED)
- **Data Persistence Requirement**: Uses backend API for all persistence (no local storage of task data) (PASSED)
- **Frontend-Backend Separation**: Next.js frontend communicates via API client with JWT (PASSED)

## Project Structure

### Documentation (this feature)

```text
specs/003-frontend-task-ui/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   └── ui-components.yaml
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
frontend/
├── app/
│   ├── api/auth/[...all]/route.ts    # Existing (Spec 2)
│   ├── (auth)/
│   │   ├── sign-in/page.tsx          # Existing (Spec 2)
│   │   └── sign-up/page.tsx          # Existing (Spec 2)
│   ├── dashboard/
│   │   └── page.tsx                  # NEW: Main task dashboard
│   ├── layout.tsx                    # Existing (Spec 2)
│   ├── globals.css                   # UPDATED: Add custom styles
│   └── page.tsx                      # UPDATED: Landing page with links
├── components/
│   ├── auth/                         # Existing (Spec 2)
│   └── tasks/                        # NEW: Task UI components
│       ├── task-dashboard.tsx        # Main dashboard container
│       ├── task-list.tsx             # Task list with states
│       ├── task-item.tsx             # Individual task display
│       ├── create-task-form.tsx      # Task creation form
│       ├── edit-task-modal.tsx       # Task editing modal
│       ├── delete-confirmation.tsx   # Delete confirmation dialog
│       └── loading-skeleton.tsx      # Loading state component
├── lib/
│   ├── auth.ts                       # Existing (Spec 2)
│   ├── auth-client.ts                # Existing (Spec 2)
│   └── api-client.ts                 # Existing (Spec 2)
├── tailwind.config.js                # NEW: Tailwind configuration
└── .env.local.example                # Existing (Spec 2)
```

**Structure Decision**: Extends the Next.js frontend from Spec 2 by adding task management UI components in a new `components/tasks/` directory and a dashboard page. Reuses existing auth infrastructure and API client.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |

## Key Design Decisions

### 1. Component Architecture: Server + Client Components

**Decision**: Use React Server Components for layout with client components for interactivity

**Rationale**:
- Next.js App Router defaults to server components
- Reduces JavaScript bundle size
- Client components only where needed (forms, interactive elements)
- Better initial page load performance

**Implementation**: Dashboard page is client component since it manages state and API calls

---

### 2. State Management: React Hooks Only

**Decision**: Use useState and useEffect without external state library

**Rationale**:
- Simple application with localized state (tasks list, forms)
- Reduces dependencies and complexity
- Sufficient for single-page dashboard
- Easy to understand and maintain

**State Structure**: Tasks array, loading boolean, error string per component

---

### 3. Styling: Tailwind CSS Utility Classes

**Decision**: Use Tailwind CSS for all styling

**Rationale**:
- Built-in responsive utilities (`sm:`, `md:`, `lg:`)
- Fast development with utility classes
- Mobile-first by default
- No custom CSS needed

**Responsive**: Mobile (default), Tablet (sm: 640px), Desktop (md: 768px, lg: 1024px)

---

### 4. Form Strategy: Controlled Components

**Decision**: Use React controlled components with inline validation

**Rationale**:
- React best practice for forms
- Immediate validation feedback
- Easy state management
- No form library overhead

**Validation**: Client-side (title required, length limits) + server-side (backend 422 responses)

---

### 5. Modal Implementation: Native HTML Dialog

**Decision**: Use `<dialog>` element for modals and confirmations

**Rationale**:
- Native browser support (95%+)
- No additional dependencies
- Built-in backdrop and focus trap
- Accessible by default

**Use Cases**: Edit task modal, delete confirmation dialog

---

### 6. Error Handling: Inline with Retry

**Decision**: Display errors inline with actionable retry buttons

**Error Types**:
- Network errors: Banner with "Retry" button
- Validation errors: Inline below field
- Auth errors (401): Automatic redirect to sign-in (handled by API client)
- Not found (404): Remove from UI

---

### 7. Loading States: Skeleton Screens + Spinners

**Decision**: Use skeleton screens for initial load, spinners for actions

**Rationale**:
- Skeleton screens reduce perceived wait time
- Better UX than blank screen or full-page spinner
- Spinners on buttons during save/delete operations

**Implementation**: 3-5 skeleton task cards during initial fetch

---

## Implementation Phases

### Phase 1: Dashboard Foundation
- Create dashboard page structure
- Implement task list container
- Add loading skeleton component
- Add empty state message

### Phase 2: Task Display
- Create TaskItem component
- Display task title and completion status
- Style completed vs incomplete tasks
- Add responsive layout

### Phase 3: Task Creation
- Create task creation form component
- Add form validation
- Integrate with API client
- Handle success/error states

### Phase 4: Task Completion
- Add completion toggle to TaskItem
- Implement optimistic UI update
- Call API to persist change
- Handle errors with rollback

### Phase 5: Task Editing
- Create edit task modal component
- Pre-fill form with current data
- Implement save functionality
- Update task in list

### Phase 6: Task Deletion
- Create delete confirmation dialog
- Implement delete action
- Remove task from list
- Handle errors

### Phase 7: Polish & Responsive
- Ensure mobile responsiveness (320px+)
- Add touch-friendly targets (44x44px)
- Implement visual feedback for all actions
- Test across different screen sizes

---

## Dependencies

### External Dependencies
- Next.js: ^14.0.0 (npm - already installed)
- React: ^18.2.0 (npm - already installed)
- Tailwind CSS: Configured in Next.js
- Better Auth: Already installed (Spec 2)

### Internal Dependencies
- Spec 1: Backend task API endpoints
- Spec 2: Better Auth setup, API client with JWT, auth pages

---

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| API client errors not handled | High - Poor UX | Comprehensive error handling in api-client.ts |
| Session expiration during use | Medium - User interruption | Detect 401 and redirect with message |
| Mobile layout issues | Medium - Reduced usability | Test with device emulation, use Tailwind responsive utilities |
| Slow task list rendering | Low - Performance issue | Limit initial display to 50 tasks, add pagination if needed |

---

## Success Metrics

- [ ] Dashboard loads in < 3 seconds
- [ ] Task creation completes in < 30 seconds
- [ ] Completion toggle responds in < 1 second
- [ ] All errors display user-friendly messages
- [ ] Interface works on 320px+ screens
- [ ] Touch targets are ≥ 44x44px on mobile
- [ ] Visual feedback within 200ms for all actions
