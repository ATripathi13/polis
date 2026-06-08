"""
Polis — Celery Tasks
"""

from app.worker.celery_app import celery_app


@celery_app.task(bind=True, name="polis.analyze_document")
def analyze_document(self, document_id: str, organization_id: str):
    """
    Run the full analysis pipeline on a document.
    This task is dispatched asynchronously from the /analyze endpoint.
    Will be fully implemented in Phase 5 (Orchestration).
    """
    self.update_state(state="PROCESSING", meta={"document_id": document_id})

    # Placeholder — orchestrator integration in Phase 5
    return {
        "status": "completed",
        "document_id": document_id,
        "message": "Analysis pipeline will be connected in Phase 5",
    }
