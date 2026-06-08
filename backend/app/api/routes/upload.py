"""
Upload API — POST /upload
"""

from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db

router = APIRouter()


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    """Upload a document (audio, PDF, text) for analysis."""
    # Will be implemented in Phase 3 (services)
    return {
        "status": "uploaded",
        "filename": file.filename,
        "content_type": file.content_type,
    }
