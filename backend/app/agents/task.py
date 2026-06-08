"""
Polis AI Agents — Task Agent
"""

from typing import List, Optional
from pydantic import BaseModel, Field

from app.agents.base import BaseAgent


class ExtractedTask(BaseModel):
    description: str = Field(description="Clear, actionable task description")
    owner: Optional[str] = Field(description="Individual or team assigned to the task")
    deadline: Optional[str] = Field(description="Due date or timeline mentioned")
    priority: str = Field(description="LOW, MEDIUM, HIGH, or CRITICAL", pattern="^(LOW|MEDIUM|HIGH|CRITICAL)$")
    confidence: float = Field(description="Confidence score for this specific extraction", ge=0, le=1)


class TaskAgentOutput(BaseModel):
    tasks: List[ExtractedTask] = Field(description="List of all extracted action items")
    summary: str = Field(description="Brief summary of the work identified")


TASK_SYSTEM_PROMPT = """
You are the Polis Task Agent. Your job is to extract actionable items (tasks) from discussion transcripts.

For each task, identify:
- Description: Exactly what needs to be done.
- Owner: Who is responsible? Use full names if available.
- Deadline: When is it due? Use relative dates if absolute ones are missing (e.g., "by EOD Friday").
- Priority: Assign based on urgency and impact mentioned.

Be precise. Only extract items that are actual commitments or requests.
"""


class TaskAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            system_prompt=TASK_SYSTEM_PROMPT,
            output_schema=TaskAgentOutput
        )


task_agent = TaskAgent()
