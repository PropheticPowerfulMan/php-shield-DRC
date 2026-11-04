"""HTTP entry point for the PHP-SHIELD RDC API foundation."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import os
from app.auth import router as auth_router

app = FastAPI(title="PHP-SHIELD RDC API", version="0.1.0", description="API de fondation; modules métier en construction.")
origins = [x.strip() for x in os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",") if x.strip()]
secret_key = os.getenv("SECRET_KEY", "development-only-change-me")
if os.getenv("APP_ENV", "development") != "development" and len(secret_key) < 32:
    raise RuntimeError("Set a unique SECRET_KEY of at least 32 characters outside development.")
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["GET", "POST"], allow_headers=["Authorization", "Content-Type"])
app.add_middleware(SessionMiddleware, secret_key=secret_key, session_cookie="php_shield_session", max_age=8 * 60 * 60, same_site="lax", https_only=os.getenv("APP_ENV", "development") != "development")
app.include_router(auth_router, prefix="/api/v1")

@app.get("/api/v1/health", tags=["system"])
def health():
    return {"status": "ok", "service": "php-shield-rdc-api", "phase": "foundation"}

@app.get("/api/v1/dashboard", tags=["dashboard"])
def dashboard():
    """Honest empty-state counts until persistent modules are implemented."""
    return {"applications": 0, "servers": 0, "audited_applications": 0, "awaiting_audit": 0,
            "vulnerabilities": {"critical": 0, "high": 0, "moderate": 0, "low": 0},
            "open_remediations": 0, "resolved": 0, "unsupported_php": 0,
            "recent_alerts": [], "recent_activity": [], "risk_distribution": [],
            "notice": "Aucune donnée inventoriée. Les modules métier sont en cours de construction."}
