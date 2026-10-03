from google import genai

from app.config import GEMINI_API_KEY


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


def ask_gemini(prompt):
    client = get_client()

    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input=prompt,
    )

    return interaction.output_text


def create_embedding(text):
    client = get_client()

    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
    )

    return response.embeddings[0].values