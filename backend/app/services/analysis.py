"""
Polis Analysis Service — Orchestration of the analysis pipeline
"""

import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.document import Document
from app.models.meeting import Meeting
from app.services.file_processor import file_processor
from app.services.memory import memory_manager


class AnalysisService:
    """
    Service to orchestrate document processing and handoff to AI agents.
    """

    async def ingest_document(
        self, 
        db: AsyncSession, 
        filename: str, 
        content: bytes, 
        file_type: str,
        organization_id: uuid.UUID
    ) -> Document:
        """
        Save file, create DB record, and trigger text extraction.
        """
        # Save physical file
        file_path = await file_processor.save_file(filename, content)
        
        # Create DB record
        doc = Document(
            filename=filename,
            file_path=file_path,
            file_type=file_type,
            file_size=len(content),
            organization_id=organization_id
        )
        db.add(doc)
        await db.flush()
        
        # Extract text
        extracted_text = await file_processor.process_file(file_path, file_type)
        
        # If it's a meeting-like document, create a meeting record
        # (This logic will be more sophisticated in Phase 5)
        meeting = Meeting(
            title=f"Meeting: {filename}",
            raw_transcript=extracted_text,
            source=file_type,
            organization_id=organization_id
        )
        db.add(meeting)
        await db.flush()
        
        doc.meeting_id = meeting.id
        
        # Store in semantic memory
        await memory_manager.store_document(
            doc_id=str(doc.id),
            text=extracted_text,
            metadata={
                "document_id": str(doc.id),
                "meeting_id": str(meeting.id),
                "organization_id": str(organization_id),
                "filename": filename
            }
        )
        
        await db.commit()
        return doc


analysis_service = AnalysisService()
