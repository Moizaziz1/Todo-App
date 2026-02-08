---
description: "Task list for Frontend Web Application (UI + API Integration) feature implementation"
---

# Tasks: Frontend Web Application (UI + API Integration)

**Input**: Design documents from `/specs/003-frontend-task-ui/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `frontend/` (extends Spec 2 foundation)
- Frontend: Next.js 16+ App Router with TypeScript

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Configure Tailwind CSS and project dependencies

- [X] T001 Install Tailwind CSS dependencies in frontend/package.json
- [X] T002 Create Tailwind configuration in frontend/tailwind.config.js
- [X] T003 [P] Update globals.css with Tailwind directives in frontend/app/globals.css
- [X] T004 [P] Create tasks component directory structure in frontend/components/tasks/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core UI infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 Create dashboard page with auth protection in frontend/app/dashboard/page.tsx
- [X] T006 Create loading skeleton component in frontend/components/tasks/loading-skeleton.tsx
- [X] T007 [P] Create error display component in frontend/components/tasks/error-message.tsx
- [X] T008 [P] Create empty state component in frontend/components/tasks/empty-state.tsx
- [X] T009 Update landing page with navigation links in frontend/app/page.tsx

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - View Task Dashboard (Priority: P1) 🎯 MVP

**Goal**: Enable authenticated users to view their task list with proper loading, error, and empty states

**Independent Test**: Can be fully tested by signing in and verifying the task list displays correctly, including loading state while fetching and empty state when no tasks exist.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T010 [P] [US1] Integration test for dashboard load in frontend/tests/dashboard/test_dashboard_load.test.ts

### Implementation for User Story 1

- [X] T011 [P] [US1] Create TaskDashboard container component in frontend/components/tasks/task-dashboard.tsx
- [X] T012 [US1] Implement task fetching logic with useEffect in frontend/components/tasks/task-dashboard.tsx
- [X] T013 [US1] Create TaskList component in frontend/components/tasks/task-list.tsx
- [X] T014 [US1] Create basic TaskItem component in frontend/components/tasks/task-item.tsx
- [X] T015 [US1] Integrate loading skeleton state in frontend/components/tasks/task-list.tsx
- [X] T016 [US1] Integrate empty state display in frontend/components/tasks/task-list.tsx
- [X] T017 [US1] Integrate error handling with retry in frontend/components/tasks/task-list.tsx
- [X] T018 [US1] Add user session integration for user_id in frontend/components/tasks/task-dashboard.tsx

**Checkpoint**: At this point, User Story 1 should be fully functional - users can view their tasks

---

## Phase 4: User Story 2 - Create New Task (Priority: P1) 🎯 MVP

**Goal**: Enable users to create new tasks via a form with validation

**Independent Test**: Can be fully tested by clicking the create button, entering task details, submitting, and verifying the new task appears in the list.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T019 [P] [US2] Integration test for task creation flow in frontend/tests/tasks/test_create_task.test.ts

### Implementation for User Story 2

- [X] T020 [P] [US2] Create CreateTaskForm component in frontend/components/tasks/create-task-form.tsx
- [X] T021 [US2] Add form state management (title, description) in frontend/components/tasks/create-task-form.tsx
- [X] T022 [US2] Add form validation (title required, length limits) in frontend/components/tasks/create-task-form.tsx
- [X] T023 [US2] Integrate API client createTask method in frontend/components/tasks/create-task-form.tsx
- [X] T024 [US2] Add success handling (update task list) in frontend/components/tasks/task-dashboard.tsx
- [X] T025 [US2] Add error handling with display in frontend/components/tasks/create-task-form.tsx
- [X] T026 [US2] Add form toggle button to dashboard in frontend/components/tasks/task-dashboard.tsx

**Checkpoint**: At this point, User Stories 1 AND 2 should both work - users can view and create tasks

---

## Phase 5: User Story 3 - Complete/Uncomplete Task (Priority: P1) 🎯 MVP

**Goal**: Enable users to toggle task completion with optimistic UI updates

**Independent Test**: Can be fully tested by clicking the completion toggle on a task and verifying the visual state changes and persists.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T027 [P] [US3] Integration test for task completion toggle in frontend/tests/tasks/test_toggle_complete.test.ts

### Implementation for User Story 3

- [X] T028 [P] [US3] Add completion checkbox to TaskItem in frontend/components/tasks/task-item.tsx
- [X] T029 [US3] Implement toggle handler with optimistic update in frontend/components/tasks/task-item.tsx
- [X] T030 [US3] Integrate API client completeTask method in frontend/components/tasks/task-item.tsx
- [X] T031 [US3] Add visual distinction for completed tasks (strikethrough) in frontend/components/tasks/task-item.tsx
- [X] T032 [US3] Implement error handling with rollback in frontend/components/tasks/task-item.tsx
- [X] T033 [US3] Add loading indicator during toggle operation in frontend/components/tasks/task-item.tsx

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work - full MVP operational

---

## Phase 6: User Story 4 - Edit Task (Priority: P2)

**Goal**: Enable users to edit existing task title and description

**Independent Test**: Can be fully tested by clicking edit on a task, modifying details, saving, and verifying changes appear in the list.

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [ ] T034 [P] [US4] Integration test for task editing flow in frontend/tests/tasks/test_edit_task.test.ts

### Implementation for User Story 4

- [X] T035 [P] [US4] Create EditTaskModal component in frontend/components/tasks/edit-task-modal.tsx
- [X] T036 [US4] Add modal state management (open/close) in frontend/components/tasks/task-dashboard.tsx
- [X] T037 [US4] Pre-fill form with current task data in frontend/components/tasks/edit-task-modal.tsx
- [X] T038 [US4] Add validation matching CreateTaskForm in frontend/components/tasks/edit-task-modal.tsx
- [X] T039 [US4] Integrate API client updateTask method in frontend/components/tasks/edit-task-modal.tsx
- [X] T040 [US4] Update task in list on successful save in frontend/components/tasks/task-dashboard.tsx
- [X] T041 [US4] Add edit button to TaskItem in frontend/components/tasks/task-item.tsx

**Checkpoint**: At this point, User Stories 1-4 should all work - users can view, create, complete, and edit tasks

---

## Phase 7: User Story 5 - Delete Task (Priority: P2)

**Goal**: Enable users to delete tasks with confirmation dialog

**Independent Test**: Can be fully tested by clicking delete, confirming, and verifying the task is removed from the list.

### Tests for User Story 5 (OPTIONAL - only if tests requested) ⚠️

- [ ] T042 [P] [US5] Integration test for task deletion flow in frontend/tests/tasks/test_delete_task.test.ts

### Implementation for User Story 5

- [X] T043 [P] [US5] Create DeleteConfirmationDialog component in frontend/components/tasks/delete-confirmation.tsx
- [X] T044 [US5] Add dialog state management in frontend/components/tasks/task-dashboard.tsx
- [X] T045 [US5] Implement confirm action with API call in frontend/components/tasks/delete-confirmation.tsx
- [X] T046 [US5] Remove task from list on successful delete in frontend/components/tasks/task-dashboard.tsx
- [X] T047 [US5] Add error handling for delete failures in frontend/components/tasks/delete-confirmation.tsx
- [X] T048 [US5] Add delete button to TaskItem in frontend/components/tasks/task-item.tsx

**Checkpoint**: At this point, User Stories 1-5 should all work - full CRUD functionality operational

---

## Phase 8: User Story 6 - Responsive Layout (Priority: P3)

**Goal**: Ensure the interface adapts seamlessly to desktop, tablet, and mobile devices

**Independent Test**: Can be fully tested by resizing the browser or using device emulation to verify the layout adapts appropriately.

### Tests for User Story 6 (OPTIONAL - only if tests requested) ⚠️

- [ ] T049 [P] [US6] Visual regression test for responsive breakpoints in frontend/tests/visual/test_responsive.test.ts

### Implementation for User Story 6

- [X] T050 [P] [US6] Add mobile-first responsive classes to TaskDashboard in frontend/components/tasks/task-dashboard.tsx
- [X] T051 [P] [US6] Add responsive layout to TaskList in frontend/components/tasks/task-list.tsx
- [X] T052 [P] [US6] Add responsive styling to TaskItem in frontend/components/tasks/task-item.tsx
- [X] T053 [P] [US6] Ensure touch targets are 44x44px minimum in frontend/components/tasks/task-item.tsx
- [X] T054 [US6] Add responsive breakpoints to CreateTaskForm in frontend/components/tasks/create-task-form.tsx
- [X] T055 [US6] Add responsive styling to EditTaskModal in frontend/components/tasks/edit-task-modal.tsx

**Checkpoint**: All user stories should now be independently functional and responsive

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T056 [P] Add visual feedback animations (fade, slide) across components
- [X] T057 [P] Standardize error message formatting in all components
- [X] T058 [P] Add loading states to all async actions
- [X] T059 [P] Update dashboard header with sign-out button in frontend/components/tasks/task-dashboard.tsx
- [X] T060 Code cleanup and prop types verification
- [X] T061 Accessibility review (ARIA labels, keyboard nav)
- [X] T062 Run quickstart validation with full UI flow

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-8)**: All depend on Foundational phase completion
  - US1 (View Dashboard) must complete first - provides base for other stories
  - US2 (Create Task) and US3 (Toggle Complete) can run in parallel after US1
  - US4 (Edit Task) and US5 (Delete Task) can run in parallel after US1
  - US6 (Responsive Layout) can run in parallel with any user story
- **Polish (Phase 9)**: Depends on all user stories being complete

### User Story Dependencies

```
US1 (View Dashboard) ──┬──► US2 (Create Task)
                       ├──► US3 (Toggle Complete)
                       ├──► US4 (Edit Task)
                       └──► US5 (Delete Task)

