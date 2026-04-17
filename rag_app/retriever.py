from sentence_transformers import SentenceTransformer
import numpy as np
from rag_app.vector_store import build_vector_store

model = SentenceTransformer("all-MiniLM-L6-v2")


def retrieve_chunks(query: str, top_k: int = 3):
    index, chunks = build_vector_store()
    query_vector = model.encode([query], convert_to_numpy=True).astype(np.float32)
    distances, indices = index.search(query_vector, top_k)

    results = []
    for idx in indices[0]:
        if idx != -1:
            results.append(chunks[idx])

    return results


if __name__ == "__main__":
    matches = retrieve_chunks("How do I investigate repeated SSH failures?")
    print(f"Found {len(matches)} chunks")
    for match in matches:
        print(match["source"], match["chunk_id"])