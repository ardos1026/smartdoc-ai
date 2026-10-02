from google import genai

from app.config import GEMINI_API_KEY


client = genai.Client(api_key=GEMINI_API_KEY)


def ask_gemini(prompt):
    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input=prompt,
    )

    return interaction.output_text