---
id: 1
title: Create Todo App Constitution
stage: constitution
date: 2026-02-06
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: Moizaziz1
command: /sp.phr
labels: ["constitution", "todo-app", "spec-driven", "security"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - D:\hackathon II\Phase II\.specify\memory\constitution.md
tests:
 - none
---

## Prompt

/sp.constitution

Project: Todo Full-Stack Web Application with Authentication

Core principles:
- Spec-driven development (no manual coding)
- Correctness of API behavior and data flow
- Security-first design (JWT-based authentication)
- Clear separation of frontend, backend, and database concerns
- Reproducibility of results through deterministic prompts

Key standards:
- All features must be implemented via spec → plan → tasks → Claude Code
- All API endpoints must follow REST conventions
- All task operations must be scoped to the authenticated user
- JWT verification must be enforced on every protected route
- Database schema must be defined using SQLModel
- Frontend must use Next.js App Router conventions

Constraints:
- Technology stack:
  - Frontend: Next.js 16+ (App Router)
  - Backend: Python FastAPI
  - ORM: SQLModel
  - Database: Neon Serverless PostgreSQL
  - Authentication: Better Auth with JWT
- No manual coding (only Claude Code execution)
- All data must persist in the database (no in-memory storage)
- All endpoints must reject unauthenticated requests (401 Unauthorized)

Success criteria:
- Users can sign up and sign in successfully
- Authenticated users can create, read, update, delete, and complete tasks
- Each user can only access their own tasks
- JWT tokens are correctly issued, attached, and verified
- API returns correct HTTP status codes
- Frontend is responsive and functional
- Project can be reviewed and reproduced from prompts alone

## Response snapshot

Created a comprehensive constitution file for the Todo Full-Stack Web Application with Authentication, including core principles, constraints, development workflow, and governance sections.

## Outcome

- ✅ Impact: Created complete constitution.md file with all required principles and constraints
- 🧪 Tests: none
- 📁 Files: D:\hackathon II\Phase II\.specify\memory\constitution.md
- 🔁 Next prompts: none
- 🧠 Reflection: Successfully established foundational governance document for the project

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): none
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): none