"""
Polis — FastAPI Application Entry Point
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events."""
    # Startup
    from app.database import engine, Base
    from app.models import (  # noqa: F401 — ensure all models are loaded
        user, organization, conversation, meeting,
        task, decision, contradiction, risk, summary, document,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown
    await engine.dispose()


app = FastAPI(
    title=settings.app_name,
    description="AI Operational Intelligence Chatbot — Analyzes discussions to identify tasks, decisions, risks, contradictions, and generates executive summaries.",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    redoc_url="/api/redoc",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---- Route Includes ----
from app.api.routes import upload, analyze, chat, memory, slack, whatsapp  # noqa: E402

app.include_router(upload.router, prefix="/api", tags=["Upload"])
app.include_router(analyze.router, prefix="/api", tags=["Analysis"])
app.include_router(chat.router, prefix="/api", tags=["Chat"])
app.include_router(memory.router, prefix="/api", tags=["Memory"])
app.include_router(slack.router, prefix="/api", tags=["Slack"])
app.include_router(whatsapp.router, prefix="/api", tags=["WhatsApp"])


@app.get("/api/health", tags=["Health"])
async def health_check():
    return {"status": "healthy", "service": settings.app_name}
