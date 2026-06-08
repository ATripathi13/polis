"""
Meetings API — GET /meetings/{id}
Retrieval of analysis results.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
import uuid
from typing import List, Any

from app.database import get_db
from app.models.meeting import Meeting
from app.models.task import Task
from app.models.risk import Risk
from app.models.contradiction import Contradiction
from app.models.decision import Decision
from app.models.summary import Summary

router = APIRouter()


@router.get("/meetings", tags=["Meetings"])
async def list_meetings(
    db: AsyncSession = Depends(get_db),
    limit: int = 20,
    offset: int = 0
):
    """List all meetings with basic info."""
    stmt = select(Meeting).order_by(Meeting.created_at.desc()).limit(limit).offset(offset)
    result = await db.execute(stmt)
    meetings = result.scalars().all()
    return meetings


@router.get("/meetings/{meeting_id}", tags=["Meetings"])
async def get_meeting_details(
    meeting_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Get full analysis results for a specific meeting."""
    uid = uuid.UUID(meeting_id)
    
    # Fetch meeting with all related insights
    stmt = (
        select(Meeting)
        .where(Meeting.id == uid)
        .options(
            selectinload(Meeting.tasks),
            selectinload(Meeting.risks),
            selectinload(Meeting.contradictions),
            selectinload(Meeting.decisions),
            selectinload(Meeting.summaries)
        )
    )
    result = await db.execute(stmt)
    meeting = result.scalar_one_or_none()
    
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
        
    return {
        "id": meeting.id,
        "title": meeting.title,
        "date": meeting.date,
        "processed_transcript": meeting.processed_transcript,
        "speaker_mapping": meeting.speaker_mapping,
        "tasks": meeting.tasks,
        "risks": meeting.risks,
        "contradictions": meeting.contradictions,
        "decisions": meeting.decisions,
        "summaries": meeting.summaries
    }
