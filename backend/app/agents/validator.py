"""
Polis AI Agents — Validator Agent
"""

from typing import Any, Dict
from pydantic import BaseModel, Field

from app.agents.base import BaseAgent


class ValidatorOutput(BaseModel):
    is_valid: bool = Field(description="Whether the overall data is consistent and free of hallucinations")
    corrections: str = Field(description="Summary of any changes or removals made")
    normalized_data: Dict[str, Any] = Field(description="The cleaned and validated state")
    overall_confidence: float = Field(description="Calculated overall confidence score", ge=0, le=1)


VALIDATOR_SYSTEM_PROMPT = """
You are the Polis Validator Agent. Your job is to cross-examine outputs from multiple specialized agents (Task, Risk, Contradiction, Feasibility) and ensure:
1. No Hallucinations: All items must be derived from the source text.
2. Consistency: No internal contradictions between agent findings.
3. Normalization: Ensure all confidence scores are realistic and aligned.

If you find a hallucination, remove it. If you find a conflict, flag it or resolve it based on the source text.
The output data must be the authoritative 'source of truth' for the executive report.
"""


class ValidatorAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            system_prompt=VALIDATOR_SYSTEM_PROMPT,
            output_schema=ValidatorOutput
        )


validator_agent = ValidatorAgent()
