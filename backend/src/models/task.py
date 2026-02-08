from sqlmodel import SQLModel, Field
from typing import Optional, Literal
from datetime import datetime
from pydantic import field_validator
import uuid


VALID_PRIORITIES = ("low", "normal", "high")


class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    user_id: str = Field(max_length=255, index=True)  # Indexed for efficient user-based filtering
    priority: Optional[str] = Field(default="normal", max_length=20)
    due_date: Optional[datetime] = Field(default=None)

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in VALID_PRIORITIES:
            raise ValueError(f"Priority must be one of: {', '.join(VALID_PRIORITIES)}")
        return v


class Task(TaskBase, table=True):
    """
    Task model representing a user's task in the database.
    Indexed on user_id and completed for efficient querying.
    """
    __tablename__ = "task"

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    external_id: str = Field(default_factory=lambda: str(uuid.uuid4()), unique=True, index=True)


class TaskRead(TaskBase):
    """
    Response model for reading tasks
    """
    id: int
    external_id: str
    created_at: datetime
    updated_at: datetime


class TaskUpdate(SQLModel):
    """
    Model for updating tasks - all fields optional for partial updates.
    """
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = None
    priority: Optional[str] = Field(default=None, max_length=20)
    due_date: Optional[datetime] = None

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in VALID_PRIORITIES:
            raise ValueError(f"Priority must be one of: {', '.join(VALID_PRIORITIES)}")
        return v


class TaskCreate(TaskBase):
    """
    Model for creating new tasks
    """
    title: str
    user_id: str