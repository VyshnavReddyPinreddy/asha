from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from rag.vectorstore import RAGVectorStore
from rag.retriever import RAGRetriever
from core.security import get_current_user

router = APIRouter(prefix="/rag", tags=["RAG"])

class KnowledgeQueryRequest(BaseModel):
    query: str

class KnowledgeQueryResponse(BaseModel):
    answer: str
    sources: list[str]

# Singleton — loaded once when server starts
_store = None
_retriever = None

def get_retriever():
    global _store, _retriever
    if _retriever is None:
        _store = RAGVectorStore()
        _retriever = RAGRetriever(_store)
    return _retriever

@router.post("/query", response_model=KnowledgeQueryResponse)
async def knowledge_query(
    request: KnowledgeQueryRequest,
    current_user: dict = Depends(get_current_user)
):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    retriever = get_retriever()
    result = retriever.answer(request.query)
    return KnowledgeQueryResponse(
        answer=result["answer"],
        sources=result["sources"]
    )