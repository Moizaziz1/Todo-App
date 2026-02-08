# Research: Frontend Web Application (UI + API Integration)

**Date**: 2026-02-07
**Feature**: 003-frontend-task-ui

## Research Summary

This document consolidates research findings for building a responsive task management UI in Next.js that integrates with the JWT-secured backend API.

---

## Decision 1: Component Architecture

**Decision**: Use React Server Components (RSC) with client components for interactivity

**Rationale**:
- Next.js 16+ App Router defaults to server components
- Task list fetching can happen on server for better performance
- Client components only where needed (forms, toggles, modals)
- Reduces JavaScript bundle size

**Alternatives Considered**:
- Full client-side rendering: Simpler but less performant
- Full server-side rendering: More complex, not needed for this use case

**Implementation Pattern**:
```typescript
// Server component for layout
export default async function DashboardPage() {
  return <TaskDashboard />
}

// Client component for interactive task list
"use client"
export function TaskDashboard() {
  // Handle state, API calls, interactions
}
```

---

## Decision 2: State Management Strategy

**Decision**: Use React hooks (useState, useEffect) with API client - no external state library

**Rationale**:
- Simple application state (tasks list, loading, errors)
- React hooks sufficient for local component state
- API client already implemented in Spec 2
- Avoids complexity of Redux/Zustand for small scope

**Alternatives Considered**:
- Context API: Overkill for single-page state
- Redux: Too complex for this scope
- TanStack Query: Good but adds dependency

**State Structure**:
```typescript
const [tasks, setTasks] = useState<Task[]>([])
const [isLoading, setIsLoading] = useState(true)
const [error, setError] = useState<string | null>(null)
```

---

## Decision 3: Styling Approach

**Decision**: Use Tailwind CSS utility classes for responsive design

**Rationale**:
- Already configured in Next.js projects
- Responsive classes built-in (`sm:`, `md:`, `lg:`)
- Quick development for hackathon
- Mobile-first by default

**Responsive Breakpoints**:
- Mobile: default (< 640px)
- Tablet: `sm:` (≥ 640px)
- Desktop: `md:` and `lg:` (≥ 768px, ≥ 1024px)

**Touch Targets**: Minimum 44x44px using `min-h-[44px] min-w-[44px]` or equivalent

**Alternatives Considered**:
- CSS Modules: More boilerplate
- Styled Components: Requires setup
- Plain CSS: Less maintainable

---

## Decision 4: Form Handling

**Decision**: Use controlled components with inline validation

**Rationale**:
- React best practice for form state
- Immediate validation feedback
- Easy to integrate with API calls
- No form library needed for simple forms

**Validation Strategy**:
- Client-side: Title required, max 255 characters
- Server-side: Backend validates and returns 422 on error
- Display validation errors inline below fields

**Implementation Pattern**:
```typescript
const [title, setTitle] = useState("")
const [errors, setErrors] = useState<{title?: string}>({})

const validate = () => {
  if (!title.trim()) {
    setErrors({ title: "Title is required" })
    return false
  }
  return true
}
```

---

## Decision 5: Modal/Dialog Strategy

**Decision**: Use native HTML dialog element for confirmation dialogs

**Rationale**:
- Modern browser support (95%+)
- No additional dependencies
- Built-in backdrop and focus management
- Accessible by default

**Alternatives Considered**:
- Headless UI: Good but adds dependency
- Radix UI: More features than needed
- Custom modal: More work

---

## Decision 6: Error Handling UX

**Decision**: Display errors inline with retry actions

**Error Display Strategy**:
| Error Type | Display | Action |
|------------|---------|--------|
| API network error | Banner with "Retry" button | Allow user to retry |
| Validation error | Inline below field | Prevent submission |
| Auth error (401) | Redirect to sign-in | Automatic redirect |
| Not found (404) | Inline message | Remove from UI |

**Implementation**:
```typescript
{error && (
  <div className="p-4 bg-red-50 text-red-600 rounded-md">
    {error}
    <button onClick={retry}>Retry</button>
  </div>
)}
```

---

## Decision 7: Loading State Pattern

**Decision**: Use skeleton screens for initial load, spinners for actions

**Rationale**:
- Skeleton screens reduce perceived wait time
- Spinners for buttons during save/delete operations
- Better UX than full-page loaders

**Implementation**:
- Initial load: Skeleton items (3-5 placeholder cards)
- Button actions: Disabled state + spinner icon
- Inline operations: Show loading indicator next to item

---

## Technology Summary

### Frontend Stack
- **Framework**: Next.js 16+ (App Router)
- **UI Components**: React functional components with hooks
- **Styling**: Tailwind CSS utility classes
- **Forms**: Controlled components with inline validation
- **Modals**: HTML `<dialog>` element
- **Auth**: Better Auth client (from Spec 2)
- **API**: fetch with JWT attachment (from Spec 2)

### Component Architecture
- Server components: Page layouts, static content
- Client components: Task list, forms, interactive elements
- No external state management library

### Responsive Strategy
- Mobile-first design using Tailwind breakpoints
- Touch targets: Minimum 44x44px
- Responsive breakpoints: sm (640px), md (768px), lg (1024px)

---

## References

- [Next.js App Router Documentation](https://nextjs.org/docs/app)
- [React Hooks Documentation](https://react.dev/reference/react)
- [Tailwind CSS Responsive Design](https://tailwindcss.com/docs/responsive-design)
- [HTML Dialog Element](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/dialog)
