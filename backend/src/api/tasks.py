"""Task API endpoints."""

# Task T010: Update task_to_dict() to include new fields + computed is_overdue
# Task T041-T044: Integrate EventPublisher with TaskService

import traceback
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from config import settings
from database import get_session
from models.task import Priority, Task
from schemas.task import AddTagRequest, CreateTaskRequest, UpdateTaskRequest
from services.task_service import TaskService
from services.event_publisher import get_event_publisher

router = APIRouter()


def task_to_dict(t: Task) -> dict:
    """Safely serialize a Task to a dict with Phase 5 fields (T010)."""
    now = datetime.utcnow()

    # Compute is_overdue: due_at < now and not completed
    is_overdue = False
    if t.due_at and not t.completed:
        is_overdue = t.due_at < now

    return {
        "id": t.id,
        "title": t.title,
        "completed": t.completed,
        "priority": t.priority.value if hasattr(t.priority, 'value') else t.priority,
        "tags": t.tags if t.tags else [],
        "created_at": t.created_at.isoformat() if t.created_at else None,
        "updated_at": t.updated_at.isoformat() if t.updated_at else None,
        # Phase 5 fields
        "due_at": t.due_at.isoformat() if t.due_at else None,
        "remind_at": t.remind_at.isoformat() if t.remind_at else None,
        "recurrence_rule": t.recurrence_rule.value if t.recurrence_rule and hasattr(t.recurrence_rule, 'value') else t.recurrence_rule,
        "recurrence_interval": t.recurrence_interval,
        "is_overdue": is_overdue,
    }


def get_task_service(session: Session = Depends(get_session)) -> TaskService:
    """Dependency to get TaskService instance with EventPublisher."""
    event_publisher = get_event_publisher(
        dapr_port=settings.dapr_http_port,
        pubsub_name=settings.pubsub_name
    )
    return TaskService(session, event_publisher=event_publisher)


@router.get("/tasks")
def list_tasks(
    search: Optional[str] = Query(None, description="Search term for task titles"),
    status: Optional[str] = Query(None, description="Filter by status: complete/incomplete"),
    priority: Optional[Priority] = Query(None, description="Filter by priority"),
    tag: Optional[str] = Query(None, description="Filter by tag"),
    sort: Optional[str] = Query("id", description="Sort by: priority/alpha/id/due_date/created_at"),
    due_before: Optional[datetime] = Query(None, description="Filter tasks due before this datetime"),
    due_after: Optional[datetime] = Query(None, description="Filter tasks due after this datetime"),
    overdue: Optional[bool] = Query(None, description="Filter only overdue tasks"),
    sort_dir: Optional[str] = Query("asc", description="Sort direction: asc/desc"),
    service: TaskService = Depends(get_task_service),
):
    """List all tasks with optional filtering, searching, and sorting.

    Task T031: Add due_before, due_after, and overdue query parameters.
    Task T032: Add sort_dir query parameter.
    """
    try:
        tasks = service.list_tasks(
            search=search,
            status=status,
            priority=priority,
            tag=tag,
            sort_by=sort,
            due_before=due_before,
            due_after=due_after,
            overdue=overdue,
            sort_dir=sort_dir,
        )
        return [task_to_dict(t) for t in tasks]
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tasks", status_code=201)
def create_task(
    request: CreateTaskRequest,
    service: TaskService = Depends(get_task_service),
):
    """Create a new task.

    Task T015: Pass due_at and remind_at from request to service.
    """
    try:
        task = service.create_task(
            title=request.title,
            priority=request.priority,
            tags=request.tags,
            due_at=request.due_at,
            remind_at=request.remind_at,
            recurrence_rule=request.recurrence_rule,
            recurrence_interval=request.recurrence_interval,
        )
        return task_to_dict(task)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tasks/{task_id}")
def get_task(
    task_id: int,
    service: TaskService = Depends(get_task_service),
):
    """Get a single task by ID."""
    try:
        task = service.get_task(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task_to_dict(task)
    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/tasks/{task_id}")
def update_task(
    task_id: int,
    request: UpdateTaskRequest,
    service: TaskService = Depends(get_task_service),
):
    """Update an existing task.

    Task T016: Pass due_at and remind_at from request to service.
    """
    try:
        # Check if any field is provided
        if all(v is None for v in [request.title, request.priority, request.due_at, request.remind_at, request.recurrence_rule, request.recurrence_interval]):
            raise HTTPException(status_code=400, detail="No changes specified")

        task = service.update_task(
            task_id=task_id,
            title=request.title,
            priority=request.priority,
            due_at=request.due_at,
            remind_at=request.remind_at,
            recurrence_rule=request.recurrence_rule,
            recurrence_interval=request.recurrence_interval,
        )
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task_to_dict(task)
    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/tasks/{task_id}", status_code=204)
def delete_task(
    task_id: int,
    service: TaskService = Depends(get_task_service),
) -> None:
    """Delete a task."""
    success = service.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")


@router.patch("/tasks/{task_id}/complete")
def toggle_complete(
    task_id: int,
    service: TaskService = Depends(get_task_service),
):
    """Toggle the completion status of a task."""
    try:
        task = service.toggle_complete(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task_to_dict(task)
    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tasks/{task_id}/tags")
def add_tag(
    task_id: int,
    request: AddTagRequest,
    service: TaskService = Depends(get_task_service),
):
    """Add a tag to a task."""
    try:
        task = service.add_tag(task_id, request.tag)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task_to_dict(task)
    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/tasks/{task_id}/tags/{tag}")
def remove_tag(
    task_id: int,
    tag: str,
    service: TaskService = Depends(get_task_service),
):
    """Remove a tag from a task."""
    try:
        task = service.remove_tag(task_id, tag)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task_to_dict(task)
    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
def health_check() -> dict:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
