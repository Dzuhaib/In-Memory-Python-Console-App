"""FastAPI application entry point."""

import os
import sys
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings

# Print startup info for debugging
print(f"Starting Todo API...", file=sys.stderr)
print(f"DATABASE_URL configured: {'Yes' if os.environ.get('DATABASE_URL') else 'No (using default)'}", file=sys.stderr)
print(f"PORT: {os.environ.get('PORT', 'Not set (using 8000)')}", file=sys.stderr)
print(f"CORS_ORIGINS: {os.environ.get('CORS_ORIGINS', 'Not set (using defaults)')}", file=sys.stderr)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager."""
    print("Initializing application...", file=sys.stderr)

    # Import here to avoid circular imports and to delay DB connection
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

# Configure CORS - be permissive to avoid issues
# Check if we're in production (Railway sets various env vars)
is_production = any([
    os.environ.get("RAILWAY_ENVIRONMENT_NAME"),
    os.environ.get("RAILWAY_PROJECT_ID"),
    os.environ.get("RAILWAY_SERVICE_ID"),
])

print(f"Production mode: {is_production}", file=sys.stderr)

# In production, allow all origins without credentials (simplest, works)
# In development, use configured origins
if is_production:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,  # Must be False when using wildcard
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
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
