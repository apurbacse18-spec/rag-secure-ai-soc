import json
import re
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

from rag_app.vector_store import build_vector_store

model = SentenceTransformer("all-MiniLM-L6-v2")

BASE_DIR = Path(__file__).resolve().parent.parent
BANKING_TOPICS_PATH = BASE_DIR / "data" / "banking_topics.json"


def normalize_text(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text


def tokenize(text: str):
    return normalize_text(text).split()


def load_banking_topics():
    if not BANKING_TOPICS_PATH.exists():
        return []

    with open(BANKING_TOPICS_PATH, "r", encoding="utf-8") as f:
        topics = json.load(f)

    if not isinstance(topics, list):
        return []

    return topics


def score_topic(query: str, topic: dict) -> int:
    normalized_query = normalize_text(query)
    query_tokens = set(tokenize(query))
    score = 0

    title = normalize_text(topic.get("title", ""))
    if title and title in normalized_query:
        score += 5

    for keyword in topic.get("keywords", []):
        normalized_keyword = normalize_text(keyword)
        keyword_tokens = set(tokenize(keyword))

        if normalized_keyword in normalized_query:
            score += 4
        elif keyword_tokens and keyword_tokens.issubset(query_tokens):
            score += 3

    for phrase in topic.get("user_phrases", []):
        normalized_phrase = normalize_text(phrase)
        phrase_tokens = set(tokenize(phrase))

        if normalized_phrase in normalized_query:
            score += 6
        else:
            overlap = len(query_tokens.intersection(phrase_tokens))
            if overlap >= 2:
                score += overlap

    return score


def retrieve_banking_topic(query: str, min_score: int = 2):
    topics = load_banking_topics()
    if not topics:
        return None

    best_topic = None
    best_score = -1

    for topic in topics:
        score = score_topic(query, topic)
        if score > best_score:
            best_score = score
            best_topic = topic

    if best_score >= min_score:
        return best_topic

    return None


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
    topic = retrieve_banking_topic("my card is missing")
    print("Banking topic match:")
    print(topic)

    matches = retrieve_chunks("How do I investigate repeated SSH failures?")
    print(f"\nFound {len(matches)} chunks")
    for match in matches:
        print(match["source"], match["chunk_id"])