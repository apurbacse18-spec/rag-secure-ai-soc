from typing import List, Dict


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks


def chunk_documents(documents: List[Dict]) -> List[Dict]:
    chunked_docs = []

    for doc in documents:
        chunks = chunk_text(doc["content"])
        for i, chunk in enumerate(chunks):
            chunked_docs.append(
                {
                    "source": doc["source"],
                    "chunk_id": i,
                    "content": chunk,
                }
            )

    return chunked_docs


if __name__ == "__main__":
    sample_docs = [
        {"source": "sample.md", "content": "This is a sample document for testing chunking." * 20}
    ]
    chunks = chunk_documents(sample_docs)
    print(f"Created {len(chunks)} chunks")
    for chunk in chunks[:3]:
        print(chunk["source"], chunk["chunk_id"])