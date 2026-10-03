import streamlit as st

from app.chunker import split_text
from app.document_loader import load_document
from app.gemini_client import create_embedding
from app.vector_store import VectorStore
from app.rag import ask_question


st.set_page_config(
    page_title="SmartDoc AI",
    page_icon="📄",
)


# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


st.title("📄 SmartDoc AI")

st.write(
    "Cloud-Native AI Document Question Answering Platform"
)

st.divider()


# Upload document
st.header("Upload a Document")

uploaded_file = st.file_uploader(
    "Choose a PDF or TXT file",
    type=["pdf", "txt"],
)


if uploaded_file:

    st.success(f"Uploaded: {uploaded_file.name}")

    # Detect a new document
    if st.session_state.get("file_name") != uploaded_file.name:

        # Clear previous chat
        st.session_state.chat_history = []

        # Save uploaded document
        with open(uploaded_file.name, "wb") as file:
            file.write(uploaded_file.getbuffer())

        # Load document
        content = load_document(uploaded_file.name)

        # Split document into chunks
        chunks = split_text(content)

        # Create vector store
        store = VectorStore()

        # Create embeddings
        with st.spinner("Creating document embeddings..."):

            for chunk in chunks:
                embedding = create_embedding(chunk)
                store.add(chunk, embedding)

        # Save processed document
        st.session_state.vector_store = store
        st.session_state.file_name = uploaded_file.name

        st.success(
            f"Document processed into {len(chunks)} chunks."
        )

    else:

        st.success("Document already processed.")

    st.divider()

    # Chat input
    question = st.chat_input(
        "Ask a question about your document..."
    )

    if question:

        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):

            with st.spinner("Generating answer..."):

                answer = ask_question(
                    question,
                    st.session_state.vector_store,
                    top_k=2,
                )

            st.write(answer)

        # Save conversation
        st.session_state.chat_history.append({
            "question": question,
            "answer": answer,
        })


# Display chat history
if st.session_state.chat_history:

    st.divider()

    st.header("💬 Chat History")

    for chat in st.session_state.chat_history:

        with st.chat_message("user"):
            st.write(chat["question"])

        with st.chat_message("assistant"):
            st.write(chat["answer"])