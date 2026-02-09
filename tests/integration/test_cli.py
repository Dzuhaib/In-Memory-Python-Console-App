"""Integration tests for CLI commands."""

import pytest

from src.services.task_service import TaskService
from src.cli.commands import CommandHandler, parse_args


class TestParseArgs:
    """Tests for command argument parsing."""

    def test_parse_simple_command(self):
        """Test parsing a simple command."""
        cmd, args, flags = parse_args("add test")
        assert cmd == "add"
        assert args == ["test"]
        assert flags == {}

    def test_parse_quoted_string(self):
        """Test parsing quoted strings."""
        cmd, args, flags = parse_args('add "Buy groceries"')
        assert cmd == "add"
        assert args == ["Buy groceries"]

    def test_parse_flags(self):
        """Test parsing flags."""
        cmd, args, flags = parse_args("add test --priority high --tags work,home")
        assert cmd == "add"
        assert args == ["test"]
        assert flags == {"priority": "high", "tags": "work,home"}

    def test_parse_empty_input(self):
        """Test parsing empty input."""
        cmd, args, flags = parse_args("")
        assert cmd == ""
        assert args == []
        assert flags == {}


@pytest.fixture
def handler():
    """Create a fresh CommandHandler for each test."""
    service = TaskService()
    return CommandHandler(service)


@pytest.fixture
def handler_with_tasks(handler):
    """Create a CommandHandler with sample tasks."""
    handler.execute('add "Buy groceries" --priority high --tags shopping')
    handler.execute('add "Review PR" --tags work,code')
    handler.execute('add "Call mom" --priority low')
    handler.execute("complete 2")
    return handler


class TestAddCommand:
    """Integration tests for add command."""

    def test_add_simple(self, handler):
        """Test adding a simple task."""
        result = handler.execute('add "Buy groceries"')
        assert 'Created task #1: "Buy groceries" [medium]' in result

    def test_add_with_priority(self, handler):
        """Test adding a task with priority."""
        result = handler.execute('add "Urgent" --priority high')
        assert "[high]" in result

    def test_add_with_tags(self, handler):
        """Test adding a task with tags."""
        result = handler.execute('add "Work task" --tags work,urgent')
        assert "(tags: work, urgent)" in result

    def test_add_empty_title_error(self, handler):
        """Test that empty title produces error."""
        result = handler.execute("add")
        assert "Error:" in result
        assert "title" in result.lower()

    def test_add_invalid_priority_error(self, handler):
        """Test that invalid priority produces error."""
        result = handler.execute('add "Test" --priority urgent')
        assert "Error:" in result
        assert "priority" in result.lower()


class TestListCommand:
    """Integration tests for list command."""

    def test_list_empty(self, handler):
        """Test listing when no tasks exist."""
        result = handler.execute("list")
        assert "No tasks found" in result

    def test_list_all(self, handler_with_tasks):
        """Test listing all tasks."""
        result = handler_with_tasks.execute("list")
        assert "Tasks (3)" in result
        assert "Buy groceries" in result
        assert "Review PR" in result
        assert "Call mom" in result

    def test_list_filter_status(self, handler_with_tasks):
        """Test filtering by status."""
        result = handler_with_tasks.execute("list --status incomplete")
        assert "Tasks (2)" in result
        assert "Buy groceries" in result
        assert "Review PR" not in result

    def test_list_filter_priority(self, handler_with_tasks):
        """Test filtering by priority."""
        result = handler_with_tasks.execute("list --priority high")
        assert "Tasks (1)" in result
        assert "Buy groceries" in result

    def test_list_filter_tag(self, handler_with_tasks):
        """Test filtering by tag."""
        result = handler_with_tasks.execute("list --tag work")
        assert "Tasks (1)" in result
        assert "Review PR" in result

    def test_list_sort_priority(self, handler_with_tasks):
        """Test sorting by priority."""
        result = handler_with_tasks.execute("list --sort priority")
        lines = result.split("\n")
        # HIGH should come before LOW
        high_index = next(i for i, l in enumerate(lines) if "high" in l)
        low_index = next(i for i, l in enumerate(lines) if "low" in l)
        assert high_index < low_index

    def test_list_sort_alpha(self, handler_with_tasks):
        """Test sorting alphabetically."""
        result = handler_with_tasks.execute("list --sort alpha")
        lines = result.split("\n")
        # "Buy" should come before "Call" should come before "Review"
        buy_index = next(i for i, l in enumerate(lines) if "Buy" in l)
        call_index = next(i for i, l in enumerate(lines) if "Call" in l)
        review_index = next(i for i, l in enumerate(lines) if "Review" in l)
        assert buy_index < call_index < review_index


