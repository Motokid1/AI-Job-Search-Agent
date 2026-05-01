import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.analysis import router as analysis_router
from app.api.routes.health import router as health_router
from app.api.routes.jobs import router as jobs_router
from app.api.routes.match import router as match_router
from app.api.routes.resume import router as resume_router
from app.core.config import get_settings
from app.core.logging import configure_logging

settings = get_settings()
configure_logging()

logger = logging.getLogger(__name__)
logger.info("Starting AI Job Search Agent Backend")

app = FastAPI(
    title=settings.app_name,
    version="3.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api/v1")
app.include_router(resume_router, prefix="/api/v1")
app.include_router(jobs_router, prefix="/api/v1")
app.include_router(analysis_router, prefix="/api/v1")
app.include_router(match_router, prefix="/api/v1")


@app.get("/")
def root():
    return {
        "message": "AI Job Search Agent Backend is running",
        "docs": "/docs",
        "version": "3.0.0",
    }