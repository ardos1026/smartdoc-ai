from app.rag import ask_question
from app.vector_store import VectorStore
from app.vector_store import cosine_similarity
from app.chunker import split_text
from app.utils import get_app_info
from app.document_loader import load_document


def test_get_app_info():
    info = get_app_info()

    assert info["name"] == "SmartDoc AI"
    assert info["version"] == "0.1.0"
    assert info["status"] == "running"


def test_load_text_document():
    content = load_document("sample.txt")

    assert "SmartDoc AI" in content
    assert "cloud-native" in content

def test_split_text():
    text = " ".join(["SmartDoc"] * 200)

    chunks = split_text(text, chunk_size=500, overlap=50)

    assert len(chunks) > 1
    assert all(len(chunk) <= 500 for chunk in chunks)


def test_cosine_similarity():
    vector_a = [1, 0, 0]
    vector_b = [1, 0, 0]

    similarity = cosine_similarity(vector_a, vector_b)

    assert similarity == 1.0


def test_vector_store_search():
    store = VectorStore()

    store.add("Document A", [1, 0, 0])
    store.add("Document B", [0, 1, 0])

    results = store.search([1, 0, 0], top_k=1)

    assert len(results) == 1
    assert results[0]["text"] == "Document A"
    assert results[0]["score"] == 1.0




def test_rag_rejects_unknown_question(monkeypatch):
    store = VectorStore()

    store.add(
        "SmartDoc AI uses RAG to answer questions from documents.",
        [1, 0, 0],
    )

    # Mock the embedding API
    def fake_embedding(text):
        return [1, 0, 0]

    # Mock the Gemini generation API
    def fake_gemini(prompt):
        return "I could not find the answer in the provided document."

    monkeypatch.setattr(
        "app.rag.create_embedding",
        fake_embedding,
    )

    monkeypatch.setattr(
        "app.rag.ask_gemini",
        fake_gemini,
    )

    answer = ask_question(
        "Who is the CEO of SmartDoc AI?",
        store,
        top_k=1,
    )

    assert "could not find" in answer.lower()