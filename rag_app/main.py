import uuid

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from rag_app.schemas import QueryRequest, QueryResponse
from rag_app.logger import log_query
from rag_app.retriever import retrieve_chunks, retrieve_banking_topic
from rag_app.answer_generator import build_answer, build_topic_answer
from rag_app.security import classify_threat
from rag_app.ml_security import is_anomalous
from rag_app.memory import get_session_memory, update_session_memory, clear_session_memory

app = FastAPI(title="RAG Secure AI SOC")
templates = Jinja2Templates(directory="templates")

FOLLOW_UP_QUERIES = {
    "what should i do next",
    "what next",
    "what do i do now",
    "what now",
    "what should i do",
    "now what",
    "then what",
    "and now",
    "next step",
    "next steps",
    "what happened",
    "what can i do",
    "what do i do",
    "help me",
}

CLEAR_MEMORY_QUERIES = {
    "clear memory",
    "reset conversation",
    "forget previous",
    "start over",
    "new conversation",
}


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        name="index.html",
        request=request
    )


@app.post("/query", response_model=QueryResponse)
def query_rag(request: QueryRequest):
    request_id = str(uuid.uuid4())
    session_id = request.session_id
    query_text = request.query.strip()
    normalized_query = query_text.lower()

    if normalized_query in CLEAR_MEMORY_QUERIES:
        clear_session_memory(session_id)

        log_query(
            request_id=request_id,
            query=request.query,
            source_count=0,
            sources=[],
            status="memory_cleared",
        )

        return QueryResponse(
            answer="🧠 Conversation memory cleared. We can start fresh.",
            source_count=0,
            request_id=request_id,
        )

    threat = classify_threat(request.query)
    anomaly_detected = is_anomalous(request.query)

    if threat:
        block_reason = threat

        log_query(
            request_id=request_id,
            query=request.query,
            source_count=0,
            sources=[],
            status=f"blocked_{block_reason}",
        )

        return QueryResponse(
            answer=f"⚠️ Query blocked due to {block_reason}.",
            source_count=0,
            request_id=request_id,
        )

    memory = get_session_memory(session_id)
    topic = retrieve_banking_topic(request.query)

    if topic:
        answer = build_topic_answer(topic)
        source_count = 1
        source_names = [topic.get("title", "banking_topic")]
        status = "success_topic"
        update_session_memory(session_id, request.query, topic)

    elif normalized_query in FOLLOW_UP_QUERIES and memory.get("last_topic_data"):
        previous_topic = memory["last_topic_data"]

        answer = (
            f"🧠 Continuing from your previous issue: {previous_topic.get('title', 'Previous topic')}\n\n"
            f"{build_topic_answer(previous_topic)}"
        )
        source_count = 1
        source_names = [previous_topic.get("title", "previous_topic")]
        status = "success_memory_followup"

    else:
        matches = retrieve_chunks(request.query)
        source_count = len(matches)
        source_names = [match["source"] for match in matches]
        answer = build_answer(request.query, matches)
        status = "success_rag"
        update_session_memory(session_id, request.query, None)

    if anomaly_detected:
        answer = "⚠️ **Unusual query pattern detected.**\n\n" + answer
        status = f"{status}_anomaly_flagged"

    log_query(
        request_id=request_id,
        query=request.query,
        source_count=source_count,
        sources=source_names,
        status=status,
    )

    return QueryResponse(
        answer=answer,
        source_count=source_count,
        request_id=request_id,
    )