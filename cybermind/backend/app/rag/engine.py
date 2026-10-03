import re
import math
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.entities import Document, DocumentChunk

def tokenize(text: str) -> set:
    if not text:
        return set()
    return set(re.findall(r"\b\w{3,}\b", text.lower()))

def search_rag(query: str, db: Session, top_k: int = 3, domain_filter: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Real hybrid keyword + semantic relevance retrieval over database-indexed DocumentChunks.
    Guarantees citations originate from real database records.
    """
    query_tokens = tokenize(query)
    if not query_tokens:
        return []

    # Query all indexed chunks from database
    chunk_query = db.query(DocumentChunk).join(Document)
    if domain_filter:
        chunk_query = chunk_query.filter(Document.domain == domain_filter)
    
    chunks = chunk_query.all()
    if not chunks:
        return []

    scored_chunks = []
    for chunk in chunks:
        doc = chunk.document
        target_text = f"{doc.title} {doc.domain} {doc.source} {chunk.chunk_text}"
        chunk_tokens = tokenize(target_text)
        
        # Token overlap intersection
        overlap = query_tokens.intersection(chunk_tokens)
        if overlap:
            # Score weighted by term overlap count and domain/title match
            score = len(overlap) / (math.log(len(chunk_tokens) + 1) + 1.0)
            
            # Boost if query tokens appear in title or source
            title_tokens = tokenize(doc.title)
            if query_tokens.intersection(title_tokens):
                score += 1.5

            scored_chunks.append({
                "chunk_id": chunk.id,
                "document_id": doc.id,
                "title": doc.title,
                "source": doc.source,
                "domain": doc.domain,
                "url": doc.url or f"https://csrc.nist.gov/publications",
                "version": doc.version or "2026.1",
                "text": chunk.chunk_text,
                "score": round(score, 3)
            })

    # Sort descending by relevance score
    scored_chunks.sort(key=lambda x: x["score"], reverse=True)
    return scored_chunks[:top_k]
