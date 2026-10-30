import os
from pathlib import Path
from fastapi import APIRouter, Request, Response, HTTPException, Header
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

from app.core.ai_brain import AIBrain
from app.core.security import SecurityManager

router = APIRouter()
brain = AIBrain()

CLIENT_SCRIPT_PATH = Path(__file__).resolve().parents[3] / "client" / "kronos.ps1"
if not CLIENT_SCRIPT_PATH.exists():
    for candidate in [
        Path(__file__).resolve().parents[2] / "client" / "kronos.ps1",
        Path.cwd().parent / "client" / "kronos.ps1",
        Path.cwd() / "client" / "kronos.ps1",
    ]:
        if candidate.exists():
            CLIENT_SCRIPT_PATH = candidate
            break

class DiagnoseRequest(BaseModel):
    problem: str = Field(..., max_length=2000)
    telemetry: Optional[Dict[str, Any]] = None
    session_token: Optional[str] = None
    history: Optional[list] = None
    last_output: Optional[str] = None

@router.get("/health")
async def health_check():
    return {"status": "HEALTHY", "service": "KRONOS-CORE", "version": "3.1.0"}

@router.get("/api/v1/skills")
async def list_skills():
    from app.core.skills.registry import SKILLS
    return [
        {
            "id": s.skill_id,
            "name": s.name,
            "description": s.description,
            "triggers": s.triggers[:6]
        }
        for s in SKILLS
    ]

@router.get("/kronos")
async def serve_bootstrap(request: Request):
    """
    Serves bootstrap payload with dynamically embedded:
    1. Base URL
    2. Signed ephemeral session token
    """
    if not CLIENT_SCRIPT_PATH.exists():
        raise HTTPException(status_code=404, detail="Bootstrap payload not found")

    content = CLIENT_SCRIPT_PATH.read_text(encoding="utf-8-sig").lstrip("\ufeff")
    proto = request.headers.get("x-forwarded-proto", request.url.scheme)
    host = request.headers.get("x-forwarded-host", request.url.netloc)
    base_url = f"{proto}://{host}".rstrip("/")
    session_token = SecurityManager.generate_session_token()

    # Inject URL and Token into script parameters
    modified_content = content.replace('http://127.0.0.1:8000', base_url)
    modified_content = modified_content.replace('SESSION_TOKEN_PLACEHOLDER', session_token)

    return Response(content=modified_content, media_type="text/plain; charset=utf-8")

@router.post("/api/v1/diagnose")
async def diagnose_problem(req: DiagnoseRequest, request: Request, x_session_token: Optional[str] = Header(None)):
    """
    Guarded diagnosis endpoint:
    - Rate limit verification
    - Session signature verification
    - AST command sanitization
    """
    client_ip = request.client.host if request.client else "unknown"

    # 1. Rate Limiting Check
    allowed, reason = SecurityManager.check_rate_limit(client_ip)
    if not allowed:
        raise HTTPException(status_code=429, detail=reason)

    # 2. Session Signature Verification
    token = req.session_token or x_session_token
    if not SecurityManager.verify_session_token(token):
        raise HTTPException(status_code=401, detail="Invalid or expired session authorization signature.")

    # 3. AI Diagnosis & Guardrail Execution
    telemetry_data = req.telemetry or {}
    verdict = await brain.diagnose(
        req.problem,
        telemetry_data,
        history=req.history,
        last_output=req.last_output
    )
    return verdict
