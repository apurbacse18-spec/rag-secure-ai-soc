from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from rag_app.load_documents import load_markdown_documents
from rag_app.chunk_documents import chunk_documents

model = SentenceTransformer("all-MiniLM-L6-v2")


def build_vector_store():
    documents = load_markdown_documents()
    chunks = chunk_documents(documents)

    texts = [chunk["content"] for chunk in chunks]
    embeddings = model.encode(texts, convert_to_numpy=True)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings, dtype=np.float32))

    return index, chunks


if __name__ == "__main__":
    index, chunks = build_vector_store()
    print(f"Built vector store with {len(chunks)} chunks")