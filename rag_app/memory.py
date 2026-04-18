from typing import Dict, Optional

SESSION_MEMORY: Dict[str, Dict] = {}


def get_session_memory(session_id: str) -> Dict:
    if session_id not in SESSION_MEMORY:
        SESSION_MEMORY[session_id] = {
            "last_query": None,
            "last_topic": None,
            "last_topic_title": None,
            "last_topic_data": None,
        }
    return SESSION_MEMORY[session_id]


def update_session_memory(session_id: str, query: str, topic: Optional[Dict] = None):
    memory = get_session_memory(session_id)
    memory["last_query"] = query

    if topic:
        memory["last_topic"] = topic.get("intent_name")
        memory["last_topic_title"] = topic.get("title")
        memory["last_topic_data"] = topic


def clear_session_memory(session_id: str):
    SESSION_MEMORY[session_id] = {
        "last_query": None,
        "last_topic": None,
        "last_topic_title": None,
        "last_topic_data": None,
    }