"""Unit tests for TaskService."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import pytest
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from models.task import Priority, Task
from services.task_service import TaskService


@pytest.fixture(name="session")
def session_fixture():
    """Create an in-memory test database session."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="service")
def service_fixture(session: Session):
    """Create a TaskService with test session."""
    return TaskService(session)


class TestCreateTask:
    """Tests for TaskService.create_task()."""

    def test_create_task_basic(self, service: TaskService):
        """Test creating a task with just a title."""
        task = service.create_task(title="Test task")
        assert task.id is not None
        assert task.title == "Test task"
        assert task.completed is False
        assert task.priority == Priority.MEDIUM
        assert task.tags == []

    def test_create_task_with_priority(self, service: TaskService):
        """Test creating a task with custom priority."""
        task = service.create_task(title="High priority", priority=Priority.HIGH)
        assert task.priority == Priority.HIGH

    def test_create_task_with_tags(self, service: TaskService):
        """Test creating a task with tags."""
        task = service.create_task(title="Tagged task", tags=["work", "urgent"])
        assert task.tags == ["work", "urgent"]

    def test_create_task_with_all_options(self, service: TaskService):
        """Test creating a task with all options."""
        task = service.create_task(
            title="Full task",
            priority=Priority.LOW,
            tags=["personal"],
        )
        assert task.title == "Full task"
        assert task.priority == Priority.LOW
        assert task.tags == ["personal"]


class TestListTasks:
    """Tests for TaskService.list_tasks()."""

    def test_list_tasks_empty(self, service: TaskService):
        """Test listing when no tasks exist."""
        tasks = service.list_tasks()
        assert tasks == []

    def test_list_tasks_returns_all(self, service: TaskService):
        """Test listing returns all tasks."""
        service.create_task(title="Task 1")
        service.create_task(title="Task 2")
        service.create_task(title="Task 3")

        tasks = service.list_tasks()
        assert len(tasks) == 3

    def test_list_tasks_sorted_by_id(self, service: TaskService):
        """Test tasks are sorted by ID by default."""
        task1 = service.create_task(title="First")
        task2 = service.create_task(title="Second")

        tasks = service.list_tasks()
        assert tasks[0].id == task1.id
        assert tasks[1].id == task2.id


class TestToggleComplete:
    """Tests for TaskService.toggle_complete()."""

    def test_toggle_incomplete_to_complete(self, service: TaskService):
        """Test marking incomplete task as complete."""
        task = service.create_task(title="Test task")
        assert task.completed is False

        toggled = service.toggle_complete(task.id)
        assert toggled.completed is True

    def test_toggle_complete_to_incomplete(self, service: TaskService):
        """Test marking complete task as incomplete."""
        task = service.create_task(title="Test task")
        service.toggle_complete(task.id)  # Make complete

        toggled = service.toggle_complete(task.id)  # Toggle back
        assert toggled.completed is False

    def test_toggle_nonexistent_task(self, service: TaskService):
        """Test toggling a non-existent task returns None."""
        result = service.toggle_complete(999)
        assert result is None


class TestUpdateTask:
    """Tests for TaskService.update_task()."""

    def test_update_title(self, service: TaskService):
        """Test updating task title."""
        task = service.create_task(title="Original")
        updated = service.update_task(task.id, title="Updated")
        assert updated.title == "Updated"

    def test_update_priority(self, service: TaskService):
        """Test updating task priority."""
        task = service.create_task(title="Test", priority=Priority.LOW)
        updated = service.update_task(task.id, priority=Priority.HIGH)
        assert updated.priority == Priority.HIGH

    def test_update_both_fields(self, service: TaskService):
        """Test updating both title and priority."""
        task = service.create_task(title="Original", priority=Priority.LOW)
        updated = service.update_task(task.id, title="New Title", priority=Priority.HIGH)
        assert updated.title == "New Title"
        assert updated.priority == Priority.HIGH

    def test_update_nonexistent_task(self, service: TaskService):
        """Test updating a non-existent task returns None."""
        result = service.update_task(999, title="Test")
        assert result is None


class TestDeleteTask:
    """Tests for TaskService.delete_task()."""

    def test_delete_existing_task(self, service: TaskService):
        """Test deleting an existing task."""
        task = service.create_task(title="To delete")
        assert service.delete_task(task.id) is True

        # Verify deleted
        assert service.get_task(task.id) is None

    def test_delete_nonexistent_task(self, service: TaskService):
        """Test deleting a non-existent task returns False."""
        result = service.delete_task(999)
        assert result is False


class TestAddTag:
    """Tests for TaskService.add_tag()."""

    def test_add_tag_to_task(self, service: TaskService):
        """Test adding a tag to a task."""
        task = service.create_task(title="Test task")
        updated = service.add_tag(task.id, "work")
        assert "work" in updated.tags

    def test_add_tag_no_duplicates(self, service: TaskService):
        """Test adding same tag twice doesn't duplicate."""
        task = service.create_task(title="Test task", tags=["work"])
        updated = service.add_tag(task.id, "work")
        assert updated.tags.count("work") == 1

    def test_add_multiple_tags(self, service: TaskService):
        """Test adding multiple tags."""
        task = service.create_task(title="Test task")
        service.add_tag(task.id, "tag1")
        updated = service.add_tag(task.id, "tag2")
        assert "tag1" in updated.tags
        assert "tag2" in updated.tags

    def test_add_tag_nonexistent_task(self, service: TaskService):
        """Test adding tag to non-existent task returns None."""
        result = service.add_tag(999, "tag")
        assert result is None


