from app.gemini_client import ask_gemini, create_embedding


def ask_question(question, vector_store, top_k=3):
    # Convert the user's question into an embedding
    query_embedding = create_embedding(question)

    # Retrieve the most relevant document chunks
    results = vector_store.search(query_embedding, top_k=top_k)

    # Build context from retrieved chunks
    context = "\n\n".join(
        result["text"]
        for result in results
    )

    # Create the prompt for Gemini
    prompt = f"""
You are SmartDoc AI, a document question-answering assistant.

Answer the user's question using only the provided document context.

If the answer cannot be found in the context, say:
"I could not find the answer in the provided document."

Document Context:
{context}

User Question:
{question}

Answer:
"""

    # Generate the final answer
    answer = ask_gemini(prompt)

    return answer