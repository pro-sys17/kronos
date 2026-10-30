import json
import re
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from app.api.routes import router

class CleanBodyMiddleware:
    """
    Pure ASGI Middleware that cleans incoming JSON payloads,
    stripping illegal ANSI control codes and escaping malformed characters
    to prevent JSONDecodeError (400 Bad Request) on FastAPI.
    """
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            content_type = ""
            for k, v in scope.get("headers", []):
                if k.lower() == b"content-type":
                    content_type = v.decode("latin1", errors="ignore").lower()
                    break

            if "json" in content_type:
                body_parts = []
                more_body = True
                while more_body:
                    message = await receive()
                    body_parts.append(message.get("body", b""))
                    more_body = message.get("more_body", False)

                raw_body = b"".join(body_parts)
                try:
                    text = raw_body.decode("utf-8", errors="replace")
                    # Clean ANSI escape sequences
                    text = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', text)
                    # Clean illegal unescaped ASCII control codes (0x00 - 0x1F except \t \n \r)
                    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', text)
                    data = json.loads(text, strict=False)
                    clean_bytes = json.dumps(data).encode("utf-8")
                except Exception:
                    clean_bytes = raw_body

                body_sent = False
                async def custom_receive():
                    nonlocal body_sent
                    if not body_sent:
                        body_sent = True
                        return {"type": "http.request", "body": clean_bytes, "more_body": False}
                    return {"type": "http.request", "body": b"", "more_body": False}

                await self.app(scope, custom_receive, send)
                return

        await self.app(scope, receive, send)

app = FastAPI(
    title="KRONOS Neural Core",
    description="Autonomous System Diagnostic and Self-Healing Engine",
    version="3.1.0"
)

app.add_middleware(CleanBodyMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

