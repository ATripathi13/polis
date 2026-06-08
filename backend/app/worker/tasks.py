"""
Polis — Celery Tasks
"""

from app.worker.celery_app import celery_app


@celery_app.task(bind=True, name="polis.analyze_document")
def analyze_document(self, document_id: str, organization_id: str):
    """
    Run the full analysis pipeline on a document.
    """
    import asyncio
    import uuid
    from app.database import async_session_factory
    from app.services.analysis import analysis_service
    from app.models.document import Document
    from sqlalchemy import select

    async def run_async():
        async with async_session_factory() as db:
            # 1. Get the document to find linked meeting
            stmt = select(Document).where(Document.id == uuid.UUID(document_id))
            res = await db.execute(stmt)
            doc = res.scalar_one_or_none()
            
            if not doc or not doc.meeting_id:
                return {"error": "Document or linked meeting not found"}
                
            # 2. Run the orchestration pipeline
            return await analysis_service.run_analysis_pipeline(db, doc.meeting_id)

    # Celery tasks are synchronous wrappers for our async logic
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(run_async())
