from google import genai

from app.config import GEMINI_API_KEY


client = genai.Client(api_key=GEMINI_API_KEY)


def ask_gemini(prompt):
    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input=prompt,
    )
    return interaction.output_text

def create_embedding(text):
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
    )

    return response.embeddings[0].values
