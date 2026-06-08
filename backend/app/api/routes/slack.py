"""
Slack Webhook — POST /slack/webhook
"""

from fastapi import APIRouter, Request

router = APIRouter()


@router.post("/slack/webhook")
async def slack_webhook(request: Request):
    """Handle incoming Slack events (messages, commands, interactions)."""
    body = await request.json()

    # Slack URL verification challenge
    if body.get("type") == "url_verification":
        return {"challenge": body.get("challenge")}

    # Will be implemented with Slack connector in Phase 7
    return {"status": "ok"}
