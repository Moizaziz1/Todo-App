"""
Unit tests for Task model validation and behavior.
"""
import pytest
from datetime import datetime, timezone
from pydantic import ValidationError

from backend.src.models.task import (
    Task,
    TaskBase,
    TaskCreate,
    TaskUpdate,
    TaskRead,
    VALID_PRIORITIES,
)


class TestTaskBase:
    """Tests for TaskBase model validation."""

    def test_valid_task_base(self):
        """Test creating a valid TaskBase instance."""
        task = TaskBase(
            title="Test Task",
            description="A test description",
            completed=False,
            user_id="user123",
            priority="normal",
        )
        assert task.title == "Test Task"
        assert task.description == "A test description"
        assert task.completed is False
        assert task.user_id == "user123"
        assert task.priority == "normal"

    def test_title_min_length(self):
        """Test that title must have at least 1 character."""
        with pytest.raises(ValidationError) as exc_info:
            TaskBase(title="", user_id="user123")
        assert "title" in str(exc_info.value)

    def test_title_max_length(self):
        """Test that title must not exceed 255 characters."""
        with pytest.raises(ValidationError) as exc_info:
            TaskBase(title="x" * 256, user_id="user123")
        assert "title" in str(exc_info.value)

    def test_description_max_length(self):
        """Test that description must not exceed 1000 characters."""
        with pytest.raises(ValidationError) as exc_info:
            TaskBase(
                title="Test",
                user_id="user123",
                description="x" * 1001,
            )
        assert "description" in str(exc_info.value)

    def test_optional_description(self):
        """Test that description is optional."""
        task = TaskBase(title="Test", user_id="user123")
        assert task.description is None

    def test_default_completed_false(self):
        """Test that completed defaults to False."""
        task = TaskBase(title="Test", user_id="user123")
        assert task.completed is False

    def test_default_priority_normal(self):
        """Test that priority defaults to 'normal'."""
        task = TaskBase(title="Test", user_id="user123")
        assert task.priority == "normal"

    @pytest.mark.parametrize("priority", VALID_PRIORITIES)
    def test_valid_priorities(self, priority):
        """Test all valid priority values."""
        task = TaskBase(title="Test", user_id="user123", priority=priority)
        assert task.priority == priority

    def test_invalid_priority(self):
        """Test that invalid priority raises validation error."""
        with pytest.raises(ValidationError) as exc_info:
            TaskBase(title="Test", user_id="user123", priority="invalid")
        assert "priority" in str(exc_info.value).lower()


class TestTaskCreate:
    """Tests for TaskCreate model."""

    def test_create_task_minimal(self):
        """Test creating task with only required fields."""
        task = TaskCreate(title="New Task", user_id="user123")
        assert task.title == "New Task"
        assert task.user_id == "user123"
        assert task.completed is False
        assert task.priority == "normal"

    def test_create_task_full(self):
        """Test creating task with all fields."""
        due_date = datetime.now(timezone.utc)
        task = TaskCreate(
            title="Full Task",
            description="Full description",
            completed=True,
            user_id="user123",
            priority="high",
            due_date=due_date,
        )
        assert task.title == "Full Task"
        assert task.description == "Full description"
        assert task.completed is True
        assert task.priority == "high"
        assert task.due_date == due_date


class TestTaskUpdate:
    """Tests for TaskUpdate model."""

    def test_update_all_none(self):
        """Test that all fields can be None (partial update)."""
        update = TaskUpdate()
        assert update.title is None
        assert update.description is None
        assert update.completed is None
        assert update.priority is None
        assert update.due_date is None

    def test_update_single_field(self):
        """Test updating a single field."""
        update = TaskUpdate(title="Updated Title")
        assert update.title == "Updated Title"
        assert update.description is None

    def test_update_title_validation(self):
        """Test that title validation applies to updates."""
        with pytest.raises(ValidationError):
            TaskUpdate(title="")  # Empty string should fail

    def test_update_priority_validation(self):
        """Test that priority validation applies to updates."""
        with pytest.raises(ValidationError):
            TaskUpdate(priority="invalid")


class TestTaskRead:
    """Tests for TaskRead response model."""

    def test_read_model_requires_all_fields(self):
        """Test that TaskRead requires all response fields."""
        now = datetime.now(timezone.utc)
        task = TaskRead(
            id=1,
            external_id="uuid-123",
            title="Test",
            user_id="user123",
            completed=False,
            priority="normal",
            created_at=now,
            updated_at=now,
        )
        assert task.id == 1
        assert task.external_id == "uuid-123"
        assert task.created_at == now
        assert task.updated_at == now


class TestTaskModel:
    """Tests for the Task database model."""

    def test_task_defaults(self):
        """Test Task model default values."""
        task = Task(title="Test", user_id="user123")
        assert task.id is None  # Not persisted yet
        assert task.completed is False
        assert task.priority == "normal"
        assert task.external_id is not None  # UUID generated

    def test_task_external_id_unique(self):
        """Test that each Task gets a unique external_id."""
        task1 = Task(title="Test 1", user_id="user123")
        task2 = Task(title="Test 2", user_id="user123")
        assert task1.external_id != task2.external_id
