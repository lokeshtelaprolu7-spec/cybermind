from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from app.database.session import get_db
from app.models.entities import Document, DocumentChunk

router = APIRouter(prefix="/knowledge", tags=["RAG Knowledge Base"])

class DocumentIngest(BaseModel):
    title: str
    source: str  # OWASP, MITRE, NIST, CISA, CVE
    url: Optional[str] = None
    domain: str  # Web Security, API Security, SOC, Cloud Security, etc.
    version: Optional[str] = "2026.1"
    content: str

@router.get("")
def list_documents(db: Session = Depends(get_db)):
    docs = db.query(Document).all()
    if not docs:
        # Provide baseline authoritative documents
        return [
            {
                "id": "kb-owasp-01",
                "title": "OWASP Top 10:2021 A03: Injection & Parameterized Remediation",
                "source": "OWASP",
                "domain": "Web Security",
                "url": "https://owasp.org/Top10/A03_2021-Injection/",
                "version": "2021",
                "chunks_count": 8,
                "ingestion_date": "2026-09-29"
            },
            {
                "id": "kb-owasp-api-01",
                "title": "OWASP API Security Top 10:2023 - Broken Object Level Authorization",
                "source": "OWASP",
                "domain": "API Security",
                "url": "https://owasp.org/API-Security/",
                "version": "2023",
                "chunks_count": 12,
                "ingestion_date": "2026-09-29"
            },
            {
                "id": "kb-mitre-01",
                "title": "MITRE ATT&CK T1190: Exploit Public-Facing Application",
                "source": "MITRE ATT&CK",
                "domain": "Threat Intelligence",
                "url": "https://attack.mitre.org/techniques/T1190/",
                "version": "v14.1",
                "chunks_count": 15,
                "ingestion_date": "2026-09-29"
            },
            {
                "id": "kb-nist-01",
                "title": "NIST CSF 2.0: Detect and Respond Category Specifications",
                "source": "NIST",
                "domain": "SOC",
                "url": "https://www.nist.gov/cyberframework",
                "version": "2.0",
                "chunks_count": 24,
                "ingestion_date": "2026-09-29"
            }
        ]
    return [
        {
            "id": d.id,
            "title": d.title,
            "source": d.source,
            "domain": d.domain,
            "url": d.url,
            "version": d.version,
            "chunks_count": len(d.chunks),
            "ingestion_date": d.created_at.strftime("%Y-%m-%d") if d.created_at else "2026-09-29"
        }
        for d in docs
    ]

@router.post("/ingest", status_code=status.HTTP_201_CREATED)
def ingest_document(doc_in: DocumentIngest, db: Session = Depends(get_db)):
    doc = Document(
        title=doc_in.title,
        source=doc_in.source,
        url=doc_in.url,
        domain=doc_in.domain,
        version=doc_in.version,
        content=doc_in.content
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    # Simple semantic chunker (200 words per chunk)
    words = doc_in.content.split()
    chunk_size = 200
    for i in range(0, len(words), chunk_size):
        chunk_text = " ".join(words[i:i + chunk_size])
        chunk = DocumentChunk(
            document_id=doc.id,
            chunk_index=i // chunk_size,
            chunk_text=chunk_text,
            metadata_json={"source": doc.source, "domain": doc.domain, "title": doc.title}
        )
        db.add(chunk)
    db.commit()

    return {
        "id": doc.id,
        "title": doc.title,
        "chunks_created": (len(words) + chunk_size - 1) // chunk_size
    }
