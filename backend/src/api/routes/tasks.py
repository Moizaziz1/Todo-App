from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from pydantic import BaseModel
from ...services.database import get_session
from ...models.task import TaskCreate, TaskRead, TaskUpdate
from ...services.task_service import task_service
from ..deps import AuthenticatedUser, verify_user_access

router = APIRouter()


@router.post("/users/{user_id}/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    user_id: str,
    task_data: TaskCreate,
    current_user: AuthenticatedUser,
    db_session: Session = Depends(get_session)
):
    """
    Create a new task for a specific user.
    Requires JWT authentication. User can only create tasks for themselves.
    """
    # Verify the authenticated user matches the URL user_id
    verify_user_access(current_user, user_id)

    # Override task user_id with authenticated user's ID
    task_data_dict = task_data.model_dump()
    task_data_dict["user_id"] = current_user.user_id
    validated_task = TaskCreate(**task_data_dict)

    try:
        return task_service.create_task(db_session, validated_task)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create task: {str(e)}"
        )


@router.get("/users/{user_id}/tasks", response_model=List[TaskRead])
def get_tasks(
    user_id: str,
    current_user: AuthenticatedUser,
    skip: int = 0,
    limit: int = 100,
    db_session: Session = Depends(get_session)
):
    """
    Retrieve all tasks for a specific user.
    Requires JWT authentication. User can only access their own tasks.
    """
    # Verify the authenticated user matches the URL user_id
    verify_user_access(current_user, user_id)

    try:
        return task_service.get_tasks_by_user(db_session, current_user.user_id, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve tasks: {str(e)}"
        )


@router.get("/users/{user_id}/tasks/{task_id}", response_model=TaskRead)
def get_task(
    user_id: str,
    task_id: int,
    current_user: AuthenticatedUser,
    db_session: Session = Depends(get_session)
):
    """
    Retrieve a specific task for a specific user.
    Requires JWT authentication. User can only access their own tasks.
    """
    # Verify the authenticated user matches the URL user_id
    verify_user_access(current_user, user_id)

    task = task_service.get_task_by_id(db_session, task_id, current_user.user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@router.put("/users/{user_id}/tasks/{task_id}", response_model=TaskRead)
def update_task(
    user_id: str,
    task_id: int,
    task_data: TaskUpdate,
    current_user: AuthenticatedUser,
    db_session: Session = Depends(get_session)
):
    """
    Update a specific task for a specific user.
    Requires JWT authentication. User can only update their own tasks.
    """
    # Verify the authenticated user matches the URL user_id
    verify_user_access(current_user, user_id)

    updated_task = task_service.update_task(db_session, task_id, current_user.user_id, task_data)
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return updated_task


@router.delete("/users/{user_id}/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    user_id: str,
    task_id: int,
    current_user: AuthenticatedUser,
    db_session: Session = Depends(get_session)
):
    """
    Delete a specific task for a specific user.
    Requires JWT authentication. User can only delete their own tasks.
    """
    # Verify the authenticated user matches the URL user_id
    verify_user_access(current_user, user_id)

    success = task_service.delete_task(db_session, task_id, current_user.user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Return nothing for 204 status code


class TaskCompletionUpdate(BaseModel):
    """
    Request model for updating task completion status
    """
    completed: bool


@router.patch("/users/{user_id}/tasks/{task_id}/complete", response_model=TaskRead)
def update_task_completion(
    user_id: str,
    task_id: int,
    completion_data: TaskCompletionUpdate,
    current_user: AuthenticatedUser,
    db_session: Session = Depends(get_session)
):
    """
    Update the completion status of a specific task for a specific user.
    Requires JWT authentication. User can only update their own tasks.
    """
    # Verify the authenticated user matches the URL user_id
    verify_user_access(current_user, user_id)

    updated_task = task_service.update_task_completion_status(
        db_session, task_id, current_user.user_id, completion_data.completed
    )
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return updated_task
