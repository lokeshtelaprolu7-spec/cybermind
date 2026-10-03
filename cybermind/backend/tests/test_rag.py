import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database.session import SessionLocal
from app.models.entities import Document, DocumentChunk
from app.rag.engine import search_rag

client = TestClient(app)

def test_database_indexed_documents():
    with SessionLocal() as db:
        docs = db.query(Document).all()
        assert len(docs) >= 4
        titles = [d.title for d in docs]
        assert any("OWASP Top 10" in t for t in titles)
        assert any("MITRE ATT&CK" in t for t in titles)

def test_rag_retrieval_engine():
    with SessionLocal() as db:
        # Search for SQL injection
        results = search_rag("SQL injection vulnerabilities in web applications", db=db, top_k=2)
        assert len(results) > 0
        assert results[0]["source"] == "OWASP"
        assert "A03: Injection" in results[0]["title"]
        assert results[0]["url"] is not None

        # Search for credential stuffing
        cs_results = search_rag("Credential stuffing brute force against authentication portal", db=db, top_k=2)
        assert len(cs_results) > 0
        assert cs_results[0]["source"] == "MITRE ATT&CK"
        assert "T1110.004" in cs_results[0]["title"]

def test_chat_citations_come_from_real_database():
    res = client.post("/api/chat", json={
        "message": "Explain SQL injection remediation for our web tier"
    })
    assert res.status_code == 200
    data = res.json()
    assert len(data["sources"]) > 0
    # Verify the citation matches the real database document
    source_titles = [s["title"] for s in data["sources"]]
    assert any("OWASP" in t for t in source_titles)
