"""
Chat API — POST /chat
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.config import settings

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
    import uuid
    from app.models.conversation import Conversation, Message
    from app.services.memory import memory_manager
    from langchain_openai import ChatOpenAI
    from sqlalchemy import select
    
    # 1. Get or create conversation
    conv_id = request.conversation_id
    if not conv_id or conv_id == "new":
        conversation = Conversation(
            user_id=uuid.uuid4(), # Placeholder user_id
            channel="web",
            title=request.message[:50] + "..."
        )
        db.add(conversation)
        await db.flush()
        conv_id = str(conversation.id)
    else:
        stmt = select(Conversation).where(Conversation.id == uuid.UUID(conv_id))
        res = await db.execute(stmt)
        conversation = res.scalar_one_or_none()
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

    # 2. Save user message
    user_msg = Message(
        content=request.message,
        role="user",
        conversation_id=conversation.id
    )
    db.add(user_msg)
    
    # 3. Retrieve relevant context from memory
    context = await memory_manager.retrieve_context(request.message, limit=3)
    
    # 4. Generate response with LLM
    llm = ChatOpenAI(model=settings.openai_model, api_key=settings.openai_api_key)
    
    system_prompt = f"""
    You are Polis, an AI Operational Intelligence Assistant.
    Use the following organizational memory context to answer the user's question.
    If the context doesn't contain the answer, use your internal knowledge but mention if it's not in the memory.
    
    Context:
    {context}
    """
    
    # Fetch recent history
    history_stmt = select(Message).where(Message.conversation_id == conversation.id).order_by(Message.created_at.desc()).limit(5)
    history_res = await db.execute(history_stmt)
    history = history_res.scalars().all()[::-1]
    
    messages = [("system", system_prompt)]
    for m in history:
        messages.append((m.role, m.content))
    messages.append(("user", request.message))
    
    ai_response = await llm.ainvoke(messages)
    
    # 5. Save assistant response
    assistant_msg = Message(
        content=ai_response.content,
        role="assistant",
        conversation_id=conversation.id
    )
    db.add(assistant_msg)
    
    await db.commit()
    
    return ChatResponse(
        response=ai_response.content,
        conversation_id=conv_id,
    )
