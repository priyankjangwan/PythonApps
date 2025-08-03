# app.py

import streamlit as st
# What is streamlit?
# Streamlit is an open-source app framework for Machine Learning and Data Science projects.
# It allows you to create web applications for your data projects with minimal effort.
# Streamlit is designed to make it easy to build and share data applications, allowing you to
# focus on your data and models rather than the complexities of web development.

import PyPDF2
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import pipeline

# -------------------- SETUP --------------------

# cache_data - This decorator is used to cache the results of a function so that it does not need to be recomputed every time it is called.
# show_spinner=False - This argument is used to disable the spinner that is shown while the function is being executed.
@st.cache_data(show_spinner=True)
def load_pdf_chunks(pdf_path, chunk_size=300):
    reader = PyPDF2.PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    text = text.replace("\n", " ")
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

@st.cache_resource(show_spinner=False)
def setup_rag(pdf_path):
    chunks = load_pdf_chunks(pdf_path)
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    chunk_embeddings = embedder.encode(chunks, convert_to_tensor=False)
    dimension = len(chunk_embeddings[0])
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(chunk_embeddings))
    qa_pipeline = pipeline("text2text-generation", model="google/flan-t5-base", max_length=256)
    return chunks, embedder, index, qa_pipeline

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

st.set_page_config(page_title="HR FAQ Assistant - Naive RAG", layout="centered")
st.title("🤖 HR FAQ Assistant (Naive RAG)")

pdf_path = "company_policy.pdf"

if not os.path.exists(pdf_path):
    st.error("'company_policy.pdf' not found. Please upload it to the app directory.")
    st.stop()

with st.spinner("Setting up RAG system..."):
    chunks, embedder, index, qa_pipeline = setup_rag(pdf_path)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat Interface
with st.form(key="chat_form"):
    user_query = st.text_input("Ask your HR-related question:", placeholder="e.g., What is the leave policy?")
    submit_button = st.form_submit_button("Ask")

if submit_button and user_query:
    response = answer_query(user_query, chunks, embedder, index, qa_pipeline)
    st.session_state.chat_history.append(("You", user_query))
    st.session_state.chat_history.append(("Assistant", response))

# Show chat history
for speaker, text in st.session_state.chat_history:
    if speaker == "You":
        st.markdown(f"🧑 **{speaker}**: {text}")
    else:
        st.markdown(f"🤖 **{speaker}**: {text}")


# To run this app, save it and run the following command in your terminal:
# streamlit run <file_name>.py
# Make sure you have the required libraries installed:
# pip install streamlit PyPDF2 faiss-cpu sentence-transformers transformers