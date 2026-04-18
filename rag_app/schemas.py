from pydantic import BaseModel


class QueryRequest(BaseModel):
    query: str
    session_id: str


class QueryResponse(BaseModel):
    answer: str
    source_count: int
    request_id: str