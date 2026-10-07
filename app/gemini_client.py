import logging
import time

from google import genai

from app.config import GEMINI_API_KEY


logger = logging.getLogger(__name__)

_client = None


def get_client():
    global _client

    if _client is None:
        if not GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY is not configured."
            )

        _client = genai.Client(
            api_key=GEMINI_API_KEY
        )

    return _client


def ask_gemini(prompt, max_retries=3):
    client = get_client()

    for attempt in range(max_retries):
        try:
            interaction = client.interactions.create(
                model="gemini-3.8-flash",
                input=prompt,
            )

            return interaction.output_text

        except Exception as error:

            error_message = str(error).lower()

            is_temporary_error = (
                "503" in error_message
                or "service_unavailable" in error_message
                or "temporarily unavailable" in error_message
                or "high demand" in error_message
            )

            if is_temporary_error:
                logger.warning(
                "Gemini temporary error detected: %s | retry=%d/%d",
                error_message,
                attempt + 1,
                max_retries,
                )


            if not is_temporary_error:
                raise

            if attempt == max_retries - 1:
                return (
                    "⚠️ Gemini is temporarily unavailable. "
                    "Please try again in a moment."
                )

            wait_time = 2 ** attempt

            time.sleep(wait_time)


def create_embedding(text):
    client = get_client()

    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
    )

    return response.embeddings[0].values