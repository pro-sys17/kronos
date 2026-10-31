MASTER_SYSTEM_INSTRUCTION = r"""# KRONOS — MASTER SYSTEM INSTRUCTIONS

## 1. IDENTITY
You are KRONOS AI Co-Pilot, an advanced Windows System Administrator, Troubleshooting Specialist, and System Recovery Assistant for 'Professor' (or 'bhai').
Your responsibility is to help users understand, diagnose, troubleshoot, optimize, and maintain Windows systems.
You are not a generic chatbot.

You must prioritize:
- Technical accuracy
- Context awareness
- Relevant answers
- Root-cause analysis
- Practical solutions
- Safe system operations
- Result verification

## 2. UNDERSTAND THE USER'S INTENT
Before answering, identify what the user actually wants.
Classify the request into one of these categories:
- General technical question
- Windows troubleshooting
- Network diagnostics
- System performance
- Memory and CPU problems
- Disk and storage problems
- Windows security
- Application errors
- Hardware-related problems
- System recovery
- KRONOS feature explanation
- Follow-up question
- General conversation

Never force every conversation into troubleshooting.
If the user asks what DNS means, explain DNS. Do not automatically generate PowerShell commands.
If the user reports that their internet is not working, begin troubleshooting.

## 3. CONTEXT AWARENESS
You may receive:
- Current user message
- Previous conversation history
- Windows system information
- Diagnostic results
- Available system tools
- Previous troubleshooting steps
- Previous action results

Use all relevant information before responding.
Never ask the user to repeat information already available.
Maintain context across multiple messages.
Do not restart the troubleshooting process from the beginning after every message.

## 4. TECHNICAL ACCURACY
Never invent:
- System specifications
- Diagnostic results
- Error messages
- Windows configurations
- Command execution results
- Network status
- Root causes

Differentiate between:
- Confirmed facts
- Likely causes
- Unverified assumptions

If information is insufficient, ask one specific question or request the relevant diagnostic information.
Do not pretend that you have inspected the user's computer unless actual diagnostic data has been provided.

## 5. TROUBLESHOOTING METHODOLOGY
Follow this workflow:
1. Understand the reported problem.
2. Identify the most likely causes.
3. Check available diagnostic information.
4. Select the smallest relevant diagnostic operation.
5. Analyze the returned result.
6. Identify the root cause where possible.
7. Recommend the appropriate fix.
8. Request confirmation before consequential system modifications.
9. Execute only authorized operations through registered tools.
10. Verify the actual result.

Prefer the least invasive solution.
Do not recommend reinstalling Windows, resetting the PC, or performing destructive operations when a smaller fix is available.

## 6. TOOL USAGE
You can access system capabilities through tools provided by KRONOS.
Use only tools that are explicitly registered and available.
Before selecting a tool:
- Understand what it does.
- Check whether it is relevant.
- Check its required arguments.
- Consider its impact on the system.

Rules:
- Diagnostic operations can run when authorized.
- Modifying configurations requires appropriate authorization.
- Destructive operations require explicit confirmation.
- Never invent tool names or tool results.
- Never claim an operation succeeded without receiving its execution result.
- Verify important modifications after execution.
- If no tool is needed (conceptual explanation, general conversation, or asking clarification), leave "selected_tools": [].
- Do not generate arbitrary executable PowerShell commands as a substitute for registered tools.

## 7. RESPONSE QUALITY
Answer the exact question asked.
Avoid:
- Unnecessary introductions
- Repeating the user's question
- Generic troubleshooting lists
- Irrelevant technical information
- Unnecessary PowerShell commands
- Overly complicated explanations
- Recommending the same failed solution repeatedly

For technical explanations:
1. What happened?
2. Why did it happen?
3. How can it be fixed?

For troubleshooting:
1. Current finding
2. Likely cause
3. Next diagnostic step or fix

Keep responses concise unless detailed explanations are requested.

## 8. CONVERSATION PERSONALITY
Communicate naturally.
Support English and Hinglish seamlessly. (If user asks in Hinglish, reply warmly in natural Hinglish with terms like 'bhai', 'Professor'; if in English, reply in clean professional English).
Adapt your technical depth to the user's understanding.
Explain complicated technical concepts in simple language when necessary.
Never sacrifice technical accuracy to sound confident.
Do not behave like a scripted customer-support bot.

## 9. SPECIAL CASES
- Greetings: Respond naturally. Do not run diagnostics.
- Follow-up questions: Use previous conversation context and previous command outputs.
- Insufficient information: Ask a relevant clarification instead of guessing.
- Failed operations: Analyze the returned error. Do not blindly repeat the same operation.
- Multiple possible causes: Prioritize the most probable cause and test it.
- Unavailable AI provider: Do not fabricate an answer or pretend that AI analysis occurred.
- Dangerous system operations: Do not execute unauthorized or destructive operations.

## 10. CORE PRINCIPLE
Your objective is not to produce the longest answer.
Your objective is to understand the user's actual problem and provide the most accurate, relevant, and actionable solution.
Think like a professional Windows System Administrator.
Respond like an intelligent technical assistant.
Act only through authorized KRONOS capabilities.

## RESPONSE FORMATTING INTELLIGENCE
Always select the most appropriate response format based on the user's query.
Do not force every response into paragraphs or bullet points.

1. TABLE FORMAT: Use tables whenever information involves:
   - Comparisons (e.g. NTFS vs exFAT, TCP vs UDP)
   - Multiple components or specifications
   - Advantages and disadvantages
   - Diagnostic results
   - System configurations
   - Step-by-step comparisons
   - Before/after results
   Example:
   | Component | Status | Details |
   |---|---|---|
   | CPU | Normal | 25% usage |
   | RAM | High | 91% usage |
   | Disk | Normal | 35% usage |

2. BULLET POINTS: Use bullet points ('-') for lists, multiple recommendations, important findings, key takeaways, and troubleshooting observations.
3. NUMBERED STEPS: Use numbered steps ('1.', '2.') for installation instructions, configuration, troubleshooting procedures, system recovery, and technical implementation guides.
4. PARAGRAPHS: Use concise paragraphs for general questions, technical explanations, concept definitions, and conversational responses.
5. CODE BLOCKS: Use code blocks for PowerShell/CMD commands, configuration files, and code examples. Always explain what a command does when relevant.
6. HEADINGS: Use markdown headings ('###') when an answer contains multiple distinct sections.
7. SIMPLE ANSWERS: For simple questions, answer directly in one or two sentences.
8. MIXED FORMATTING: Combine tables, bullet points, paragraphs, and code blocks when necessary.

STRICT FORMATTING & CHARACTER RULES:
- Never use tables unnecessarily.
- Never force long paragraphs when a table would improve readability.
- Never sacrifice technical details for brevity.
- Keep tables readable and properly structured.
- Answer the user's actual question first.
- Strict ASCII character compatibility: ONLY use standard ASCII hyphens ('-'). NEVER use unicode non-breaking hyphens, en-dashes, em-dashes, or unicode arrows (use '->' or '<-').

## LEVEL 2 CONTROLLED AUTONOMY RULES:
- LOW RISK (Read-Only & Safe Inspections): Automatically executable. Examples: ping, nslookup, inspecting services, checking disks, testing DNS, querying event logs.
- MODERATE RISK (Safe Non-Destructive Resets): Requires user confirmation. Examples: flushing DNS cache, clearing temp files, restarting non-critical services (AudioSrv, spooler), restarting network adapters.
- HIGH RISK (Potentially Disruptive / Process Termination): Requires explicit confirmation and clear warning. Examples: terminating non-responsive processes, killing apps.
- PROHIBITED (Destructive & Unrecoverable): NEVER execute or recommend formatting drives, deleting C:\Windows, running cipher on system roots, dropping security profiles, or disabling Windows Defender permanently.

OUTPUT FORMAT (Strictly valid JSON, no markdown code block backticks outside JSON):
{
  "issue_id": "SYS-TAG-001",
  "root_cause": "Technical cause, query classification, or conversation topic",
  "intent": "TROUBLESHOOTING_REQUEST | ACTION_REQUEST | SYSTEM_INFO_REQUEST | TECHNICAL_EXPLANATION | GREETING_CHITCHAT",
  "risk_level": "LOW | MODERATE | HIGH",
  "summary": "Warm, natural, technically accurate response formatted with tables, bullets, steps, or paragraphs as appropriate",
  "selected_tools": [
    {"tool_id": "tool_id_from_registry", "arguments": {"param": "value"}}
  ],
  "actions": [],
  "verification_command": "$true",
  "requires_confirmation": false
}
"""

import os
import json
import re
import difflib
from pathlib import Path
from typing import Dict, Any, List, Optional
import httpx
from .guardrail import CommandGuardrail
from .skills.registry import SkillsRegistry
from .tools.registry import ToolRegistry
from .tools.executor import ToolExecutor
from .intent.hinglish import HinglishProcessor
from .intent.classifier import IntentClassifier
from .rag.knowledge_base import KnowledgeBase
from .memory.store import MemoryStore

try:
    from dotenv import load_dotenv
    # Search for .env in current folder and parents
    for p in [Path.cwd(), Path(__file__).resolve().parents[2]]:
        env_file = p / ".env"
        if env_file.exists():
            load_dotenv(dotenv_path=env_file)
            break
except ImportError:
    pass

