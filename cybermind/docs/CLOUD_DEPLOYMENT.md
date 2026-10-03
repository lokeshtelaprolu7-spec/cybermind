# CyberMIND — Complete Cloud Deployment Guide (Vercel + Render + PostgreSQL)

This guide documents the exact, production-grade cloud deployment workflow for **CyberMIND (Autonomous Cybersecurity Digital Twin)**:
- **Frontend:** Next.js 14 deployed to **Vercel**
- **Backend:** FastAPI + Uvicorn deployed to **Render**
- **Database:** Managed **PostgreSQL** on Render (with `pgvector` / `uuid-ossp`)

---

## 1. System Architecture

```
  ┌────────────────────────────────────────────────────────┐
  │                   PUBLIC INTERNET                      │
  └──────────┬─────────────────────────────────┬───────────┘
             │ HTTPS (Port 443)                │ HTTPS (Port 443)
             ▼                                 ▼
  ┌───────────────────────┐         ┌────────────────────────┐
  │    Vercel Edge CDN    │         │     Render Web Service │
  │  (Next.js 14 Frontend)│  CORS   │    (FastAPI / Uvicorn) │
  │                       ├────────►│                        │
  │ cybermind.vercel.app  │         │ cybermind-api.onrender │
  └───────────────────────┘         └───────────┬────────────┘
                                                │ Internal Network / SSL
                                                ▼
                                    ┌────────────────────────┐
                                    │    Render Managed DB   │
                                    │    (PostgreSQL 16)     │
                                    └────────────────────────┘
```

---

## 2. Step 1: Push Code to GitHub

Verify that secrets and database files are excluded by `.gitignore`:
```bash
# Verify .env and *.db are untracked
git status --ignored
```

Initialize and push to your private or public GitHub repository:
```bash
git add .
git commit -m "feat: configure CyberMIND for Vercel and Render production deployment"
git branch -M main
git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/<YOUR_REPOSITORY_NAME>.git
git push -u origin main
```

---

## 3. Step 2: Provision PostgreSQL on Render

