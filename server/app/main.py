import json
import re
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
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


@app.get("/", response_class=HTMLResponse)
async def root_index(request: Request):
    base_url = str(request.base_url).rstrip("/")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KRONOS // Autonomous Windows Co-Pilot</title>
    <style>
        body {{
            background-color: #0d1117;
            color: #c9d1d9;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            margin: 0;
            padding: 20px;
            box-sizing: border-box;
        }}
        .card {{
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 12px;
            padding: 32px;
            max-width: 680px;
            width: 100%;
            box-shadow: 0 8px 24px rgba(0,0,0,0.5);
        }}
        h1 {{
            color: #58a6ff;
            margin-top: 0;
            font-size: 26px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .badge {{
            background: #238636;
            color: white;
            font-size: 12px;
            padding: 3px 8px;
            border-radius: 20px;
            font-weight: 600;
        }}
        p {{
            color: #8b949e;
            line-height: 1.6;
        }}
        .cmd-box {{
            background: #090d13;
            border: 1px solid #388bfd40;
            border-radius: 8px;
            padding: 16px;
            font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
            font-size: 14px;
            color: #7ee787;
            margin: 20px 0;
            word-break: break-all;
            user-select: all;
        }}
        .footer {{
            margin-top: 24px;
            font-size: 13px;
            color: #6e7681;
            display: flex;
            gap: 16px;
        }}
        a {{
            color: #58a6ff;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="card">
        <h1>KRONOS Core <span class="badge">ONLINE</span></h1>
        <p>Autonomous Windows Systems Administrator & Live TUI Operations Framework.</p>
        <p>Run the command below in <strong>PowerShell</strong> or <strong>Windows Run (Win + R)</strong> on any Windows PC:</p>
        <div class="cmd-box">
            irm {base_url}/kronos | iex
        </div>
        <p style="font-size: 13px; color: #8b949e;">Includes KRONOS Doctor, Turbo Boost, Startup Manager, WinGet, Privacy Debloat, Native Voice Engine, and 12 Responsive TUIs.</p>
        <div class="footer">
            <a href="/health">Health API</a>
            <a href="/docs">API Docs (Swagger)</a>
            <a href="https://github.com/pro-sys17/kronos" target="_blank">GitHub Repository</a>
        </div>
    </div>
</body>
</html>"""

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

