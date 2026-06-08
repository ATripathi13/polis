"""
Polis Memory — Qdrant Vector Store Service
"""

from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.exceptions import UnexpectedResponse

from app.config import settings


class MemoryService:
    """
    Service for semantic memory storage and retrieval using Qdrant.
    """

    def __init__(self):
        self.client = QdrantClient(
            host=settings.qdrant_host,
            port=settings.qdrant_port,
        )
        self.collection_name = settings.qdrant_collection
        self.vector_size = 1536  # Default for OpenAI text-embedding-3-small

    async def ensure_collection(self):
        """Ensure the collection exists in Qdrant."""
        try:
            self.client.get_collection(self.collection_name)
        except (UnexpectedResponse, Exception):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=self.vector_size,
                    distance=models.Distance.COSINE,
                ),
            )

    async def upsert_memory(self, id: str, vector: list[float], payload: dict):
        """Insert or update a memory point."""
        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                models.PointStruct(
                    id=id,
                    vector=vector,
                    payload=payload,
                )
            ],
        )

    async def search_memory(self, vector: list[float], limit: int = 10, filters: dict = None):
        """Search for similar memories."""
        query_filter = None
        if filters:
            must_filters = []
            for key, value in filters.items():
                must_filters.append(
                    models.FieldCondition(
                        key=key,
                        match=models.MatchValue(value=value),
                    )
                )
            query_filter = models.Filter(must=must_filters)

        return self.client.search(
            collection_name=self.collection_name,
            query_vector=vector,
            limit=limit,
            query_filter=query_filter,
        )


memory_service = MemoryService()
