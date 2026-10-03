from app.chunker import split_text
from app.document_loader import load_document
from app.gemini_client import create_embedding
from app.vector_store import VectorStore
from app.rag import ask_question


def main():
    content = load_document("sample.txt")
    chunks = split_text(content)

    store = VectorStore()

    print(f"Document loaded: {len(content)} characters")
    print(f"Created {len(chunks)} chunks")

    for chunk in chunks:
        embedding = create_embedding(chunk)
        store.add(chunk, embedding)

    print("All chunks embedded and stored.")

    question = "Who is the CEO of SmartDoc AI?"
    print(f"\nQuestion: {question}")
    print("\nGenerating answer...")

    answer = ask_question(
        question,
        store,
        top_k=2,
    )

    print("\nAnswer:")
    print(answer)


if __name__ == "__main__":
    main()