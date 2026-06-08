"""
Chat API — POST /chat
"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    conversation_id: str | None = None


class ChatResponse(BaseModel):
    response: str
    conversation_id: str


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db),
):
    """Chat with Polis — conversational interface with memory context."""
    # Will be implemented with agents in Phase 4-5
    return ChatResponse(
        response="Polis is initializing. Full chat will be available after agent setup.",
        conversation_id=request.conversation_id or "new",
    )
