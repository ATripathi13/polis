"""
Polis AI Agents — Feasibility Agent
"""

from typing import List, Optional
from pydantic import BaseModel, Field

from app.agents.base import BaseAgent


class FeasibilityAssessment(BaseModel):
    item: str = Field(description="The specific plan, goal, or timeline being assessed")
    finding: str = Field(description="REALISTIC, UNREALISTIC, IMPOSSIBLE, or UNDER-SCOPED", pattern="^(REALISTIC|UNREALISTIC|IMPOSSIBLE|UNDER-SCOPED|MISSING-INFO)$")
    explanation: str = Field(description="Why this assessment was made")
    confidence: float = Field(description="Confidence score", ge=0, le=1)


class FeasibilityOutput(BaseModel):
    assessments: List[FeasibilityAssessment] = Field(description="List of feasibility findings")
    validation_status: str = Field(description="Overall health of the plan proposed")


FEASIBILITY_SYSTEM_PROMPT = """
You are the Polis Feasibility Agent. Your job is to analyze the realism of commitments and timelines discussed.

Assess whether items are:
- REALISTIC: Achievable with reasonable effort.
- UNREALISTIC: High risk of failure, overly optimistic.
- IMPOSSIBLE: Contradicts known constraints or physical reality.
- UNDER-SCOPED: The goal is clear but the required resources/steps are missing.
- MISSING-INFO: Not enough context to determine feasibility.

Look for missing dependencies, impossible timelines (e.g., development in 2 hours for a complex feature), and resource gaps.
"""


class FeasibilityAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            system_prompt=FEASIBILITY_SYSTEM_PROMPT,
            output_schema=FeasibilityOutput
        )


feasibility_agent = FeasibilityAgent()
