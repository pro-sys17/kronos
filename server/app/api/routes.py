import os
from pathlib import Path
from fastapi import APIRouter, Request, Response, HTTPException, Header
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

from app.core.ai_brain import AIBrain
from app.core.security import SecurityManager
from app.core.tools.registry import ToolRegistry
from app.core.authorization import OperationAuthorizer

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
    model: Optional[str] = None

class SwitchModelRequest(BaseModel):
    model: str
    session_token: Optional[str] = None

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
            "triggers": (s.natural_triggers[:6] if hasattr(s, "natural_triggers") else getattr(s, "triggers", [])[:6])
        }
        for s in SKILLS
    ]

@router.get("/api/v1/tools")
async def list_tools():
    """
    Returns registered system tools, parameters, and risk classifications.
    """
    from app.core.tools.registry import ToolRegistry
    return {
        "status": "SUCCESS",
        "total_tools": len(ToolRegistry.list_all()),
        "tools": ToolRegistry.get_schemas()
    }

@router.get("/api/v1/memory")
async def get_memory_summary():
    """
    Returns non-sensitive persistent troubleshooting memory, recent chat summaries, and host profile.
    """
    from app.core.memory.store import MemoryStore
    recent_episodes = MemoryStore.get_recent_history(limit=10)
    recent_chats = MemoryStore.get_chat_history(limit=20)
    profile = MemoryStore.get_latest_profile()
    return {
        "status": "SUCCESS",
        "profile": profile,
        "recent_troubleshooting_count": len(recent_episodes),
        "recent_episodes": [
            {
                "issue_summary": ep.get("issue_summary", ""),
                "root_cause": ep.get("root_cause", ""),
                "tools_executed": ep.get("tools_executed", ""),
                "outcome": ep.get("outcome", ""),
                "timestamp": ep.get("timestamp", "")
            }
            for ep in recent_episodes
        ],
        "recent_chats_count": len(recent_chats),
        "recent_chats": [
            {
                "id": c.get("id"),
                "timestamp": c.get("timestamp", ""),
                "user_message": c.get("user_message", ""),
                "ai_summary": c.get("ai_summary", ""),
                "intent": c.get("intent", ""),
                "actions_count": c.get("actions_count", 0)
            }
            for c in recent_chats
        ]
    }

@router.post("/api/v1/memory/clear")
async def clear_memory():
    """
    Clears local persistent troubleshooting memory store.
    """
    from app.core.memory.store import MemoryStore
    try:
        MemoryStore.clear_memory()
        return {"status": "SUCCESS", "message": "Memory store cleared successfully."}
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}

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


@router.get("/api/v1/session")
async def get_session():
    """
    Returns an ephemeral cryptographically signed session token for local/CLI clients.
    """
    token = SecurityManager.generate_session_token()
    return {"status": "SUCCESS", "session_token": token}

@router.get("/api/v1/models")
async def get_models():
    """
    Returns available models, active model, and capabilities.
    """
    return {
        "status": "SUCCESS",
        "active_model": brain.active_model,
        "available_models": brain.get_available_models()
    }

@router.post("/api/v1/model")
async def switch_model(req: SwitchModelRequest):
    """
    Switches active AI model on the fly.
    """
    new_model = brain.set_active_model(req.model)
    return {
        "status": "SUCCESS",
        "active_model": new_model,
        "message": f"Active AI model switched to: {new_model}"
    }

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
        last_output=req.last_output,
        session_token=token,
        requested_model=req.model
    )
    return verdict

class ExecuteToolRequest(BaseModel):
    tool_id: str
    arguments: Dict[str, Any] = Field(default_factory=dict)
    approval_ticket: Optional[str] = None
    session_token: Optional[str] = None


@router.post("/api/v1/execute")
async def execute_tool(req: ExecuteToolRequest, request: Request, x_session_token: Optional[str] = Header(None)):
    """
    Cryptographically guarded endpoint for executing registered Windows system tools.
    Enforces:
    1. Client IP rate limiting
    2. Ephemeral session signature verification
    3. Tool existence in ToolRegistry
    4. Strict argument type, bounds, and unexpected argument schema validation
    5. Single-use, non-expired cryptographic approval ticket verification for modifying or MODERATE/HIGH/CRITICAL operations.
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

    # 3. Tool Existence Verification
    tool = ToolRegistry.get(req.tool_id)
    if not tool:
        raise HTTPException(status_code=400, detail=f"Unauthorized or unknown tool ID: '{req.tool_id}'.")

    # 4. Parameter Schema Validation
    is_valid, err = tool.validate_args(req.arguments)
    if not is_valid:
        raise HTTPException(status_code=400, detail=f"Validation failed for tool '{req.tool_id}': {err}")

    # 5. Cryptographic Approval Verification for Modifying / High-Risk Operations
    if tool.requires_confirmation or tool.risk in ["MODERATE", "HIGH", "CRITICAL"]:
        if not req.approval_ticket:
            raise HTTPException(
                status_code=403,
                detail=f"Operation '{req.tool_id}' ({tool.risk} risk) requires an explicit cryptographic approval ticket."
            )
        auth_ok, auth_err = OperationAuthorizer.verify_and_consume_ticket(
            req.approval_ticket,
            req.tool_id,
            req.arguments
        )
        if not auth_ok:
            raise HTTPException(status_code=403, detail=f"Authorization rejected: {auth_err}")

    # 6. Generate Deterministic Command and Verification
    cmd = tool.build_command(req.arguments)
    verif = tool.build_verification(req.arguments)

    return {
        "status": "AUTHORIZED",
        "tool_id": tool.tool_id,
        "tool_name": tool.name,
        "risk": tool.risk,
        "command": cmd,
        "verification": verif
    }

