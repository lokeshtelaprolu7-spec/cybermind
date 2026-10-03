# CyberMIND — Testing & Quality Assurance Suite

CyberMIND features a multi-layered automated testing suite validating security, functionality, and performance across all components.

## 1. Running Automated Pytest Suites
```bash
cd cybermind/backend
.\.venv\Scripts\pytest tests/ -v
```

### Test Coverage
- **`tests/test_phase1.py`:**
  - Health checks (`/health`, `/api/health`)
  - Security headers (`X-Request-ID`, `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`)
  - BCrypt password hashing & verification
  - Authentication flow (Register, Duplicate rejection, Login, JWT verification, `/me`, Logout)
  - LLM MockProvider structured response schema
- **`tests/test_full_platform.py`:**
  - Seeded asset verification (WEB-01, API-01, DB-01, AWS-S3-01)
  - Security findings and active incidents
  - Digital Twin graph topology and scenario simulation delta recalculation
  - Attack surface scoring and crown-jewel attack path traversal
  - Threat intelligence reputation lookups
  - Cyber memory summary and similar incident matching
  - Blockchain evidence SHA-256 calculation, anchoring, and positive integrity verification
  - Executive security report generation

## 2. Running Research & Evaluation Benchmark
```bash
cd cybermind
python scripts/evaluate.py
```
This script computes numerical metrics across:
- RAG retrieval precision & citation grounding rate
- Multi-agent structured JSON schema compliance
- Digital Twin shortest-path pathfinding latency
- Deterministic risk engine consistency
- Blockchain tamper detection accuracy (100% detection of byte alterations)
