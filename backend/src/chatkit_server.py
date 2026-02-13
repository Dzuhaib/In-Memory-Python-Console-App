"""ChatKit server implementation for AI-powered todo assistant using OpenAI Agents SDK."""

# Task T017: Update chatbot create_task tool to accept optional due_at and remind_at
# Task T018: Update chatbot update_task tool to accept optional due_at and remind_at
# Task T019: Update chatbot format_task() to show due date and overdue indicator

import os
import json
from datetime import datetime
from typing import AsyncIterator

from fastapi import Request
from fastapi.responses import StreamingResponse
from agents import Agent, function_tool, Runner, set_default_openai_key

from config import settings
from database import get_session
from services.task_service import TaskService
from models.task import Priority, RecurrenceRule

# Set OpenAI API key
api_key = settings.openai_api_key or os.environ.get("OPENAI_API_KEY")
if api_key:
    set_default_openai_key(api_key)


def format_task(task) -> str:
    """Format a task for display.

    Task T019: Show due date and overdue indicator.
    """
    status = "✓" if task.completed else "○"
    priority_icon = "🔴" if task.priority == Priority.HIGH else "🟡" if task.priority == Priority.MEDIUM else "🟢"
    tags = f" [{', '.join(task.tags)}]" if task.tags else ""

    # Add due date and overdue indicator (T019)
    due_info = ""
    if task.due_at:
        now = datetime.utcnow()
        is_overdue = task.due_at < now and not task.completed
        overdue_flag = " ⚠️ OVERDUE" if is_overdue else ""
        due_info = f" | Due: {task.due_at.strftime('%Y-%m-%d %H:%M')}{overdue_flag}"

    return f"{status} #{task.id}: {task.title} {priority_icon}{tags}{due_info}"


def format_task_list(tasks) -> str:
    """Format multiple tasks for display."""
    if not tasks:
        return "You don't have any tasks yet. Try adding one!"
    return "\n".join(format_task(task) for task in tasks)


# Define tools for the todo assistant
@function_tool
def create_task(
    title: str,
    priority: str = "medium",
    tags: list[str] = None,
    due_at: str = None,
    remind_at: str = None,
    recurrence_rule: str = None,
    recurrence_interval: int = None,
) -> str:
    """Create a new task with a title and optional priority, tags, due date, reminder, and recurrence.

    Task T017: Accept optional due_at and remind_at string parameters (ISO 8601).

    Args:
        title: The task title/description
        priority: Priority level (high, medium, or low)
        tags: Optional list of tags
        due_at: Optional due date in ISO 8601 format (e.g., "2026-02-15T10:00:00")
        remind_at: Optional reminder time in ISO 8601 format
        recurrence_rule: Optional recurrence pattern (daily, weekly, monthly, every_N_days)
        recurrence_interval: Optional custom interval for every_N_days rule
    """
    with next(get_session()) as session:
        service = TaskService(session)

        # Parse datetime strings
        due_at_dt = datetime.fromisoformat(due_at) if due_at else None
        remind_at_dt = datetime.fromisoformat(remind_at) if remind_at else None
        recurrence_rule_enum = RecurrenceRule(recurrence_rule) if recurrence_rule else None

        task = service.create_task(
            title=title,
            priority=Priority(priority),
            tags=tags or [],
            due_at=due_at_dt,
            remind_at=remind_at_dt,
            recurrence_rule=recurrence_rule_enum,
            recurrence_interval=recurrence_interval,
        )
        return f"Created task: {format_task(task)}"


@function_tool
def list_tasks(
    search: str = None,
    status: str = None,
    priority: str = None,
    tag: str = None,
    due_before: str = None,
    due_after: str = None,
    overdue: bool = None,
) -> str:
    """List all tasks with optional filters.

    Task T035: Support due_before, due_after, and overdue filter params.

    Args:
        search: Search term to filter tasks by title
        status: Filter by 'complete' or 'incomplete'
        priority: Filter by priority (high, medium, low)
        tag: Filter by tag
        due_before: Filter tasks due before this datetime (ISO 8601)
        due_after: Filter tasks due after this datetime (ISO 8601)
        overdue: Filter only overdue tasks
    """
    with next(get_session()) as session:
        service = TaskService(session)

        # Parse datetime strings
        priority_enum = Priority(priority) if priority else None
        due_before_dt = datetime.fromisoformat(due_before) if due_before else None
        due_after_dt = datetime.fromisoformat(due_after) if due_after else None

        tasks = service.list_tasks(
            search=search,
            status=status,
            priority=priority_enum,
            tag=tag,
            due_before=due_before_dt,
            due_after=due_after_dt,
            overdue=overdue,
        )
        return format_task_list(tasks)


@function_tool
def get_task(task_id: int) -> str:
    """Get a single task by its ID.

    Args:
        task_id: The task ID to retrieve
    """
    with next(get_session()) as session:
        service = TaskService(session)
        task = service.get_task(task_id)
        if task:
            return format_task(task)
        return f"Task #{task_id} not found."


