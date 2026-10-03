# CyberMIND — Production Deployment Guide

This guide describes how to deploy **CyberMIND (Agentic AI-Powered Cybersecurity Digital Twin)** to production environments with high availability, security hardening, dynamic origins, and persistent infrastructure.

---

## 1. System Architecture Overview

In production, CyberMIND operates as a decoupled, multi-tier cloud application:

```
                          ┌──────────────────────────┐
                          │   Internet Users / SOC   │
                          └─────────────┬────────────┘
                                        │ HTTPS (443)
                                        ▼
             ┌──────────────────────────────────────────────────────┐
             │       Edge / CDN / Reverse Proxy (Cloudflare / Nginx) │
             └──────────┬─────────────────────────────┬─────────────┘
                        │                             │
       https://cybermind.domain.com       https://api.cybermind.domain.com
                        │                             │
                        ▼                             ▼
             ┌─────────────────────┐       ┌────────────────────────┐
             │ Next.js 14 Frontend │       │  FastAPI 0.110 Backend │
             │  (Node.js / Vercel) │       │ (Uvicorn / Render / VM)│
             └─────────────────────┘       └───────────┬────────────┘
                                                       │
                     ┌───────────────────┬─────────────┴─────────────┬────────────────────┐
                     ▼                   ▼                           ▼                    ▼
             ┌───────────────┐   ┌───────────────┐           ┌───────────────┐    ┌───────────────┐
             │ PostgreSQL 16 │   │ Neo4j Graph DB│           │ Redis Cache   │    │ EVM / Polygon │
             │  + pgvector   │   │  (Opt. Twin)  │           │ & Rate-Limit  │    │ Anchor RPC    │
             └───────────────┘   └───────────────┘           └───────────────┘    └───────────────┘
```

---

## 2. Environment Variables Specification

### Backend Configuration (`cybermind/backend/.env`)

| Variable | Recommended Production Value | Description |
| :--- | :--- | :--- |
| `ENVIRONMENT` | `production` | Enables production security checks and strict validation |
| `DEMO_MODE` | `false` | **Crucial:** Prevents synthetic demo assets/users from auto-populating |
| `HOST` | `0.0.0.0` | Network interface to bind |
| `PORT` | `8000` (or injected by PaaS) | Listening port |
| `FRONTEND_URL` | `https://cybermind.yourdomain.com` | Primary web client origin |
| `BACKEND_URL` | `https://api.cybermind.yourdomain.com` | Publicly resolvable backend URL |
| `CORS_ORIGINS` | `https://cybermind.yourdomain.com` | Comma-separated allowed CORS origins |
| `SECRET_KEY` | *(generate via `openssl rand -hex 32`)* | Master cryptographically secure JWT signing key |
| `DATABASE_URL` | `postgresql+psycopg2://user:pass@host:5432/cybermind` | Production PostgreSQL connection string |
| `RATE_LIMIT_REQUESTS_PER_MINUTE` | `60` | In-memory / edge throttle threshold for `/chat`, `/reports`, `/evidence` |
| `LLM_PROVIDER` | `openai` (or `compatible`) | Production AI reasoning provider (`openai`, `compatible`, `mock`) |
| `OPENAI_API_KEY` | `sk-proj-...` | Production OpenAI API key (or self-hosted LLM gateway key) |
| `LLM_MODEL` | `gpt-4o` | Production foundation model |

### Frontend Configuration (`cybermind/frontend/.env.production`)

| Variable | Recommended Production Value | Description |
| :--- | :--- | :--- |
| `NEXT_PUBLIC_API_URL` | `https://api.cybermind.yourdomain.com` | Public REST & WebSocket endpoint |

---

## 3. Database Setup & First-Time Initialization

### A. Provision PostgreSQL with `pgvector`
Deploy a managed PostgreSQL 16 instance (AWS RDS, Supabase, Neon, Railway, or self-hosted) and enable the vector extension:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

### B. Initialize Database & Seed Knowledge Base
Run database table generation with `DEMO_MODE=false`. This automatically provisions schema tables and imports authoritative security documents (OWASP Top 10, MITRE ATT&CK techniques, NIST CSF) without seeding fake demo companies:

```bash
cd cybermind/backend
export DEMO_MODE=false
export DATABASE_URL="postgresql+psycopg2://cybermind_user:StrongPassword@postgres.internal:5432/cybermind"
python -c "from app.database.session import Base, engine; Base.metadata.create_all(bind=engine); from app.services.seed import seed_knowledge_base; from app.database.session import SessionLocal; seed_knowledge_base(SessionLocal())"
```

### C. Provision Production Administrator
Create the initial SecOps Administrator using the standalone utility:

