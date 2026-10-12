# 🛡️ CyberMIND

> **CyberMIND is an Agentic AI-powered Cybersecurity Digital Twin that models organizational infrastructure, analyzes evolving attack surfaces, coordinates specialized security agents, retrieves authoritative cybersecurity intelligence through RAG and knowledge graphs, learns from historical incidents through cyber memory, and provides blockchain-backed evidence provenance.**

---

## 🌟 Key Features

1. **Cybersecurity Digital Twin:** Graph-based infrastructure representation mapping Assets, Network Hops, Applications, Databases, Cloud Resources, and Security Controls with dual-backend support (NetworkX / Neo4j).
2. **Deterministic Attack Path & Surface Engine:** Traversal algorithms computing exposure scores and step-by-step adversary paths towards Crown Jewels (e.g. `Internet -> WEB-01 -> APP-01 -> DB-01`).
3. **What-If Scenario Simulation:** Non-destructive delta simulations (e.g., *"Make API-01 public"*) calculating before/after metrics, new attack vectors, and defender recommendations without touching production.
4. **Multi-Agent AI Orchestrator:** LangGraph state machine directing 11 specialized security agents:
   - **SOC Agent:** Log analysis, triage, and MITRE mapping.
   - **VAPT Agent:** Vulnerability correlation and CVSS severity assessment.
   - **API / Web Agent:** Broken object authorization and endpoint analysis.
   - **Cloud Agent:** IAM over-privileging and S3 bucket security.
   - **Threat Intel Agent:** IOC reputation lookup (IPs, domains, hashes, CVEs).
   - **Reviewer Agent:** Adversarial hallucination self-check for factual grounding.
5. **RAG Cybersecurity Brain:** Vector retrieval across authoritative knowledge bases (OWASP Top 10, MITRE ATT&CK, NIST CSF 2.0, CISA KEV, CVE).
6. **Cyber Memory:** 4-tier organizational security memory (Episodic, Semantic, Procedural, Historical) with vector-based similar incident matching.
7. **Blockchain Evidence Provenance:** Cryptographic SHA-256 evidence hashing and immutable anchoring for tamper-evident forensics with real-time verification (`INTEGRITY_VERIFIED` vs `INTEGRITY_MISMATCH`).
8. **Automated Security Reporting:** Executive and technical report synthesis with exportable JSON/Markdown format.

---

## 🚀 Quick Start

### 1. Launch Backend (FastAPI)
```bash
cd cybermind/backend
python -m venv .venv
.\.venv\Scripts\activate      # On Windows
# source .venv/bin/activate   # On Linux/macOS
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
- API is available at: `http://localhost:8000`
- Interactive Swagger documentation: `http://localhost:8000/docs`

### 2. Launch Frontend (Next.js)
```bash
cd cybermind/frontend
npm install
npm run dev
```
- Web Application is available at: `http://localhost:3000`

### 3. Docker Compose (Full Stack)
```bash
cd cybermind
docker compose up --build -d
```

---

## 🔑 Demo Operator Credentials

Pre-configured in `DEMO_MODE=true`:
- **Username:** `secops_admin`
- **Password:** `CyberSecP@ssw0rd2026!`
- **Role:** `ADMIN`

---

## 🧪 Automated Testing & Evaluation

Run the complete test suite:
```bash
cd cybermind/backend
.\.venv\Scripts\pytest tests/ -v
```
All 13 test suites validate:
- Authentication & JWT/RBAC
- Security Headers & Request Tracing
- Seeded Digital Twin Topology & Assets
- Non-destructive Scenario Simulation
- Attack Surface & Attack Path Pathfinding
- Threat Intelligence Correlation
- Cyber Memory Similar Incident Retrieval
- Blockchain Evidence SHA-256 Anchoring & Tamper Detection
- Executive Report Synthesis

Run the Research & Evaluation Benchmark:
```bash
cd cybermind
python scripts/evaluate.py
```

---

## 📁 Repository Structure

```text
cybermind/
├── frontend/             # Next.js 14, React 18, Tailwind CSS, Lucide icons
├── backend/              # FastAPI, SQLAlchemy 2.0, Pydantic v2, NetworkX
│   ├── app/
│   │   ├── api/          # Modular REST endpoints
│   │   ├── auth/         # JWT issuance, password hashing & RBAC
│   │   ├── core/         # Config, security, and LLM abstraction
│   │   ├── models/       # SQLAlchemy database entities
│   │   ├── services/     # Seed data & orchestration services
│   │   └── main.py       # Application entry point
│   └── tests/            # Automated pytest suites
├── docker/               # Backend and Frontend Dockerfiles
├── docker-compose.yml    # Multi-container orchestration (FastAPI, Next.js, Postgres, Neo4j, Redis)
├── scripts/              # Evaluation & research benchmark scripts
├── docs/                 # System architecture, API, and security documentation
├── .env.example          # Environment template
└── Makefile              # Developer shortcuts
```
