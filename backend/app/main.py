"""HTTP entry point for the PHP-SHIELD RDC API foundation."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="PHP-SHIELD RDC API", version="0.1.0", description="API de fondation; modules métier en construction.")
origins = [x.strip() for x in os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",") if x.strip()]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=False, allow_methods=["GET"], allow_headers=["Authorization", "Content-Type"])

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
