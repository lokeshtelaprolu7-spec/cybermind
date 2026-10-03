# CyberMIND — REST API Reference

All endpoints are prefixed with `/api`. Interactive OpenAPI documentation is served at `/docs`.

## Authentication & RBAC
- `POST /api/auth/register` — Enroll operator with role (ADMIN, ANALYST, VIEWER)
- `POST /api/auth/login` — Authenticate and receive JWT bearer token
- `GET  /api/auth/me` — Inspect authenticated operator session
- `POST /api/auth/logout` — Terminate session

## Digital Twin & Attack Surface
- `GET  /api/digital-twin` — Retrieve graph topology (nodes, edges, vulnerabilities)
- `POST /api/digital-twin/scenario` — Non-destructive what-if simulation (e.g., "Make API-01 Public")
- `GET  /api/attack-surface` — Perimeter exposure index and internet-facing assets
- `GET  /api/attack-paths` — Calculated traversal paths discovering crown jewel access

## Multi-Agent AI Analyst
- `POST /api/chat` — Invoke orchestrator coordinating SOC, VAPT, Threat Intel, Cloud & Reviewer agents

## Assets, Findings & Incidents
- `GET  /api/assets` / `POST /api/assets`
- `GET  /api/findings` / `POST /api/findings`
- `GET  /api/incidents` / `POST /api/incidents`

## Threat Intelligence & Cyber Memory
- `GET  /api/threat-intel/{indicator}` — Look up IP, domain, hash, or CVE reputation
- `GET  /api/cyber-memory/summary` — Four-tier memory summary
- `POST /api/cyber-memory/similar-incidents` — Vector correlation against historical playbooks

## Evidence Provenance
- `GET  /api/evidence` / `POST /api/evidence` — Ingest evidence and anchor SHA-256 hash
- `POST /api/evidence/{id}/verify` — Recompute hash and verify blockchain ledger integrity

## Reporting
- `POST /api/reports/generate` — Synthesize executive security reports
