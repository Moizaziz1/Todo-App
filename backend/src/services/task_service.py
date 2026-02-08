from sqlmodel import Session, select
from ..models.task import Task, TaskCreate, TaskUpdate, TaskRead
from typing import List, Optional
from datetime import datetime, timezone


class TaskService:
    """
    Service class for handling task-related business logic.
    Provides CRUD operations with user-scoped data isolation.
    """

    def create_task(self, db_session: Session, task_data: TaskCreate) -> TaskRead:
        """
        Create a new task in the database.

        Args:
            db_session: Database session
            task_data: Task creation data with user_id

        Returns:
            TaskRead: The created task with all fields populated
        """
        task = Task(**task_data.model_dump())
        now = datetime.now(timezone.utc)
        task.created_at = now
        task.updated_at = now

        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)

        return TaskRead.model_validate(task)

    def get_tasks_by_user(
        self,
        db_session: Session,
        user_id: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[TaskRead]:
        """
        Retrieve all tasks for a specific user with pagination.

        Args:
            db_session: Database session
            user_id: User identifier for data isolation
            skip: Number of records to skip (pagination offset)
            limit: Maximum number of records to return (capped at 100)

        Returns:
            List[TaskRead]: List of tasks belonging to the user
        """
        # Cap limit to prevent excessive data retrieval
        limit = min(limit, 100)

        statement = (
            select(Task)
            .where(Task.user_id == user_id)
            .order_by(Task.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        tasks = db_session.exec(statement).all()

        return [TaskRead.model_validate(task) for task in tasks]

    def get_task_by_id(
        self,
        db_session: Session,
        task_id: int,
        user_id: str
    ) -> Optional[TaskRead]:
        """
        Retrieve a specific task by ID with user ownership verification.

        Args:
            db_session: Database session
            task_id: Task primary key
            user_id: User identifier for access control

        Returns:
            TaskRead if found and owned by user, None otherwise
        """
        statement = (
            select(Task)
            .where(Task.id == task_id, Task.user_id == user_id)
        )
        task = db_session.exec(statement).first()

        if task:
            return TaskRead.model_validate(task)
        return None

    def update_task(
        self,
        db_session: Session,
        task_id: int,
        user_id: str,
        task_data: TaskUpdate
    ) -> Optional[TaskRead]:
        """
        Update a specific task for a specific user (partial update supported).

        Args:
            db_session: Database session
            task_id: Task primary key
            user_id: User identifier for access control
            task_data: Fields to update (only non-None fields are applied)

        Returns:
            TaskRead if updated successfully, None if task not found/not owned
        """
        statement = (
            select(Task)
            .where(Task.id == task_id, Task.user_id == user_id)
        )
        task = db_session.exec(statement).first()

        if not task:
            return None

        # Only update fields that were explicitly set
        update_data = task_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        task.updated_at = datetime.now(timezone.utc)
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)

        return TaskRead.model_validate(task)

    def delete_task(
        self,
        db_session: Session,
        task_id: int,
        user_id: str
    ) -> bool:
        """
        Delete a specific task with user ownership verification.

        Args:
            db_session: Database session
            task_id: Task primary key
            user_id: User identifier for access control

        Returns:
            True if deleted successfully, False if task not found/not owned
        """
        statement = (
            select(Task)
            .where(Task.id == task_id, Task.user_id == user_id)
        )
        task = db_session.exec(statement).first()

        if not task:
            return False

        db_session.delete(task)
        db_session.commit()
        return True

    def update_task_completion_status(
        self,
        db_session: Session,
        task_id: int,
        user_id: str,
        completed: bool
    ) -> Optional[TaskRead]:
        """
        Update only the completion status of a task.

        Args:
            db_session: Database session
            task_id: Task primary key
            user_id: User identifier for access control
            completed: New completion status

        Returns:
            TaskRead if updated successfully, None if task not found/not owned
        """
        statement = (
            select(Task)
            .where(Task.id == task_id, Task.user_id == user_id)
        )
        task = db_session.exec(statement).first()

        if not task:
            return None

        task.completed = completed
        task.updated_at = datetime.now(timezone.utc)
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)

        return TaskRead.model_validate(task)


# Global instance for easy access
task_service = TaskService()