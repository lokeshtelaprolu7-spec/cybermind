# CyberMIND — RAG Cybersecurity Brain

CyberMIND implements a Retrieval-Augmented Generation (RAG) architecture grounded strictly in authoritative cybersecurity standards.

## 1. Authoritative Knowledge Repositories
- **OWASP:** Top 10 Web (2021) and Top 10 API Security (2023).
- **MITRE ATT&CK:** Enterprise Matrix v14 techniques, sub-techniques, and mitigations.
- **NIST:** Cybersecurity Framework (CSF 2.0) categories (Identify, Protect, Detect, Respond, Recover).
- **CISA:** Known Exploited Vulnerabilities (KEV) catalog and emergency directives.
- **NVD / CVE:** Common Vulnerability and Exposures database feeds.

## 2. Ingestion & Retrieval Pipeline
```
Document Source (OWASP/MITRE/NIST)
       ↓
Document Loader & Sanitizer (Prompt Injection Filter)
       ↓
Semantic Chunker (200 words / preserves header context)
       ↓
Metadata Tagging (Domain, Version, Source, URL)
       ↓
Vector Embeddings & Keyword Index (pgvector / SQLite)
       ↓
Hybrid Retrieval & Reranking
       ↓
LLM Synthesis with Mandatory Citations
```

## 3. Strict Citation Rule
The AI Analyst is configured to display explicit source citations for all factual assertions. Hallucinated sources are systematically caught and flagged by the Security Reviewer Agent.
