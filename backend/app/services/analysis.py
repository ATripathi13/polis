"""
Polis Analysis Service — Orchestration of the analysis pipeline
"""

import uuid
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.document import Document
from app.models.meeting import Meeting
from app.services.file_processor import file_processor
from app.services.memory import memory_manager
from app.agents.orchestrator import orchestrator


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
        
    async def run_analysis_pipeline(
        self,
        db: AsyncSession,
        meeting_id: uuid.UUID
    ) -> Dict[str, Any]:
        """
        Run the full AI orchestration pipeline on a meeting's transcript
        and persist results to the database.
        """
        # 1. Fetch the meeting
        stmt = select(Meeting).where(Meeting.id == meeting_id)
        result = await db.execute(stmt)
        meeting = result.scalar_one_or_none()
        
        if not meeting or not meeting.raw_transcript:
            return {"error": "Meeting not found or has no transcript"}

        # 2. Run Orchestrator
        state = await orchestrator.run(meeting.raw_transcript)
        
        # 3. Update Meeting with cleaned transcript and mapping
        if state["transcript"]:
            meeting.processed_transcript = state["transcript"].cleaned_transcript
            meeting.speaker_mapping = {s.speaker_id: s.full_name for s in state["transcript"].speakers}
        
        # 4. Persist Tasks
        if state["tasks"]:
            from app.models.task import Task
            for t in state["tasks"].tasks:
                db_task = Task(
                    description=t.description,
                    owner=t.owner,
                    deadline=t.deadline,
                    priority=t.priority,
                    confidence_score=t.confidence,
                    meeting_id=meeting.id
                )
                db.add(db_task)

        # 5. Persist Contradictions
        if state["contradictions"]:
            from app.models.contradiction import Contradiction
            for c in state["contradictions"].contradictions:
                db_c = Contradiction(
                    category=c.category,
                    explanation=c.explanation,
                    severity=c.severity,
                    confidence_score=c.confidence,
                    meeting_id=meeting.id
                )
                db.add(db_c)

        # 6. Persist Risks
        if state["risks"]:
            from app.models.risk import Risk
            for r in state["risks"].risks:
                db_r = Risk(
                    category=r.category,
                    description=r.description,
                    severity=r.severity,
                    likelihood=r.likelihood,
                    impact=r.impact,
                    confidence_score=r.confidence,
                    meeting_id=meeting.id
                )
                db.add(db_r)

        # 7. Persist Final Summary
        if state["final_summary"]:
            from app.models.summary import Summary
            db_s = Summary(
                content=state["final_summary"].executive_summary,
                type="EXECUTIVE",
                confidence_score=1.0, # Validator score could go here
                meeting_id=meeting.id
            )
            db.add(db_s)

        await db.commit()
        return {"status": "completed", "meeting_id": str(meeting_id)}


analysis_service = AnalysisService()
