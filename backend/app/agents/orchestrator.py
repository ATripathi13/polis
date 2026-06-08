"""
Polis AI Orchestrator — LangGraph Pipeline
Coordinates specialized agents to produce operational intelligence.
"""

import asyncio
from typing import TypedDict, List, Dict, Any, Optional
from langgraph.graph import StateGraph, END

from app.agents.transcript import transcript_agent, TranscriptOutput
from app.agents.task import task_agent, TaskAgentOutput
from app.agents.contradiction import contradiction_agent, ContradictionOutput
from app.agents.risk import risk_agent, RiskOutput
from app.agents.feasibility import feasibility_agent, FeasibilityOutput
from app.agents.validator import validator_agent, ValidatorOutput
from app.agents.executive_summary import executive_summary_agent, ExecutiveSummaryOutput


class AgentState(TypedDict):
    """The shared state for the Polis orchestration pipeline."""
    input_text: str
    transcript: Optional[TranscriptOutput]
    tasks: Optional[TaskAgentOutput]
    contradictions: Optional[ContradictionOutput]
    risks: Optional[RiskOutput]
    feasibility: Optional[FeasibilityOutput]
    validation: Optional[ValidatorOutput]
    final_summary: Optional[ExecutiveSummaryOutput]
    errors: List[str]


# ---- Nodes ----

async def transcript_node(state: AgentState) -> Dict[str, Any]:
    """Cleans and segments the raw input text."""
    try:
        result = await transcript_agent.run(state["input_text"])
        return {"transcript": result}
    except Exception as e:
        return {"errors": state.get("errors", []) + [f"TranscriptAgent: {str(e)}"]}


async def task_node(state: AgentState) -> Dict[str, Any]:
    """Extracts tasks from the cleaned transcript."""
    text = state["transcript"].cleaned_transcript if state["transcript"] else state["input_text"]
    result = await task_agent.run(text)
    return {"tasks": result}


async def contradiction_node(state: AgentState) -> Dict[str, Any]:
    """Detects conflicts in the transcript."""
    text = state["transcript"].cleaned_transcript if state["transcript"] else state["input_text"]
    result = await contradiction_agent.run(text)
    return {"contradictions": result}


async def risk_node(state: AgentState) -> Dict[str, Any]:
    """Assesses risks and blockers."""
    text = state["transcript"].cleaned_transcript if state["transcript"] else state["input_text"]
    result = await risk_agent.run(text)
    return {"risks": result}


async def feasibility_node(state: AgentState) -> Dict[str, Any]:
    """Checks the realism of the plan."""
    text = state["transcript"].cleaned_transcript if state["transcript"] else state["input_text"]
    result = await feasibility_agent.run(text)
    return {"feasibility": result}


async def validator_node(state: AgentState) -> Dict[str, Any]:
    """Cross-validates all agent outputs."""
    # Combine all findings for validation
    findings = {
        "tasks": state["tasks"].model_dump() if state["tasks"] else {},
        "contradictions": state["contradictions"].model_dump() if state["contradictions"] else {},
        "risks": state["risks"].model_dump() if state["risks"] else {},
        "feasibility": state["feasibility"].model_dump() if state["feasibility"] else {},
    }
    
    import json
    input_text = f"Source Transcript: {state['transcript'].cleaned_transcript if state['transcript'] else state['input_text']}\n\nAgent Findings: {json.dumps(findings)}"
    
    result = await validator_agent.run(input_text)
    return {"validation": result}


async def summary_node(state: AgentState) -> Dict[str, Any]:
    """Generates the final executive summary."""
    # Use validated data if available, otherwise raw findings
    data_to_summarize = state["validation"].normalized_data if state["validation"] else {
        "tasks": state["tasks"],
        "contradictions": state["contradictions"],
        "risks": state["risks"],
        "feasibility": state["feasibility"],
    }
    
    import json
    input_text = json.dumps(data_to_summarize, default=lambda x: x.model_dump() if hasattr(x, 'model_dump') else str(x))
    
    result = await executive_summary_agent.run(input_text)
    return {"final_summary": result}


# ---- Connect the Graph ----

workflow = StateGraph(AgentState)

# Add Nodes
workflow.add_node("transcript", transcript_node)
workflow.add_node("tasks", task_node)
workflow.add_node("contradictions", contradiction_node)
workflow.add_node("risks", risk_node)
workflow.add_node("feasibility", feasibility_node)
workflow.add_node("validator", validator_node)
workflow.add_node("summary", summary_node)

# Set Entry Point
workflow.set_entry_point("transcript")

# Parallel Execution Paths
workflow.add_edge("transcript", "tasks")
workflow.add_edge("transcript", "contradictions")
workflow.add_edge("transcript", "risks")
workflow.add_edge("transcript", "feasibility")

# Converge to Validator
workflow.add_edge("tasks", "validator")
workflow.add_edge("contradictions", "validator")
workflow.add_edge("risks", "validator")
workflow.add_edge("feasibility", "validator")

# Final Synthesis
workflow.add_edge("validator", "summary")
workflow.add_edge("summary", END)

# Compile
polis_app = workflow.compile()


class PolisOrchestrator:
    """
    Public interface to run the Polis intelligence pipeline.
    """
    
    async def run(self, input_text: str) -> AgentState:
        initial_state: AgentState = {
            "input_text": input_text,
            "transcript": None,
            "tasks": None,
            "contradictions": None,
            "risks": None,
            "feasibility": None,
            "validation": None,
            "final_summary": None,
            "errors": []
        }
        
        return await polis_app.ainvoke(initial_state)

orchestrator = PolisOrchestrator()
