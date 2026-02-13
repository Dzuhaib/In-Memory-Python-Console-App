"""Notification Service - Processes reminder events.

Task T048: FastAPI app with GET /dapr/subscribe and POST /api/events/reminders
that logs reminder notifications and optionally republishes to task-updates.
"""

import json
import logging
from datetime import datetime
from typing import Any, Dict, List

from fastapi import FastAPI, Request
from pydantic import BaseModel

# Configure structured JSON logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Notification Service", version="1.0.0")


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

    Task T048: Dapr subscription endpoint for notification-service.
    """
    return [
        DaprSubscription(
            pubsubname="kafka-pubsub",
            topic="reminders",
            route="/api/events/reminders"
        )
    ]


@app.post("/api/events/reminders")
async def handle_reminder_event(request: Request) -> Dict[str, str]:
    """Process reminder event from Dapr Pub/Sub.

    Task T048: Log reminder notifications and optionally republish to task-updates.

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

        # Log the reminder notification
        notification = {
            "service": "notification-service",
            "type": "reminder",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "event_id": event.event_id,
            "task_id": event.task_id,
            "task_title": event.task_snapshot.get("title", ""),
            "due_at": event.task_snapshot.get("due_at"),
            "remind_at": event.task_snapshot.get("remind_at"),
            "message": f"Reminder: Task #{event.task_id} - {event.task_snapshot.get('title', '')} is due soon"
        }

        logger.info(json.dumps(notification))

        # TODO: In production, send actual notifications (email, SMS, push)
        # For now, we just log the reminder notification

        # Optionally republish to task-updates for WebSocket broadcast
        # (This would require httpx and Dapr Pub/Sub client - skipped for MVP)

        return {"status": "success"}

    except Exception as e:
        logger.error(json.dumps({
            "service": "notification-service",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }))
        return {"status": "error", "message": str(e)}


@app.get("/health")
def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "notification-service",
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
