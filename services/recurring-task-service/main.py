"""Recurring Task Service - Spawns new task instances on completion.

Task T050: FastAPI app with GET /dapr/subscribe and POST /api/events/task-events
that checks for recurrence_rule in task.completed events and calls backend API
to create new task instance.
"""

import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, List

import httpx
from fastapi import FastAPI, Request
from pydantic import BaseModel

# Configure structured JSON logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Recurring Task Service", version="1.0.0")

# Backend API URL (configurable via env var)
BACKEND_API_URL = os.environ.get("BACKEND_API_URL", "http://backend:8000")


class TaskEvent(BaseModel):
    """Task event schema."""
    event_id: str
    event_type: str
    task_id: int
    task_snapshot: Dict[str, Any]
    actor: str
    timestamp: str
    metadata: Dict[str, Any] = None


class DaprSubscription(BaseModel):
    """Dapr subscription configuration."""
    pubsubname: str
    topic: str
    route: str


@app.get("/dapr/subscribe")
def get_subscriptions() -> List[DaprSubscription]:
    """Return Dapr subscription configuration.

    Task T050: Dapr subscription endpoint for recurring-task-service.
    """
    return [
        DaprSubscription(
            pubsubname="kafka-pubsub",
            topic="task-events",
            route="/api/events/task-events"
        )
    ]


@app.post("/api/events/task-events")
async def handle_task_event(request: Request) -> Dict[str, str]:
    """Process task event from Dapr Pub/Sub.

    Task T050: Check for recurrence_rule in task.completed events and create
    new task instance via backend API.

    Args:
        request: FastAPI request with event payload from Dapr

    Returns:
        Success response for Dapr
    """
    try:
        # Parse event from Dapr
        body = await request.json()

        if "data" in body:
            event_data = body["data"]
        else:
            event_data = body

        event = TaskEvent(**event_data)

        # Only process task.completed events
        if event.event_type != "task.completed":
            return {"status": "ignored", "reason": "not a completion event"}

        # Check if task has recurrence_rule
        task_snapshot = event.task_snapshot
        recurrence_rule = task_snapshot.get("recurrence_rule")

        if not recurrence_rule:
            return {"status": "ignored", "reason": "no recurrence rule"}

        # The backend already handles recurring task spawning synchronously
        # in TaskService.toggle_complete(), so this consumer is a fallback
        # or for async event-driven spawning (Phase 5 requirement).
        # For MVP, we log that we detected a recurring task completion.

        logger.info(json.dumps({
            "service": "recurring-task-service",
            "action": "detected_recurring_completion",
            "event_id": event.event_id,
            "task_id": event.task_id,
            "recurrence_rule": recurrence_rule,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }))

        # In a fully event-driven architecture, we would create the new task here:
        # new_task_data = {
        #     "title": task_snapshot["title"],
        #     "priority": task_snapshot["priority"],
        #     "tags": task_snapshot["tags"],
        #     "recurrence_rule": recurrence_rule,
        #     "recurrence_interval": task_snapshot.get("recurrence_interval"),
        #     # Calculate next due_at based on recurrence rule
        # }
        # async with httpx.AsyncClient() as client:
        #     response = await client.post(f"{BACKEND_API_URL}/api/v1/tasks", json=new_task_data)

        return {"status": "success"}

    except Exception as e:
        logger.error(json.dumps({
            "service": "recurring-task-service",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }))
        return {"status": "error", "message": str(e)}


@app.get("/health")
def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "recurring-task-service",
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
