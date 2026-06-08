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
    from app.worker.tasks import analyze_document as analyze_task
    from app.models.document import Document
    import uuid
    
    # 1. Verify document exists
    stmt = select(Document).where(Document.id == uuid.UUID(document_id))
    result = await db.execute(stmt)
    doc = result.scalar_one_or_none()
    
    if not doc:
        return {"status": "error", "message": "Document not found"}

    # 2. Trigger Celery Task
    task = analyze_task.delay(document_id, str(doc.organization_id))
    
    return {
        "status": "queued",
        "job_id": task.id,
        "document_id": document_id,
        "message": "Analysis pipeline started",
    }
