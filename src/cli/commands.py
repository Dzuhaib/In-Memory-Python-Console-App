"""Command handlers for the todo CLI."""

import re
import sys
from typing import Dict, List, Optional, Tuple, Callable

from src.models.task import Priority
from src.services.task_service import TaskService
from src.cli.display import format_task_list, format_success, format_error


def parse_args(input_str: str) -> Tuple[str, List[str], Dict[str, str]]:
    """Parse command input into command, positional args, and flags.

    Handles quoted strings and --flag value pairs.

    Args:
        input_str: Raw input string

    Returns:
        Tuple of (command, positional_args, flags)
    """
    # Match quoted strings or non-whitespace sequences
    pattern = r'"([^"]*)"|\'([^\']*)\'|(\S+)'
    matches = re.findall(pattern, input_str)

    # Flatten matches (each match is a tuple with one non-empty group)
    tokens = [m[0] or m[1] or m[2] for m in matches]

    if not tokens:
        return "", [], {}

    command = tokens[0].lower()
    positional: List[str] = []
    flags: Dict[str, str] = {}

    i = 1
    while i < len(tokens):
        token = tokens[i]
        if token.startswith("--"):
            flag_name = token[2:]
            if i + 1 < len(tokens) and not tokens[i + 1].startswith("--"):
                flags[flag_name] = tokens[i + 1]
                i += 2
            else:
                flags[flag_name] = ""
                i += 1
        else:
            positional.append(token)
            i += 1

    return command, positional, flags


