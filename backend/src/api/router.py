"""API router aggregation."""

from fastapi import APIRouter

from api.tasks import router as tasks_router

api_router = APIRouter()

# Include task routes
api_router.include_router(tasks_router, tags=["Tasks"])
