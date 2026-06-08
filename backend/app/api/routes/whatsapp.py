"""
WhatsApp Webhook — POST /whatsapp/webhook
"""

from fastapi import APIRouter, Request

router = APIRouter()


@router.post("/whatsapp/webhook")
async def whatsapp_webhook(request: Request):
    """Handle incoming WhatsApp messages via Twilio."""
    form_data = await request.form()

    # Will be implemented with WhatsApp connector in Phase 7
    return {"status": "ok"}
