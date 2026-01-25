"""Task API endpoints."""

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from database import get_session
from models.task import Priority, Task
from schemas.task import AddTagRequest, CreateTaskRequest, UpdateTaskRequest
from services.task_service import TaskService

router = APIRouter()


def get_task_service(session: Session = Depends(get_session)) -> TaskService:
    """Dependency to get TaskService instance."""
    return TaskService(session)


@router.get("/tasks", response_model=List[Task])
def list_tasks(
    search: Optional[str] = Query(None, description="Search term for task titles"),
    status: Optional[str] = Query(None, description="Filter by status: complete/incomplete"),
    priority: Optional[Priority] = Query(None, description="Filter by priority"),
    tag: Optional[str] = Query(None, description="Filter by tag"),
    sort: Optional[str] = Query("id", description="Sort by: priority/alpha/id"),
    service: TaskService = Depends(get_task_service),
) -> List[Task]:
    """List all tasks with optional filtering, searching, and sorting."""
    return service.list_tasks(
        search=search,
        status=status,
        priority=priority,
        tag=tag,
        sort_by=sort,
    )


@router.post("/tasks", response_model=Task, status_code=201)
def create_task(
    request: CreateTaskRequest,
    service: TaskService = Depends(get_task_service),
) -> Task:
    """Create a new task."""
    return service.create_task(
        title=request.title,
        priority=request.priority,
        tags=request.tags,
    )


@router.get("/tasks/{task_id}", response_model=Task)
def get_task(
    task_id: int,
    service: TaskService = Depends(get_task_service),
) -> Task:
    """Get a single task by ID."""
    task = service.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/tasks/{task_id}", response_model=Task)
def update_task(
    task_id: int,
    request: UpdateTaskRequest,
    service: TaskService = Depends(get_task_service),
) -> Task:
    """Update an existing task."""
    if request.title is None and request.priority is None:
        raise HTTPException(status_code=400, detail="No changes specified")

    task = service.update_task(
        task_id=task_id,
        title=request.title,
        priority=request.priority,
    )
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/tasks/{task_id}", status_code=204)
def delete_task(
    task_id: int,
    service: TaskService = Depends(get_task_service),
) -> None:
    """Delete a task."""
    success = service.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")


@router.patch("/tasks/{task_id}/complete", response_model=Task)
def toggle_complete(
    task_id: int,
    service: TaskService = Depends(get_task_service),
) -> Task:
    """Toggle the completion status of a task."""
    task = service.toggle_complete(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("/tasks/{task_id}/tags", response_model=Task)
def add_tag(
    task_id: int,
    request: AddTagRequest,
    service: TaskService = Depends(get_task_service),
) -> Task:
    """Add a tag to a task."""
    task = service.add_tag(task_id, request.tag)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/tasks/{task_id}/tags/{tag}", response_model=Task)
def remove_tag(
    task_id: int,
    tag: str,
    service: TaskService = Depends(get_task_service),
) -> Task:
    """Remove a tag from a task."""
    task = service.remove_tag(task_id, tag)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.get("/health")
def health_check() -> dict:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
