"""
Polis File Processor — PDF, Text, Audio, and Word Document Parsing
"""

import os
import aiofiles
from PyPDF2 import PdfReader
from docx import Document as DocxDocument
from openai import AsyncOpenAI
from pydub import AudioSegment

from app.config import settings


class FileProcessor:
    """
    Handles extraction of text and metadata from various file formats.
    """

    def __init__(self):
        self.openai_client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.uploads_dir = "uploads"
        os.makedirs(self.uploads_dir, exist_ok=True)

    async def save_file(self, filename: str, content: bytes) -> str:
        """Save raw bytes to the uploads directory and return the path."""
        file_path = os.path.join(self.uploads_dir, filename)
        async with aiofiles.open(file_path, "wb") as f:
            await f.write(content)
        return file_path

    async def process_file(self, file_path: str, file_type: str) -> str:
        """
        Extract text from the file based on its type.
        """
        if file_type == "text/plain":
            return await self._process_text(file_path)
        elif file_type == "application/pdf":
            return await self._process_pdf(file_path)
        elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return await self._process_docx(file_path)
        elif file_type.startswith("audio/"):
            return await self._process_audio(file_path)
        else:
            # Fallback for unrecognized types
            try:
                return await self._process_text(file_path)
            except Exception:
                raise ValueError(f"Unsupported file type: {file_type}")

    async def _process_text(self, file_path: str) -> str:
        async with aiofiles.open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return await f.read()

    async def _process_pdf(self, file_path: str) -> str:
        text = ""
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text

    async def _process_docx(self, file_path: str) -> str:
        doc = DocxDocument(file_path)
        return "\n".join([para.text for para in doc.paragraphs])

    async def _process_audio(self, file_path: str) -> str:
        """
        Transcribe audio using OpenAI Whisper.
        """
        # Note: Large files might need chunking. Whisper API limit is 25MB.
        # For simplicity in this implementation, we assume files are < 25MB.
        with open(file_path, "rb") as audio_file:
            transcript = await self.openai_client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file,
                response_format="text"
            )
        return transcript


file_processor = FileProcessor()
