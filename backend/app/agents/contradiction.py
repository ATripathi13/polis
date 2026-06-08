"""
Polis AI Agents — Contradiction Agent
"""

from typing import List
from pydantic import BaseModel, Field

from app.agents.base import BaseAgent


class ContradictionItem(BaseModel):
    category: str = Field(description="Timeline, Resource, Technical, Business, or Dependency")
    explanation: str = Field(description="Detailed explanation of why this is a contradiction")
    severity: str = Field(description="LOW, MEDIUM, HIGH, or CRITICAL", pattern="^(LOW|MEDIUM|HIGH|CRITICAL)$")
    confidence: float = Field(description="Confidence score for this detection", ge=0, le=1)


class ContradictionOutput(BaseModel):
    contradictions: List[ContradictionItem] = Field(description="List of detected contradictions")
    summary: str = Field(description="Overall synthesis of internal conflicts")


CONTRADICTION_SYSTEM_PROMPT = """
You are the Polis Contradiction Agent. Your job is to identify logical, technical, or operational conflicts within a discussion.

Focus on:
1. Timeline Contradictions: (e.g., "Ship tomorrow" vs "Testing starts next week")
2. Resource Contradictions: (e.g., "Assign to Alice" vs "Alice is on vacation")
3. Technical Contradictions: (e.g., "Real-time" vs "Daily batch processing")
4. Business Contradictions: (e.g., "Enterprise security level" vs "No budget allocated")
5. Dependency Contradictions: (e.g., Task scheduled before its prerequisite can finish)

Each detection must be explained clearly with evidence from the text.
"""


class ContradictionAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            system_prompt=CONTRADICTION_SYSTEM_PROMPT,
            output_schema=ContradictionOutput
        )


contradiction_agent = ContradictionAgent()
