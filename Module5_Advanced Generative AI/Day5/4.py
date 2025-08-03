# app.py

import streamlit as st
import PyPDF2
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import pipeline

# -------------------- SETUP --------------------

def load_pdf_chunks(files, chunk_size=300):
    all_chunks = []
    for file in files:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        text = text.replace("\n", " ")
        chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
        all_chunks.extend(chunks)
    return all_chunks

@st.cache_resource(show_spinner=False)
def setup_rag(chunks):
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    chunk_embeddings = embedder.encode(chunks, convert_to_tensor=False)
    dimension = len(chunk_embeddings[0])
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(chunk_embeddings))
    qa_pipeline = pipeline("text2text-generation", model="google/flan-t5-base", max_length=256)
    return embedder, index, qa_pipeline

def retrieve_top_k(query, chunks, embedder, index, k=3):
    query_embedding = embedder.encode([query])
    distances, indices = index.search(np.array(query_embedding), k)
    return [chunks[i] for i in indices[0]]

def answer_query(query, chunks, embedder, index, qa_pipeline):
    top_chunks = retrieve_top_k(query, chunks, embedder, index)
    context = "\n".join(top_chunks)
    prompt = f"Context: {context}\n\nQuestion: {query}\n\nAnswer:"
    response = qa_pipeline(prompt)[0]["generated_text"]
    return response.strip()

def summarize_docs(chunks, qa_pipeline, num_chunks=5):
    context = "\n".join(chunks[:num_chunks])
    prompt = f"Context: {context}\n\nSummarize this document in 10 lines."
    response = qa_pipeline(prompt)[0]["generated_text"]
    return response.strip()

# -------------------- STREAMLIT UI --------------------

st.set_page_config(page_title="📄 Multi-PDF RAG Chat", layout="centered")
st.title("🤖 HR FAQ Assistant (Naive RAG)")
st.markdown("Upload one or more HR policy PDFs. Ask questions or generate a summary!")

uploaded_files = st.file_uploader("📎 Upload one or more PDF files", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    with st.spinner("📚 Processing PDFs..."):
        chunks = load_pdf_chunks(uploaded_files)
        embedder, index, qa_pipeline = setup_rag(chunks)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # 🔹 Ask a question
    with st.form(key="chat_form"):
        user_query = st.text_input("💬 Ask your HR-related question:", placeholder="e.g., What is the leave policy?")
        submit_button = st.form_submit_button("Ask")

    if submit_button and user_query:
        response = answer_query(user_query, chunks, embedder, index, qa_pipeline)
        st.session_state.chat_history.append(("You", user_query))
        st.session_state.chat_history.append(("Assistant", response))

    # 🔹 Summarize all documents
    if st.button("🧠 Summarize All Documents"):
        summary = summarize_docs(chunks, qa_pipeline, num_chunks=8)
        st.session_state.chat_history.append(("You", "Summarize all documents"))
        st.session_state.chat_history.append(("Assistant", summary))

    # 🔹 Display chat history
    for speaker, msg in st.session_state.chat_history:
        if speaker == "You":
            st.markdown(f"🧑 **{speaker}**: {msg}")
        else:
            st.markdown(f"🤖 **{speaker}**: {msg}")
else:
    st.info("⬆️ Please upload at least one PDF to begin.")
