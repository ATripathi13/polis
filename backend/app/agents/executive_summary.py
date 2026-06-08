"""
Polis AI Agents — Executive Summary Agent
"""

from pydantic import BaseModel, Field

from app.agents.base import BaseAgent


class ExecutiveSummaryOutput(BaseModel):
    executive_summary: str = Field(description="High-level narrative for leadership")
    key_takeaways: str = Field(description="Bulleted list of critical points")
    health_score: str = Field(description="Traffic light color: GREEN, AMBER, RED")
    primary_recommendation: str = Field(description="Single most important next step")


EXECUTIVE_SUMMARY_SYSTEM_PROMPT = """
You are the Polis Executive Summary Agent. Your job is to synthesize all validated findings (Tasks, Decisions, Risks, Contradictions, Feasibility) into a concise, professional executive report.

Structure:
- Narrative: A 2-3 paragraph overview of the discussion/meeting.
- Key Takeaways: High-level results that leadership needs to know.
- Health Score: Based on risks and contradictions (GREEN = Good, AMBER = Caution, RED = Critical Issues).
- Primary Recommendation: What is the most important action to take immediately?

The report must be professional, direct, and actionable.
"""


class ExecutiveSummaryAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            system_prompt=EXECUTIVE_SUMMARY_SYSTEM_PROMPT,
            output_schema=ExecutiveSummaryOutput
        )


executive_summary_agent = ExecutiveSummaryAgent()
