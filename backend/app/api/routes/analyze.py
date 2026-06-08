"""
Analysis API — POST /analyze
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db

router = APIRouter()


@router.post("/analyze")
async def analyze_document(
    document_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Trigger analysis pipeline on an uploaded document."""
    # Will dispatch to Celery task in Phase 5
    return {
        "status": "queued",
        "document_id": document_id,
        "message": "Analysis pipeline started",
    }
