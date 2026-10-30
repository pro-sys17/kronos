import sys
import os
from pathlib import Path

# Add server directory to python path
server_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(server_dir))

try:
    from dotenv import load_dotenv
    load_dotenv(server_dir / ".env")
except ImportError:
    pass

import uvicorn

if __name__ == "__main__":
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8000"))
    print(f"[*] Starting KRONOS Cloud Diagnostic Core on http://{host}:{port}")
    print(f"[*] Bootstrap script endpoint: http://{host}:{port}/kronos")
    print(f"[*] Diagnostic API: http://{host}:{port}/api/v1/diagnose")
    uvicorn.run("app.main:app", host=host, port=port, reload=True, reload_dirs=[str(server_dir)])
