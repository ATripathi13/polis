"""
Polis AI Agents — Transcript Agent
"""

from typing import List, Dict, Optional
from pydantic import BaseModel, Field

from app.agents.base import BaseAgent


class SpeakerMap(BaseModel):
    speaker_id: str = Field(description="ID of the speaker in the raw text")
    full_name: str = Field(description="Inferred or known full name of the speaker")
    role: Optional[str] = Field(description="Role or title of the speaker if identifiable")


class Segment(BaseModel):
    title: str = Field(description="Brief title of the segment/topic")
    start_timestamp: Optional[str] = Field(description="Start time or line number")
    end_timestamp: Optional[str] = Field(description="End time or line number")
    content: str = Field(description="Summarized or cleaned content of this segment")


class TranscriptOutput(BaseModel):
    cleaned_transcript: str = Field(description="The full transcript with speaker mapping applied and noise removed")
    speakers: List[SpeakerMap] = Field(description="List of detected speakers and their identified names")
    segments: List[Segment] = Field(description="Discussion segmented by topic")
    confidence: float = Field(description="Confidence score between 0.0 and 1.0", ge=0, le=1)


TRANSCRIPT_SYSTEM_PROMPT = """
You are the Polis Transcript Agent. Your job is to clean up raw meeting transcripts, map anonymous speaker tags to real names based on context (introductions, sign-offs, names mentioned), and segment the discussion into logical topics.

Responsibilities:
1. Cleanup: Remove filler words, stuttering, and non-essential chatter.
2. Speaker Mapping: Identify who is speaking (e.g., Change "Speaker 1" to "John Doe").
3. Segmentation: Identify distinct topics discussed and group the transcript around them.

The output must be structured, professional, and suitable for further operational analysis.
"""


class TranscriptAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            system_prompt=TRANSCRIPT_SYSTEM_PROMPT,
            output_schema=TranscriptOutput
        )


transcript_agent = TranscriptAgent()
