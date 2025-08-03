# app.py

import streamlit as st
import PyPDF2
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import tempfile

# -------------------- SETUP --------------------

def load_pdf_chunks(file, chunk_size=300):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    text = text.replace("\n", " ")
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

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

# -------------------- STREAMLIT UI --------------------

st.set_page_config(page_title="📄 Naive RAG Chat", layout="centered")
st.title("🤖 HR FAQ Assistant (Naive RAG)")
st.markdown("Upload your HR policy PDF and ask any question!")

uploaded_file = st.file_uploader("📎 Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    with st.spinner("📚 Reading and processing your PDF..."):
        chunks = load_pdf_chunks(uploaded_file)
        embedder, index, qa_pipeline = setup_rag(chunks)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    with st.form(key="chat_form"):
        user_query = st.text_input("💬 Ask your HR-related question:", placeholder="e.g., What is the leave policy?")
        submit_button = st.form_submit_button("Ask")

    if submit_button and user_query:
        response = answer_query(user_query, chunks, embedder, index, qa_pipeline)
        st.session_state.chat_history.append(("You", user_query))
        st.session_state.chat_history.append(("Assistant", response))

    # Display chat
    for speaker, msg in st.session_state.chat_history:
        if speaker == "You":
            st.markdown(f"🧑 **{speaker}**: {msg}")
        else:
            st.markdown(f"🤖 **{speaker}**: {msg}")

else:
    st.info("⬆️ Please upload a PDF to begin.")