class TestCompleteCommand:
    """Integration tests for complete command."""

    def test_complete_success(self, handler):
        """Test completing a task."""
        handler.execute('add "Test task"')
        result = handler.execute("complete 1")
        assert "Completed task #1" in result

    def test_complete_already_complete(self, handler):
        """Test completing an already complete task."""
        handler.execute('add "Test task"')
        handler.execute("complete 1")
        result = handler.execute("complete 1")
        assert "already complete" in result

    def test_complete_not_found(self, handler):
        """Test completing a non-existent task."""
        result = handler.execute("complete 99")
        assert "Error:" in result
        assert "not found" in result


class TestUncompleteCommand:
    """Integration tests for uncomplete command."""

    def test_uncomplete_success(self, handler):
        """Test uncompleting a task."""
        handler.execute('add "Test task"')
        handler.execute("complete 1")
        result = handler.execute("uncomplete 1")
        assert "incomplete" in result.lower()

    def test_uncomplete_already_incomplete(self, handler):
        """Test uncompleting an already incomplete task."""
        handler.execute('add "Test task"')
        result = handler.execute("uncomplete 1")
        assert "already incomplete" in result


class TestUpdateCommand:
    """Integration tests for update command."""

    def test_update_title(self, handler):
        """Test updating task title."""
        handler.execute('add "Old title"')
        result = handler.execute('update 1 --title "New title"')
        assert "Updated task #1" in result
        assert "New title" in result

    def test_update_priority(self, handler):
        """Test updating task priority."""
        handler.execute('add "Test task"')
        result = handler.execute("update 1 --priority high")
        assert "[high]" in result

    def test_update_not_found(self, handler):
        """Test updating a non-existent task."""
        result = handler.execute('update 99 --title "Test"')
        assert "Error:" in result
        assert "not found" in result

    def test_update_no_changes(self, handler):
        """Test update with no changes specified."""
        handler.execute('add "Test task"')
        result = handler.execute("update 1")
        assert "Error:" in result


class TestDeleteCommand:
    """Integration tests for delete command."""

    def test_delete_success(self, handler):
        """Test deleting a task."""
        handler.execute('add "Test task"')
        result = handler.execute("delete 1")
        assert "Deleted task #1" in result

        # Verify task is gone
        list_result = handler.execute("list")
        assert "No tasks found" in list_result

    def test_delete_not_found(self, handler):
        """Test deleting a non-existent task."""
        result = handler.execute("delete 99")
        assert "Error:" in result
        assert "not found" in result


class TestTagCommand:
    """Integration tests for tag command."""

    def test_tag_add(self, handler):
        """Test adding a tag."""
        handler.execute('add "Test task"')
        result = handler.execute("tag 1 add work")
        assert 'Added tag "work"' in result

    def test_tag_remove(self, handler):
        """Test removing a tag."""
        handler.execute('add "Test task" --tags work')
        result = handler.execute("tag 1 remove work")
        assert 'Removed tag "work"' in result

    def test_tag_not_found(self, handler):
        """Test tagging a non-existent task."""
        result = handler.execute("tag 99 add work")
        assert "Error:" in result
        assert "not found" in result


class TestSearchCommand:
    """Integration tests for search command."""

    def test_search_found(self, handler_with_tasks):
        """Test searching for matching tasks."""
        result = handler_with_tasks.execute("search groceries")
        assert "Buy groceries" in result
        assert "Review PR" not in result

    def test_search_case_insensitive(self, handler_with_tasks):
        """Test that search is case-insensitive."""
        result = handler_with_tasks.execute("search GROCERIES")
        assert "Buy groceries" in result

    def test_search_no_match(self, handler_with_tasks):
        """Test searching with no matches."""
        result = handler_with_tasks.execute("search xyz123")
        assert "No tasks found" in result


class TestHelpCommand:
    """Integration tests for help command."""

    def test_help_shows_commands(self, handler):
        """Test that help shows available commands."""
        result = handler.execute("help")
        assert "add" in result
        assert "list" in result
        assert "complete" in result
        assert "delete" in result


class TestUnknownCommand:
    """Integration tests for unknown commands."""

    def test_unknown_command(self, handler):
        """Test that unknown command shows error."""
        result = handler.execute("foobar")
        assert "Error:" in result
        assert "Unknown command" in result
        assert "foobar" in result