US6 (Responsive) ──────► (Runs in parallel with all)
```

### Parallel Execution Opportunities

**Within Setup Phase:**
- T001, T002, T003, T004 can all run in parallel (independent config files)

**Within Foundational Phase:**
- T006, T007, T008 can run in parallel (independent components)

**Within User Story Phases:**
- After US1 completes: US2, US3, US4, US5 can all run in parallel
- US6 (Responsive) can run in parallel with any user story

---

## Implementation Strategy

### MVP Scope (Recommended First Delivery)

**Phases 1-5 (US1 + US2 + US3)**: Core task management
- Users can view their task list
- Users can create new tasks
- Users can mark tasks as complete
- Loading, error, and empty states work

### Incremental Delivery

1. **Increment 1**: Setup + Foundational (T001-T009)
2. **Increment 2**: View Dashboard (T011-T018)
3. **Increment 3**: Create Task (T020-T026)
4. **Increment 4**: Toggle Complete (T028-T033)
5. **Increment 5**: Edit Task (T035-T041)
6. **Increment 6**: Delete Task (T043-T048)
7. **Increment 7**: Responsive + Polish (T050-T062)

### File Touch Summary

| File | Tasks |
|------|-------|
| frontend/app/dashboard/page.tsx | T005 |
| frontend/components/tasks/task-dashboard.tsx | T011, T012, T018, T024, T026, T036, T040, T044, T046, T050, T059 |
| frontend/components/tasks/task-list.tsx | T013, T015, T016, T017, T051 |
| frontend/components/tasks/task-item.tsx | T014, T028, T029, T030, T031, T032, T033, T041, T048, T052, T053 |
| frontend/components/tasks/create-task-form.tsx | T020, T021, T022, T023, T025, T054 |
| frontend/components/tasks/edit-task-modal.tsx | T035, T037, T038, T039, T055 |
| frontend/components/tasks/delete-confirmation.tsx | T043, T045, T047 |
| frontend/components/tasks/loading-skeleton.tsx | T006 |
| frontend/components/tasks/error-message.tsx | T007 |
| frontend/components/tasks/empty-state.tsx | T008 |