class TestRemoveTag:
    """Tests for TaskService.remove_tag()."""

    def test_remove_existing_tag(self, service: TaskService):
        """Test removing an existing tag."""
        task = service.create_task(title="Test task", tags=["work", "home"])
        updated = service.remove_tag(task.id, "work")
        assert "work" not in updated.tags
        assert "home" in updated.tags

    def test_remove_nonexistent_tag(self, service: TaskService):
        """Test removing a tag that doesn't exist."""
        task = service.create_task(title="Test task", tags=["work"])
        updated = service.remove_tag(task.id, "nonexistent")
        assert updated.tags == ["work"]

    def test_remove_tag_nonexistent_task(self, service: TaskService):
        """Test removing tag from non-existent task returns None."""
        result = service.remove_tag(999, "tag")
        assert result is None


class TestSearchTasks:
    """Tests for TaskService.list_tasks() with search."""

    def test_search_case_insensitive(self, service: TaskService):
        """Test search is case-insensitive."""
        service.create_task(title="Buy GROCERIES")
        service.create_task(title="Call mom")

        results = service.list_tasks(search="groceries")
        assert len(results) == 1
        assert "GROCERIES" in results[0].title

    def test_search_partial_match(self, service: TaskService):
        """Test search matches partial titles."""
        service.create_task(title="Buy groceries today")

        results = service.list_tasks(search="grocer")
        assert len(results) == 1

    def test_search_no_match(self, service: TaskService):
        """Test search with no matches."""
        service.create_task(title="Buy groceries")

        results = service.list_tasks(search="xyz123")
        assert len(results) == 0


class TestFilterTasks:
    """Tests for TaskService.list_tasks() with filters."""

    def test_filter_by_status_complete(self, service: TaskService):
        """Test filtering by complete status."""
        task1 = service.create_task(title="Task 1")
        task2 = service.create_task(title="Task 2")
        service.toggle_complete(task1.id)

        results = service.list_tasks(status="complete")
        assert len(results) == 1
        assert results[0].id == task1.id

    def test_filter_by_status_incomplete(self, service: TaskService):
        """Test filtering by incomplete status."""
        task1 = service.create_task(title="Task 1")
        task2 = service.create_task(title="Task 2")
        service.toggle_complete(task1.id)

        results = service.list_tasks(status="incomplete")
        assert len(results) == 1
        assert results[0].id == task2.id

    def test_filter_by_priority(self, service: TaskService):
        """Test filtering by priority."""
        service.create_task(title="High", priority=Priority.HIGH)
        service.create_task(title="Medium", priority=Priority.MEDIUM)
        service.create_task(title="Low", priority=Priority.LOW)

        results = service.list_tasks(priority=Priority.HIGH)
        assert len(results) == 1
        assert results[0].title == "High"

    def test_filter_by_tag(self, service: TaskService):
        """Test filtering by tag."""
        service.create_task(title="Work task", tags=["work"])
        service.create_task(title="Home task", tags=["home"])
        service.create_task(title="Both", tags=["work", "home"])

        results = service.list_tasks(tag="work")
        assert len(results) == 2

    def test_filter_combined_and_logic(self, service: TaskService):
        """Test multiple filters use AND logic."""
        task1 = service.create_task(title="High work", priority=Priority.HIGH, tags=["work"])
        task2 = service.create_task(title="High home", priority=Priority.HIGH, tags=["home"])
        task3 = service.create_task(title="Low work", priority=Priority.LOW, tags=["work"])

        results = service.list_tasks(priority=Priority.HIGH, tag="work")
        assert len(results) == 1
        assert results[0].id == task1.id


class TestSortTasks:
    """Tests for TaskService.sort_tasks()."""

    def test_sort_by_priority(self, service: TaskService):
        """Test sorting by priority (high first)."""
        service.create_task(title="Low", priority=Priority.LOW)
        service.create_task(title="High", priority=Priority.HIGH)
        service.create_task(title="Medium", priority=Priority.MEDIUM)

        results = service.list_tasks(sort_by="priority")
        assert results[0].priority == Priority.HIGH
        assert results[1].priority == Priority.MEDIUM
        assert results[2].priority == Priority.LOW

    def test_sort_by_alpha(self, service: TaskService):
        """Test sorting alphabetically by title."""
        service.create_task(title="Zebra")
        service.create_task(title="Apple")
        service.create_task(title="Mango")

        results = service.list_tasks(sort_by="alpha")
        assert results[0].title == "Apple"
        assert results[1].title == "Mango"
        assert results[2].title == "Zebra"

    def test_sort_by_id(self, service: TaskService):
        """Test sorting by ID (creation order)."""
        task1 = service.create_task(title="First")
        task2 = service.create_task(title="Second")
        task3 = service.create_task(title="Third")

        results = service.list_tasks(sort_by="id")
        assert results[0].id == task1.id
        assert results[1].id == task2.id
        assert results[2].id == task3.id
