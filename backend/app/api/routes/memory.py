"""
Memory API — GET /memory/search
"""

from fastapi import APIRouter, Query

router = APIRouter()


@router.get("/memory/search")
async def search_memory(
    q: str = Query(..., description="Search query for organizational memory"),
    limit: int = Query(10, ge=1, le=50),
):
    """Search organizational memory using semantic retrieval."""
    from app.services.memory import memory_manager
    
    # Retrieve context with metadata
    context_vector = await memory_manager.embeddings.aembed_query(q)
    from app.services.memory import memory_service
    results = await memory_service.search_memory(vector=context_vector, limit=limit)
    
    formatted_results = []
    for res in results:
        formatted_results.append({
            "id": res.id,
            "content": res.payload.get("content"),
            "metadata": {
                "filename": res.payload.get("filename"),
                "document_id": res.payload.get("document_id"),
                "meeting_id": res.payload.get("meeting_id"),
                "organization_id": res.payload.get("organization_id"),
            },
            "score": res.score
        })
        
    return {
        "query": q,
        "results": formatted_results,
        "total": len(formatted_results),
    }