```bash
python scripts/create_admin.py \
  --email "secops-lead@yourcompany.com" \
  --password "YourSecureProductionPassw0rd!" \
  --full-name "Lead Security Engineer" \
  --org-name "Enterprise SOC" \
  --role "admin"
```

---

## 4. Deployment Strategies

### Strategy A: Docker Compose on VPS / Cloud VM (Recommended for All-In-One)

1. Provision an Ubuntu 22.04 / Debian 12 instance (min 4 vCPU, 8 GB RAM).
2. Clone repository:
   ```bash
   git clone <your-repo-url> /opt/cybermind
   cd /opt/cybermind/cybermind
   ```
3. Create production `.env`:
   ```bash
   cp .env.example .env
   # Edit variables (set DEMO_MODE=false, SECRET_KEY, OPENAI_API_KEY, etc.)
   ```
4. Build and start containers:
   ```bash
   docker compose -f docker-compose.yml up -d --build
   ```
5. Configure Nginx with SSL via Let's Encrypt / Certbot:
   ```nginx
   server {
       server_name cybermind.yourdomain.com;
       location / {
           proxy_pass http://127.0.0.1:3000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }

   server {
       server_name api.cybermind.yourdomain.com;
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

---

### Strategy B: Managed PaaS (Vercel + Render / Railway / Fly.io)

#### 1. Deploy Frontend to Vercel:
1. Connect Git repository to [Vercel](https://vercel.com).
2. Set Root Directory: `cybermind/frontend`.
3. Set Framework: `Next.js`.
4. Add Environment Variable:
   - `NEXT_PUBLIC_API_URL` = `https://api.cybermind.yourdomain.com`
5. Click **Deploy**. Assign your custom domain: `cybermind.yourdomain.com`.

#### 2. Deploy Backend to Render / Railway / Fly.io:
1. Connect Git repository.
2. Set Root Directory: `cybermind/backend`.
3. Build Command: `pip install -r requirements.txt`.
4. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 4`.
5. Set Environment Variables:
   - `ENVIRONMENT` = `production`
   - `DEMO_MODE` = `false`
   - `SECRET_KEY` = `[Generated Key]`
   - `FRONTEND_URL` = `https://cybermind.yourdomain.com`
   - `CORS_ORIGINS` = `https://cybermind.yourdomain.com`
   - `DATABASE_URL` = `postgresql://...`
   - `LLM_PROVIDER` = `openai`
   - `OPENAI_API_KEY` = `sk-...`
6. Assign custom domain: `api.cybermind.yourdomain.com`.

---

## 5. Security Hardening Checklist

- [x] **No Default Credentials:** `DEMO_MODE=false` prevents default demo admin seeding.
- [x] **Rate Limiting:** In-memory sliding-window throttle active on `/api/chat`, `/api/reports`, and `/api/evidence`.
- [x] **Strict CORS:** Configured explicitly to reject cross-origin requests outside `CORS_ORIGINS` and `FRONTEND_URL`.
- [x] **Security Headers:** Enforced via middleware:
  - `X-Content-Type-Options: nosniff`
  - `X-Frame-Options: DENY`
  - `X-XSS-Protection: 1; mode=block`
  - `Strict-Transport-Security: max-age=31536000; includeSubDomains`
  - `Referrer-Policy: strict-origin-when-cross-origin`
- [x] **Sanitized Audit Logging:** Request IDs (`X-Request-ID`) tracked across all invocations; passwords and bearer tokens are never output to stdout or logs.

---

## 6. Health Checks & Monitoring

CyberMIND exposes production liveness and readiness probes:

- **Liveness probe:** `GET /health` or `GET /api/health`
  ```json
  {
    "status": "healthy",
    "service": "CyberMIND",
    "version": "1.0.0",
    "environment": "production",
    "demo_mode": false,
    "llm_provider": "openai"
  }
  ```
- **API Documentation (OpenAPI/Swagger):** Available at `/docs` (or disable in extreme locked environments by passing `docs_url=None` when `ENVIRONMENT == 'production'`).

---

## 7. Disaster Recovery & Rollback Procedure

1. **Database Backups:**
   - Execute daily automated snapshots using `pg_dump`:
     ```bash
     pg_dump -Fc "$DATABASE_URL" > cybermind_backup_$(date +%F).dump
     ```
2. **Rollback Strategy:**
   - For Vercel frontend: Select previous Instant Rollback deployment in Vercel UI.
   - For containerized backend: Pin docker images using commit hashes (e.g. `cybermind-backend:v1.0.0`), allowing one-line rollback:
     ```bash
     docker compose down && docker compose up -d
     ```
