"""
WhatsApp Webhook — POST /whatsapp/webhook
"""

from fastapi import APIRouter, Request

router = APIRouter()


@router.post("/whatsapp/webhook")
async def whatsapp_webhook(request: Request):
    """Handle incoming WhatsApp messages via Twilio."""
    form_data = await request.form()
    
    from_number = form_data.get("From", "").replace("whatsapp:", "")
    incoming_msg = form_data.get("Body", "")
    
    # Check for media (voice notes, PDFs)
    num_media = int(form_data.get("NumMedia", 0))
    if num_media > 0:
        # In a real app, we'd download the media and process via file_processor
        pass

    # Use the centralized brain (Chat / Analysis)
    from app.connectors.whatsapp import whatsapp_connector
    await whatsapp_connector.send_message(from_number, "Polis has received your message via WhatsApp and is analyzing it.")
    
    return {"status": "ok"}
