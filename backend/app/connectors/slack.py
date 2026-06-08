"""
Polis Slack Connector — Handles translation between Slack and Polis.
"""

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from app.config import settings


class SlackConnector:
    """
    Interface for Slack communication.
    Supports DMs, channel messages, and thread replies.
    """

    def __init__(self):
        self.client = WebClient(token=settings.slack_bot_token)

    async def send_message(self, channel_id: str, text: str, thread_ts: str = None):
        """Send a message to a Slack channel or thread."""
        try:
            self.client.chat_postMessage(
                channel=channel_id,
                text=text,
                thread_ts=thread_ts
            )
        except SlackApiError as e:
            print(f"Slack Error: {e}")

    async def extract_thread_history(self, channel_id: str, thread_ts: str) -> str:
        """Fetch all messages from a Slack thread and combine into a transcript."""
        try:
            response = self.client.conversations_replies(
                channel=channel_id,
                ts=thread_ts
            )
            messages = response.get("messages", [])
            transcript = "\n".join([f"{msg.get('user', 'User')}: {msg.get('text')}" for msg in messages])
            return transcript
        except SlackApiError as e:
            print(f"Slack Error: {e}")
            return ""


slack_connector = SlackConnector()
