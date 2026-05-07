from fastapi import FastAPI

from app.routes.upload import router as upload_router
from app.routes.query import router as query_router
from app.routes.health import router as health_router

app = FastAPI(
    title="Intellexa AI",
    description="An AI-powered document management system that allows users to upload, query, and manage their documents efficiently.",
    version="1.0.0"
)

app.include_router(upload_router)
app.include_router(query_router)
app.include_router(health_router)