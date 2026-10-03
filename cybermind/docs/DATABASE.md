# CyberMIND — Database Schema & Data Dictionary

CyberMIND utilizes SQLAlchemy 2.0 with a dual-dialect architecture supporting SQLite (zero-setup local demonstration) and PostgreSQL with `pgvector` (production deployment).

## Core Tables

| Table | Primary Key | Purpose |
| :--- | :--- | :--- |
| `users` | UUID | Operator credentials, roles (ADMIN, ANALYST, VIEWER), status |
| `organizations` | UUID | Multi-tenant organization boundaries and telemetry metadata |
| `assets` | UUID | Infrastructure assets (type, IP, hostname, criticality, risk score) |
| `asset_relationships` | UUID | Graph edges (CONNECTS_TO, RUNS, USES, EXPOSED_TO) |
| `vulnerabilities` | UUID | Correlated CVE records, CVSS scores, remediation notes |
| `security_controls` | UUID | Active defensive controls (WAF, EDR, MFA, Firewall) |
| `findings` | UUID | AI-generated and scanner-detected security findings |
| `incidents` | UUID | Security incidents, timelines, affected assets, MITRE mappings |
| `threat_indicators` | UUID | Threat intelligence indicators (IP, Domain, Hash, CVE) |
| `evidence` | UUID | Evidence registry, raw payloads, SHA-256 hashes, anchor TXs |
| `investigations` | UUID | AI-agent investigation sessions and execution summaries |
| `agent_runs` | UUID | Individual agent execution logs, latencies, confidence metrics |
| `chat_sessions` | UUID | Operator chat sessions |
| `chat_messages` | UUID | Chat messages, domain tags, source citations, agent traces |
| `documents` | UUID | RAG documents (OWASP, MITRE, NIST, CISA) |
| `document_chunks` | UUID | Semantic chunks and embedding vector coordinates |
| `attack_paths` | UUID | Identified traversal paths targeting Crown Jewels |
| `scenarios` | UUID | What-if simulation parameters, before/after metrics |
| `reports` | UUID | Synthesized security reports (Executive, Technical) |
| `audit_logs` | UUID | Tamper-evident operator activity audit trail |
