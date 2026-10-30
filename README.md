# KRONOS // Autonomous Windows Co-Pilot & System Restoration Framework

KRONOS is a cloud-powered, offline-resilient autonomous diagnostic and self-healing engine for Windows endpoints. It delivers zero-install, on-demand incident remediation and live terminal operations directly from the Windows Run prompt (`Win + R`) or via global CLI.

Designed with an ultra-clean, minimal terminal aesthetic (zero emojis, responsive layout, Warp/Claude Code inspired).

---

## Key Capabilities

- **Zero-Install Client Bootstrap**: Ephemeral in-memory execution via PowerShell (`irm <url>/kronos | iex`).
- **Global Terminal Command**: 1-click installation (`/install-cli`) enabling typing `kronos` anywhere in CMD, PowerShell, or Windows Terminal.
- **Categorized Hub & Sub-Menus**:
  - `[1] SYSTEM HEALTH & DIAGNOSTICS`: 10-Point Doctor Audit, Hardware & Problem Driver Audit, S.M.A.R.T. Disks Heatmap, Fastfetch Specs.
  - `[2] PERFORMANCE & OPTIMIZATION`: Turbo Boost & Temp Cleaner, Live Task Monitor (Top), Windows Startup & Boot Apps Manager, Power & Battery Schemes.
  - `[3] NETWORK & SECURITY COCKPIT`: Network Radar & Latency, Active Listening Ports Audit, Defender Firewall Cockpit, Privacy & Telemetry Debloat.
  - `[4] APPS, SYSTEM TOOLS & AUDIO`: WinGet Software Updater, Services Manager, Audio Subsystem Deep Reset, Folder Explorer (Tree), Cyber Matrix Stream.
  - `[5] KRONOS AI CO-PILOT & VOICE`: Natural Hinglish/English Chatbot, Native Speech Voice Engine, Global CLI Installer, Safety Rollback Recovery.
- **Full Windows CMD & PowerShell Direct Passthrough**: Execute any CMD command or PowerShell cmdlet (`!ipconfig`, `> Get-Service`, `ping`, `tasklist`, `whoami`) with real-time responsive card formatting and multi-turn context retention.
- **Fail-Safe Rollback Engine**: Automatic service and system state snapshotting prior to change execution.
- **100% Offline-First Architecture**: Loopback internal socket support (`127.0.0.1`), embedded deterministic expert engine, and client-side offline fallbacks.
- **Command Security Guardrail**: Strict AST and pattern-based validation preventing execution of destructive commands (no disk format, no critical file deletion, no obfuscation).
- **Dual-Tier Reasoning**: Real-time Groq / Gemini LLM reasoning with fallback to an embedded Windows SysAdmin rule engine.

---

## Directory Layout

```
kronos/
|-- client/
|   `-- kronos.ps1          # Production client bootstrap & telemetry agent
|-- server/
|   |-- app/
|   |   |-- api/
|   |   |   `-- routes.py   # Bootstrap delivery & diagnosis endpoints
|   |   |-- core/
|   |   |   |-- ai_brain.py # Dual-tier reasoning (Groq/Gemini + Rule engine)
|   |   |   |-- guardrail.py# Security AST & deny-list validator
|   |   |   `-- security.py # Ephemeral session signatures & rate limiting
|   |   `-- main.py         # FastAPI application entry point
|   |-- requirements.txt    # Python dependencies
|   |-- run.py              # Local server launcher
|   `-- .env.example        # Environment variable template
`-- README.md
```

---

## Quick Start (Local Development)

### 1. Launch Server Core
```powershell
cd server
pip install -r requirements.txt
python run.py
```
The server will bind to `http://127.0.0.1:8000`.

### 2. Trigger Client via Run (`Win + R`) or PowerShell
```powershell
powershell -ExecutionPolicy Bypass -Command "irm http://127.0.0.1:8000/kronos | iex"
```

---

## Deployment (Cloud Production)

### Option A: Render.com / Railway
1. Push this repository to GitHub.
2. Link the repository to Render or Railway as a Python Web Service.
3. Root Directory: `server`
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. Add Environment Variables:
   - `GROQ_API_KEY=<your_key>` (optional, ultra-fast LLM)
   - `GEMINI_API_KEY=<your_key>` (optional)

### Option B: Cloudflare Tunnel (Instant Public HTTPS)
```powershell
cloudflared tunnel --url http://127.0.0.1:8000
```
Use the provided HTTPS tunnel URL in `Win + R`:
```powershell
powershell -c "irm https://<tunnel-id>.trycloudflare.com/kronos | iex"
```

---

## Security Guardrails

The server-side AST validator checks every action against `DENY_LIST` patterns:
- Prohibits storage formatters (`format`, `diskpart`).
- Prohibits system file deletion (`C:\Windows`).
- Prohibits shadow copy destruction (`vssadmin delete`).
- Blocks encoded/obfuscated command lines (`-enc`, `-encodedcommand`).
- Enforces explicit operator confirmation prior to executing changes.