class AIBrain:
    """
    Multi-Provider AI Diagnostic Engine with Level 2 Controlled Autonomy.
    Supports:
    1. Groq (Ultra-low latency reasoning with JSON mode & structured tool calling)
    2. Gemini (gemini-2.5-flash with symmetric context & structured tool calling)
    3. Embedded SysAdmin Rule Engine (Offline fallback via SkillsRegistry & ToolExecutor)
    """

    def __init__(self):
        MemoryStore.initialize()
        self._client: Optional[httpx.AsyncClient] = None

    async def get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(timeout=12.0)
        return self._client

    async def close(self):
        if self._client and not self._client.is_closed:
            await self._client.aclose()

    @classmethod
    def build_tools_instruction(cls) -> str:
        schemas = ToolRegistry.get_schemas()
        lines = ["REGISTERED SYSTEM TOOLS (Select tools via 'selected_tools'):"]
        for s in schemas:
            params = ", ".join(f"{p} ({info.get('type', 'string')})" for p, info in s["parameters"].items())
            lines.append(f"- {s['tool_id']} [Risk: {s['risk']}]: {s['description']} | Parameters: {{{params}}}")
        return "\n".join(lines)

    @property
    def groq_api_key(self) -> str:
        return os.getenv("GROQ_API_KEY", "").strip()

    @property
    def gemini_api_key(self) -> str:
        return os.getenv("GEMINI_API_KEY", "").strip()

    @property
    def groq_models(self) -> List[str]:
        custom_model = os.getenv("GROQ_MODEL", "").strip()
        models = []
        if custom_model:
            models.append(custom_model)
        defaults = ["openai/gpt-oss-20b", "openai/gpt-oss-120b", "qwen/qwen3.8-27b"]
        for m in defaults:
            if m not in models:
                models.append(m)
        return models

    def _check_conversational_query(self, problem: str) -> Optional[Dict[str, Any]]:
        """
        Instant conversational handler for greetings, casual chatter, acknowledgements,
        and 'I didn't ask for anything / do nothing' statements.
        Guarantees actions: [] so no unexpected commands are executed.
        """
        p = problem.strip().lower()
        p_clean = re.sub(r'[\?\!\.\,\;\:]', '', p).strip()

        # 1. Statements of not asking for anything or telling bot to stop
        no_action_triggers = [
            "pr mene to kaha hi nahi kuch bhi", "par mene to kaha hi nahi", "mene to kaha hi nahi",
            "mene kuch nahi bola", "mene kab bola", "maine kab bola", "maine kuch nahi kaha",
            "mene kab problem batai", "mene problem kab batai", "mene kab bola problem", "mene kab kaha problem",
            "problem kab batai", "problem kisne batai", "kisine nahi bola", "maine kab problem batai",
            "kuch mat karo", "kuch mat kr", "kuch mat kijiye", "kuch nahi", "nothing",
            "mene to kuch nahi kaha", "mene to kuch bola hi nahi", "kuch mat chhedo",
            "kuch nahi karna", "rehne do", "rehne de", "chhod do", "chhod de", "chhod yaar",
            "mene to kuch bola hi nhi", "mene kuch bola hi nahi", "kuch mat karna"
        ]
        if any(t in p_clean for t in no_action_triggers):
            return {
                "issue_id": "SYS-CONVERSATION",
                "root_cause": "User clarified no action is requested",
                "risk_level": "LOW",
                "risk_color": "CYAN",
                "summary": "Haha arre haan sahi baat hai bhai! Maine kab bola koi problem hai! Mast chill karo, main bilkul shanti se baitha hoon jab tak aap kuch na bolo!",
                "actions": [],
                "verification_command": "$true"
            }

        # 2. Clarifying about a plan / confusion
        plan_confusions = ["plan", "plan kya hai", "kaisa plan", "kya plan", "kaunsa plan", "konsa plan", "plan kyu", "plan kyun"]
        if p_clean in plan_confusions or p_clean.startswith("plan "):
            return {
                "issue_id": "SYS-CONVERSATION",
                "root_cause": "User asking about diagnostic plan",
                "risk_level": "LOW",
                "risk_color": "CYAN",
                "summary": "Koi plan nahi bhai! Main bas ready tha. Jab tak aap koi specific issue na batao ya file open na karne ko kaho, tab tak koi plan nahi chalega. Chill karo!",
                "actions": [],
                "verification_command": "$true"
            }

        # 3. Simple acknowledgements & casual reactions
        acknowledgements = [
            "acha", "accha", "achha", "acha ji", "theek hai", "theek he", "thik hai", "thik he",
            "ok", "okay", "sahi hai", "sahi he", "haa", "haan", "hnn", "hmm", "hmmm", "yes", "yep",
            "badhiya", "nice", "good", "cool", "shukriya", "thanks", "thank you", "dhanyawad",
            "aur batao", "aur", "kya haal", "kaise ho", "oh esa", "oh aisa", "aisa kya", "accha aisa",
            "acha esa", "achha esa", "aisa he kya", "aisa hai", "esa kya", "chill karte he", "chill marte he"
        ]
        if p_clean in acknowledgements:
            replies = {
                "acha": "Haan bhai, batao aage kya chal raha hai?",
                "accha": "Haan bhai, batao aage kya chal raha hai?",
                "theek hai": "Bilkul bhai! Chill karo, jab zaroorat ho batana.",
                "theek he": "Bilkul bhai! Chill karo, jab zaroorat ho batana.",
                "ok": "Ji bhai! Main ready hoon jab bhi kuch kaam ho.",
                "okay": "Ji bhai! Main ready hoon jab bhi kuch kaam ho.",
                "hmm": "Haan bhai, sab badiya?",
                "hmmm": "Haan bhai, sab badiya?",
                "oh esa": "Haan bhai bilkul! Aur sunao, sab badhiya?",
                "oh aisa": "Haan bhai bilkul! Aur sunao, sab badhiya?",
                "aisa kya": "Haan bhai! Koi tension nahi hai.",
                "accha aisa": "Haan bhai bilkul! Mast raho.",
                "chill karte he": "Bilkul bhai, full chill mode ON! Jab koi file ya game chalana ho toh bata dena.",
                "chill marte he": "Bilkul bhai, full chill mode ON! Jab koi file ya game chalana ho toh bata dena."
            }
            reply = replies.get(p_clean, "Haan Professor! Main yahi hoon, mast raho.")
            return {
                "issue_id": "SYS-CONVERSATION",
                "root_cause": "Casual acknowledgement",
                "risk_level": "LOW",
                "risk_color": "CYAN",
                "summary": reply,
                "actions": [],
                "verification_command": "$true"
            }

        # 4. Pure Greetings
        greetings = ["hi", "hello", "hey", "suno", "sun", "are bhai", "bhai", "namaste", "good morning", "good evening", "good afternoon"]
        if p_clean in greetings:
            return {
                "issue_id": "SYS-CONVERSATION",
                "root_cause": "Friendly greeting",
                "risk_level": "LOW",
                "risk_color": "CYAN",
                "summary": "Hi Professor! Kaise ho? Koi bhi file open karni ho, delete karni ho, dhundhni ho ya Windows problem ho toh batao, main ready hoon!",
                "actions": [],
                "verification_command": "$true"
            }

        return None

    def _check_tui_request(self, problem: str) -> Optional[Dict[str, Any]]:
        """
        Intercepts requests for specialized Interactive TUIs (Wi-Fi, Disk, Specs, Task Monitor, Tree, Ports, Audio).
        """
        p = problem.lower().strip()

        if p in ["/doctor", "doctor", "/health", "health", "health check", "system check", "checkup"]:
            return {
                "issue_id": "SYS-TUI-DOCTOR",
                "root_cause": "Request to launch KRONOS System Doctor 10-Point Health Audit",
                "risk_level": "LOW",
                "risk_color": "CYAN",
                "summary": "Launching KRONOS System Doctor 10-Point Health Audit...",
                "actions": [{"description": "Launch Doctor TUI", "command": "Show-DoctorHealthCheckTUI"}],
                "verification_command": "$true"
            }

        if p in ["/boost", "boost", "/clean", "clean", "turbo boost", "clean junk", "clean temp", "free ram"]:
            return {
                "issue_id": "SYS-TUI-BOOST",
                "root_cause": "Request to launch KRONOS Turbo Boost & Junk Cleaner",
                "risk_level": "LOW",
                "risk_color": "GREEN",
                "summary": "Launching KRONOS Turbo Boost & Disk Cleaner...",
                "actions": [{"description": "Launch Turbo Boost TUI", "command": "Show-TurboBoostTUI"}],
                "verification_command": "$true"
            }

        if p in ["/startup", "startup", "/boot", "boot", "startup apps", "boot apps"]:
            return {
                "issue_id": "SYS-TUI-STARTUP",
                "root_cause": "Request to launch Windows Boot & Startup Applications Manager",
                "risk_level": "LOW",
                "risk_color": "CYAN",
                "summary": "Launching Windows Boot & Startup Manager...",
                "actions": [{"description": "Launch Startup Manager TUI", "command": "Show-StartupManagerTUI"}],
                "verification_command": "$true"
            }

        if p in ["/apps", "apps", "/winget", "winget", "software update", "package manager"]:
            return {
                "issue_id": "SYS-TUI-APPS",
                "root_cause": "Request to launch Windows Package & Software Manager",
                "risk_level": "LOW",
                "risk_color": "CYAN",
                "summary": "Launching Windows Package & Software Manager...",
                "actions": [{"description": "Launch App Manager TUI", "command": "Show-AppManagerTUI"}],
                "verification_command": "$true"
            }

        if p in ["/debloat", "debloat", "/privacy", "privacy", "windows debloat", "telemetry off"]:
            return {
                "issue_id": "SYS-TUI-DEBLOAT",
                "root_cause": "Request to launch Windows Privacy & Telemetry Debloat Cockpit",
                "risk_level": "LOW",
                "risk_color": "CYAN",
                "summary": "Launching Windows Privacy & Telemetry Debloat Cockpit...",
                "actions": [{"description": "Launch Privacy Debloat TUI", "command": "Show-PrivacyDebloatTUI"}],
                "verification_command": "$true"
            }

        if p in ["/voice", "voice", "/speak", "speak", "voice mode", "talk"]:
            return {
                "issue_id": "SYS-VOICE-TOGGLE",
                "root_cause": "Request to toggle Native Voice Engine",
                "risk_level": "LOW",
                "risk_color": "GREEN",
                "summary": "Toggling Native Speech Voice Engine...",
                "actions": [{"description": "Toggle Voice Engine", "command": "Toggle-VoiceEngine"}],
                "verification_command": "$true"
            }

        if p in ["/install-cli", "install-cli", "/cli", "cli", "install kronos"]:
            return {
                "issue_id": "SYS-CLI-INSTALL",
                "root_cause": "Request to install Global 'kronos' CLI command",
                "risk_level": "LOW",
                "risk_color": "GREEN",
                "summary": "Installing Global 'kronos' terminal command...",
                "actions": [{"description": "Install Global CLI", "command": "Install-KronosGlobalCLI"}],
                "verification_command": "$true"
            }

        # Fast-path for Battery & Power status
        if any(w in p for w in ["battery report", "battery status", "power plan", "battery health", "battery kitni"]):
            return {
                "issue_id": "SYS-FAST-POWER",
                "root_cause": "Battery and power subsystem query",
                "risk_level": "LOW",
                "risk_color": "GREEN",
                "summary": "Generating battery and power diagnostics. You can also open the live /power TUI dashboard anytime!",
                "actions": [
                    {
                        "description": "Inspect active power scheme and battery health",
                        "command": "powercfg /getactivescheme; Get-CimInstance Win32_Battery -ErrorAction SilentlyContinue | Select-Object EstimatedChargeRemaining, BatteryStatus, EstimatedRunTime | Format-List"
                    }
                ],
                "verification_command": "$true"
            }

        # Fast-path for Firewall Status
        if any(w in p for w in ["firewall status", "firewall check", "firewall profiles", "firewall kaisa he", "firewall on he"]):
            return {
                "issue_id": "SYS-FAST-FIREWALL",
                "root_cause": "Windows Defender Firewall configuration query",
                "risk_level": "LOW",
                "risk_color": "CYAN",
                "summary": "Checking Windows Defender Firewall profile states. You can also launch '/firewall' for the interactive cockpit!",
                "actions": [
                    {
                        "description": "Query active firewall profiles",
                        "command": "Get-NetFirewallProfile | Select-Object Name, Enabled, DefaultInboundAction, DefaultOutboundAction | Format-Table -AutoSize"
                    }
                ],
                "verification_command": "$true"
            }

        # Fast-path for Running Services
        if any(w in p for w in ["services status", "running services", "service list", "services check", "kaunse service"]):
            return {
                "issue_id": "SYS-FAST-SERVICES",
                "root_cause": "Core Windows services audit",
                "risk_level": "LOW",
                "risk_color": "CYAN",
                "summary": "Listing critical running Windows services. Check out '/services' for full interactive scroll and filter control!",
                "actions": [
                    {
                        "description": "Query running core system services",
                        "command": "Get-Service | Where-Object Status -eq 'Running' | Select-Object -First 15 Name, DisplayName, StartType | Format-Table -AutoSize"
                    }
                ],
                "verification_command": "$true"
            }

        # Fast-path for Hardware & Driver health
        if any(w in p for w in ["hardware check", "hardware status", "driver error", "degraded device", "problem hardware", "hardware devices"]):
            return {
                "issue_id": "SYS-FAST-HARDWARE",
                "root_cause": "Hardware device and driver integrity audit",
                "risk_level": "LOW",
                "risk_color": "CYAN",
                "summary": "Auditing hardware devices for error codes or degradation. Launch '/devices' for the complete hardware inventory!",
                "actions": [
                    {
                        "description": "Scan for problem or degraded hardware devices",
                        "command": "$errs = @(Get-PnpDevice -Status Error, Degraded -ErrorAction SilentlyContinue); if ($errs.Count -gt 0) { $errs | Select-Object FriendlyName, InstanceId, Status | Format-Table -AutoSize } else { Write-Host 'All installed hardware devices are HEALTHY.' }"
                    }
                ],
                "verification_command": "$true"
            }

        # Fast-path for IP Address
        if any(w in p for w in ["my ip", "ip address", "ip kya he", "ip batao", "ip check"]):
            return {
                "issue_id": "SYS-FAST-IP",
                "root_cause": "IPv4 network configuration query",
                "risk_level": "LOW",
                "risk_color": "GREEN",
                "summary": "Fetching all active IPv4 addresses and default gateways on your adapters:",
                "actions": [
                    {
                        "description": "Retrieve active IPv4 addresses",
                        "command": "Get-NetIPAddress -AddressFamily IPv4 -ErrorAction SilentlyContinue | Where-Object { $_.IPAddress -notlike '127.*' -and $_.IPAddress -notlike '169.254.*' } | Select-Object InterfaceAlias, IPAddress, PrefixLength | Format-Table -AutoSize"
                    }
                ],
                "verification_command": "$true"
            }
        if p in ["/wifi", "/net", "wifi", "net", "wifi radar"]:
            return {
                "issue_id": "SYS-TUI-NET",
                "root_cause": "Interactive Network & Wi-Fi Latency Radar",
                "risk_level": "LOW",
                "risk_color": "CYAN",
                "summary": "Launching Interactive Network & Wi-Fi Radar TUI...",
                "actions": [{"description": "Launch Network Radar TUI", "command": "Show-NetworkRadarTUI"}],
                "verification_command": "$true"
            }
        if p in ["/disk", "/storage", "disk", "storage", "disk health", "ssd health"]:
            return {
                "issue_id": "SYS-TUI-DISK",
                "root_cause": "Interactive Storage & S.M.A.R.T. Health Map",
                "risk_level": "LOW",
                "risk_color": "CYAN",
                "summary": "Launching Interactive Storage & Health TUI...",
                "actions": [{"description": "Launch Storage Health TUI", "command": "Show-DiskHealthTUI"}],
                "verification_command": "$true"
            }
        if p in ["/specs", "/sys", "specs", "system specs", "fastfetch", "neofetch"]:
            return {
                "issue_id": "SYS-TUI-SPECS",
                "root_cause": "Interactive Windows Architecture & Fastfetch Specs",
                "risk_level": "LOW",
                "risk_color": "CYAN",
                "summary": "Generating Windows Architecture Specs Card...",
                "actions": [{"description": "Launch System Specs TUI", "command": "Show-SystemSpecsTUI"}],
                "verification_command": "$true"
            }
        if p in ["/top", "/task", "top", "task", "task manager"]:
            return {
                "issue_id": "SYS-TUI-TOP",
                "root_cause": "Interactive Live Resource & Task Monitor",
                "risk_level": "LOW",
                "risk_color": "CYAN",
                "summary": "Launching Interactive Live Resource Monitor...",
                "actions": [{"description": "Launch Resource Monitor TUI", "command": "Show-TaskMonitorTUI"}],
                "verification_command": "$true"
            }
        if p in ["/tree", "/folder", "/browse", "/superfile", "/fm", "/yazi", "/ranger", "tree", "superfile"]:
            return {
                "issue_id": "SYS-TUI-TREE",
                "root_cause": "Superfile Dual-Pane Workspace & Live Preview (awesome-tuis)",
                "risk_level": "LOW",
                "risk_color": "CYAN",
                "summary": "Launching Superfile Workspace & Syntax Preview TUI...",
                "actions": [{"description": "Launch Superfile TUI", "command": "Show-FolderNavigatorTUI"}],
                "verification_command": "$true"
            }
        if p in ["/ports", "/netstat", "ports", "netstat", "port audit"]:
            return {
                "issue_id": "SYS-TUI-PORTS",
                "root_cause": "Active Listening Ports & Process Audit",
                "risk_level": "LOW",
                "risk_color": "CYAN",
                "summary": "Inspecting Active Listening Ports...",
                "actions": [{"description": "Launch Port Audit TUI", "command": "Show-PortAuditTUI"}],
                "verification_command": "$true"
            }
        if p in ["/audio", "/sound", "/cava", "cava", "audio tui", "sound visualizer"]:
            return {
                "issue_id": "SYS-TUI-AUDIO",
                "root_cause": "Audio Subsystem & CAVA Real-Time Spectrum Equalizer",
                "risk_level": "LOW",
                "risk_color": "CYAN",
                "summary": "Launching Audio Subsystem & CAVA Spectrum TUI...",
                "actions": [{"description": "Launch Audio TUI", "command": "Show-AudioTUI"}],
                "verification_command": "$true"
            }
        if p in ["/band", "/flow", "/netflow", "/bandwhich", "bandwhich"]:
            return {
                "issue_id": "SYS-TUI-BAND",
                "root_cause": "Process Bandwidth & Socket Flow Analyzer (bandwhich)",
                "risk_level": "LOW",
                "risk_color": "CYAN",
                "summary": "Launching Process Bandwidth & Socket Radar TUI...",
                "actions": [{"description": "Launch Bandwidth Radar TUI", "command": "Show-BandwidthRadarTUI"}],
                "verification_command": "$true"
            }
        if p in ["/dust", "/ncdu", "/treesize", "dust", "ncdu"]:
            return {
                "issue_id": "SYS-TUI-DUST",
                "root_cause": "Disk Usage Treemap & Depth Visualizer (dust/ncdu)",
                "risk_level": "LOW",
                "risk_color": "CYAN",
                "summary": "Launching Disk Treemap & Depth Visualizer TUI...",
                "actions": [{"description": "Launch Dust Treemap TUI", "command": "Show-DustTreemapTUI"}],
                "verification_command": "$true"
            }
        if any(w in p for w in ["/git", "/lazygit", "git", "lazygit", "git status", "repo status", "git log"]):
            return {
                "issue_id": "SYS-TUI-GIT",
                "root_cause": "Git Repository Cockpit & Inspector (lazygit)",
                "risk_level": "LOW",
                "risk_color": "CYAN",
                "summary": "Launching Git Repository Cockpit TUI...",
                "actions": [{"description": "Launch Git Cockpit TUI", "command": "Show-GitCockpitTUI"}],
                "verification_command": "$true"
            }
        if any(w in p for w in ["/matrix", "/cmatrix", "matrix", "cmatrix", "cyber rain", "screensaver", "matrix code"]):
            return {
                "issue_id": "SYS-TUI-MATRIX",
                "root_cause": "Cyber Matrix Stream Screensaver (cmatrix)",
                "risk_level": "LOW",
                "risk_color": "GREEN",
                "summary": "Starting Cyber Matrix Digital Rain Screensaver...",
                "actions": [{"description": "Launch Matrix Screensaver", "command": "Show-MatrixScreensaverTUI"}],
                "verification_command": "$true"
            }
        return None

    def _check_network_control_request(self, problem: str, history: Optional[List[Dict[str, Any]]] = None) -> Optional[Dict[str, Any]]:
        """
        Smart, dynamic network adapter control that inspects physical & tethered adapters
        instead of hardcoding adapter names like 'Wi-Fi'.
        """
        p = problem.lower().strip()

        # Fast-path for Battery & Power status
        if any(w in p for w in ["battery report", "battery status", "power plan", "battery health", "battery kitni"]):
            return {
                "issue_id": "SYS-FAST-POWER",
                "root_cause": "Battery and power subsystem query",
                "risk_level": "LOW",
                "risk_color": "GREEN",
                "summary": "Generating battery and power diagnostics. You can also open the live /power TUI dashboard anytime!",
                "actions": [
                    {
                        "description": "Inspect active power scheme and battery health",
                        "command": "powercfg /getactivescheme; Get-CimInstance Win32_Battery -ErrorAction SilentlyContinue | Select-Object EstimatedChargeRemaining, BatteryStatus, EstimatedRunTime | Format-List"
                    }
                ],
                "verification_command": "$true"
            }

        # Fast-path for Firewall Status
        if any(w in p for w in ["firewall status", "firewall check", "firewall profiles", "firewall kaisa he", "firewall on he"]):
            return {
                "issue_id": "SYS-FAST-FIREWALL",
                "root_cause": "Windows Defender Firewall configuration query",
                "risk_level": "LOW",
                "risk_color": "CYAN",
                "summary": "Checking Windows Defender Firewall profile states. You can also launch '/firewall' for the interactive cockpit!",
                "actions": [
                    {
                        "description": "Query active firewall profiles",
                        "command": "Get-NetFirewallProfile | Select-Object Name, Enabled, DefaultInboundAction, DefaultOutboundAction | Format-Table -AutoSize"
                    }
                ],
                "verification_command": "$true"
            }

        # Fast-path for Running Services
        if any(w in p for w in ["services status", "running services", "service list", "services check", "kaunse service"]):
            return {
                "issue_id": "SYS-FAST-SERVICES",
                "root_cause": "Core Windows services audit",
                "risk_level": "LOW",
                "risk_color": "CYAN",
                "summary": "Listing critical running Windows services. Check out '/services' for full interactive scroll and filter control!",
                "actions": [
                    {
                        "description": "Query running core system services",
                        "command": "Get-Service | Where-Object Status -eq 'Running' | Select-Object -First 15 Name, DisplayName, StartType | Format-Table -AutoSize"
                    }
                ],
                "verification_command": "$true"
            }

        # Fast-path for Hardware & Driver health
        if any(w in p for w in ["hardware check", "hardware status", "driver error", "degraded device", "problem hardware", "hardware devices"]):
            return {
                "issue_id": "SYS-FAST-HARDWARE",
                "root_cause": "Hardware device and driver integrity audit",
                "risk_level": "LOW",
                "risk_color": "CYAN",
                "summary": "Auditing hardware devices for error codes or degradation. Launch '/devices' for the complete hardware inventory!",
                "actions": [
                    {
                        "description": "Scan for problem or degraded hardware devices",
                        "command": "$errs = @(Get-PnpDevice -Status Error, Degraded -ErrorAction SilentlyContinue); if ($errs.Count -gt 0) { $errs | Select-Object FriendlyName, InstanceId, Status | Format-Table -AutoSize } else { Write-Host 'All installed hardware devices are HEALTHY.' }"
                    }
                ],
                "verification_command": "$true"
            }

        # Fast-path for IP Address
        if any(w in p for w in ["my ip", "ip address", "ip kya he", "ip batao", "ip check"]):
            return {
                "issue_id": "SYS-FAST-IP",
                "root_cause": "IPv4 network configuration query",
                "risk_level": "LOW",
                "risk_color": "GREEN",
                "summary": "Fetching all active IPv4 addresses and default gateways on your adapters:",
                "actions": [
                    {
                        "description": "Retrieve active IPv4 addresses",
                        "command": "Get-NetIPAddress -AddressFamily IPv4 -ErrorAction SilentlyContinue | Where-Object { $_.IPAddress -notlike '127.*' -and $_.IPAddress -notlike '169.254.*' } | Select-Object InterfaceAlias, IPAddress, PrefixLength | Format-Table -AutoSize"
                    }
                ],
                "verification_command": "$true"
            }

        is_retry = any(phrase in p for phrase in ["tu hi kr run", "tu hi run kar", "tu run kar", "tu chala", "tu hi chala", "ise run kar", "tu hi kr", "kr run", "run kar"])
        prev_is_net = False
        if is_retry and history:
            for turn in reversed(history[-4:]):
                txt = turn.get("content", "").lower()
                if any(w in txt for w in ["wifi", "wi-fi", "ethernet", "adapter", "internet", "net"]):
                    prev_is_net = True
                    break

        is_turn_off = any(w in p for w in ["band kar", "band kr", "band krdo", "off kar", "off kr", "disable", "turn off", "disconnect", "rok de"]) or (is_retry and prev_is_net)
        is_turn_on = any(w in p for w in ["chalu kar", "chalu kr", "on kar", "on kr", "enable", "turn on", "connect", "start"])
        is_net = any(w in p for w in ["internet", "net", "network", "wifi", "wi-fi", "ethernet", "lan"]) or prev_is_net

        if is_turn_off and is_net:
            if "ethernet" in p and "wifi" not in p and not prev_is_net:
                # Targeted physical Ethernet
                cmd = (
                    '$ad = Get-NetAdapter | Where-Object { $_.InterfaceDescription -match "PCIe|Gigabit|Ethernet|Family Controller|Realtek|Intel" -and $_.Name -notmatch "VMware|Virtual|Loopback" }; '
                    'if ($ad) { $ad | Disable-NetAdapter -Confirm:$false; "[✓] Physical Ethernet adapter ($($ad.Name)) disabled." } else { "[!] Koi physical Ethernet adapter nahi mila." }'
                )
                summary = "Bhai physical Ethernet adapter ko turn off kar rahe hain..."
            else:
                # Wi-Fi or all internet or retry
                cmd = (
                    '$ads = Get-NetAdapter | Where-Object { $_.Status -eq "Up" -and $_.Name -notmatch "VMware|Loopback" }; '
                    'if ($ads) { '
                    '  $names = ($ads | Select-Object -ExpandProperty Name) -join ", "; '
                    '  $ads | Disable-NetAdapter -Confirm:$false; '
                    '  "[✓] Active internet adapters ($names) successfully disabled!" '
                    '} else { '
                    '  "[✓] Pehle se hi saare active internet adapters disabled hain." '
                    '}'
                )
                summary = "Bhai, aapke PC par jo bhi active connection chal raha tha (chaahe Ethernet ho ya Phone USB Tethering), usko disable kar diya hai!"

            return {
                "issue_id": "SYS-NET-OFF",
                "root_cause": "User requested network disconnect",
                "risk_level": "LOW",
                "risk_color": "YELLOW",
                "summary": summary,
                "actions": [{"description": "Disable active internet adapters", "command": cmd}],
                "verification_command": "$true"
            }

        if is_turn_on and is_net:
            cmd = (
                '$ads = Get-NetAdapter | Where-Object { $_.Name -notmatch "VMware|Loopback" }; '
                '$ads | Enable-NetAdapter -Confirm:$false; '
                '"[✓] Network adapters re-enabled: " + (($ads | Select-Object -ExpandProperty Name) -join ", ")'
            )
            return {
                "issue_id": "SYS-NET-ON",
                "root_cause": "User requested network enable",
                "risk_level": "LOW",
                "risk_color": "GREEN",
                "summary": "Bhai network adapters ko wapas enable (chalu) kar rahe hain...",
                "actions": [{"description": "Enable all network adapters", "command": cmd}],
                "verification_command": "$true"
            }

        return None

    def _check_kill_request(self, problem: str) -> Optional[Dict[str, Any]]:
        """
        Instant process & application killer handler.
        Detects requests like 'everything app ko kill karna he', 'chrome close kar', 'taskkill notepad'.
        """
        p = problem.lower().strip()
        is_kill = (
            any(re.search(rf'\b{kv}\b', p) for kv in ["kill", "terminate", "close", "taskkill"])
            or any(ph in p for ph in ["band kar", "band kr", "band karo", "band krdo", "hata do", "hata de", "end task", "rok do", "rok de"])
        )
        if not is_kill:
            return None

        # If user is asking a question, advice, or diagnosis (e.g., 'kaun sa process band karu?'):
        if any(w in p for w in ["kaun", "which", "kisko", "kise", "what", "kaise", "how", "?", "suggest", "advice", "batao", "bata"]):
            return None

        # Exclude wifi/ethernet network turning off (handled by _check_network_control_request)
        if any(w in p for w in ["wifi", "wi-fi", "ethernet", "internet", "net", "adapter", "ram", "cpu", "disk", "usage", "%"]):
            return None

        # Extract process target
        clean = problem
        quoted = re.findall(r'"([^"]+)"', problem) or re.findall(r"'([^']+)'", problem)
        if quoted:
            target = quoted[0].strip()
        else:
            m_naam = re.search(r'([a-zA-Z0-9_\-\.]+)\s+(?:naam|wali)\s+(?:ki\s+)?(?:ek\s+)?(?:app|process|program)', problem, re.IGNORECASE)
            if m_naam:
                target = m_naam.group(1).strip()
            else:
                m_ko = re.search(r'([a-zA-Z0-9_\-\.]+)\s+ko\s+(?:kill|band|close)', problem, re.IGNORECASE)
                if m_ko:
                    target = m_ko.group(1).strip()
                else:
                    words_to_strip = [
                        "mujhe", "naam", "ki", "ek", "app", "application", "software", "program", "ko",
                        "kill", "karna", "krna", "he", "hai", "karo", "krdo", "kar", "kr", "de", "do",
                        "jo", "foreground", "background", "me", "par", "pe", "open", "chal", "rahi", "raha",
                        "please", "plz", "zara", "bhai", "task", "process", "close", "terminate", "band"
                    ]
                    for sw in words_to_strip:
                        clean = re.sub(rf'\b{sw}\b', ' ', clean, flags=re.IGNORECASE)
                    candidates = clean.split()
                    target = candidates[0].strip() if candidates else None

        if not target or len(target) < 2 or target.lower() in ["ye", "wo", "ise", "isko", "usko", "sab", "sare", "ram", "cpu", "disk", "system", "pc", "laptop", "computer", "process", "usage"]:
            return None

        clean_target = target.replace("'", "").replace('"', "").replace("*", "").replace("?", "").strip()
        ps_cmd = (
            f"$procs = @(Get-Process -Name '*{clean_target}*' -ErrorAction SilentlyContinue); "
            f"if ($procs.Count -gt 0) {{ "
            f"  foreach ($pr in $procs) {{ Stop-Process -Id $pr.Id -Force -ErrorAction SilentlyContinue }}; "
            f"  \"[✓] Successfully terminated $($procs.Count) process(es) matching '{clean_target}'.\" "
            f"}} else {{ "
            f"  \"[!] No running process matched '{clean_target}'.\" "
            f"}}"
        )

        return {
            "issue_id": "SYS-PROCESS-KILL",
            "root_cause": f"User requested process termination for '{clean_target}'",
            "risk_level": "LOW",
            "risk_color": "YELLOW",
            "summary": f"'{clean_target}' process ko terminate kiya ja raha hai...",
            "actions": [
                {
                    "description": f"Terminate running processes matching '{clean_target}'",
                    "command": ps_cmd
                }
            ],
            "verification_command": "$true"
        }

    def _check_open_request(self, problem: str, last_output: Optional[str] = None, history: Optional[List[Dict[str, Any]]] = None) -> Optional[Dict[str, Any]]:
        """
        Universal Instant File & Folder Opener Engine with Semantic Intent, Typo Tolerance & List-Awareness.
        Searches recent command outputs (last_output), storage drives, and shortcuts.
        """
        p = problem.lower().strip()

        # Absolute kill/terminate exclusion guard:
        if any(re.search(rf'\b{kv}\b', p) for kv in ["kill", "terminate", "close", "taskkill"]):
            return None
        if any(phrase in p for phrase in ["band kar", "band kr", "band karo", "band krdo", "hata do", "hata de", "end task", "rok do", "rok de"]):
            return None

        # Check if "open" is only used as a state adjective ("open he", "open hai", "open tha")
        p_no_state = re.sub(r'\bopen\s+(he|hai|tha|raha|hona|karega)\b', ' ', p)
        if "open" in p and "open" not in p_no_state and not p.startswith("/open "):
            return None

        # STRICT GUARD: Never treat system inspection, telemetry, ports, services, processes, hardware as file-open requests!
        system_info_keywords = [
            "port", "ports", "service", "services", "ip", "adapter", "adapters", "wifi", "wi-fi",
            "ethernet", "network", "netstat", "disk", "storage", "smart", "specs", "cpu", "ram",
            "memory", "hardware", "firewall", "battery", "power", "process", "processes", "task",
            "tasks", "driver", "drivers", "logs", "events", "error", "errors", "registry",
            "connection", "connections", "ping", "dns", "uptime", "temp", "temperature", "chkdsk", "sfc", "dism"
        ]
        if any(re.search(rf'\b{kw}\b', p) for kw in system_info_keywords):
            return None

        # Informational request words ("dikhao", "batao", "show", "list", "status") without explicit file/app words must never open files
        info_query_words = ["dikhao", "batao", "show", "kaunse", "kya", "list", "status", "check", "scan"]
        file_app_indicators = ["file", "folder", "directory", "video", "movie", "song", "audio", "image", "photo", "game", ".exe", ".pdf", ".mp4", ".mkv", ".png", ".jpg", ".txt"]
        if any(w in p for w in info_query_words) and not any(w in p for w in file_app_indicators) and not p.startswith("/open "):
            return None

        if p.startswith("/open "):
            p = "open " + p[6:].strip()
            problem = "open " + problem[6:].strip()
        # Exclude conversational command execution requests
        cmd_execution_phrases = [
            "tu hi kr run", "tu hi run kar", "tu run kar", "run kar", "run karo", "run kr", "run krdo",
            "tu chala", "command chala", "command run", "ise run kar", "execute kar", "chal na", "chala de",
            "run it", "you run it", "run this", "execute this", "kaha hua", "hua kya", "kuch nahi hua", "kuch nhi hua",
            "kya hua", "hua hi nahi", "hua nhi", "chalu nahi hua", "band nahi hua", "off nahi hua"
        ]
        if any(cp in p for cp in cmd_execution_phrases):
            return None

        is_list_ref = any(phrase in p for phrase in ["list me he", "list me to he", "list me hai", "list me to hai", "list me dekho", "dikh to raha he", "dikh to raha hai", "samne to he", "samne to hai", "list me"])
        open_verbs = ["open", "kholo", "launch", "start", "chalao", "play", "run"]
        if not any(v in p for v in open_verbs) and not is_list_ref:
            return None

        # Exclude conversational questions about associations
        if any(w in p for w in ["open ho rahi he", "open hoti he", "kyun open", "default app", "association", "setting"]):
            return None

        # Semantic media & file type hints
        hint = None
        is_game = any(w in p for w in ["game", "khel"])
        if is_game:
            hint = "game"
        elif any(w in p for w in ["movie", "video", "film", "clip"]):
            hint = "video"
        elif any(w in p for w in ["song", "music", "audio", "mp3", "gaana", "track"]):
            hint = "audio"
        elif any(w in p for w in ["image", "photo", "pic", "picture", "wallpaper"]):
            hint = "image"
        elif any(w in p for w in ["folder", "directory"]):
            hint = "folder"

        # Detect target app
        app_exe = None
        app_name = None
        if "vlc" in p:
            app_exe = r"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe"
            app_name = "VLC"
            if not hint:
                hint = "video"
        elif "void" in p or "voidimageviewer" in p:
            app_exe = r"C:\Program Files\voidImageViewer\voidImageViewer.exe"
            app_name = "voidImageViewer"
            if not hint:
                hint = "image"
        elif "faststone" in p or "fscapture" in p:
            app_exe = r"C:\Program Files (x86)\FastStone Capture\FSCapture.exe"
            app_name = "FastStone"
            if not hint:
                hint = "image"
        elif "notepad" in p and any(w in p for w in [".txt", ".log", ".py", ".json", ".ini", "file"]):
            app_exe = "notepad.exe"
            app_name = "Notepad"
        elif "paint" in p and any(w in p for w in [".jpg", ".png", ".jpeg", ".bmp", "image"]):
            app_exe = "mspaint.exe"
            app_name = "Paint"
            if not hint:
                hint = "image"

        # Extract target item with full multi-word phrase and Hindi filler filtering
        clean = problem
        words_to_strip = [
            "open", "kholo", "launch", "start", "view", "dikhao", "play", "run", "chalao",
            "sun", "bhai", "are", "yaar", "yr", "zara", "ek", "tu", "be", "plz", "please",
            "honi", "chahiye", "sari", "sare", "sab", "kardo", "kar do", "karo", "krdo",
            "in", "with", "me", "pe", "par", "ko", "se", "ke", "ki", "ka", "ye", "wo", "to",
            "bosdike", "bhosdike", "list", "hai", "he", "dikh", "raha", "samne",
            "movie", "video", "film", "game", "song", "music", "audio", "file", "folder", "image", "photo"
        ]
        for v in words_to_strip:
            clean = re.sub(rf'\b{v}\b', ' ', clean, flags=re.IGNORECASE)
        if app_name:
            clean = re.sub(rf'\b{app_name}\b', ' ', clean, flags=re.IGNORECASE)
            clean = re.sub(r'\bvlc\b', ' ', clean, flags=re.IGNORECASE)
            clean = re.sub(r'\bvoidimageviewer\b', ' ', clean, flags=re.IGNORECASE)
            clean = re.sub(r'\bfaststone\b', ' ', clean, flags=re.IGNORECASE)

        quoted = re.findall(r'["\']([^"\']+)["\']', problem)
        if quoted:
            target = quoted[0].strip()
        else:
            stop_candidates = ["the", "a", "an", "is", "ki", "ka", "ke", "ko", "se", "me", "pe", "par", "ye", "wo", "to", "bhi"]
            candidates = [c.strip() for c in clean.split() if len(c.strip()) > 0 and c.strip().lower() not in stop_candidates]
            target = " ".join(candidates).strip() if candidates else None
        if target:
            target_clean = target.lower().strip()
            if len(target_clean) <= 2 or target_clean in ["kr", "hi", "tu", "kar", "karo", "run", "chala", "bhi", "na", "to", "ye", "wo", "kuch", "apne", "aap"]:
                return None

        # Resolve target from history if user is referring to the list output
        if (not target or is_list_ref) and history:
            for turn in reversed(history):
                if turn.get("role") == "user":
                    prev_txt = turn.get("content", "")
                    m_prev = re.findall(r'["\']([^"\']+)["\']', prev_txt)
                    if m_prev:
                        target = m_prev[0].strip()
                        break
                    p_clean = prev_txt
                    for w_s in ["open", "kholo", "folder", "file", "drive", "list"]:
                        p_clean = re.sub(rf'\b{w_s}\b', ' ', p_clean, flags=re.IGNORECASE)
                    cands = [w.strip() for w in p_clean.split() if len(w.strip()) > 2]
                    if cands:
                        target = cands[-1].strip()
                        break

        # Check last_output directly for immediate 0ms match with spaces and fuzzy typo tolerance
        if last_output:
            paths = []
            for line in last_output.splitlines():
                line_str = line.strip()
                if re.match(r'^[a-zA-Z]:\\', line_str):
                    parts = re.split(r'\s{3,}', line_str)
                    if parts and parts[0]:
                        paths.append(parts[0].strip())
                else:
                    found_inline = re.findall(r'[a-zA-Z]:\\[^\r\n\t]+', line_str)
                    for inline_p in found_inline:
                        clean_inline = re.split(r'\s{3,}|\s+\(', inline_p)[0].strip()
                        if clean_inline and clean_inline not in paths:
                            paths.append(clean_inline)

            # Check if user requested by ordinal number (e.g. 1st, 2nd, pehli, dusri, last)
            ord_map = {
                '1st': 0, 'first': 0, 'pehli': 0, 'pehla': 0, 'pehle': 0, '1': 0,
                '2nd': 1, 'second': 1, 'dusri': 1, 'dusra': 1, 'dusre': 1, '2': 1,
                '3rd': 2, 'third': 2, 'teesri': 2, 'teesra': 2, 'teesre': 2, '3': 2,
                '4th': 3, 'fourth': 3, 'chauthi': 3, 'chautha': 3, 'chauthe': 3, '4': 3,
                '5th': 4, 'fifth': 4, 'panchwi': 4, 'panchwa': 4, 'panchwe': 4, '5': 4,
                'last': -1, 'aakhri': -1, 'akhri': -1
            }
            ord_idx = None
            p_words = p.split()
            for k, v in ord_map.items():
                if k in p_words:
                    ord_idx = v
                    break

            best_match = None
            if ord_idx is not None and paths:
                if ord_idx < len(paths) and (ord_idx >= 0 or ord_idx == -1):
                    best_match = paths[ord_idx]
            elif target and paths:
                best_ratio = 0.0
                search_k = target.lower()
                for p_str in paths:
                    base = os.path.basename(p_str.rstrip("\\")).lower()
                    ratio = difflib.SequenceMatcher(None, search_k, base).ratio()
                    if search_k in base or base in search_k:
                        ratio = max(ratio, 0.85)
                    if ratio > best_ratio:
                        best_ratio = ratio
                        best_match = p_str
                if best_ratio < 0.65:
                    best_match = None

            if best_match:
                clean_match = best_match.replace("'", "''")
                launch = (
                    f"$target = '{clean_match}'; "
                    "if ($target -match '\\.\\.\\.$') { "
                    "  $prefix = $target -replace '\\.\\.\\.$', '*'; "
                    "  $realItem = Get-ChildItem -Path $prefix -ErrorAction SilentlyContinue | Select-Object -First 1; "
                    "  if ($realItem) { $target = $realItem.FullName } "
                    "}; "
                    "if (Test-Path $target) { "
                    "  if ((Get-Item $target).PSIsContainer) { Start-Process explorer.exe $target } else { Start-Process $target }; "
                    "  \"Opened: $target\" "
                    "} else { "
                    "  Start-Process $target; \"Opened: $target\" "
                    "}"
                )
                return {
                    "issue_id": "SYS-FAST-OPEN-LIST",
                    "root_cause": f"Matched item '{best_match}' from recent list output",
                    "risk_level": "LOW",
                    "risk_color": "CYAN",
                    "summary": f"Arre haan bhai, list me mil gaya! '{os.path.basename(best_match)}' open kar diya.",
                    "actions": [
                        {
                            "description": f"Open {best_match}",
                            "command": launch
                        }
                    ],
                    "verification_command": "$true"
                }

        if not target or target.lower() in ["again", "use", "ise"]:
            return None

        clean_target = target.replace("'", "''")
        if app_exe:
            launch_code = f"Start-Process '{app_exe}' -ArgumentList ('\"' + $found.FullName + '\"'); \"Launched in {app_name}: $($found.FullName)\""
        else:
            launch_code = "if ($found.PSIsContainer) { Start-Process explorer.exe -ArgumentList ('\"' + $found.FullName + '\"') } else { Start-Process ('\"' + $found.FullName + '\"') }; \"Opened: $($found.FullName)\""

        ps_cmd = (
            f"$target = '{clean_target}'; "
            f"$hint = '{hint or ''}'; "
            f"$appName = '{app_name or ''}'; "
            f"$isGame = {'$true' if is_game else '$false'}; "
            "# 1. Tier 1 Check: Installed Application or Desktop/Start-Menu Shortcut\n"
            "$appMap = @{ 'idm' = 'Internet Download Manager'; 'vlc' = 'VLC media player'; 'chrome' = 'Google Chrome'; 'code' = 'Visual Studio Code'; 'vscode' = 'Visual Studio Code'; 'voidimageviewer' = 'void Image Viewer'; 'faststone' = 'FastStone Capture'; 'ldplayer' = 'LDPlayer'; 'photoshop' = 'Photoshop' }; "
            "$appSearch = if ($appMap.ContainsKey($target.ToLower())) { $appMap[$target.ToLower()] } else { $target }; "
            "$shortcutDirs = @(\"$env:USERPROFILE\\Desktop\", \"C:\\Users\\Public\\Desktop\", \"$env:APPDATA\\Microsoft\\Windows\\Start Menu\\Programs\", \"$env:ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\"); "
            "$appFound = $null; "
            "foreach ($sd in $shortcutDirs) { if (Test-Path $sd) { "
            "  $lnk = Get-ChildItem -Path $sd -Recurse -Filter \"*$appSearch*.lnk\" -ErrorAction SilentlyContinue | Where-Object { $_.Name -notmatch '(?i)(uninstall|help|update)' } | Select-Object -First 1; "
            "  if ($lnk) { $appFound = $lnk.FullName; break } "
            "} }; "
            "if ($appFound -and -not $isGame) { "
            "  Start-Process $appFound; "
            "  \"Launched Application: $([System.IO.Path]::GetFileNameWithoutExtension($appFound))\"; return "
            "}; "
            "# 2. Tier 2 Check: Game Folder and Main Executable\n"
            "if ($isGame) { "
            "  $firstWord = ($target -split '\\s+')[0]; "
            "  $compact = $target -replace '\\s+', ''; "
            "  $gameDirs = @('D:\\', 'C:\\Program Files', 'C:\\Program Files (x86)', \"$env:USERPROFILE\\Desktop\"); "
            "  $foundGame = $null; "
            "  foreach ($gd in $gameDirs) { if (Test-Path $gd) { "
            "    $gFolder = Get-ChildItem -Path $gd -Directory -ErrorAction SilentlyContinue | Where-Object { $_.Name -match \"(?i)$compact\" -or $_.Name -match \"(?i)$firstWord\" } | Select-Object -First 1; "
            "    if ($gFolder) { "
            "      $mainExe = Get-ChildItem -Path $gFolder.FullName -Recurse -Depth 4 -Filter '*.exe' -ErrorAction SilentlyContinue | Where-Object { $_.Name -notmatch '(?i)(unins|setup|redist|dxweb|vcredist|crash|report|updater|dotNet)' } | Select-Object -First 1; "
            "      if ($mainExe) { $foundGame = $mainExe.FullName; break } "
            "    } "
            "  } }; "
            "  if ($foundGame) { Start-Process $foundGame; \"Launched Game: $(Split-Path $foundGame -Leaf)\"; return } "
            "}; "
            "# 3. Tier 3: Search Files and Media with Multi-Word Keyword Matching\n"
            "$dirs = @([Environment]::GetFolderPath('Desktop'), [Environment]::GetFolderPath('MyDocuments'), (Join-Path $env:USERPROFILE 'Downloads'), (Join-Path $env:USERPROFILE 'Videos'), (Join-Path $env:USERPROFILE 'Pictures'), $env:USERPROFILE); "
            "Get-PSDrive -PSProvider FileSystem | Where-Object { $_.Root -ne 'C:\\' -and $_.Free -gt 0 } | ForEach-Object { $dirs += $_.Root }; "
            "$videoExts = @('.mkv', '.mp4', '.avi', '.mov', '.wmv', '.webm', '.flv'); "
            "$imageExts = @('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp'); "
            "$textExts  = @('.txt', '.log', '.py', '.json', '.ini', '.csv', '.md'); "
            "$keywords = ($target -split '\\s+') | Where-Object { $_.Length -gt 1 }; "
            "$candidates = @(); "
            "foreach ($d in $dirs) { if (Test-Path $d) { "
            "  $items = Get-ChildItem -Path $d -Attributes !ReparsePoint -ErrorAction SilentlyContinue | Where-Object { $_.FullName -notmatch '(node_modules|\\.git|\\.gradle|\\.vscode|AppData)' }; "
            "  if ($items) { $candidates += $items }; "
            "  $subItems = Get-ChildItem -Path $d -Recurse -Depth 3 -Attributes !ReparsePoint -ErrorAction SilentlyContinue | Where-Object { $_.FullName -notmatch '(node_modules|\\.git|\\.gradle|\\.vscode|AppData)' }; "
            "  if ($subItems) { $candidates += $subItems } "
            "} }; "
            "$scored = foreach ($item in $candidates) { "
            "  $score = 0; $name = $item.Name.ToLower(); $ext = $item.Extension.ToLower(); "
            "  if ($name -eq $target.ToLower()) { $score += 200 } "
            "  elseif ($item.BaseName.ToLower() -eq $target.ToLower()) { $score += 150 } "
            "  elseif ($name -match \"(?i)\\b$target\\b\") { $score += 80 } "
            "  elseif ($name -match \"(?i)^$target\") { $score += 40 } "
            "  elseif ($name -match \"(?i)$target\") { $score += 20 }; "
            "  $matchCount = 0; "
            "  foreach ($kw in $keywords) { if ($name -match \"(?i)\\b$kw\\b\" -or $name -like \"*$kw*\") { $matchCount++ } }; "
            "  if ($matchCount -eq 0 -and $name.Length -ge 4 -and $target.Length -ge 4) { "
            "    $triMatch = 0; $maxTri = $target.Length - 2; "
            "    for ($k = 0; $k -le ($target.Length - 3); $k++) { "
            "      $sub = $target.Substring($k, 3); "
            "      if ($name -like \"*$sub*\") { $triMatch++ } "
            "    }; "
            "    if ($maxTri -gt 0 -and ($triMatch / $maxTri) -ge 0.5) { "
            "      $score += 70; $matchCount++ "
            "    } "
            "  }; "
            "  if ($matchCount -gt 0) { "
            "    $score += ($matchCount * 30); "
            "    if ($isGame) { "
            "      if (@('.zip', '.rar', '.iso', '.7z', '.mp3') -contains $ext) { $score -= 200 } "
            "      elseif (@('.exe', '.lnk') -contains $ext) { $score += 150 } "
            "    } elseif ($hint -eq 'video' -or $appName -eq 'VLC') { "
            "      if ($videoExts -contains $ext) { $score += 100 } else { $score -= 50 } "
            "    } elseif ($hint -eq 'image' -or $appName -in @('voidImageViewer', 'FastStone')) { "
            "      if ($imageExts -contains $ext) { $score += 100 } else { $score -= 50 } "
            "    } elseif ($hint -eq 'folder') { "
            "      if ($item.PSIsContainer) { $score += 100 } "
            "    }; "
            "    [PSCustomObject]@{ Item = $item; Score = $score } "
            "  } "
            "}; "
            "$best = $scored | Sort-Object Score -Descending | Select-Object -First 1; "
            "if ($best -and $best.Score -gt 0) { "
            "  $found = $best.Item; "
            f"  {launch_code} "
            "} else { "
            f"  \"Could not find '{clean_target}' in storage drives.\" "
            "}"
        )

        display_name = f"'{target}'" + (f" ({hint})" if hint else "") + (f" with {app_name}" if app_name else "")
        return {
            "issue_id": "SYS-FAST-OPEN",
            "root_cause": f"Semantic autonomous locator and launcher for {display_name}",
            "risk_level": "LOW",
            "risk_color": "CYAN",
            "summary": f"Locating and opening {display_name}",
            "actions": [
                {
                    "description": f"Locate and launch {display_name}",
                    "command": ps_cmd
                }
            ],
            "verification_command": "$true"
        }

    def _check_delete_request(self, problem: str) -> Optional[Dict[str, Any]]:
        """
        Universal Safe File & Folder Deleter Engine.
        Locates target across storage, but enforces CRITICAL risk level
        so client strictly requires user confirmation (y/N) before deleting.
        """
        p = problem.lower().strip()

        # Fast-path for Battery & Power status
        if any(w in p for w in ["battery report", "battery status", "power plan", "battery health", "battery kitni"]):
            return {
                "issue_id": "SYS-FAST-POWER",
                "root_cause": "Battery and power subsystem query",
                "risk_level": "LOW",
                "risk_color": "GREEN",
                "summary": "Generating battery and power diagnostics. You can also open the live /power TUI dashboard anytime!",
                "actions": [
                    {
                        "description": "Inspect active power scheme and battery health",
                        "command": "powercfg /getactivescheme; Get-CimInstance Win32_Battery -ErrorAction SilentlyContinue | Select-Object EstimatedChargeRemaining, BatteryStatus, EstimatedRunTime | Format-List"
                    }
                ],
                "verification_command": "$true"
            }

        # Fast-path for Firewall Status
        if any(w in p for w in ["firewall status", "firewall check", "firewall profiles", "firewall kaisa he", "firewall on he"]):
            return {
                "issue_id": "SYS-FAST-FIREWALL",
                "root_cause": "Windows Defender Firewall configuration query",
                "risk_level": "LOW",
                "risk_color": "CYAN",
                "summary": "Checking Windows Defender Firewall profile states. You can also launch '/firewall' for the interactive cockpit!",
                "actions": [
                    {
                        "description": "Query active firewall profiles",
                        "command": "Get-NetFirewallProfile | Select-Object Name, Enabled, DefaultInboundAction, DefaultOutboundAction | Format-Table -AutoSize"
                    }
                ],
                "verification_command": "$true"
            }

        # Fast-path for Running Services
        if any(w in p for w in ["services status", "running services", "service list", "services check", "kaunse service"]):
            return {
                "issue_id": "SYS-FAST-SERVICES",
                "root_cause": "Core Windows services audit",
                "risk_level": "LOW",
                "risk_color": "CYAN",
                "summary": "Listing critical running Windows services. Check out '/services' for full interactive scroll and filter control!",
                "actions": [
                    {
                        "description": "Query running core system services",
                        "command": "Get-Service | Where-Object Status -eq 'Running' | Select-Object -First 15 Name, DisplayName, StartType | Format-Table -AutoSize"
                    }
                ],
                "verification_command": "$true"
            }

        # Fast-path for Hardware & Driver health
        if any(w in p for w in ["hardware check", "hardware status", "driver error", "degraded device", "problem hardware", "hardware devices"]):
            return {
                "issue_id": "SYS-FAST-HARDWARE",
                "root_cause": "Hardware device and driver integrity audit",
                "risk_level": "LOW",
                "risk_color": "CYAN",
                "summary": "Auditing hardware devices for error codes or degradation. Launch '/devices' for the complete hardware inventory!",
                "actions": [
                    {
                        "description": "Scan for problem or degraded hardware devices",
                        "command": "$errs = @(Get-PnpDevice -Status Error, Degraded -ErrorAction SilentlyContinue); if ($errs.Count -gt 0) { $errs | Select-Object FriendlyName, InstanceId, Status | Format-Table -AutoSize } else { Write-Host 'All installed hardware devices are HEALTHY.' }"
                    }
                ],
                "verification_command": "$true"
            }

        # Fast-path for IP Address
        if any(w in p for w in ["my ip", "ip address", "ip kya he", "ip batao", "ip check"]):
            return {
                "issue_id": "SYS-FAST-IP",
                "root_cause": "IPv4 network configuration query",
                "risk_level": "LOW",
                "risk_color": "GREEN",
                "summary": "Fetching all active IPv4 addresses and default gateways on your adapters:",
                "actions": [
                    {
                        "description": "Retrieve active IPv4 addresses",
                        "command": "Get-NetIPAddress -AddressFamily IPv4 -ErrorAction SilentlyContinue | Where-Object { $_.IPAddress -notlike '127.*' -and $_.IPAddress -notlike '169.254.*' } | Select-Object InterfaceAlias, IPAddress, PrefixLength | Format-Table -AutoSize"
                    }
                ],
                "verification_command": "$true"
            }
        if p.startswith("/del "):
            p = "delete " + p[5:].strip()
            problem = "delete " + problem[5:].strip()
        elif p.startswith("/delete "):
            p = "delete " + p[8:].strip()
            problem = "delete " + problem[8:].strip()
        del_verbs = ["delete", "remove", "hata do", "hata de", "uda do", "uda de", "delete kardo", "delete kar do", "delete kr do", "delete krde"]
        if not any(v in p for v in del_verbs):
            return None

        clean = problem
        for v in ["delete", "remove", "hata", "uda", "do", "de", "kardo", "kar", "kr", "krdo", "krde", "please", "bhai", "file", "folder", "wali", "wala"]:
            clean = re.sub(rf'\b{v}\b', ' ', clean, flags=re.IGNORECASE)

        quoted = re.findall(r'["\']([^"\']+)["\']', problem)
        if quoted:
            target = quoted[0].strip()
        else:
            stop_candidates = ["the", "a", "an", "is", "ki", "ka", "ke", "ko", "se", "me", "pe", "par", "ye", "wo", "to", "bhi"]
            candidates = [c.strip() for c in clean.split() if len(c.strip()) > 0 and c.strip().lower() not in stop_candidates]
            target = " ".join(candidates).strip() if candidates else None
        if target:
            target_clean = target.lower().strip()
            if len(target_clean) <= 2 or target_clean in ["kr", "hi", "tu", "kar", "karo", "run", "chala", "bhi", "na", "to", "ye", "wo", "kuch", "apne", "aap"]:
                return None

        if not target:
            return None

        clean_target = target.replace("'", "''")
        ps_cmd = (
            f"$target = '{clean_target}'; "
            "$dirs = @([Environment]::GetFolderPath('Desktop'), [Environment]::GetFolderPath('MyDocuments'), (Join-Path $env:USERPROFILE 'Downloads'), (Join-Path $env:USERPROFILE 'Pictures'), (Join-Path $env:USERPROFILE 'Videos'), $env:USERPROFILE); "
            "Get-PSDrive -PSProvider FileSystem | Where-Object { $_.Root -ne 'C:\\' -and $_.Free -gt 0 } | ForEach-Object { $dirs += $_.Root }; "
            "$found = $null; "
            "foreach ($d in $dirs) { if (Test-Path $d) { "
            "  $item = Get-ChildItem -Path $d -Attributes !ReparsePoint -ErrorAction SilentlyContinue | Where-Object { $_.FullName -notmatch '(node_modules|\\.git|\\.gradle|\\.vscode|AppData)' -and ($_.Name -like \"*$target*\" -or $_.BaseName -eq $target) } | Select-Object -First 1; "
            "  if ($item) { $found = $item; break }; "
            "  $item = Get-ChildItem -Path $d -Recurse -Depth 4 -Attributes !ReparsePoint -ErrorAction SilentlyContinue | Where-Object { $_.FullName -notmatch '(node_modules|\\.git|\\.gradle|\\.vscode|AppData)' -and ($_.Name -like \"*$target*\" -or $_.BaseName -eq $target) } | Select-Object -First 1; "
            "  if ($item) { $found = $item; break } "
            "} }; "
            "if ($found) { "
            "  $delPath = $found.FullName; "
            "  Remove-Item -LiteralPath $delPath -Recurse -Force -ErrorAction SilentlyContinue; "
            "  \"[DELETED] Successfully removed: $delPath\" "
            "} else { "
            f"  \"Could not find '{clean_target}' to delete.\" "
            "}"
        )

        return {
            "issue_id": "SYS-FAST-DELETE",
            "root_cause": f"User requested deletion of '{target}'",
            "risk_level": "CRITICAL",
            "risk_color": "RED",
            "summary": f"Permanently delete '{target}' from storage",
            "actions": [
                {
                    "description": f"Delete '{target}' from filesystem",
                    "command": ps_cmd
                }
            ],
            "verification_command": "$true"
        }

    def _check_find_request(self, problem: str) -> Optional[Dict[str, Any]]:
        """
        Universal Storage Search Engine (All Storage Drives & User Profiles).
        Instantly searches across C:, D:, E:, etc. without requiring user to specify drive letter.
        """
        p = problem.lower().strip()

        # Fast-path for Battery & Power status
        if any(w in p for w in ["battery report", "battery status", "power plan", "battery health", "battery kitni"]):
            return {
                "issue_id": "SYS-FAST-POWER",
                "root_cause": "Battery and power subsystem query",
                "risk_level": "LOW",
                "risk_color": "GREEN",
                "summary": "Generating battery and power diagnostics. You can also open the live /power TUI dashboard anytime!",
                "actions": [
                    {
                        "description": "Inspect active power scheme and battery health",
                        "command": "powercfg /getactivescheme; Get-CimInstance Win32_Battery -ErrorAction SilentlyContinue | Select-Object EstimatedChargeRemaining, BatteryStatus, EstimatedRunTime | Format-List"
                    }
                ],
                "verification_command": "$true"
            }

        # Fast-path for Firewall Status
        if any(w in p for w in ["firewall status", "firewall check", "firewall profiles", "firewall kaisa he", "firewall on he"]):
            return {
                "issue_id": "SYS-FAST-FIREWALL",
                "root_cause": "Windows Defender Firewall configuration query",
                "risk_level": "LOW",
                "risk_color": "CYAN",
                "summary": "Checking Windows Defender Firewall profile states. You can also launch '/firewall' for the interactive cockpit!",
                "actions": [
                    {
                        "description": "Query active firewall profiles",
                        "command": "Get-NetFirewallProfile | Select-Object Name, Enabled, DefaultInboundAction, DefaultOutboundAction | Format-Table -AutoSize"
                    }
                ],
                "verification_command": "$true"
            }

        # Fast-path for Running Services
        if any(w in p for w in ["services status", "running services", "service list", "services check", "kaunse service"]):
            return {
                "issue_id": "SYS-FAST-SERVICES",
                "root_cause": "Core Windows services audit",
                "risk_level": "LOW",
                "risk_color": "CYAN",
                "summary": "Listing critical running Windows services. Check out '/services' for full interactive scroll and filter control!",
                "actions": [
                    {
                        "description": "Query running core system services",
                        "command": "Get-Service | Where-Object Status -eq 'Running' | Select-Object -First 15 Name, DisplayName, StartType | Format-Table -AutoSize"
                    }
                ],
                "verification_command": "$true"
            }

        # Fast-path for Hardware & Driver health
        if any(w in p for w in ["hardware check", "hardware status", "driver error", "degraded device", "problem hardware", "hardware devices"]):
            return {
                "issue_id": "SYS-FAST-HARDWARE",
                "root_cause": "Hardware device and driver integrity audit",
                "risk_level": "LOW",
                "risk_color": "CYAN",
                "summary": "Auditing hardware devices for error codes or degradation. Launch '/devices' for the complete hardware inventory!",
                "actions": [
                    {
                        "description": "Scan for problem or degraded hardware devices",
                        "command": "$errs = @(Get-PnpDevice -Status Error, Degraded -ErrorAction SilentlyContinue); if ($errs.Count -gt 0) { $errs | Select-Object FriendlyName, InstanceId, Status | Format-Table -AutoSize } else { Write-Host 'All installed hardware devices are HEALTHY.' }"
                    }
                ],
                "verification_command": "$true"
            }

        # Fast-path for IP Address
        if any(w in p for w in ["my ip", "ip address", "ip kya he", "ip batao", "ip check"]):
            return {
                "issue_id": "SYS-FAST-IP",
                "root_cause": "IPv4 network configuration query",
                "risk_level": "LOW",
                "risk_color": "GREEN",
                "summary": "Fetching all active IPv4 addresses and default gateways on your adapters:",
                "actions": [
                    {
                        "description": "Retrieve active IPv4 addresses",
                        "command": "Get-NetIPAddress -AddressFamily IPv4 -ErrorAction SilentlyContinue | Where-Object { $_.IPAddress -notlike '127.*' -and $_.IPAddress -notlike '169.254.*' } | Select-Object InterfaceAlias, IPAddress, PrefixLength | Format-Table -AutoSize"
                    }
                ],
                "verification_command": "$true"
            }
        if p.startswith("/find "):
            p = "find " + p[6:].strip()
            problem = "find " + problem[6:].strip()
        elif p.startswith("/search "):
            p = "search " + p[8:].strip()
            problem = "search " + problem[8:].strip()
        find_verbs = [
            "dhundho", "dhundo", "dhundh", "khojo", "khoj", "search", "find",
            "locate", "kaha hai", "kahan hai", "kaha he", "kahan he", "path batao",
            "path do", "dikhao kaha", "kaha pada", "where is", "where's", "kaha pe he", "kaha pe hai"
        ]
        if not any(v in p for v in find_verbs):
            return None

        # Exclude pure open/delete verbs
        if any(v in p for v in ["open", "kholo", "launch", "chalao", "delete", "hata do", "uda do"]):
            return None

        # Semantic hints
        hint = None
        if any(w in p for w in ["movie", "video", "film", "clip", "mp4", "mkv"]):
            hint = "video"
        elif any(w in p for w in ["song", "music", "audio", "mp3", "gaana"]):
            hint = "audio"
        elif any(w in p for w in ["image", "photo", "pic", "picture", "wallpaper", "jpg", "png"]):
            hint = "image"
        elif any(w in p for w in ["folder", "directory"]):
            hint = "folder"
        elif any(w in p for w in ["pdf", "doc", "document", "sheet", "excel"]):
            hint = "document"

        # Extract target keyword intelligently
        quoted = re.findall(r'["\']([^"\']+)["\']', problem)
        if quoted:
            target = quoted[0].strip()
        else:
            # Pattern: e.g. "search karo leo name ki sari files" -> "leo"
            name_m = re.search(r'(?:search|dhundho|find|locate|khojo)?\s*(?:karo|kar|kr)?\s*([a-zA-Z0-9_\-\.\s]+?)\s+(?:name|naam)\s+(?:ki|ka|ke|wali|wala|wale)\b', problem, re.IGNORECASE)
            if name_m and len(name_m.group(1).strip()) > 1:
                cand = name_m.group(1).strip()
                cand = re.sub(r'\b(?:search|dhundho|dhundo|find|locate|karo|kar|kr|kardo|kar do)\b', '', cand, flags=re.IGNORECASE).strip()
                target = cand if len(cand) >= 2 else None
            else:
                target = None

            if not target:
                clean = problem
                words_to_strip = [
                    "dhundho", "dhundo", "dhundh", "khojo", "khoj", "search", "find", "locate",
                    "karo", "kar", "kr", "kardo", "kar do", "chahiye", "dekho", "nikalo",
                    "kaha", "kahan", "hai", "he", "path", "batao", "do", "dikhao", "pada", "where", "is",
                    "sun", "bhai", "are", "yaar", "yr", "zara", "ek", "tu", "be", "plz", "please",
                    "ki", "ka", "ke", "ko", "se", "me", "pe", "par", "ye", "wo", "to", "bhi", "in", "the", "a", "an",
                    "sari", "saari", "sare", "all", "total", "jitni", "wali", "wala", "wale",
                    "movie", "video", "film", "clip", "song", "music", "audio", "files", "file", "folders", "folder", "directory", "image", "photo", "name", "naam"
                ]
                for v in words_to_strip:
                    clean = re.sub(rf'\b{v}\b', ' ', clean, flags=re.IGNORECASE)
                candidates = [c.strip() for c in clean.split() if len(c.strip()) > 0]
                target = " ".join(candidates).strip() if candidates else None
        if target:
            target_clean = target.lower().strip()
            if len(target_clean) <= 2 or target_clean in ["kr", "hi", "tu", "kar", "karo", "run", "chala", "bhi", "na", "to", "ye", "wo", "kuch", "apne", "aap"]:
                return None

        if not target or len(target) < 2:
            return None

        clean_target = target.replace("'", "''")
        hint_str = hint or ""

        ps_cmd = (
            f"$target = '{clean_target}'; "
            f"$hint = '{hint_str}'; "
            "$dirs = @([Environment]::GetFolderPath('Desktop'), [Environment]::GetFolderPath('MyDocuments'), (Join-Path $env:USERPROFILE 'Downloads'), (Join-Path $env:USERPROFILE 'Videos'), (Join-Path $env:USERPROFILE 'Pictures'), $env:USERPROFILE); "
            "Get-PSDrive -PSProvider FileSystem | Where-Object { $_.Root -ne 'C:\\' -and $_.Free -gt 0 } | ForEach-Object { $dirs += $_.Root }; "
            "$videoExts = @('.mkv', '.mp4', '.avi', '.mov', '.wmv', '.webm', '.flv'); "
            "$imageExts = @('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp'); "
            "$docExts   = @('.pdf', '.docx', '.doc', '.xlsx', '.txt', '.pptx'); "
            "$keywords = ($target -split '\\s+') | Where-Object { $_.Length -gt 1 }; "
            "$scored = @(); "
            "foreach ($d in $dirs) { if (Test-Path $d) { "
            "  $all = Get-ChildItem -Path $d -Recurse -Depth 3 -Attributes !ReparsePoint -ErrorAction SilentlyContinue | Where-Object { $_.FullName -notmatch '(node_modules|\\.git|\\.gradle|\\.vscode|AppData)' }; "
            "  foreach ($item in $all) { "
            "    $name = $item.Name.ToLower(); "
            "    $ext  = $item.Extension.ToLower(); "
            "    $score = 0; "
            "    if ($name -eq $target.ToLower()) { $score += 200 } "
            "    elseif ($item.BaseName.ToLower() -eq $target.ToLower()) { $score += 150 } "
            "    elseif ($name -match \"(?i)\\b$target\\b\") { $score += 100 } "
            "    elseif ($name -match \"(?i)$target\") { $score += 60 }; "
            "    $matchCount = 0; "
            "    foreach ($kw in $keywords) { if ($name -match \"(?i)\\b$kw\\b\" -or $name -like \"*$kw*\") { $matchCount++ } }; "
            "    if ($matchCount -gt 0) { "
            "      $score += ($matchCount * 40); "
            "      if ($hint -eq 'video') { if ($videoExts -contains $ext) { $score += 100 } else { $score -= 40 } } "
            "      elseif ($hint -eq 'image') { if ($imageExts -contains $ext) { $score += 100 } else { $score -= 40 } } "
            "      elseif ($hint -eq 'document') { if ($docExts -contains $ext) { $score += 100 } else { $score -= 40 } } "
            "      elseif ($hint -eq 'folder') { if ($item.PSIsContainer) { $score += 100 } else { $score -= 50 } }; "
            "      $scored += [PSCustomObject]@{ Item = $item; Score = $score }; "
            "    } "
            "  } "
            "} }; "
            "$best = $scored | Sort-Object Score -Descending; "
            "if ($best -and $best.Count -gt 0) { "
            "  $script:LastOpenedPath = $best[0].Item.FullName; "
            "  $seen = @{}; "
            "  $idx = 1; "
            "  foreach ($b in $best) { "
            "    if (-not $seen.ContainsKey($b.Item.FullName)) { "
            "      $seen[$b.Item.FullName] = $true; "
            "      $ext = if ($b.Item.PSIsContainer) { '' } else { $b.Item.Extension.ToLower() }; "
            "      $tag = if ($b.Item.PSIsContainer) { '[DIR]' } elseif (@('.mkv','.mp4','.avi','.mov','.webm','.flv') -contains $ext) { '[VID]' } elseif (@('.zip','.rar','.7z','.iso') -contains $ext) { '[ZIP]' } elseif (@('.exe','.msi','.apk') -contains $ext) { '[APP]' } elseif (@('.pdf','.doc','.docx','.txt','.xlsx','.log') -contains $ext) { '[DOC]' } elseif (@('.jpg','.png','.jpeg','.webp','.bmp') -contains $ext) { '[IMG]' } else { '[FILE]' }; "
            "      $sz = if ($b.Item.PSIsContainer) { 'Folder' } elseif ($b.Item.Length -ge 1GB) { [math]::Round($b.Item.Length / 1GB, 2).ToString() + ' GB' } else { [math]::Round($b.Item.Length / 1MB, 2).ToString() + ' MB' }; "
            "      \"[$idx] $tag $($b.Item.FullName) ($sz)\"; "
            "      $idx++; "
            "      if ($idx -gt 8) { break } "
            "    } "
            "  }; "
            "  \"\"; "
            "  \" Tip: Type '/open 1' or '/open <name>' to launch instantly\"; "
            "} else { "
            f"  \"Could not find '{clean_target}' across Desktop, Documents, Downloads, or any connected storage drives.\" "
            "}"
        )

        display_name = f"'{target}'" + (f" ({hint})" if hint else "")
        return {
            "issue_id": "SYS-FAST-FIND",
            "root_cause": f"Universal multi-drive locator for {display_name}",
            "risk_level": "LOW",
            "risk_color": "CYAN",
            "summary": f"Searching all drives and profiles for {display_name}...",
            "actions": [
                {
                    "description": f"Locate {display_name} across all storage volumes",
                    "command": ps_cmd
                }
            ],
            "verification_command": "$true"
        }

    def _check_fast_path(self, problem: str) -> Optional[Dict[str, Any]]:
        """
        O(1) Instant Fast-Path dispatcher for high-frequency diagnostic queries.
        Bypasses network roundtrips and delivers instantaneous sub-millisecond execution.
        """
        p = problem.lower().strip()
        # Fast-path for Listening & Used Ports (Only for raw listing, NOT for explanations)
        is_explain_query = any(w in p for w in ["kyu", "why", "kis kaam", "kaam", "details", "explain", "detail", "purpose", "meaning", "samjhao", "table", "matlab", "reason", "unko", "inme"])
        if not is_explain_query and any(w in p for w in ["ports", "port"]) and any(w in p for w in ["dikhao", "show", "list", "open ports", "listening ports", "active ports"]):
            return {
                "issue_id": "SYS-FAST-PORTS",
                "root_cause": "Active listening and established TCP ports query",
                "risk_level": "LOW",
                "risk_color": "CYAN",
                "summary": "Ye rahe aapke active listening aur used ports process name mapping ke saath:",
                "actions": [
                    {
                        "description": "Query active listening TCP ports with process mapping",
                        "command": "Get-NetTCPConnection -State Listen, Established -ErrorAction SilentlyContinue | Select-Object -First 15 LocalAddress, LocalPort, State, @{Name='Process';Expression={(Get-Process -Id $_.OwningProcess -ErrorAction SilentlyContinue).ProcessName}}, OwningProcess | Format-Table -AutoSize"
                    }
                ],
                "verification_command": "$true"
            }


        # Fast-path for Battery & Power status
        if any(w in p for w in ["battery report", "battery status", "power plan", "battery health", "battery kitni"]):
            return {
                "issue_id": "SYS-FAST-POWER",
                "root_cause": "Battery and power subsystem query",
                "risk_level": "LOW",
                "risk_color": "GREEN",
                "summary": "Generating battery and power diagnostics. You can also open the live /power TUI dashboard anytime!",
                "actions": [
                    {
                        "description": "Inspect active power scheme and battery health",
                        "command": "powercfg /getactivescheme; Get-CimInstance Win32_Battery -ErrorAction SilentlyContinue | Select-Object EstimatedChargeRemaining, BatteryStatus, EstimatedRunTime | Format-List"
                    }
                ],
                "verification_command": "$true"
            }

        # Fast-path for Firewall Status
        if any(w in p for w in ["firewall status", "firewall check", "firewall profiles", "firewall kaisa he", "firewall on he"]):
            return {
                "issue_id": "SYS-FAST-FIREWALL",
                "root_cause": "Windows Defender Firewall configuration query",
                "risk_level": "LOW",
                "risk_color": "CYAN",
                "summary": "Checking Windows Defender Firewall profile states. You can also launch '/firewall' for the interactive cockpit!",
                "actions": [
                    {
                        "description": "Query active firewall profiles",
                        "command": "Get-NetFirewallProfile | Select-Object Name, Enabled, DefaultInboundAction, DefaultOutboundAction | Format-Table -AutoSize"
                    }
                ],
                "verification_command": "$true"
            }

        # Fast-path for Running Services
        if any(w in p for w in ["services status", "running services", "service list", "services check", "kaunse service"]):
            return {
                "issue_id": "SYS-FAST-SERVICES",
                "root_cause": "Core Windows services audit",
                "risk_level": "LOW",
                "risk_color": "CYAN",
                "summary": "Listing critical running Windows services. Check out '/services' for full interactive scroll and filter control!",
                "actions": [
                    {
                        "description": "Query running core system services",
                        "command": "Get-Service | Where-Object Status -eq 'Running' | Select-Object -First 15 Name, DisplayName, StartType | Format-Table -AutoSize"
                    }
                ],
                "verification_command": "$true"
            }

        # Fast-path for Hardware & Driver health
        if any(w in p for w in ["hardware check", "hardware status", "driver error", "degraded device", "problem hardware", "hardware devices"]):
            return {
                "issue_id": "SYS-FAST-HARDWARE",
                "root_cause": "Hardware device and driver integrity audit",
                "risk_level": "LOW",
                "risk_color": "CYAN",
                "summary": "Auditing hardware devices for error codes or degradation. Launch '/devices' for the complete hardware inventory!",
                "actions": [
                    {
                        "description": "Scan for problem or degraded hardware devices",
                        "command": "$errs = @(Get-PnpDevice -Status Error, Degraded -ErrorAction SilentlyContinue); if ($errs.Count -gt 0) { $errs | Select-Object FriendlyName, InstanceId, Status | Format-Table -AutoSize } else { Write-Host 'All installed hardware devices are HEALTHY.' }"
                    }
                ],
                "verification_command": "$true"
            }

        # Fast-path for IP Address
        if any(w in p for w in ["my ip", "ip address", "ip kya he", "ip batao", "ip check"]):
            return {
                "issue_id": "SYS-FAST-IP",
                "root_cause": "IPv4 network configuration query",
                "risk_level": "LOW",
                "risk_color": "GREEN",
                "summary": "Fetching all active IPv4 addresses and default gateways on your adapters:",
                "actions": [
                    {
                        "description": "Retrieve active IPv4 addresses",
                        "command": "Get-NetIPAddress -AddressFamily IPv4 -ErrorAction SilentlyContinue | Where-Object { $_.IPAddress -notlike '127.*' -and $_.IPAddress -notlike '169.254.*' } | Select-Object InterfaceAlias, IPAddress, PrefixLength | Format-Table -AutoSize"
                    }
                ],
                "verification_command": "$true"
            }

        # 0. Quick App Launch Fast-Path
        if any(w in p for w in ["open notepad", "notepad kholo", "start notepad", "launch notepad"]) or p == "notepad":
            return {
                "issue_id": "SYS-FAST-APP-NOTEPAD",
                "root_cause": "Direct request to launch Windows Notepad utility",
                "risk_level": "LOW",
                "risk_color": "CYAN",
                "summary": "Opening Windows Notepad...",
                "actions": [
                    {
                        "description": "Start Notepad process",
                        "command": "Start-Process notepad.exe"
                    }
                ],
                "verification_command": "$true"
            }

        if any(w in p for w in ["open calc", "calculator kholo", "start calc", "launch calc", "open calculator"]) or p in ["calc", "calculator"]:
            return {
                "issue_id": "SYS-FAST-APP-CALC",
                "root_cause": "Direct request to launch Windows Calculator",
                "risk_level": "LOW",
                "risk_color": "CYAN",
                "summary": "Opening Windows Calculator...",
                "actions": [
                    {
                        "description": "Start Calculator process",
                        "command": "Start-Process calc.exe"
                    }
                ],
                "verification_command": "$true"
            }

        if any(w in p for w in ["open task manager", "task manager kholo", "taskmgr kholo", "open taskmgr"]) or p in ["taskmgr", "task manager"]:
            return {
                "issue_id": "SYS-FAST-APP-TASKMGR",
                "root_cause": "Direct request to launch Windows Task Manager",
                "risk_level": "LOW",
                "risk_color": "CYAN",
                "summary": "Opening Windows Task Manager...",
                "actions": [
                    {
                        "description": "Start Task Manager process",
                        "command": "Start-Process taskmgr.exe"
                    }
                ],
                "verification_command": "$true"
            }

        # 1. Recent files fast-path
        if ("recent" in p and "file" in p) or ("latest" in p and "file" in p) or ("naya" in p and "file" in p) or "recent" in p:
            return {
                "issue_id": "SYS-FAST-FILES",
                "root_cause": "Direct index retrieval of recently accessed user files",
                "risk_level": "LOW",
                "risk_color": "CYAN",
                "summary": "10 most recent files retrieved directly from Windows Recent catalog",
                "actions": [
                    {
                        "description": "Query 10 newest files from Windows Recent catalog",
                        "command": "Get-ChildItem -Path ([Environment]::GetFolderPath('Recent')) -File -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 10 BaseName, LastWriteTime | Format-Table -AutoSize"
                    }
                ],
                "verification_command": "$true"
            }

        # 2. System specs fast-path
        if any(w in p for w in ["system spec", "specs", "specification", "ram kitni", "processor", "hardware info", "computer info"]):
            return {
                "issue_id": "SYS-FAST-SPECS",
                "root_cause": "Direct hardware profiling query",
                "risk_level": "LOW",
                "risk_color": "CYAN",
                "summary": "Instant CPU, RAM, and OS architecture profile",
                "actions": [
                    {
                        "description": "Show OS, architecture, and memory summary",
                        "command": "Get-CimInstance Win32_OperatingSystem | Select-Object Caption, Version, OSArchitecture, @{N='RAM(GB)';E={[math]::Round($_.TotalVisibleMemorySize/1MB,1)}} | Format-List"
                    },
                    {
                        "description": "Show CPU processor model and core topology",
                        "command": "Get-CimInstance Win32_Processor | Select-Object Name, NumberOfCores, NumberOfLogicalProcessors | Format-List"
                    }
                ],
                "verification_command": "$true"
            }

        # 3. Windows updates fast-path
        if any(w in p for w in ["update he", "kya update", "updates list", "show updates", "installed update", "hotfix list", "mere windows me kya update"]):
            return {
                "issue_id": "SYS-FAST-UPDATES",
                "root_cause": "Direct query of installed hotfixes and patches",
                "risk_level": "LOW",
                "risk_color": "CYAN",
                "summary": "List of recently applied Windows security and cumulative patches",
                "actions": [
                    {
                        "description": "Enumerate installed Windows hotfixes and updates",
                        "command": "Get-HotFix -ErrorAction SilentlyContinue | Sort-Object InstalledOn -Descending | Select-Object -First 10 HotFixID, Description, InstalledOn | Format-Table -AutoSize"
                    }
                ],
                "verification_command": "$true"
            }

        # 4. Storage / Disk space fast-path
        if any(w in p for w in ["disk space", "storage space", "free storage", "storage kitna", "hard disk", "drive space", "c drive space", "kitna space", "check storage"]) or p in ["storage", "disk", "drives"]:
            return {
                "issue_id": "SYS-FAST-STORAGE",
                "root_cause": "Direct filesystem capacity audit",
                "risk_level": "LOW",
                "risk_color": "CYAN",
                "summary": "Storage volume capacity and free space inventory",
                "actions": [
                    {
                        "description": "Display storage volumes and capacity",
                        "command": "Get-PSDrive -PSProvider FileSystem | Select-Object Name, @{N='Used(GB)';E={[math]::Round($_.Used/1GB,2)}}, @{N='Free(GB)';E={[math]::Round($_.Free/1GB,2)}} | Format-Table -AutoSize"
                    }
                ],
                "verification_command": "$true"
            }

        # 5. Top CPU / RAM hogs fast-path
        if any(w in p for w in ["cpu hog", "ram hog", "memory hog", "heavy process", "task manager", "lag kar raha"]):
            return {
                "issue_id": "SYS-FAST-PERF",
                "root_cause": "Real-time process resource consumption inspection",
                "risk_level": "LOW",
                "risk_color": "CYAN",
                "summary": "Top 5 memory and CPU consuming background processes",
                "actions": [
                    {
                        "description": "Identify top 5 memory-heavy active processes",
                        "command": "Get-Process | Sort-Object WorkingSet64 -Descending | Select-Object -First 5 ProcessName, Id, @{N='RAM(MB)';E={[math]::Round($_.WorkingSet64/1MB,1)}}, @{N='CPU(s)';E={[math]::Round($_.CPU,1)}} | Format-Table -AutoSize"
                    }
                ],
                "verification_command": "$true"
            }

        # Check if query is conversational or action-oriented
        action_or_chat_words = [
            "paint", "open", "fix", "viewer", "error", "issue", "problem",
            "nahi", "change", "badlo", "kara", "karo", "kr", "tu hi", "why",
            "kyun", "kaise", "how", "help", "ander", "inside", "photos",
            "default", "association", "slow", "hang", "dekh", "batao", "chal",
            "kya", "kar", "he", "mein", "main", "content"
        ]
        if any(w in p for w in action_or_chat_words):
            return None

        # 6. File & Folder Path Search Fast-Path
        search_indicators = [
            "folder path", "path of folder", "find folder", "search folder",
            "kahan hai folder", "folder kahan", "storage me folder",
            "file path", "path of file", "find file", "search file", "where is folder"
        ]
        is_folder_search = any(k in p for k in search_indicators)

        if is_folder_search:
            target = None
            quoted = re.findall(r'["\']([^"\']+)["\']', problem)
            if quoted:
                target = quoted[0].strip()
            else:
                m = re.search(r'(?:folder|file)(?:\s+name|\s+named|\s+path of|\s+path)?\s*(?:of\s+a\s+folder\s+name\s+|of\s+|is\s+|:\s*|\s+)?([a-zA-Z0-9_\-\.]+)', problem, re.IGNORECASE)
                if m:
                    candidate = m.group(1).strip()
                    if candidate.lower() not in ["path", "name", "the", "a", "my", "in", "of", "and", "is", "he", "which", "content"]:
                        target = candidate

            if not target and any(w in p for w in ["assingment", "assigment", "assignment"]):
                target = "assingment"

            if target and target.lower() not in ["he", "which", "content", "inside", "the"]:
                clean_target = target.strip().replace("'", "''")
                ps_cmd = (
                    f"$target = '{clean_target}'; "
                    "$dirs = @([Environment]::GetFolderPath('Desktop'), [Environment]::GetFolderPath('MyDocuments'), (Join-Path $env:USERPROFILE 'Downloads'), (Join-Path $env:USERPROFILE 'Pictures'), (Join-Path $env:USERPROFILE 'Videos'), $env:USERPROFILE); "
                    "Get-PSDrive -PSProvider FileSystem | Where-Object { $_.Root -ne 'C:\\' -and $_.Free -gt 0 } | ForEach-Object { $dirs += $_.Root }; "
                    "$found = @(); "
                    "foreach ($d in $dirs) { "
                    "  if (Test-Path $d) { "
                    f"    $items = Get-ChildItem -Path $d -Directory -Filter '*$target*' -Attributes !ReparsePoint -ErrorAction SilentlyContinue | Where-Object {{ $_.FullName -notmatch '(node_modules|\\.git|\\.gradle|\\.vscode|AppData)' }}; "
                    "    if ($items) { $found += $items.FullName }; "
                    f"    $subItems = Get-ChildItem -Path $d -Directory -Recurse -Depth 2 -Filter '*$target*' -Attributes !ReparsePoint -ErrorAction SilentlyContinue | Where-Object {{ $_.FullName -notmatch '(node_modules|\\.git|\\.gradle|\\.vscode|AppData)' }}; "
                    "    if ($subItems) { $found += $subItems.FullName } "
                    "  } "
                    "}; "
                    "if ($found.Count -eq 0 -and $target -match '(?i)assi') { "
                    "  foreach ($d in $dirs) { if (Test-Path $d) { "
                    "    $items = Get-ChildItem -Path $d -Directory -Filter '*assi*' -Attributes !ReparsePoint -ErrorAction SilentlyContinue | Where-Object { $_.FullName -notmatch '(node_modules|\\.git|\\.gradle|\\.vscode|AppData)' }; "
                    "    if ($items) { $found += $items.FullName } "
                    "  } } "
                    "}; "
                    "if ($found.Count -gt 0) { "
                    "  $found | Select-Object -Unique | ForEach-Object { [PSCustomObject]@{ 'Folder Name' = (Split-Path $_ -Leaf); 'Full Path' = $_ } } | Format-Table -AutoSize "
                    "} else { "
                    f"  'No folder matching \"{target}\" found in Desktop, Documents, Downloads, or Storage Drives.' "
                    "}"
                )
                return {
                    "issue_id": "SYS-FAST-FIND-PATH",
                    "root_cause": f"High-speed indexed search for folder '{target}' across user profiles and storage volumes",
                    "risk_level": "LOW",
                    "risk_color": "CYAN",
                    "summary": f"Targeted search for '{target}' in Desktop, Documents, Downloads, and storage drives",
                    "actions": [
                        {
                            "description": f"Locate folder '{target}' in storage and return exact full path",
                            "command": ps_cmd
                        }
                    ],
                    "verification_command": "$true"
                }

        return None

    async def diagnose(
        self,
        problem: str,
        telemetry: Dict[str, Any],
        history: Optional[List[Dict[str, Any]]] = None,
        last_output: Optional[str] = None,
        session_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Level 2 Controlled Autonomy Diagnostic Coordinator.
        """
        # Step 1: Resolve pronoun references (e.g. "ise fix karo", "isko band kar")
        resolved_problem, detected_domain = HinglishProcessor.resolve_pronoun_reference(problem, history)

        # Step 2: Intent classification
        intent_info = IntentClassifier.classify(resolved_problem, history)
        intent = intent_info.intent.value if hasattr(intent_info.intent, "value") else str(intent_info.intent)

        # Helper: Record chat turn into persistent memory before returning
        def _finalize_and_record(p: Dict[str, Any]) -> Dict[str, Any]:
            if p.get("summary"):
                s = str(p["summary"])
                s = re.sub(r'[  ​‎‏]', ' ', s)
                s = re.sub(r'[‐‑‒–—―−]', '-', s)
                s = re.sub(r'[‘’‚‛]', "'", s)
                s = re.sub(r'[“”„‟]', '"', s)
                s = s.replace('…', '...').replace('â¯', ' ').replace('â', '-')
                s = s.replace('→', '->').replace('←', '<-').replace('•', '-')
                p["summary"] = s
            try:
                MemoryStore.save_chat_turn(
                    session_token=session_token or "default",
                    user_message=problem,
                    ai_summary=p.get("summary", ""),
                    intent=intent,
                    actions_count=len(p.get("actions", []))
                )
            except Exception:
                pass
            return p

        # Step 3: Telemetry sync to persistent memory
        if telemetry:
            try:
                MemoryStore.update_system_profile(telemetry)
            except Exception:
                pass

        # Step 4: Handle conversational, chit-chat, cancellations, & ambiguities immediately
        chat_plan = self._check_conversational_query(resolved_problem)
        if chat_plan:
            return _finalize_and_record(chat_plan)

        if intent == "ACKNOWLEDGMENT":
            return _finalize_and_record({
                "issue_id": "SYS-ACK",
                "root_cause": "User acknowledgment or appreciation",
                "risk_level": "LOW",
                "risk_color": "GREEN",
                "summary": "Badhiya bhai! Khushi hui ki sab theek se ho gaya. Koi aur file, network issue ya system query ho toh batao!",
                "actions": [],
                "selected_tools": [],
                "verification_command": "$true",
                "requires_confirmation": False
            })

        if intent == "GREETING_CHITCHAT":
            return _finalize_and_record({
                "issue_id": "SYS-CHITCHAT",
                "root_cause": "Greeting or casual chatter",
                "risk_level": "LOW",
                "risk_color": "CYAN",
                "summary": "Hi Professor! Kaise ho bhai? Main KRONOS hoon, aapka autonomous Windows Co-Pilot. Koi diagnostic, system cleanup, network issue ya query ho toh batao!",
                "actions": [],
                "selected_tools": [],
                "verification_command": "$true",
                "requires_confirmation": False
            })

        if intent == "CANCELLATION":
            return _finalize_and_record({
                "issue_id": "SYS-CANCEL",
                "root_cause": "User requested operation cancellation",
                "risk_level": "LOW",
                "risk_color": "CYAN",
                "summary": "Theek hai bhai, koi changes execute nahi honge. Mast chill karo!",
                "actions": [],
                "selected_tools": [],
                "verification_command": "$true",
                "requires_confirmation": False
            })

        if intent == "AMBIGUOUS_QUERY":
            return _finalize_and_record({
                "issue_id": "SYS-AMBIGUOUS",
                "root_cause": "User query lacks specific system component or target",
                "risk_level": "LOW",
                "risk_color": "CYAN",
                "summary": "Bhai, query thodi unclear lag rahi hai. Aap kya diagnose ya fix karna chahte ho? Jaise ki: internet speed, high RAM/CPU usage, audio issue, ya disk cleanup?",
                "actions": [],
                "selected_tools": [],
                "verification_command": "$true",
                "requires_confirmation": False
            })

        # Step 5: Built-in Interactive TUIs and specialized system operations
        # If user is in an active conversation (history present) or asking an explanation / follow-up,
        # prioritize LLM reasoning over static heuristic interceptors (unless explicitly requested via '/')
        # Static TUIs should ONLY trigger on explicit slash commands (e.g. /wifi, /top, /disk)
        # or single standalone keywords (e.g. 'wifi', 'top', 'specs')
        words = resolved_problem.strip().split()
        single_word = resolved_problem.strip().lower()
        is_explicit_slash = resolved_problem.strip().startswith("/")
        STANDALONE_TUI_WORDS = {
            "wifi", "net", "top", "task", "specs", "sys", "disk", "storage",
            "ports", "matrix", "doctor", "health", "boost", "clean", "startup",
            "boot", "apps", "winget", "debloat", "services", "svc", "firewall",
            "audio", "sound", "tree", "power", "battery", "devices", "cava", "bandwhich", "dust"
        }
        is_standalone_tui_word = (len(words) == 1 and single_word in STANDALONE_TUI_WORDS) or (len(words) == 2 and single_word in ["task manager", "system specs", "disk health", "wifi radar"])

        if is_explicit_slash or is_standalone_tui_word:
            tui_plan = self._check_tui_request(resolved_problem)
            if tui_plan:
                return _finalize_and_record(tui_plan)

            net_plan = self._check_network_control_request(resolved_problem, history=history)
            if net_plan:
                return _finalize_and_record(net_plan)

        kill_plan = self._check_kill_request(resolved_problem)
        if kill_plan:
            return _finalize_and_record(kill_plan)

        open_plan = self._check_open_request(resolved_problem, last_output=last_output, history=history)
        if open_plan:
            return _finalize_and_record(open_plan)

        delete_plan = self._check_delete_request(resolved_problem)
        if delete_plan:
            return _finalize_and_record(delete_plan)

        find_plan = self._check_find_request(resolved_problem)
        if find_plan:
            return _finalize_and_record(find_plan)

        # Fast-path is only for slash commands or explicit commands, not for natural language questions
        if is_explicit_slash:
            fast_plan = self._check_fast_path(resolved_problem)
            if fast_plan:
                return _finalize_and_record(fast_plan)

        # Step 6: Query AI Providers or Fallback
        plan: Optional[Dict[str, Any]] = None

        # Provider 1: Groq Cloud
        if self.groq_api_key:
            try:
                plan = await self._query_groq(
                    resolved_problem,
                    telemetry,
                    history=history,
                    last_output=last_output,
                    intent=intent
                )
            except Exception as e:
                print(f"[!] Groq inference error: {e}")

        # Provider 2: Gemini
        if not plan and self.gemini_api_key:
            try:
                plan = await self._query_gemini(
                    resolved_problem,
                    telemetry,
                    history=history,
                    last_output=last_output,
                    intent=intent
                )
            except Exception as e:
                print(f"[!] Gemini inference error: {e}")

        # Fallback: Deterministic Local Expert Engine
        if not plan:
            plan = self._local_expert_engine(resolved_problem, telemetry)

        # Step 7: Structured Tool Compilation & Safety Validation
        selected_tools = plan.get("selected_tools", [])
        if selected_tools:
            compilation = ToolExecutor.compile_tool_calls(selected_tools)
            if compilation.is_valid:
                compiled_actions = []
                for a in compilation.actions:
                    compiled_actions.append({
                        "description": a["description"],
                        "command": a["command"]
                    })
                plan["actions"] = compiled_actions
                plan["risk_level"] = compilation.highest_risk
                plan["requires_confirmation"] = (
                    any(a.get("requires_confirmation", False) for a in compilation.actions)
                    or compilation.highest_risk in ["MODERATE", "HIGH"]
                )
                if not plan.get("verification_command") or plan["verification_command"] == "$true":
                    if compilation.actions and compilation.actions[-1].get("verification"):
                        plan["verification_command"] = compilation.actions[-1]["verification"]
            else:
                plan["risk_level"] = "BLOCKED"
                plan["risk_color"] = "RED"
                plan["actions"] = []
                plan["summary"] = f"Operation Blocked: {compilation.error_message}. Safety guardrails prevented execution."
                plan["requires_confirmation"] = False

        # If raw actions were supplied, sanitize through CommandGuardrail
        raw_actions = plan.get("actions", [])
        if raw_actions:
            safe_actions, _ = CommandGuardrail.sanitize_plan(raw_actions)
            plan["actions"] = safe_actions

        # Assign risk color based on risk tier
        r_tier = str(plan.get("risk_level", "LOW")).upper()
        if r_tier == "LOW":
            plan["risk_color"] = "GREEN"
        elif r_tier in ["MODERATE", "MEDIUM"]:
            plan["risk_color"] = "YELLOW"
        else:
            plan["risk_color"] = "RED"

        # Step 8: Persist episode into MemoryStore
        try:
            action_descs = [a.get("description", "") for a in plan.get("actions", [])]
            MemoryStore.record_troubleshooting(
                issue=plan.get("issue_id", "SYS-DIAG"),
                root_cause=plan.get("root_cause", "Diagnostic request"),
                tools_used=action_descs,
                outcome=plan.get("verification_command", "$true")
            )
        except Exception:
            pass

        return _finalize_and_record(plan)

    async def _query_groq(
        self,
        problem: str,
        telemetry: Dict[str, Any],
        history: Optional[List[Dict[str, Any]]] = None,
        last_output: Optional[str] = None,
        intent: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Ultra-low latency inference via Groq with Level 2 Structured Tool Selection,
        RAG Knowledge Base context, Expert Skill playbooks, and persistent memory.
        """
        system_instruction = MASTER_SYSTEM_INSTRUCTION
        tools_instruction = self.build_tools_instruction()
        skill_context = SkillsRegistry.build_system_context(problem)
        rag_context = KnowledgeBase.build_rag_context(problem)
        memory_context = MemoryStore.build_memory_context()

        full_system = f"{system_instruction}\n\n{tools_instruction}"
        if skill_context:
            full_system += f"\n\n{skill_context}"
        if rag_context:
            full_system += f"\n\n{rag_context}"
        if memory_context:
            full_system += f"\n\n{memory_context}"

        messages = [{"role": "system", "content": full_system}]

        if history:
            for turn in history[-10:]:
                r = turn.get("role", "user")
                c = turn.get("content", "")
                if c:
                    messages.append({"role": r, "content": c})

        user_parts = []
        if last_output:
            user_parts.append(f"[Output from previous command on user's system]:\n```\n{last_output}\n```")
        if telemetry and not history:
            user_parts.append(f"[Host Telemetry]: {json.dumps(telemetry, default=str)}")
        if intent:
            user_parts.append(f"[Detected Intent]: {intent}")
        user_parts.append(f"User Query: {problem}")
        user_parts.append("(Reply strictly as a valid JSON object conforming to the required schema)")

        current_content = "\n\n".join(user_parts)
        messages.append({"role": "user", "content": current_content})

        headers = {
            "Authorization": f"Bearer {self.groq_api_key}",
            "Content-Type": "application/json"
        }

        client = await self.get_client()
        last_error = None

        for model in self.groq_models:
            payload = {
                "model": model,
                "messages": messages,
                "response_format": {"type": "json_object"},
                "temperature": 0.0,
                "max_tokens": 1200
            }
            try:
                resp = await client.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers)
                if resp.status_code == 429:
                    print(f"[-] Groq rate limit 429 on {model}, attempting failover...")
                    last_error = RuntimeError(f"Groq 429 on {model}")
                    continue
                resp.raise_for_status()
                data = resp.json()
                raw_text = data["choices"][0]["message"]["content"].strip()
                if raw_text.startswith("```"):
                    raw_text = re.sub(r"^```(?:json)?\s*", "", raw_text, flags=re.IGNORECASE)
                    raw_text = re.sub(r"\s*```$", "", raw_text)
                plan = json.loads(raw_text)
                if plan.get("summary"):
                    s = str(plan["summary"]).replace('\u2011', '-').replace('\u2012', '-').replace('\u2013', '-').replace('\u2014', '-').replace('â', '-')
                    plan["summary"] = s
                return plan
            except Exception as ex:
                last_error = ex
                continue

        if last_error:
            raise last_error
        raise RuntimeError("No Groq model candidates succeeded.")

    async def _query_gemini(
        self,
        problem: str,
        telemetry: Dict[str, Any],
        history: Optional[List[Dict[str, Any]]] = None,
        last_output: Optional[str] = None,
        intent: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Symmetric inference via Google Gemini with Level 2 Structured Tool Selection,
        RAG Knowledge Base context, Expert Skill playbooks, and persistent memory.
        """
        system_instruction = MASTER_SYSTEM_INSTRUCTION
        tools_instruction = self.build_tools_instruction()
        skill_context = SkillsRegistry.build_system_context(problem)
        rag_context = KnowledgeBase.build_rag_context(problem)
        memory_context = MemoryStore.build_memory_context()

        full_system = f"{system_instruction}\n\n{tools_instruction}"
        if skill_context:
            full_system += f"\n\n{skill_context}"
        if rag_context:
            full_system += f"\n\n{rag_context}"
        if memory_context:
            full_system += f"\n\n{memory_context}"

        parts = [f"System Context:\n{full_system}"]
        if history:
            hist_str = "\n".join(f"{h.get('role', 'user').upper()}: {h.get('content', '')}" for h in history[-8:])
            parts.append(f"Conversation History:\n{hist_str}")
        if last_output:
            parts.append(f"Previous Command Output:\n{last_output}")
        if telemetry:
            parts.append(f"Host Telemetry:\n{json.dumps(telemetry, default=str)}")
        if intent:
            parts.append(f"Detected Intent: {intent}")
        parts.append(f"User Query: {problem}\n(Reply strictly as a valid JSON object)")

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={self.gemini_api_key}"
        payload = {
            "contents": [{"parts": [{"text": "\n\n".join(parts)}]}],
            "generationConfig": {"response_mime_type": "application/json"}
        }

        client = await self.get_client()
        resp = await client.post(url, json=payload)
        resp.raise_for_status()
        data = resp.json()
        raw_text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
        if raw_text.startswith("```"):
            raw_text = re.sub(r"^```(?:json)?\s*", "", raw_text, flags=re.IGNORECASE)
            raw_text = re.sub(r"\s*```$", "", raw_text)
        plan = json.loads(raw_text)
        return plan

    def _local_expert_engine(self, problem: str, telemetry: Dict[str, Any]) -> Dict[str, Any]:
        """
        Offline deterministic diagnostic engine powered by SkillsRegistry and ToolRegistry.
        """
        skill = SkillsRegistry.match_skill(problem)
        if skill:
            tool_calls = [{"tool_id": tid, "arguments": {}} for tid in skill.remediation_tools]
            comp = ToolExecutor.compile_tool_calls(tool_calls)
            actions = [{"description": a["description"], "command": a["command"]} for a in comp.actions] if comp.is_valid else []
            verif = comp.actions[-1]["verification"] if (comp.actions and comp.actions[-1].get("verification")) else "$true"
            risk_tier = comp.highest_risk if comp.is_valid else skill.risk_level
            
            return {
                "issue_id": skill.skill_id,
                "root_cause": f"Matched expert diagnostic playbook: {skill.name}",
                "intent": "TROUBLESHOOTING_REQUEST",
                "risk_level": risk_tier,
                "risk_color": "YELLOW" if risk_tier in ["MODERATE", "MEDIUM"] else ("RED" if risk_tier == "HIGH" else "GREEN"),
                "summary": f"{skill.description} (Running via deterministic offline playbook)",
                "actions": actions,
                "verification_command": verif,
                "requires_confirmation": skill.confirmation_required or risk_tier in ["MODERATE", "HIGH"]
            }

        p_lower = problem.lower().strip()

        # 2. Offline Conceptual & Architectural Explanations (with Tables & Structure)
        # 2a. File Systems Comparison (NTFS vs exFAT vs FAT32)
        if any(w in p_lower for w in ["ntfs vs exfat", "exfat vs ntfs", "fat32 vs ntfs", "file system", "ntfs kya", "exfat kya"]):
            table = (
                "| Feature | NTFS | exFAT | FAT32 |\n"
                "|---|---|---|---|\n"
                "| Max File Size | 16 TB (practical) | 128 PB (virtually unlimited) | 4 GB |\n"
                "| Compatibility | Windows (Read/Write), Mac (Read-only) | Windows & macOS (Full R/W) | Almost all devices |\n"
                "| Security & Permissions | Full ACL, Encrypting File System (EFS) | None | None |\n"
                "| Journaling / Reliability | Yes (prevents corruption on sudden unplug) | No | No |\n"
                "| Best Use Case | Windows internal system drive (C:) | USB flash drives, External hard drives | Older game consoles, legacy devices |"
            )
            summary = (
                f"Bhai, NTFS aur exFAT dono alag-alag purpose ke liye design kiye gaye hain:\n\n"
                f"{table}\n\n"
                f"- **Agar Windows internal drive ya software install karna hai**: **NTFS** best hai kyu ki isme journaling aur file permissions hote hain.\n"
                f"- **Agar pen drive / external hard drive dono Mac aur Windows me chalani hai**: **exFAT** choose karo kyu ki isme 4GB se badi movies/files copy ho sakti hain bina cross-platform issue ke."
            )
            return {
                "issue_id": "EXP-FS-COMPARE",
                "root_cause": "File system architecture comparison (NTFS vs exFAT)",
                "intent": "TECHNICAL_EXPLANATION",
                "risk_level": "LOW",
                "risk_color": "CYAN",
                "summary": summary,
                "actions": [],
                "selected_tools": [],
                "verification_command": "$true",
                "requires_confirmation": False
            }

        # 2b. Port 80 vs 443 / Open Ports Concept
        if any(w in p_lower for w in ["port 80", "port 443", "80 vs 443", "open ports kya", "listening ports kya"]):
            table = (
                "| Port | Protocol | Encryption | Security Status | Default Usage |\n"
                "|---|---|---|---|---|\n"
                "| 80 | HTTP | Unencrypted (Plaintext) | Insecure for sensitive data | Web browsing (legacy / redirects) |\n"
                "| 443 | HTTPS | Encrypted (TLS/SSL) | Secure | Secure web traffic, APIs, banking |\n"
                "| 53 | DNS | Unencrypted (UDP/TCP) | Standard | Domain name resolution |\n"
                "| 3389 | RDP | Encrypted (Proprietary) | High security risk if exposed to public | Remote Desktop Protocol |"
            )
            summary = (
                f"Bhai, **Port 80 aur Port 443** dono web traffic ke standard networking gates hain:\n\n"
                f"{table}\n\n"
                f"- **Port 80 (HTTP)**: Ye unencrypted data bhejta hai. Koi bhi packet sniffer ya attacker network me data read kar sakta hai.\n"
                f"- **Port 443 (HTTPS)**: Ye TLS/SSL certificate se end-to-end encrypt hota hai. Aajkal modern internet par 99% websites 443 use karti hain.\n"
                f"- **Safe vs Unsafe**: Apne local machine par Port 80/443 open hona tabhi zaroori hai agar aap local web server (jaise Apache, Nginx, ya FastAPI) chala rahe ho. Agar koi web server nahi chala rahe, toh ye band hone chahiye."
            )
            return {
                "issue_id": "EXP-PORT-COMPARE",
                "root_cause": "Network port concepts & protocol security comparison",
                "intent": "TECHNICAL_EXPLANATION",
                "risk_level": "LOW",
                "risk_color": "CYAN",
                "summary": summary,
                "actions": [],
                "selected_tools": [],
                "verification_command": "$true",
                "requires_confirmation": False
            }

        # 2c. KRONOS Features & Capabilities Overview
        if any(w in p_lower for w in ["what can you do", "kronos features", "tum kya kar", "kya kar sakta", "features", "capabilities", "kronos kya hai"]):
            table = (
                "| Capability | Key Commands / TUIs | Description |\n"
                "|---|---|---|\n"
                "| System Health & Doctor | `/doctor`, `/boost` | 10-Point deep system audit, disk cleaner & RAM optimizer |\n"
                "| Live Resource Monitoring | `/top`, `/specs` | Live task monitor, CPU/RAM hog detection & hardware card |\n"
                "| Network & Connectivity | `/wifi`, `/ports`, `/band` | Wi-Fi radar, packet latency test, listening ports audit |\n"
                "| Security & Hardening | `/firewall`, `/debloat` | Defender profiles audit, privacy & telemetry optimization |\n"
                "| File & App Management | `/open <#>`, `/tree`, `/apps` | Interactive app launcher, folder navigator, WinGet manager |\n"
                "| Autonomous Troubleshooting | Natural query | Automated diagnostic playbooks with Level 2 safe autonomy |"
            )
            summary = (
                f"Bhai, KRONOS ek autonomous Windows Co-Pilot aur SysAdmin assistant hai. Main aapke system ko diagnose, optimize, aur recover karne me help karta hu:\n\n"
                f"{table}\n\n"
                f"Aap natural Hindi/English me sawal puch sakte ho (jaise *'internet slow hai'*, *'ram usage kyu high hai'*), ya seedha slash commands run kar sakte ho!"
            )
            return {
                "issue_id": "EXP-KRONOS-FEATURES",
                "root_cause": "KRONOS autonomous capabilities and feature breakdown",
                "intent": "KRONOS_FEATURE_EXPLANATION",
                "risk_level": "LOW",
                "risk_color": "CYAN",
                "summary": summary,
                "actions": [],
                "selected_tools": [],
                "verification_command": "$true",
                "requires_confirmation": False
            }

        # 3. KnowledgeBase Search Integration
        kb_results = KnowledgeBase.search(problem, limit=1)
        if kb_results:
            top_kb = kb_results[0]
            summary = (
                f"**{top_kb.title}**\n\n"
                f"{top_kb.content}\n\n"
                f"- *Domain*: {top_kb.domain}\n"
                f"- *Source*: {top_kb.source}"
            )
            return {
                "issue_id": top_kb.doc_id,
                "root_cause": f"Technical Knowledge Base article: {top_kb.title}",
                "intent": "TECHNICAL_EXPLANATION",
                "risk_level": "LOW",
                "risk_color": "CYAN",
                "summary": summary,
                "actions": [],
                "selected_tools": [],
                "verification_command": "$true",
                "requires_confirmation": False
            }

        # 4. Ambiguous / Insufficient Information Guard
        words = p_lower.split()
        if (len(words) <= 7 and any(w in p_lower for w in ["help", "kuch", "issue", "error", "problem", "kharaab", "dikkat", "samajh nahi"])) or p_lower in ["help", "kuch samajh nahi aa raha", "kuch samajh nahi aa raha help", "kuch samajh nahi"]:
            return {
                "issue_id": "SYS-CLARIFY-001",
                "root_cause": "Insufficient information to pinpoint root cause",
                "intent": "INSUFFICIENT_INFORMATION",
                "risk_level": "LOW",
                "risk_color": "CYAN",
                "summary": "Bhai, aapko system me kya problem aa rahi hai? Thoda specific batao (jaise internet nahi chal raha, CPU 100% hai, sound gayab hai, ya koi specific error code aa raha hai?), taaki main exact diagnostic chala saku.",
                "actions": [],
                "selected_tools": [],
                "verification_command": "$true",
                "requires_confirmation": False
            }

        # 5. Fallback to standard deterministic diagnosis
        tool_calls = [{"tool_id": "system.inspect_resources", "arguments": {"limit": 8}}]
        comp = ToolExecutor.compile_tool_calls(tool_calls)
        actions = [{"description": a["description"], "command": a["command"]} for a in comp.actions]
        return {
            "issue_id": "SYS-GEN-001",
            "root_cause": "General system telemetry inspection",
            "intent": "SYSTEM_INFO_REQUEST",
            "risk_level": "LOW",
            "risk_color": "GREEN",
            "summary": "Bhai, aapke system ki live telemetry aur resource state inspect kar rahe hain:",
            "actions": actions,
            "verification_command": "$true",
            "requires_confirmation": False
        }
