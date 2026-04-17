from fastapi import FastAPI
from rag_app.schemas import QueryRequest, QueryResponse
from rag_app.logger import log_query
from rag_app.retriever import retrieve_chunks
import uuid

app = FastAPI(title="RAG Secure AI SOC")


@app.get("/")
def root():
    return {"status": "ok", "message": "RAG Secure AI SOC is running"}


@app.post("/query", response_model=QueryResponse)
def query_rag(request: QueryRequest):
    request_id = str(uuid.uuid4())
    matches = retrieve_chunks(request.query)
    source_count = len(matches)

    source_names = [match["source"] for match in matches]
    if matches:
        answer = f"Found {source_count} relevant document chunks from: {', '.join(source_names)}"
    else:
        answer = "No relevant document chunks were found."

    log_query(
        request_id=request_id,
        query=request.query,
        source_count=source_count,
        sources=source_names,
        status="success",
    )

    return QueryResponse(
        answer=answer,
        source_count=source_count,
        request_id=request_id,
    )