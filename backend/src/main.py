"""FastAPI application entry point."""

import os
import sys
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Print startup info for debugging
print(f"Starting Todo API...", file=sys.stderr)
print(f"DATABASE_URL configured: {'Yes' if os.environ.get('DATABASE_URL') else 'No (using default)'}", file=sys.stderr)
print(f"PORT: {os.environ.get('PORT', 'Not set (using 8000)')}", file=sys.stderr)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager."""
    print("Initializing application...", file=sys.stderr)

    from database import create_db_and_tables
    from models.task import Task  # Ensure model is registered

    try:
        print("Creating database tables...", file=sys.stderr)
        create_db_and_tables()
        print("Database tables created successfully", file=sys.stderr)
    except Exception as e:
        print(f"ERROR during startup: {e}", file=sys.stderr)

    print("Application ready", file=sys.stderr)
    yield
    print("Shutting down application...", file=sys.stderr)


app = FastAPI(
    title="Todo App API",
    description="REST API for Phase 2 Full Stack Web Application",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS configuration
# For production: use wildcard without credentials
# For local: specific origins with credentials
cors_origins = os.environ.get("CORS_ORIGINS", "").strip()

if cors_origins:
    # Use configured origins (for production with specific frontend URL)
    origins_list = [o.strip() for o in cors_origins.split(",") if o.strip()]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    # Default: allow localhost for development + wildcard for production
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "http://localhost:5173",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5173",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        allow_origin_regex=r"https://.*\.railway\.app",  # Allow any Railway subdomain
    )

# Include API routes
from api.router import api_router
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def root():
    """Root endpoint for basic connectivity check."""
    return {
        "status": "ok",
        "message": "Todo API is running",
        "docs": "/docs",
        "health": "/api/v1/health",
    }


@app.get("/health")
def health():
    """Alternative health endpoint at root level."""
    from datetime import datetime
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


# Chat endpoint for AI assistant
from fastapi import Request as FastAPIRequest


@app.post("/chat")
async def chat_endpoint(request: FastAPIRequest):
    """Chat endpoint for AI-powered todo assistant."""
    from chatkit_server import chat_endpoint
    return await chat_endpoint(request)


# Task T059: Dapr Jobs callback endpoint
@app.post("/api/jobs/trigger")
async def jobs_trigger_callback(request: FastAPIRequest):
    """Callback endpoint for Dapr Jobs API.

    When a scheduled reminder job fires, Dapr calls this endpoint with the job data.
    This endpoint publishes a reminder.due event to the reminders topic via Dapr Pub/Sub.

    Expected request body:
    {
        "data": {
            "task_id": <int>,
            "type": "reminder",
            "payload": {...}
        }
    }
    """
    from services.event_publisher import get_event_publisher
    from config import settings
    from utils.logger import get_logger

    logger = get_logger(__name__)

    try:
        body = await request.json()
        job_data = body.get("data", {})
        task_id = job_data.get("task_id")
        reminder_type = job_data.get("type", "reminder")
        payload = job_data.get("payload", {})

        if not task_id:
            logger.warning("Jobs callback received without task_id")
            return {"status": "DROP", "message": "Missing task_id"}

        logger.info(f"Jobs callback received for task #{task_id}")

        # Publish reminder.due event to reminders topic
        publisher = get_event_publisher(
            dapr_port=settings.dapr_http_port,
            pubsub_name=settings.pubsub_name,
        )
        await publisher.publish(
            topic="reminders",
            event_type="reminder.due",
            task_id=task_id,
            task_snapshot=payload,
            actor="system",
            metadata={"reminder_type": reminder_type},
        )

        return {"status": "SUCCESS"}

    except Exception as e:
        logger.error(f"Error processing jobs callback: {e}")
        return {"status": "RETRY"}


# Task T064: Dapr subscription endpoint
@app.get("/dapr/subscribe")
async def dapr_subscribe():
    """Dapr programmatic subscription endpoint.

    The backend publishes to topics but does not subscribe to any.
    Consumer microservices have their own /dapr/subscribe endpoints.

    Returns an empty subscription list for the backend.
    """
    return []
