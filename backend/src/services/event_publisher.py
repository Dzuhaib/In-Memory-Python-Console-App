"""Event publisher for task mutations via Dapr Pub/Sub.

Task T039: Create EventPublisher class that publishes TaskEvent JSON via HTTP POST
to Dapr Pub/Sub endpoint (http://localhost:{DAPR_HTTP_PORT}/v1.0/publish/{PUBSUB_NAME}/{topic})
Task T057: Add schedule_reminder() function for Dapr Jobs API
Task T058: Add cancel_reminder() function for Dapr Jobs API
"""

import asyncio
import uuid
from datetime import datetime
from typing import Any, Dict, Optional

import httpx

from utils.logger import get_logger

logger = get_logger(__name__)


class EventPublisher:
    """Publishes task events to Kafka topics via Dapr Pub/Sub HTTP API."""

    def __init__(self, dapr_port: int = 3500, pubsub_name: str = "kafka-pubsub"):
        """Initialize the event publisher.

        Args:
            dapr_port: Dapr sidecar HTTP port (default: 3500)
            pubsub_name: Dapr Pub/Sub component name (default: kafka-pubsub)
        """
        self.base_url = f"http://localhost:{dapr_port}/v1.0/publish/{pubsub_name}"
        self.pubsub_name = pubsub_name
        self.dapr_port = dapr_port
        logger.info(f"EventPublisher initialized with Dapr at localhost:{dapr_port}")

    async def publish(
        self,
        topic: str,
        event_type: str,
        task_id: int,
        task_snapshot: Dict[str, Any],
        actor: str = "user",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Publish a TaskEvent to the specified topic via Dapr Pub/Sub.

        This is a fire-and-forget async operation that logs errors but does not block
        or fail the main API operation.

        Args:
            topic: Kafka topic name (e.g., "task-events", "task-updates", "reminders")
            event_type: Event type (e.g., "task.created", "task.updated", "task.completed", "task.deleted")
            task_id: Task identifier
            task_snapshot: Full task state as dict (from task_to_dict())
            actor: Who triggered the event ("user" or "system")
            metadata: Optional metadata dict for additional context
        """
        event = {
            "event_id": str(uuid.uuid4()),
            "event_type": event_type,
            "task_id": task_id,
            "task_snapshot": task_snapshot,
            "actor": actor,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

        if metadata:
            event["metadata"] = metadata

        url = f"{self.base_url}/{topic}"

        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.post(url, json=event)
                response.raise_for_status()
                logger.info(
                    f"Published event {event['event_id']} ({event_type}) to topic {topic} for task #{task_id}"
                )
        except httpx.HTTPStatusError as e:
            logger.error(
                f"Failed to publish event {event['event_id']} to topic {topic}: HTTP {e.response.status_code}"
            )
        except httpx.RequestError as e:
            logger.warning(
                f"Dapr Pub/Sub not available at {url}, skipping event publish: {e}"
            )
        except Exception as e:
            logger.error(
                f"Unexpected error publishing event {event['event_id']} to topic {topic}: {e}"
            )

    def publish_sync(
        self,
        topic: str,
        event_type: str,
        task_id: int,
        task_snapshot: Dict[str, Any],
        actor: str = "user",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Synchronous wrapper for publish() to be called from sync contexts.

        Uses asyncio.create_task() for fire-and-forget behavior without blocking.
        If no event loop is running, creates a new one temporarily.

        Args:
            topic: Kafka topic name
            event_type: Event type
            task_id: Task identifier
            task_snapshot: Full task state as dict
            actor: Who triggered the event ("user" or "system")
            metadata: Optional metadata dict
        """
        try:
            # Try to get the running event loop
            loop = asyncio.get_running_loop()
            # Schedule the coroutine as a background task
            loop.create_task(
                self.publish(topic, event_type, task_id, task_snapshot, actor, metadata)
            )
        except RuntimeError:
            # No event loop is running; create one temporarily
            try:
                asyncio.run(
                    self.publish(topic, event_type, task_id, task_snapshot, actor, metadata)
                )
            except Exception as e:
                logger.error(f"Failed to publish event synchronously: {e}")


# Singleton instance to be used across the application
_event_publisher: Optional[EventPublisher] = None


def get_event_publisher(dapr_port: int = 3500, pubsub_name: str = "kafka-pubsub") -> EventPublisher:
    """Get or create the singleton EventPublisher instance.

    Args:
        dapr_port: Dapr sidecar HTTP port
        pubsub_name: Dapr Pub/Sub component name

    Returns:
        EventPublisher instance
    """
    global _event_publisher
    if _event_publisher is None:
        _event_publisher = EventPublisher(dapr_port=dapr_port, pubsub_name=pubsub_name)
    return _event_publisher


# Task T057: Dapr Jobs API for reminder scheduling
async def schedule_reminder(
    task_id: int,
    remind_at: datetime,
    payload: Dict[str, Any],
    dapr_port: int = 3500,
) -> None:
    """Schedule a reminder job via Dapr Jobs API.

    Creates a one-shot job that fires at the specified remind_at time.
    When the job fires, Dapr calls the /api/jobs/trigger callback endpoint.

    Args:
        task_id: Task identifier
        remind_at: When to fire the reminder (UTC datetime)
        payload: Additional data to pass to the callback (e.g., task details)
        dapr_port: Dapr sidecar HTTP port (default: 3500)
    """
    job_name = f"reminder-task-{task_id}"
    url = f"http://localhost:{dapr_port}/v1.0-alpha1/jobs/{job_name}"

    # Format dueTime as ISO 8601 with 'Z' suffix for UTC
    due_time = remind_at.isoformat()
    if not due_time.endswith('Z'):
        due_time += 'Z'

    job_body = {
        "schedule": "@every 0s",  # One-shot job via dueTime
        "dueTime": due_time,
        "data": {
            "task_id": task_id,
            "type": "reminder",
            "payload": payload,
        },
    }

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(url, json=job_body)
            response.raise_for_status()
            logger.info(f"Scheduled reminder job {job_name} for {remind_at.isoformat()}")
    except httpx.HTTPStatusError as e:
        logger.error(f"Failed to schedule reminder job {job_name}: HTTP {e.response.status_code}")
    except httpx.RequestError as e:
        logger.warning(f"Dapr Jobs API not available at {url}, skipping reminder scheduling: {e}")
    except Exception as e:
        logger.error(f"Unexpected error scheduling reminder job {job_name}: {e}")


# Task T058: Cancel a scheduled reminder job
async def cancel_reminder(task_id: int, dapr_port: int = 3500) -> None:
    """Cancel a scheduled reminder job via Dapr Jobs API.

    Deletes the job identified by the task_id.

    Args:
        task_id: Task identifier
        dapr_port: Dapr sidecar HTTP port (default: 3500)
    """
    job_name = f"reminder-task-{task_id}"
    url = f"http://localhost:{dapr_port}/v1.0-alpha1/jobs/{job_name}"

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.delete(url)
            # 204 No Content is the success response for DELETE
            if response.status_code in (200, 204):
                logger.info(f"Cancelled reminder job {job_name}")
            elif response.status_code == 404:
                logger.debug(f"Reminder job {job_name} not found (already fired or never created)")
            else:
                response.raise_for_status()
    except httpx.HTTPStatusError as e:
        if e.response.status_code != 404:
            logger.error(f"Failed to cancel reminder job {job_name}: HTTP {e.response.status_code}")
    except httpx.RequestError as e:
        logger.warning(f"Dapr Jobs API not available at {url}, skipping reminder cancellation: {e}")
    except Exception as e:
        logger.error(f"Unexpected error cancelling reminder job {job_name}: {e}")


# Sync wrapper for schedule_reminder
def schedule_reminder_sync(
    task_id: int,
    remind_at: datetime,
    payload: Dict[str, Any],
    dapr_port: int = 3500,
) -> None:
    """Synchronous wrapper for schedule_reminder() to be called from sync contexts.

    Args:
        task_id: Task identifier
        remind_at: When to fire the reminder (UTC datetime)
        payload: Additional data to pass to the callback
        dapr_port: Dapr sidecar HTTP port (default: 3500)
    """
    try:
        loop = asyncio.get_running_loop()
        loop.create_task(schedule_reminder(task_id, remind_at, payload, dapr_port))
    except RuntimeError:
        try:
            asyncio.run(schedule_reminder(task_id, remind_at, payload, dapr_port))
        except Exception as e:
            logger.error(f"Failed to schedule reminder synchronously: {e}")


# Sync wrapper for cancel_reminder
def cancel_reminder_sync(task_id: int, dapr_port: int = 3500) -> None:
    """Synchronous wrapper for cancel_reminder() to be called from sync contexts.

    Args:
        task_id: Task identifier
        dapr_port: Dapr sidecar HTTP port (default: 3500)
    """
    try:
        loop = asyncio.get_running_loop()
        loop.create_task(cancel_reminder(task_id, dapr_port))
    except RuntimeError:
        try:
            asyncio.run(cancel_reminder(task_id, dapr_port))
        except Exception as e:
            logger.error(f"Failed to cancel reminder synchronously: {e}")
