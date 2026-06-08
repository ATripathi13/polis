"""
Upload API — POST /upload
"""

from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.database import get_db
from app.services.analysis import analysis_service

router = APIRouter()


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    """Upload a document (audio, PDF, text) for analysis."""
    # For now, using a placeholder org ID since auth isn't fully implemented
    # In production, this would come from the current user's org
    placeholder_org_id = uuid.uuid4() 
    
    content = await file.read()
    doc = await analysis_service.ingest_document(
        db=db,
        filename=file.filename,
        content=content,
        file_type=file.content_type,
        organization_id=placeholder_org_id
    )
    
    return {
        "status": "uploaded",
        "document_id": str(doc.id),
        "meeting_id": str(doc.meeting_id),
        "filename": doc.filename,
    }
