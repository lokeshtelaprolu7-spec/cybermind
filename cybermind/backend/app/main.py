import time
import uuid
import json
import logging
import threading
from collections import defaultdict, deque
from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.database.session import engine, Base, SessionLocal
import app.models  # Register all models with Base
from app.services.seed import seed_demo_organization, seed_knowledge_base

# Configure structured logging
access_logger = logging.getLogger("cybermind.access")
if not access_logger.handlers:
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s %(name)s: %(message)s"))
    access_logger.addHandler(console_handler)
access_logger.setLevel(logging.INFO)

# Create all database tables
Base.metadata.create_all(bind=engine)

# Seed database: seed demo org when DEMO_MODE=true; otherwise initialize authoritative knowledge base
try:
    with SessionLocal() as db_session:
        if settings.DEMO_MODE:
            seed_demo_organization(db_session)
        else:
            seed_knowledge_base(db_session)
except Exception as e:
    access_logger.warning(f"Error during database initialization: {e}")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="CyberMIND — Autonomous Cybersecurity Digital Twin, Multi-Agent Intelligence & Evidence Provenance Platform",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory sliding-window rate limiter for high-cost AI, report, and evidence endpoints
_rate_limits = defaultdict(deque)
_rate_lock = threading.Lock()
EXPENSIVE_PATH_PREFIXES = ("/api/chat", "/api/reports", "/api/evidence")

# Security Headers, Rate Limiting & Structured Request Tracing Middleware
@app.middleware("http")
async def security_and_tracing_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    start_time = time.time()
    client_ip = request.client.host if request.client else "unknown"

    # Rate limiting check on expensive endpoints
    path = request.url.path
    if any(path.startswith(prefix) for prefix in EXPENSIVE_PATH_PREFIXES):
        now = time.time()
        window = 60.0  # 1 minute window
        limit = settings.RATE_LIMIT_REQUESTS_PER_MINUTE
        with _rate_lock:
            q = _rate_limits[client_ip]
            while q and q[0] <= now - window:
                q.popleft()
            if len(q) >= limit:
                access_logger.warning(
                    json.dumps({
                        "event": "rate_limit_exceeded",
                        "request_id": request_id,
                        "client_ip": client_ip,
                        "path": path,
                        "limit": limit
                    })
                )
                return JSONResponse(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content={
                        "error": "Rate limit exceeded",
                        "detail": f"Rate limit of {limit} requests/minute exceeded for high-cost security endpoints.",
                        "request_id": request_id
                    },
                    headers={"Retry-After": "60"}
                )
            q.append(now)
    
    try:
        response: Response = await call_next(request)
    except Exception as exc:
        access_logger.error(
            json.dumps({
                "event": "server_error",
                "request_id": request_id,
                "client_ip": client_ip,
                "method": request.method,
                "path": path,
                "error": str(exc)
            })
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "Internal Server Error",
                "message": "An unexpected error occurred during security processing.",
                "request_id": request_id
            }
        )
        
    process_time = time.time() - start_time
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{process_time:.4f}s"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

    # Structured access log (sanitized: never log auth tokens, passwords or bodies)
    access_logger.info(
        json.dumps({
            "request_id": request_id,
            "client_ip": client_ip,
            "method": request.method,
            "path": path,
            "status_code": response.status_code,
            "latency_ms": round(process_time * 1000, 2)
        })
    )

    return response

# Health Checks
@app.get("/health", tags=["Health"])
@app.get("/api/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "demo_mode": settings.DEMO_MODE,
        "llm_provider": settings.LLM_PROVIDER
    }

# Include All API Routers
from app.auth.routes import router as auth_router
from app.api.chat import router as chat_router
from app.api.assets import router as assets_router
from app.api.findings import router as findings_router
from app.api.incidents import router as incidents_router
from app.api.digital_twin import router as digital_twin_router
from app.api.attack_surface import router as attack_surface_router
from app.api.threat_intel import router as threat_intel_router
from app.api.cyber_memory import router as cyber_memory_router
from app.api.evidence import router as evidence_router
from app.api.reports import router as reports_router
from app.api.knowledge import router as knowledge_router

app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(chat_router, prefix=settings.API_V1_STR)
app.include_router(assets_router, prefix=settings.API_V1_STR)
app.include_router(findings_router, prefix=settings.API_V1_STR)
app.include_router(incidents_router, prefix=settings.API_V1_STR)
app.include_router(digital_twin_router, prefix=settings.API_V1_STR)
app.include_router(attack_surface_router, prefix=settings.API_V1_STR)
app.include_router(threat_intel_router, prefix=settings.API_V1_STR)
app.include_router(cyber_memory_router, prefix=settings.API_V1_STR)
app.include_router(evidence_router, prefix=settings.API_V1_STR)
app.include_router(reports_router, prefix=settings.API_V1_STR)
app.include_router(knowledge_router, prefix=settings.API_V1_STR)

@app.get(f"{settings.API_V1_STR}", tags=["Root"])
def api_root():
    return {
        "message": f"Welcome to {settings.APP_NAME} API v{settings.APP_VERSION}",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)