1. Log into your [Render Dashboard](https://dashboard.render.com).
2. Click **New +** and select **PostgreSQL**.
3. Configure the database instance:
   - **Name:** `cybermind-postgres`
   - **Database:** `cybermind`
   - **User:** `cybermind_user`
   - **Region:** Select the region closest to your target audience (e.g., Oregon, Frankfurt, Singapore).
   - **PostgreSQL Version:** 16
   - **Instance Type:** `Free` (or `Starter` for production durability).
4. Click **Create Database**.
5. Once provisioned, locate the **Connections** panel:
   - Copy the **Internal Database URL** (if deploying backend in the same Render region) or **External Database URL**.
   - Note: The URL will look like:
     `postgres://cybermind_user:<PASSWORD>@dpg-xxxxxx.render.com/cybermind`

---

## 4. Step 3: Deploy Backend to Render

### Option A: Using Render Blueprint (`render.yaml`)
1. In Render Dashboard, click **New +** -> **Blueprint**.
2. Select your connected GitHub repository.
3. Render will detect `render.yaml` and configure both the database and web service automatically.

### Option B: Manual Web Service Setup (Step-by-Step)
1. In Render Dashboard, click **New +** -> **Web Service**.
2. Connect your GitHub repository.
3. Set the build and runtime parameters:
   - **Name:** `cybermind-backend`
   - **Region:** Same region as your PostgreSQL database.
   - **Branch:** `main`
   - **Root Directory:** `cybermind/backend`
   - **Runtime:** `Python 3`
   - **Build Command:**
     ```bash
     pip install -r requirements.txt
     ```
   - **Start Command:**
     ```bash
     uvicorn app.main:app --host 0.0.0.0 --port $PORT
     ```
   - **Instance Type:** `Free` (or `Starter` for 0% sleep).

4. Configure **Environment Variables** in the Render UI:

| Key | Example Value | Description |
| :--- | :--- | :--- |
| `PYTHON_VERSION` | `3.11.9` | Pinned Python runtime |
| `ENVIRONMENT` | `production` | Enables production security checks & strict CORS |
| `DEMO_MODE` | `false` | **Crucial:** Skips fake demo data, loads authoritative OWASP/MITRE/NIST brain |
| `DATABASE_URL` | `postgresql+psycopg2://cybermind_user:<PASS>@<HOST>/cybermind` | PostgreSQL connection string |
| `SECRET_KEY` | *(generate via `openssl rand -hex 32`)* | Cryptographically secure JWT signing key |
| `FRONTEND_URL` | `https://cybermind.vercel.app` | Your Vercel domain (update after Vercel setup) |
| `CORS_ORIGINS` | `https://cybermind.vercel.app` | Comma-separated allowed frontend origins |
| `RATE_LIMIT_REQUESTS_PER_MINUTE` | `60` | In-memory sliding-window throttle limit |
| `LLM_PROVIDER` | `openai` (or `mock` for zero-cost) | AI reasoning provider |
| `OPENAI_API_KEY` | `sk-proj-...` | Production OpenAI API key (optional if mock) |
| `LLM_MODEL` | `gpt-4o` | Model designation |

5. Click **Create Web Service**.
6. When deployment finishes, note your public backend URL:
   `https://cybermind-backend.onrender.com`

---

## 5. Step 4: Deploy Frontend to Vercel

1. Log into your [Vercel Dashboard](https://vercel.com).
2. Click **Add New...** -> **Project**.
3. Import your GitHub repository.
4. In the **Configure Project** screen:
   - **Project Name:** `cybermind`
   - **Framework Preset:** `Next.js`
   - **Root Directory:** Click **Edit** and choose `cybermind/frontend`.
   - **Build Command:** `next build` (default)
   - **Output Directory:** `.next` (default)
   - **Install Command:** `npm install` (default)
5. Under **Environment Variables**, add:

| Key | Value | Description |
| :--- | :--- | :--- |
| `NEXT_PUBLIC_API_URL` | `https://cybermind-backend.onrender.com` | Resolves public REST and WebSocket APIs |

6. Click **Deploy**.
7. Vercel will build and assign your production domain:
   `https://cybermind.vercel.app` (or custom name).

---

## 6. Step 5: Finalize CORS & Handshake

Once you have both public URLs:
1. In your **Render Dashboard** -> `cybermind-backend` -> **Environment**:
   - Set `FRONTEND_URL` = `https://<YOUR_ACTUAL_VERCEL_DOMAIN>.vercel.app`
   - Set `CORS_ORIGINS` = `https://<YOUR_ACTUAL_VERCEL_DOMAIN>.vercel.app`
2. Save changes (Render will automatically redeploy with the updated CORS policy).
3. Now, only your Vercel frontend is authorized to make authenticated API requests to your Render backend.

---

## 7. Step 6: Initialize Database & Provision Admin User

### 1. Initialize Tables & Authoritative Security Knowledge Base
From your local terminal (pointing to the remote Render PostgreSQL database via external connection string):

```bash
cd cybermind
export DATABASE_URL="postgresql+psycopg2://cybermind_user:<PASS>@dpg-xxxxxx.render.com/cybermind"
export DEMO_MODE=false
export ENVIRONMENT=production

python scripts/init_db.py
```
*Output will verify table creation for all 20 security models and index OWASP Top 10, MITRE ATT&CK, and NIST CSF documents into the RAG brain.*

### 2. Create the Production Administrator
```bash
python scripts/create_admin.py \
  --email "secops@yourcompany.com" \
  --password "YourStrongPassword123!" \
  --full-name "Primary SecOps Lead" \
  --org-name "Enterprise Cyber Defense" \
  --role "admin"
```

---

## 8. Step 7: Verification & Acceptance Testing

Verify your deployment using the following checks:

### 1. Backend Health Check
```bash
curl -s https://<YOUR_BACKEND_URL>.onrender.com/health
```
Expected response:
```json
{
  "status": "healthy",
  "service": "CyberMIND",
  "version": "1.0.0",
  "environment": "production",
  "demo_mode": false,
  "llm_provider": "mock"
}
```

### 2. Interactive Swagger / OpenAPI Documentation
Open in your browser:
`https://<YOUR_BACKEND_URL>.onrender.com/docs`
Verify all 12 router categories (Auth, Chat, Digital Twin, Attack Surface, Cyber Memory, Evidence, Reports) are listed.

### 3. Frontend Web Interface
Open in your browser:
`https://<YOUR_FRONTEND_URL>.vercel.app`
1. Navigate to `/login`.
2. Enter your administrator credentials (`secops@yourcompany.com`).
3. Verify access to:
   - **Dashboard:** Metrics and threat posture summary.
   - **AI Security Analyst:** Chat with RAG citations and agent reasoning.
   - **Digital Twin:** Visual network topology graph.
   - **Attack Surface:** Ingress vector analysis and risk scoring.
   - **Cyber Memory:** Incident retrieval and playbook recommendations.
   - **Evidence Provenance:** Cryptographic hashing and integrity verification.

---

## 9. Custom Domain & HTTPS Setup (Optional)

### Custom Domain for Frontend (`cybermind.yourdomain.com`)
1. In Vercel -> Project Settings -> **Domains**.
2. Add `cybermind.yourdomain.com`.
3. In your DNS provider (Cloudflare, Route53, Namecheap), add:
   - **Type:** `CNAME`
   - **Name:** `cybermind`
   - **Target:** `cname.vercel-dns.com`

### Custom Domain for Backend (`api.cybermind.yourdomain.com`)
1. In Render -> Web Service Settings -> **Custom Domains**.
2. Add `api.cybermind.yourdomain.com`.
3. In your DNS provider, add:
   - **Type:** `CNAME`
   - **Name:** `api`
   - **Target:** `<your-service>.onrender.com`
4. Update `FRONTEND_URL` and `CORS_ORIGINS` on Render and `NEXT_PUBLIC_API_URL` on Vercel to reflect the new custom domains.
