"""
Polis WhatsApp Connector — Handles communication via Twilio WhatsApp API.
"""

from twilio.rest import Client
from app.config import settings


class WhatsAppConnector:
    """
    Interface for WhatsApp communication via Twilio.
    Supports text and media messages.
    """

    def __init__(self):
        self.client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
        self.from_number = settings.twilio_whatsapp_number

    async def send_message(self, to_number: str, text: str, media_urls: list[str] = None):
        """Send a WhatsApp message via Twilio."""
        try:
            self.client.messages.create(
                body=text,
                from_=self.from_number,
                to=f"whatsapp:{to_number}",
                media_url=media_urls
            )
        except Exception as e:
            print(f"WhatsApp Error: {str(e)}")


whatsapp_connector = WhatsAppConnector()
