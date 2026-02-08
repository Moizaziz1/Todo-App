<!-- SYNC IMPACT REPORT:
Version change: N/A -> 1.0.0
Added sections: Core Principles 1-6, Additional Constraints, Development Workflow, Governance rules
Removed sections: None (completely new constitution)
Templates requiring updates: N/A (new file)
Follow-up TODOs: None
-->
# Todo Full-Stack Web Application Constitution

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)
All features must be implemented via spec → plan → tasks → Claude Code; No manual coding allowed; All development must follow the Agentic Dev Stack workflow with proper documentation and traceability.

### II. Full-Stack Architecture
Maintain clear separation between frontend, backend, and database concerns; Each layer must be independently testable and maintainable; Proper API contracts defined between layers.

### III. Security-First Design (NON-NEGOTIABLE)
JWT-based authentication must be enforced on all protected routes; All API endpoints must reject unauthenticated requests with 401 Unauthorized; User data isolation must prevent cross-user access to resources.

### IV. REST API Conventions
All API endpoints must follow REST conventions with proper HTTP methods and status codes; Resource-based URL structures; Standardized response formats for success and error cases.

### V. Data Persistence Requirement
All task operations must persist in Neon Serverless PostgreSQL database using SQLModel ORM; No in-memory storage for production data; Database schema must be well-defined and version-controlled.

### VI. Frontend-Backend Separation
Frontend must use Next.js 16+ App Router conventions; Clear API contract between frontend and backend; Proper state management and error handling on client-side.

## Additional Constraints

### Technology Stack Requirements
- Frontend: Next.js 16+ (App Router)
- Backend: Python FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth with JWT

### Implementation Constraints
- No manual coding (only Claude Code execution)
- All data must persist in the database (no in-memory storage)
- All endpoints must reject unauthenticated requests (401 Unauthorized)
- All task operations must be scoped to the authenticated user

## Development Workflow

### Feature Implementation
- Features must be developed following the spec → plan → tasks → implementation flow
- Each feature must have clear acceptance criteria defined in specs
- Tasks must be granular enough to be completed in 15-30 minute increments
- Code reviews must verify adherence to constitutional principles

### Testing Requirements
- All API endpoints must be tested with proper authentication flows
- User isolation must be verified through comprehensive testing
- Frontend components must be tested for proper authentication handling
- Database operations must be validated for data integrity

## Governance

All development activities must comply with these constitutional principles. Deviations require explicit amendment to this constitution through proper governance procedures. The constitution supersedes all other development practices and guides decision-making when trade-offs arise. Code reviews and pull request approvals must verify constitutional compliance. The spec-driven approach must be maintained throughout the project lifecycle.

**Version**: 1.0.0 | **Ratified**: 2026-02-06 | **Last Amended**: 2026-02-06