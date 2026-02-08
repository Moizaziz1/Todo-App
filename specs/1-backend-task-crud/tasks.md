---
description: "Task list for Backend API & Database (Core CRUD) feature implementation"
---

# Tasks: Backend API & Database (Core CRUD)

**Input**: Design documents from `/specs/1-backend-task-crud/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create backend project structure per implementation plan
- [X] T002 Initialize Python project with FastAPI, SQLModel, Pydantic dependencies in backend/requirements.txt
- [X] T003 [P] Configure linting (flake8, black) and formatting tools in backend/pyproject.toml
- [X] T004 Create backend/src directory structure with models/, services/, api/, config/ subdirectories

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 Setup database schema and migrations framework with Alembic in backend/alembic/
- [X] T006 [P] Implement database connection management in backend/src/services/database.py
- [X] T007 [P] Create base settings configuration in backend/src/config/settings.py
- [X] T008 Create base models that all stories depend on in backend/src/models/__init__.py
- [X] T009 Configure error handling and logging infrastructure in backend/src/api/deps.py
- [X] T010 Setup environment configuration management with .env.example
- [X] T011 Initialize FastAPI application in backend/src/main.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create Task (Priority: P1) 🎯 MVP

**Goal**: Enable creating new tasks through the API and persisting them in the database with user_id association

**Independent Test**: Can be fully tested by making POST requests to the tasks endpoint with a user_id and task details, and verifying the task is stored in the database with the correct user association.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T012 [P] [US1] Contract test for POST /users/{user_id}/tasks endpoint in backend/tests/contract/test_task_creation_contract.py
- [ ] T013 [P] [US1] Integration test for create task user journey in backend/tests/integration/test_create_task_api.py

### Implementation for User Story 1

- [X] T014 [P] [US1] Create Task model in backend/src/models/task.py
- [X] T015 [US1] Implement TaskService in backend/src/services/task_service.py (depends on T014)
- [X] T016 [US1] Implement POST /users/{user_id}/tasks endpoint in backend/src/api/routes/tasks.py
- [X] T017 [US1] Add request/response validation schemas for create task in backend/src/api/schemas/task.py
- [X] T018 [US1] Add error handling for validation and database errors in backend/src/api/routes/tasks.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Read Tasks (Priority: P1)

**Goal**: Enable retrieving tasks associated with a specific user, ensuring only user's own tasks are accessible

**Independent Test**: Can be fully tested by creating tasks for different users and verifying that GET requests return only the tasks for the specified user_id.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T019 [P] [US2] Contract test for GET /users/{user_id}/tasks endpoint in backend/tests/contract/test_task_retrieval_contract.py
- [ ] T020 [P] [US2] Contract test for GET /users/{user_id}/tasks/{task_id} endpoint in backend/tests/contract/test_single_task_retrieval_contract.py
- [ ] T021 [P] [US2] Integration test for read tasks user journey in backend/tests/integration/test_read_tasks_api.py

### Implementation for User Story 2

- [X] T022 [P] [US2] Extend TaskService with get_tasks_by_user method in backend/src/services/task_service.py
- [X] T023 [US2] Extend TaskService with get_task_by_id method in backend/src/services/task_service.py
- [X] T024 [US2] Implement GET /users/{user_id}/tasks endpoint in backend/src/api/routes/tasks.py
- [X] T025 [US2] Implement GET /users/{user_id}/tasks/{task_id} endpoint in backend/src/api/routes/tasks.py
- [X] T026 [US2] Add response validation schemas for read operations in backend/src/api/schemas/task.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Update Task (Priority: P2)

**Goal**: Enable modifying existing task properties while ensuring only tasks belonging to the specified user can be updated

**Independent Test**: Can be fully tested by making PUT requests to update task properties and verifying the changes are reflected in the database while respecting user boundaries.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T027 [P] [US3] Contract test for PUT /users/{user_id}/tasks/{task_id} endpoint in backend/tests/contract/test_task_update_contract.py
- [ ] T028 [P] [US3] Integration test for update task user journey in backend/tests/integration/test_update_task_api.py

### Implementation for User Story 3

- [X] T029 [P] [US3] Extend TaskService with update_task method in backend/src/services/task_service.py
- [X] T030 [US3] Implement PUT /users/{user_id}/tasks/{task_id} endpoint in backend/src/api/routes/tasks.py
- [X] T031 [US3] Add request/response validation schemas for update task in backend/src/api/schemas/task.py
- [X] T032 [US3] Add user access validation for update operations in backend/src/api/routes/tasks.py

**Checkpoint**: At this point, User Stories 1, 2 AND 3 should all work independently

---

## Phase 6: User Story 4 - Delete Task (Priority: P2)

**Goal**: Enable removing tasks from the system while ensuring only tasks belonging to the specified user can be deleted

**Independent Test**: Can be fully tested by making DELETE requests and verifying that tasks are removed from the database while respecting user boundaries.

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [ ] T033 [P] [US4] Contract test for DELETE /users/{user_id}/tasks/{task_id} endpoint in backend/tests/contract/test_task_delete_contract.py
- [ ] T034 [P] [US4] Integration test for delete task user journey in backend/tests/integration/test_delete_task_api.py

### Implementation for User Story 4

- [X] T035 [P] [US4] Extend TaskService with delete_task method in backend/src/services/task_service.py
- [X] T036 [US4] Implement DELETE /users/{user_id}/tasks/{task_id} endpoint in backend/src/api/routes/tasks.py
- [X] T037 [US4] Add user access validation for delete operations in backend/src/api/routes/tasks.py

**Checkpoint**: At this point, User Stories 1, 2, 3 AND 4 should all work independently

---

## Phase 7: User Story 5 - Complete Task (Priority: P3)

**Goal**: Enable marking tasks as completed while ensuring proper user access controls

**Independent Test**: Can be fully tested by making requests to update the completion status of tasks and verifying the change is reflected in the database.

### Tests for User Story 5 (OPTIONAL - only if tests requested) ⚠️

- [ ] T038 [P] [US5] Contract test for PATCH /users/{user_id}/tasks/{task_id}/complete endpoint in backend/tests/contract/test_task_complete_contract.py
- [ ] T039 [P] [US5] Integration test for complete task user journey in backend/tests/integration/test_complete_task_api.py

### Implementation for User Story 5

- [X] T040 [P] [US5] Extend TaskService with update_task_completion_status method in backend/src/services/task_service.py
- [X] T041 [US5] Implement PATCH /users/{user_id}/tasks/{task_id}/complete endpoint in backend/src/api/routes/tasks.py
- [X] T042 [US5] Add request/response validation schemas for task completion in backend/src/api/schemas/task.py
- [X] T043 [US5] Add user access validation for completion operations in backend/src/api/routes/tasks.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T044 [P] Documentation updates in backend/README.md
- [X] T045 Code cleanup and refactoring across all task service methods
- [X] T046 Performance optimization for database queries across all endpoints
- [X] T047 [P] Additional unit tests in backend/tests/unit/test_models.py
- [X] T048 Security hardening and input validation checks
- [X] T049 Run quickstart validation with all implemented endpoints

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - May integrate with US1-US3 but should be independently testable
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - May integrate with US1-US4 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Contract test for POST /users/{user_id}/tasks endpoint in backend/tests/contract/test_task_creation_contract.py"
Task: "Integration test for create task user journey in backend/tests/integration/test_create_task_api.py"

# Launch all models for User Story 1 together:
Task: "Create Task model in backend/src/models/task.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
   - Developer E: User Story 5
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence