"""Unit tests for TaskService."""

import pytest

from src.models.task import Task, Priority
from src.services.task_service import TaskService


@pytest.fixture
def service():
    """Create a fresh TaskService for each test."""
    return TaskService()


@pytest.fixture
def service_with_tasks(service):
    """Create a TaskService with sample tasks."""
    service.create_task("Buy groceries", Priority.HIGH, ["shopping"])
    service.create_task("Review PR", Priority.MEDIUM, ["work", "code"])
    service.create_task("Call mom", Priority.LOW)
    service.complete_task(2)  # Mark "Review PR" as complete
    return service


class TestCreateTask:
    """Tests for TaskService.create_task()."""

    def test_create_task_minimal(self, service):
        """Test creating a task with just a title."""
        task = service.create_task("Buy groceries")

        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.completed is False
        assert task.priority == Priority.MEDIUM
        assert task.tags == []

    def test_create_task_with_priority(self, service):
        """Test creating a task with priority."""
        task = service.create_task("Urgent task", Priority.HIGH)

        assert task.priority == Priority.HIGH

    def test_create_task_with_tags(self, service):
        """Test creating a task with tags."""
        task = service.create_task("Work task", tags=["work", "important"])

        assert task.tags == ["work", "important"]

    def test_create_task_sequential_ids(self, service):
        """Test that task IDs are sequential."""
        task1 = service.create_task("Task 1")
        task2 = service.create_task("Task 2")
        task3 = service.create_task("Task 3")

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_create_task_empty_title_raises(self, service):
        """Test that empty title raises ValueError."""
        with pytest.raises(ValueError, match="Title cannot be empty"):
            service.create_task("")


class TestListTasks:
    """Tests for TaskService.list_tasks()."""

    def test_list_tasks_empty(self, service):
        """Test listing tasks when empty."""
        tasks = service.list_tasks()
        assert tasks == []

    def test_list_tasks_returns_all(self, service_with_tasks):
        """Test listing all tasks."""
        tasks = service_with_tasks.list_tasks()
        assert len(tasks) == 3
        assert tasks[0].title == "Buy groceries"
        assert tasks[1].title == "Review PR"
        assert tasks[2].title == "Call mom"


class TestGetTask:
    """Tests for TaskService.get_task()."""

    def test_get_task_exists(self, service_with_tasks):
        """Test getting an existing task."""
        task = service_with_tasks.get_task(1)

        assert task is not None
        assert task.title == "Buy groceries"

    def test_get_task_not_found(self, service_with_tasks):
        """Test getting a non-existent task."""
        task = service_with_tasks.get_task(99)
        assert task is None


class TestCompleteTask:
    """Tests for TaskService.complete_task()."""

    def test_complete_task_success(self, service):
        """Test completing a task."""
        service.create_task("Test task")
        task = service.complete_task(1)

        assert task is not None
        assert task.completed is True

    def test_complete_task_not_found(self, service):
        """Test completing a non-existent task."""
        task = service.complete_task(99)
        assert task is None


class TestUncompleteTask:
    """Tests for TaskService.uncomplete_task()."""

    def test_uncomplete_task_success(self, service):
        """Test uncompleting a task."""
        service.create_task("Test task")
        service.complete_task(1)
        task = service.uncomplete_task(1)

        assert task is not None
        assert task.completed is False

    def test_uncomplete_task_not_found(self, service):
        """Test uncompleting a non-existent task."""
        task = service.uncomplete_task(99)
        assert task is None


class TestUpdateTask:
    """Tests for TaskService.update_task()."""

    def test_update_task_title(self, service):
        """Test updating task title."""
        service.create_task("Old title")
        task = service.update_task(1, title="New title")

        assert task is not None
        assert task.title == "New title"

    def test_update_task_priority(self, service):
        """Test updating task priority."""
        service.create_task("Test task")
        task = service.update_task(1, priority=Priority.HIGH)

        assert task is not None
        assert task.priority == Priority.HIGH

    def test_update_task_not_found(self, service):
        """Test updating a non-existent task."""
        task = service.update_task(99, title="New title")
        assert task is None

    def test_update_task_empty_title_raises(self, service):
        """Test that empty title raises ValueError."""
        service.create_task("Test task")
        with pytest.raises(ValueError, match="Title cannot be empty"):
            service.update_task(1, title="")


class TestDeleteTask:
    """Tests for TaskService.delete_task()."""

    def test_delete_task_success(self, service):
        """Test deleting a task."""
        service.create_task("Test task")
        task = service.delete_task(1)

        assert task is not None
        assert task.title == "Test task"
        assert service.get_task(1) is None

    def test_delete_task_not_found(self, service):
        """Test deleting a non-existent task."""
        task = service.delete_task(99)
        assert task is None


