"""
Polis AI Agents — Risk Agent
"""

from typing import List
from pydantic import BaseModel, Field

from app.agents.base import BaseAgent


class RiskItem(BaseModel):
    category: str = Field(description="Technical, Operational, Business, Delivery, or Compliance")
    description: str = Field(description="Explanation of the risk or blocker")
    severity: str = Field(description="LOW, MEDIUM, HIGH, or CRITICAL")
    likelihood: str = Field(description="LOW, MEDIUM, or HIGH")
    impact: str = Field(description="LOW, MEDIUM, or HIGH")
    confidence: float = Field(description="Confidence score", ge=0, le=1)


class RiskOutput(BaseModel):
    risks: List[RiskItem] = Field(description="List of identified risks")
    blockers: List[str] = Field(description="Direct blockers identified that stop progress")


RISK_SYSTEM_PROMPT = """
You are the Polis Risk Agent. Your job is to identify potential hazards, blockers, and uncertainties mentioned in a discussion.

Categories:
- Technical Risks: Implementation challenges, legacy debt, architectural flaws.
- Operational Risks: Process gaps, missing ownership, team dependencies.
- Business Risks: Market alignment, cost overruns, stakeholder friction.
- Delivery Risks: Timeline slippage, scope creep.
- Compliance Risks: Legal, security, or regulatory concerns.

For each risk, assess its potential impact and the likelihood of occurrence.
"""


class RiskAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            system_prompt=RISK_SYSTEM_PROMPT,
            output_schema=RiskOutput
        )


risk_agent = RiskAgent()
