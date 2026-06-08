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
    # Will be implemented with Qdrant in Phase 3
    return {
        "query": q,
        "results": [],
        "total": 0,
    }
