# pip install streamlit sentence-transformers faiss-cpu pandas
# streamlit run app.py

# pip install streamlit sentence-transformers faiss-cpu pandas
# streamlit run app.py


# app.py

import streamlit as st
import pandas as pd
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer, CrossEncoder

# ------------------ SETUP ------------------

st.set_page_config(page_title="🧠 Research Paper Selector (RAG + Rerank)", layout="wide")
st.title("📚 Level 3 RAG: Research Paper Selector (Retrieve + Rerank)")

uploaded_file = st.file_uploader("📎 Upload papers.csv (with 'title' and 'abstract')", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df['content'] = df['title'] + ". " + df['abstract']
    documents = df['content'].tolist()

    # Vector encode
    st.write("🔄 Embedding papers...")
    bi_encoder = SentenceTransformer("all-MiniLM-L6-v2")
    doc_embeddings = bi_encoder.encode(documents, show_progress_bar=True)

    dim = doc_embeddings[0].shape[0]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(doc_embeddings))

    # Cross encoder for reranking
    cross_encoder = CrossEncoder("cross-encoder/ms-marco-TinyBERT-L-6")

    # Query input
    query = st.text_input("💬 Ask a research question", placeholder="e.g., What are the latest techniques in few-shot learning?")

    if st.button("🔎 Retrieve & Rerank") and query:
        st.subheader("🏆 Top Relevant Papers")

        # Step 1: Vector search
        query_embedding = bi_encoder.encode([query])
        distances, indices = index.search(np.array(query_embedding), 30)
        initial_results = [(documents[i], df.iloc[i]['title'], df.iloc[i]['abstract']) for i in indices[0]]

        # Step 2: Cross-encoder reranking
        pairs = [[query, doc] for doc, _, _ in initial_results]
        scores = cross_encoder.predict(pairs)
        reranked = sorted(zip(scores, initial_results), key=lambda x: x[0], reverse=True)

        # Step 3: Display & selection with unique keys
        selected = []
        for i, (score, (doc, title, abstract)) in enumerate(reranked[:10]):
            with st.expander(f"📄 {title}"):
                st.markdown(f"**Score:** {score:.4f}")
                st.write(abstract)
                if st.checkbox(f"✅ Select: {title}", key=f"{title}_{i}"):
                    selected.append({"title": title, "abstract": abstract, "score": score})

        # Step 4: Export to CSV
        if selected:
            result_df = pd.DataFrame(selected)
            st.markdown("### 📥 Export Selected Papers")
            st.download_button(
                label="📤 Download CSV",
                data=result_df.to_csv(index=False),
                file_name="selected_papers.csv",
                mime="text/csv"
            )
else:
    st.info("⬆️ Please upload a `papers.csv` to begin.")
