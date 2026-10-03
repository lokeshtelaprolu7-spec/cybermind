# CyberMIND — Installation & Setup Guide

## Quick Start (Local Standalone Mode)

### Prerequisites
- Python 3.11+
- Node.js 18+ (LTS) & npm

### 1. Backend Setup
```bash
cd cybermind/backend
python -m venv .venv
# Windows:
.\.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
API runs at `http://localhost:8000` with Swagger docs at `http://localhost:8000/docs`.

### 2. Frontend Setup
```bash
cd cybermind/frontend
npm install
npm run dev
```
UI runs at `http://localhost:3000`.

### 3. Docker Deployment
```bash
cd cybermind
docker compose up --build -d
```
All services (Next.js, FastAPI, PostgreSQL+pgvector, Neo4j, Redis) start automatically.
