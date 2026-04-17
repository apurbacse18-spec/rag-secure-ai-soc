from pathlib import Path


def load_markdown_documents(data_dir: str = "data") -> list[dict]:
    data_path = Path(data_dir)
    documents = []

    for file_path in data_path.glob("*.md"):
        content = file_path.read_text(encoding="utf-8")
        documents.append(
            {
                "source": file_path.name,
                "content": content,
            }
        )

    return documents


if __name__ == "__main__":
    docs = load_markdown_documents()
    print(f"Loaded {len(docs)} documents")
    for doc in docs:
        print(f"- {doc['source']}")