"""FastAPI application entry point."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.router import api_router
from config import settings
from database import create_db_and_tables
from utils.logger import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager.

    Creates database tables on startup.
    """
    logger.info("Starting application...")
    create_db_and_tables()
    logger.info("Database tables created")
    yield
    logger.info("Shutting down application...")


app = FastAPI(
    title="Todo App API",
    description="REST API for Phase 2 Full Stack Web Application",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")
