"""
Slack Webhook — POST /slack/webhook
"""

from fastapi import APIRouter, Request

router = APIRouter()


@router.post("/slack/webhook")
async def slack_webhook(request: Request):
    """Handle incoming Slack events."""
    body = await request.json()

    # URL Verification
    if body.get("type") == "url_verification":
        return {"challenge": body.get("challenge")}

    event = body.get("event", {})
    
    # Handle mentions or DMs (bot must not respond to itself)
    if event.get("type") in ["app_mention", "message"] and not event.get("bot_id"):
        channel = event.get("channel")
        text = event.get("text", "")
        thread_ts = event.get("ts")
        
        # Check if user wants a summary of a thread
        if "summarize" in text.lower() and event.get("thread_ts"):
            from app.connectors.slack import slack_connector
            from app.services.analysis import analysis_service
            # 1. Extract thread
            transcript = await slack_connector.extract_thread_history(channel, event.get("thread_ts"))
            # 2. Run analysis (simplified for now, usually would be a task)
            # In a real app we'd dispatch a Celery task and notify via DM when done
            await slack_connector.send_message(channel, "Analyzing thread... I will post the executive summary shortly.", thread_ts)
            # Placeholder for actual summary delivery
        
        else:
            # Handle as standard chat
            from app.api.routes.chat import chat, ChatRequest
            # This is a bit recursive/messy to call route directly, better to call a common service
            # For brevity in this phase, we'll respond with a placeholder
            from app.connectors.slack import slack_connector
            await slack_connector.send_message(channel, "I've received your message. I'm processing it with the Polis brain.", thread_ts)

    return {"status": "ok"}