@function_tool
def update_task(
    task_id: int,
    title: str = None,
    priority: str = None,
    due_at: str = None,
    remind_at: str = None,
    recurrence_rule: str = None,
    recurrence_interval: int = None,
) -> str:
    """Update a task's title, priority, due date, reminder, or recurrence.

    Task T018: Accept optional due_at and remind_at parameters.

    Args:
        task_id: The task ID to update
        title: New title (optional)
        priority: New priority (optional)
        due_at: New due date in ISO 8601 format (optional)
        remind_at: New reminder time in ISO 8601 format (optional)
        recurrence_rule: New recurrence pattern (optional)
        recurrence_interval: New custom interval (optional)
    """
    with next(get_session()) as session:
        service = TaskService(session)

        # Parse datetime strings
        priority_enum = Priority(priority) if priority else None
        due_at_dt = datetime.fromisoformat(due_at) if due_at else None
        remind_at_dt = datetime.fromisoformat(remind_at) if remind_at else None
        recurrence_rule_enum = RecurrenceRule(recurrence_rule) if recurrence_rule else None

        task = service.update_task(
            task_id,
            title=title,
            priority=priority_enum,
            due_at=due_at_dt,
            remind_at=remind_at_dt,
            recurrence_rule=recurrence_rule_enum,
            recurrence_interval=recurrence_interval,
        )
        if task:
            return f"Updated task: {format_task(task)}"
        return f"Task #{task_id} not found."


@function_tool
def delete_task(task_id: int) -> str:
    """Delete a task by its ID.

    Args:
        task_id: The task ID to delete
    """
    with next(get_session()) as session:
        service = TaskService(session)
        if service.delete_task(task_id):
            return f"Deleted task #{task_id}."
        return f"Task #{task_id} not found."


@function_tool
def toggle_complete(task_id: int) -> str:
    """Toggle a task's completion status.

    Args:
        task_id: The task ID to toggle
    """
    with next(get_session()) as session:
        service = TaskService(session)
        task = service.toggle_complete(task_id)
        if task:
            status = "completed" if task.completed else "incomplete"
            return f"Marked task #{task_id} as {status}: {format_task(task)}"
        return f"Task #{task_id} not found."


@function_tool
def add_tag(task_id: int, tag: str) -> str:
    """Add a tag to a task.

    Args:
        task_id: The task ID
        tag: The tag to add
    """
    with next(get_session()) as session:
        service = TaskService(session)
        task = service.add_tag(task_id, tag)
        if task:
            return f"Added tag '{tag}' to task #{task_id}: {format_task(task)}"
        return f"Task #{task_id} not found."


@function_tool
def remove_tag(task_id: int, tag: str) -> str:
    """Remove a tag from a task.

    Args:
        task_id: The task ID
        tag: The tag to remove
    """
    with next(get_session()) as session:
        service = TaskService(session)
        task = service.remove_tag(task_id, tag)
        if task:
            return f"Removed tag '{tag}' from task #{task_id}: {format_task(task)}"
        return f"Task #{task_id} not found."


# Create the todo assistant agent
todo_agent = Agent(
    name="Todo Assistant",
    instructions="""You are a helpful todo assistant. You help users manage their tasks through natural conversation.

When users want to:
- Add tasks: Use create_task with the title, priority (if mentioned), tags (if mentioned), due_at (if mentioned), remind_at (if mentioned), and recurrence_rule (if mentioned)
- View tasks: Use list_tasks with appropriate filters based on what they ask for
- Complete tasks: Use toggle_complete with the task ID
- Delete tasks: Use delete_task with the task ID
- Update tasks: Use update_task with the task ID and changes (including due_at, remind_at, recurrence_rule)
- Add/remove tags: Use add_tag or remove_tag

For dates and times:
- Parse natural language dates (e.g., "tomorrow at 3pm", "next Monday", "in 2 days") and convert to ISO 8601 format
- When users mention "remind me", set the remind_at field
- When users mention recurring tasks (e.g., "daily", "every week", "monthly"), set the recurrence_rule field

Always confirm what you did after completing an action. If a user's request is unclear, ask for clarification.

Format task lists nicely with emojis and clear formatting. Be friendly and helpful!""",
    tools=[create_task, list_tasks, get_task, update_task, delete_task, toggle_complete, add_tag, remove_tag],
    model="gpt-4o-mini",
)


async def handle_chat_message(user_message: str) -> AsyncIterator[str]:
    """Handle a chat message and stream the response."""
    from agents.stream_events import RawResponsesStreamEvent
    from openai.types.responses import ResponseTextDeltaEvent

    result = Runner.run_streamed(todo_agent, user_message)

    async for event in result.stream_events():
        # Handle text delta events from streaming response only
        if isinstance(event, RawResponsesStreamEvent):
            if isinstance(event.data, ResponseTextDeltaEvent):
                yield event.data.delta


async def chat_endpoint(request: Request):
    """Simple chat endpoint that accepts a message and streams the response."""
    import sys
    import traceback

    try:
        body = await request.json()
    except Exception:
        return {"error": "Invalid JSON body"}

    user_message = body.get("message", "")

    if not user_message:
        return {"error": "Message is required"}

    if not api_key:
        return {"error": "OpenAI API key is not configured"}

    async def generate():
        try:
            async for chunk in handle_chat_message(user_message):
                yield f"data: {json.dumps({'content': chunk})}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            error_msg = str(e)
            print(f"Chat error: {error_msg}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            if "quota" in error_msg.lower():
                error_msg = "OpenAI API quota exceeded. Please check your billing details."
            elif "api key" in error_msg.lower() or "authentication" in error_msg.lower():
                error_msg = "OpenAI API key is invalid or not configured."
            elif "could not" in error_msg.lower() or "connection" in error_msg.lower():
                error_msg = "Could not connect to OpenAI. Please try again."
            yield f"data: {json.dumps({'error': error_msg})}\n\n"
            yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")