class CommandHandler:
    """Handles CLI commands for the todo application."""

    def __init__(self, service: TaskService) -> None:
        """Initialize the command handler.

        Args:
            service: TaskService instance
        """
        self.service = service
        self._commands: Dict[str, Callable[..., str]] = {
            "add": self.cmd_add,
            "list": self.cmd_list,
            "complete": self.cmd_complete,
            "uncomplete": self.cmd_uncomplete,
            "update": self.cmd_update,
            "delete": self.cmd_delete,
            "tag": self.cmd_tag,
            "search": self.cmd_search,
            "help": self.cmd_help,
            "exit": self.cmd_exit,
            "quit": self.cmd_exit,
        }

    def execute(self, input_str: str) -> Optional[str]:
        """Execute a command from input string.

        Args:
            input_str: Raw command input

        Returns:
            Command output or None for exit
        """
        command, args, flags = parse_args(input_str.strip())

        if not command:
            return ""

        handler = self._commands.get(command)
        if handler is None:
            return format_error(
                f'Unknown command: "{command}". Type "help" for available commands.'
            )

        try:
            return handler(args, flags)
        except ValueError as e:
            return format_error(str(e))
        except Exception as e:
            return format_error(f"Unexpected error: {e}")

    def cmd_add(self, args: List[str], flags: Dict[str, str]) -> str:
        """Handle the add command."""
        if not args:
            return format_error(
                "Missing required argument: title. "
                "Usage: add <title> [--priority <level>] [--tags <tags>]"
            )

        title = args[0]
        if not title.strip():
            return format_error("Title cannot be empty")

        # Parse priority
        priority = Priority.MEDIUM
        if "priority" in flags:
            try:
                priority = Priority.from_string(flags["priority"])
            except ValueError as e:
                return format_error(str(e))

        # Parse tags
        tags: List[str] = []
        if "tags" in flags and flags["tags"]:
            tags = [t.strip() for t in flags["tags"].split(",") if t.strip()]

        task = self.service.create_task(title, priority, tags)

        result = f'Created task #{task.id}: "{task.title}" [{task.priority}]'
        if task.tags:
            result += f" (tags: {', '.join(task.tags)})"
        return result

    def cmd_list(self, args: List[str], flags: Dict[str, str]) -> str:
        """Handle the list command."""
        # Get filter parameters
        status = flags.get("status")
        priority = None
        if "priority" in flags:
            try:
                priority = Priority.from_string(flags["priority"])
            except ValueError as e:
                return format_error(str(e))

        tag = flags.get("tag")
        sort_by = flags.get("sort", "id")

        if sort_by not in ("priority", "alpha", "id"):
            return format_error(
                f'Invalid sort option: "{sort_by}". Use priority, alpha, or id.'
            )

        # Apply filters
        if status or priority or tag:
            tasks = self.service.filter_tasks(status, priority, tag)
        else:
            tasks = self.service.list_tasks()

        # Apply sorting
        tasks = self.service.sort_tasks(tasks, sort_by)

        return format_task_list(tasks)

    def cmd_complete(self, args: List[str], flags: Dict[str, str]) -> str:
        """Handle the complete command."""
        if not args:
            return format_error(
                "Missing required argument: id. Usage: complete <id>"
            )

        try:
            task_id = int(args[0])
            if task_id < 1:
                raise ValueError()
        except ValueError:
            return format_error("ID must be a positive integer")

        task = self.service.get_task(task_id)
        if task is None:
            return format_error(f"Task #{task_id} not found")

        if task.completed:
            return f"Task #{task_id} is already complete."

        self.service.complete_task(task_id)
        return f'Completed task #{task_id}: "{task.title}"'

    def cmd_uncomplete(self, args: List[str], flags: Dict[str, str]) -> str:
        """Handle the uncomplete command."""
        if not args:
            return format_error(
                "Missing required argument: id. Usage: uncomplete <id>"
            )

        try:
            task_id = int(args[0])
            if task_id < 1:
                raise ValueError()
        except ValueError:
            return format_error("ID must be a positive integer")

        task = self.service.get_task(task_id)
        if task is None:
            return format_error(f"Task #{task_id} not found")

        if not task.completed:
            return f"Task #{task_id} is already incomplete."

        self.service.uncomplete_task(task_id)
        return f'Marked task #{task_id} as incomplete: "{task.title}"'

    def cmd_update(self, args: List[str], flags: Dict[str, str]) -> str:
        """Handle the update command."""
        if not args:
            return format_error(
                "Missing required argument: id. "
                "Usage: update <id> [--title <title>] [--priority <level>]"
            )

        try:
            task_id = int(args[0])
            if task_id < 1:
                raise ValueError()
        except ValueError:
            return format_error("ID must be a positive integer")

        task = self.service.get_task(task_id)
        if task is None:
            return format_error(f"Task #{task_id} not found")

        new_title = flags.get("title")
        new_priority = None

        if "priority" in flags:
            try:
                new_priority = Priority.from_string(flags["priority"])
            except ValueError as e:
                return format_error(str(e))

        if new_title is None and new_priority is None:
            return format_error("Provide --title or --priority to update")

        if new_title is not None and not new_title.strip():
            return format_error("Title cannot be empty")

        self.service.update_task(task_id, new_title, new_priority)
        task = self.service.get_task(task_id)
        return f'Updated task #{task_id}: "{task.title}" [{task.priority}]'

    def cmd_delete(self, args: List[str], flags: Dict[str, str]) -> str:
        """Handle the delete command."""
        if not args:
            return format_error(
                "Missing required argument: id. Usage: delete <id>"
            )

        try:
            task_id = int(args[0])
            if task_id < 1:
                raise ValueError()
        except ValueError:
            return format_error("ID must be a positive integer")

        task = self.service.delete_task(task_id)
        if task is None:
            return format_error(f"Task #{task_id} not found")

        return f'Deleted task #{task_id}: "{task.title}"'

    def cmd_tag(self, args: List[str], flags: Dict[str, str]) -> str:
        """Handle the tag command."""
        if len(args) < 3:
            return format_error(
                "Missing arguments. Usage: tag <id> <add|remove> <tag>"
            )

        try:
            task_id = int(args[0])
            if task_id < 1:
                raise ValueError()
        except ValueError:
            return format_error("ID must be a positive integer")

        action = args[1].lower()
        tag = args[2]

        if action not in ("add", "remove"):
            return format_error('Action must be "add" or "remove"')

        if not tag.strip():
            return format_error("Tag cannot be empty")

        task = self.service.get_task(task_id)
        if task is None:
            return format_error(f"Task #{task_id} not found")

        if action == "add":
            self.service.add_tag(task_id, tag)
            return f'Added tag "{tag}" to task #{task_id}'
        else:
            self.service.remove_tag(task_id, tag)
            return f'Removed tag "{tag}" from task #{task_id}'

    def cmd_search(self, args: List[str], flags: Dict[str, str]) -> str:
        """Handle the search command."""
        keyword = args[0] if args else ""

        tasks = self.service.search_tasks(keyword)

        if not keyword:
            return format_task_list(tasks)

        if not tasks:
            return f'No tasks found matching "{keyword}".'

        return format_task_list(tasks, f'Search results for "{keyword}"')

    def cmd_help(self, args: List[str], flags: Dict[str, str]) -> str:
        """Handle the help command."""
        help_text = """Todo App - Available Commands:
  add <title>         Create a new task
  list                Display all tasks
  complete <id>       Mark task as complete
  uncomplete <id>     Mark task as incomplete
  update <id>         Update task details
  delete <id>         Remove a task
  tag <id>            Add or remove tags
  search <keyword>    Find tasks by keyword
  help [command]      Show this help
  exit                Quit the application

Use "help <command>" for detailed usage."""
        return help_text

    def cmd_exit(self, args: List[str], flags: Dict[str, str]) -> None:
        """Handle the exit command."""
        return None  # Signal to exit
