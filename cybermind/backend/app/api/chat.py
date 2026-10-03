from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from app.core.llm import get_llm_provider
from app.database.session import get_db
from app.rag.engine import search_rag

router = APIRouter(prefix="/chat", tags=["AI Analyst"])

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    summary: str
    domain: str
    findings: List[Dict[str, Any]]
    evidence: List[str]
    confidence: float
    relevant_techniques: List[str]
    risk: str
    recommendations: List[str]
    sources: List[Dict[str, Any]]
    limitations: Optional[str] = None

@router.post("", response_model=ChatResponse)
async def chat(
    req: ChatRequest,
    db: Session = Depends(get_db)
):
    # 1. Real RAG Retrieval over database-indexed DocumentChunks
    retrieved_chunks = search_rag(query=req.message, db=db, top_k=3)
    
    # 2. Extract grounded citations directly from verified database records
    real_citations = [
        {
            "title": c["title"],
            "url": c["url"],
            "source": c["source"],
            "domain": c["domain"]
        }
        for c in retrieved_chunks
    ]

    # 3. Call LLM provider with retrieved RAG context
    provider = get_llm_provider()
    result = await provider.generate(
        prompt=req.message,
        context=[{"source": c["source"], "text": c["text"]} for c in retrieved_chunks]
    )

    # 4. Enforce that citations come from real database-indexed records if available
    if real_citations:
        result["sources"] = real_citations
        # Align domain if identified by authoritative knowledge
        if retrieved_chunks[0].get("domain") and result.get("domain") == "AI Analysis":
            result["domain"] = retrieved_chunks[0]["domain"]

    return ChatResponse(**result)
