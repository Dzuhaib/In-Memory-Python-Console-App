"""WebSocket Service - Broadcasts task updates to connected clients.

Task T052: FastAPI app with GET /dapr/subscribe, POST /api/events/task-updates,
and WebSocket endpoint GET /ws that broadcasts task changes to connected clients.
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Set

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

# Configure structured JSON logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
)
logger = logging.getLogger(__name__)

app = FastAPI(title="WebSocket Service", version="1.0.0")


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


class ConnectionManager:
    """Manages WebSocket connections and broadcasts."""

    def __init__(self):
        self.active_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        """Accept and register a new WebSocket connection."""
        await websocket.accept()
        self.active_connections.add(websocket)
        logger.info(json.dumps({
            "service": "websocket-service",
            "action": "client_connected",
            "total_connections": len(self.active_connections),
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }))

    def disconnect(self, websocket: WebSocket):
        """Unregister a WebSocket connection."""
        self.active_connections.discard(websocket)
        logger.info(json.dumps({
            "service": "websocket-service",
            "action": "client_disconnected",
            "total_connections": len(self.active_connections),
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }))

    async def broadcast(self, message: Dict[str, Any]):
        """Broadcast a message to all connected clients."""
        disconnected = set()
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Failed to send to client: {e}")
                disconnected.add(connection)

        # Clean up disconnected clients
        for conn in disconnected:
            self.disconnect(conn)


manager = ConnectionManager()


@app.get("/dapr/subscribe")
def get_subscriptions() -> List[DaprSubscription]:
    """Return Dapr subscription configuration.

    Task T052: Dapr subscription endpoint for websocket-service.
    """
    return [
        DaprSubscription(
            pubsubname="kafka-pubsub",
            topic="task-updates",
            route="/api/events/task-updates"
        )
    ]


@app.post("/api/events/task-updates")
async def handle_task_update(request: Request) -> Dict[str, str]:
    """Process task update event from Dapr Pub/Sub and broadcast to WebSocket clients.

    Task T052: Broadcast task changes to all connected WebSocket clients.

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

        # Prepare broadcast message
        broadcast_message = {
            "type": "task_update",
            "event_id": event.event_id,
            "event_type": event.event_type,
            "task_id": event.task_id,
            "task": event.task_snapshot,
            "timestamp": event.timestamp,
        }

        # Broadcast to all connected WebSocket clients
        await manager.broadcast(broadcast_message)

        logger.info(json.dumps({
            "service": "websocket-service",
            "action": "broadcast_sent",
            "event_type": event.event_type,
            "task_id": event.task_id,
            "clients": len(manager.active_connections),
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }))

        return {"status": "success"}

    except Exception as e:
        logger.error(json.dumps({
            "service": "websocket-service",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }))
        return {"status": "error", "message": str(e)}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time task updates.

    Task T052: WebSocket endpoint that broadcasts task changes to connected clients.

    Args:
        websocket: WebSocket connection
    """
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive by receiving (but ignoring) client messages
            data = await websocket.receive_text()
            # Optionally, clients could send filters or preferences here
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@app.get("/health")
def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "websocket-service",
        "active_connections": len(manager.active_connections),
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
