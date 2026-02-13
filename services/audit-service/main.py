"""Audit Service - Logs all task events for audit trail.

Task T046: FastAPI app with GET /dapr/subscribe returning subscription config
and POST /api/events/task-events that logs events as structured JSON to stdout.
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
    format='%(message)s',  # JSON only, no prefix
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Audit Service", version="1.0.0")


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

    Task T046: Dapr subscription endpoint for audit-service.
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

    Task T046: Log all task events as structured JSON to stdout for audit trail.

    Args:
        request: FastAPI request with event payload from Dapr

    Returns:
        Success response for Dapr
    """
    try:
        # Dapr sends events in CloudEvents format or raw JSON
        # Try to parse as JSON
        body = await request.json()

        # Extract event data (Dapr wraps it in CloudEvents envelope)
        if "data" in body:
            event_data = body["data"]
        else:
            event_data = body

        # Validate event structure
        event = TaskEvent(**event_data)

        # Log the event as structured JSON
        audit_record = {
            "service": "audit-service",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "event_id": event.event_id,
            "event_type": event.event_type,
            "task_id": event.task_id,
            "actor": event.actor,
            "task_snapshot": event.task_snapshot,
            "metadata": event.metadata,
        }

        logger.info(json.dumps(audit_record))

        return {"status": "success"}

    except Exception as e:
        logger.error(json.dumps({
            "service": "audit-service",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }))
        return {"status": "error", "message": str(e)}


@app.get("/health")
def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "audit-service",
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
