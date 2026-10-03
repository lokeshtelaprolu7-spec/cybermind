# CyberMIND — Deployment Guide

## 1. Containerized Multi-Service Deployment (Production)

CyberMIND ships with a production-ready `docker-compose.yml` orchestrating:
- **`frontend`:** Next.js production build served on port 3000
- **`backend`:** FastAPI ASGI application served on port 8000
- **`postgres`:** PostgreSQL 16 with `pgvector` extension for vector embeddings on port 5432
- **`neo4j`:** Neo4j Community Edition v5 with APOC plugins on ports 7474 (HTTP) and 7687 (Bolt)
- **`redis`:** Redis 7 for cache and worker queuing on port 6379

### Quick Launch
```bash
cd cybermind
docker compose up --build -d
```

### Inspect Container Logs
```bash
docker compose logs -f backend
docker compose logs -f frontend
```

### Teardown
```bash
docker compose down
```

## 2. Local Standalone Mode (`DEMO_MODE=true`)
When external databases are unavailable, CyberMIND automatically activates standalone mode:
- SQLite for persistence
- In-memory NetworkX directed graph engine
- Deterministic cryptographic evidence ledger simulation
- Offline mock AI provider with zero third-party API dependencies
