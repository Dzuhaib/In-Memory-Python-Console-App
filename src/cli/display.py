"""Display formatting functions for CLI output."""

from typing import List

from src.models.task import Task


def format_task(task: Task) -> str:
    """Format a single task for display.

    Args:
        task: The task to format

    Returns:
        Formatted task string
    """
    status = "[x]" if task.completed else "[ ]"
    priority = f"[{task.priority}]"

    parts = [f"  {status} #{task.id} {task.title} {priority}"]

    if task.tags:
        tags_str = ", ".join(task.tags)
        parts.append(f"(tags: {tags_str})")

    return " ".join(parts)


def format_task_list(tasks: List[Task], header: str = "Tasks") -> str:
    """Format a list of tasks for display.

    Args:
        tasks: List of tasks to format
        header: Header text for the list

    Returns:
        Formatted task list string
    """
    if not tasks:
        return "No tasks found."

    lines = [f"{header} ({len(tasks)}):"]
    for task in tasks:
        lines.append(format_task(task))

    return "\n".join(lines)


def format_success(message: str) -> str:
    """Format a success message.

    Args:
        message: The success message

    Returns:
        Formatted message
    """
    return message


def format_error(message: str) -> str:
    """Format an error message.

    Args:
        message: The error message

    Returns:
        Formatted error message
    """
    return f"Error: {message}"
