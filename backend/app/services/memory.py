"""
Polis Memory System — Semantic Retrieval and Historical Reasoning
"""

import uuid
from typing import List, Dict, Any
from langchain_openai import OpenAIEmbeddings

from app.config import settings
from app.services.memory import memory_service


class MemoryManager:
    """
    High-level manager for the organizational memory system.
    Orchestrates embedding generation and Qdrant interactions.
    """

    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            model=settings.openai_embedding_model,
            api_key=settings.openai_api_key,
        )

    async def store_document(self, doc_id: str, text: str, metadata: Dict[str, Any]):
        """
        Chunk a document, embed chunks, and store in vector database.
        """
        # Ensure collection exists
        await memory_service.ensure_collection()
        
        # Split text into chunks (simple overlap strategy for now)
        chunks = self._chunk_text(text)
        
        for i, chunk in enumerate(chunks):
            vector = await self.embeddings.aembed_query(chunk)
            chunk_metadata = metadata.copy()
            chunk_metadata["content"] = chunk
            chunk_metadata["chunk_index"] = i
            
            # Create a unique ID for the chunk
            chunk_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{doc_id}_{i}"))
            
            await memory_service.upsert_memory(
                id=chunk_id,
                vector=vector,
                payload=chunk_metadata
            )

    async def retrieve_context(self, query: str, filters: Dict[str, Any] = None, limit: int = 5) -> str:
        """
        Search for relevant memory chunks and format as context string.
        """
        query_vector = await self.embeddings.aembed_query(query)
        results = await memory_service.search_memory(
            vector=query_vector,
            limit=limit,
            filters=filters
        )
        
        context_parts = []
        for res in results:
            content = res.payload.get("content", "")
            source = res.payload.get("filename", "unknown source")
            context_parts.append(f"Source [{source}]:\n{content}")
            
        return "\n\n---\n\n".join(context_parts)

    def _chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
        """Split text into overlapping chunks."""
        chunks = []
        if not text:
            return chunks
            
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start = end - overlap
            if start >= len(text) - overlap:
                break
        return chunks


memory_manager = MemoryManager()