class TestAddTag:
    """Tests for TaskService.add_tag()."""

    def test_add_tag_success(self, service):
        """Test adding a tag to a task."""
        service.create_task("Test task")
        task = service.add_tag(1, "work")

        assert task is not None
        assert "work" in task.tags

    def test_add_tag_not_found(self, service):
        """Test adding tag to non-existent task."""
        task = service.add_tag(99, "work")
        assert task is None

    def test_add_tag_empty_raises(self, service):
        """Test that empty tag raises ValueError."""
        service.create_task("Test task")
        with pytest.raises(ValueError, match="Tag cannot be empty"):
            service.add_tag(1, "")


class TestRemoveTag:
    """Tests for TaskService.remove_tag()."""

    def test_remove_tag_success(self, service):
        """Test removing a tag from a task."""
        service.create_task("Test task", tags=["work", "home"])
        task = service.remove_tag(1, "work")

        assert task is not None
        assert "work" not in task.tags
        assert "home" in task.tags

    def test_remove_tag_not_found(self, service):
        """Test removing tag from non-existent task."""
        task = service.remove_tag(99, "work")
        assert task is None


class TestSearchTasks:
    """Tests for TaskService.search_tasks()."""

    def test_search_tasks_found(self, service_with_tasks):
        """Test searching for tasks with matching keyword."""
        tasks = service_with_tasks.search_tasks("groceries")

        assert len(tasks) == 1
        assert tasks[0].title == "Buy groceries"

    def test_search_tasks_case_insensitive(self, service_with_tasks):
        """Test that search is case-insensitive."""
        tasks = service_with_tasks.search_tasks("GROCERIES")

        assert len(tasks) == 1
        assert tasks[0].title == "Buy groceries"

    def test_search_tasks_no_match(self, service_with_tasks):
        """Test searching with no matches."""
        tasks = service_with_tasks.search_tasks("xyz123")
        assert tasks == []

    def test_search_tasks_empty_keyword(self, service_with_tasks):
        """Test that empty search returns all tasks."""
        tasks = service_with_tasks.search_tasks("")
        assert len(tasks) == 3


class TestFilterTasks:
    """Tests for TaskService.filter_tasks()."""

    def test_filter_by_status_incomplete(self, service_with_tasks):
        """Test filtering by incomplete status."""
        tasks = service_with_tasks.filter_tasks(status="incomplete")

        assert len(tasks) == 2
        assert all(not t.completed for t in tasks)

    def test_filter_by_status_complete(self, service_with_tasks):
        """Test filtering by complete status."""
        tasks = service_with_tasks.filter_tasks(status="complete")

        assert len(tasks) == 1
        assert tasks[0].completed is True

    def test_filter_by_priority(self, service_with_tasks):
        """Test filtering by priority."""
        tasks = service_with_tasks.filter_tasks(priority=Priority.HIGH)

        assert len(tasks) == 1
        assert tasks[0].priority == Priority.HIGH

    def test_filter_by_tag(self, service_with_tasks):
        """Test filtering by tag."""
        tasks = service_with_tasks.filter_tasks(tag="work")

        assert len(tasks) == 1
        assert "work" in tasks[0].tags

    def test_filter_combined(self, service_with_tasks):
        """Test filtering with multiple criteria (AND logic)."""
        tasks = service_with_tasks.filter_tasks(
            status="incomplete",
            priority=Priority.HIGH
        )

        assert len(tasks) == 1
        assert tasks[0].title == "Buy groceries"


class TestSortTasks:
    """Tests for TaskService.sort_tasks()."""

    def test_sort_by_priority(self, service_with_tasks):
        """Test sorting by priority (high to low)."""
        tasks = service_with_tasks.list_tasks()
        sorted_tasks = service_with_tasks.sort_tasks(tasks, "priority")

        assert sorted_tasks[0].priority == Priority.HIGH
        assert sorted_tasks[1].priority == Priority.MEDIUM
        assert sorted_tasks[2].priority == Priority.LOW

    def test_sort_by_alpha(self, service_with_tasks):
        """Test sorting alphabetically."""
        tasks = service_with_tasks.list_tasks()
        sorted_tasks = service_with_tasks.sort_tasks(tasks, "alpha")

        assert sorted_tasks[0].title == "Buy groceries"
        assert sorted_tasks[1].title == "Call mom"
        assert sorted_tasks[2].title == "Review PR"

    def test_sort_by_id(self, service_with_tasks):
        """Test sorting by ID (default)."""
        tasks = service_with_tasks.list_tasks()
        sorted_tasks = service_with_tasks.sort_tasks(tasks, "id")

        assert sorted_tasks[0].id == 1
        assert sorted_tasks[1].id == 2
        assert sorted_tasks[2].id == 3
