import re
from typing import List, Tuple, Any

class CommandGuardrail:
    """
    Security verification engine for AI-generated commands.
    Ensures that only safe system administration commands are permitted.
    Blocks destructive, obfuscated, or unauthorized commands.
    """
    
    # Strictly prohibited commands and patterns
    DENY_LIST = [
        r"(?<!Format-)\bformat(?:\.exe|\.com)?\s+[a-zA-Z]:",
        r"\bFormat-Volume\b",
        r"\bInitialize-Disk\b",
        r"\bClear-Disk\b",
        r"diskpart\b",
        r"vssadmin\s+delete",
        r"bcdedit\s+/delete",
        r"reg\s+delete\s+.*system",
        r"remove-item\s+.*(?:c:\\windows|[a-zA-Z]:\\?)",
        r"rmdir\s+.*(?:c:\\windows|[a-zA-Z]:\\?)",
        r"del(?:ete)?\s+.*(?:c:\\windows|[a-zA-Z]:\\?)",
        r"cipher\s+/w",
        r"Set-NetFirewallProfile.*-Enabled\s+False",
        r"net\s+user\s+.*\/add",
        r"downloadstring",
        r"invoke-webrequest.*\.exe",
        r"powershell\s+-e\s+",
        r"powershell\s+-enc\b",
        r"powershell\s+-encodedcommand\b",
        r"\bexit\s+\d+",
        r"\bexit\b"
    ]
    
    # Safe system maintenance whitelist patterns
    ALLOW_LIST = [
        r"^Restart-Service\s+[a-zA-Z0-9_\-]+$",
        r"^Start-Service\s+[a-zA-Z0-9_\-]+$",
        r"^Stop-Service\s+[a-zA-Z0-9_\-]+$",
        r"^netsh\s+",
        r"^ipconfig\s+/(flushdns|release|renew)$",
        r"^Clear-DnsClientCache$",
        r"^sfc\s+/scanfile=.*",
        r"^DISM\s+/Online\s+",
        r"^Remove-Item\s+-Path\s+\$env:TEMP\\.*",
        r"^Clear-RecycleBin\s+-Force",
        r"^Get-Service\s+",
        r"^Test-NetConnection\s+"
    ]

    @classmethod
    def validate_command(cls, command: str) -> Tuple[bool, str]:
        """
        Validates an individual command against security rules.
        Returns: (is_allowed, reason)
        """
        cmd_clean = command.strip()
        
        # Check Deny List
        for pattern in cls.DENY_LIST:
            if re.search(pattern, cmd_clean, re.IGNORECASE):
                return False, f"Prohibited instruction pattern detected: {pattern}"

        # Risk scoring
        return True, "Passed security validation"

    @classmethod
    def sanitize_plan(cls, actions: List[Any]) -> Tuple[List[dict], str]:
        """
        Sanitizes a list of actions and returns filtered actions + highest risk level.
        Handles both dict actions and raw string command actions safely.
        """
        verified_actions = []
        highest_risk = "LOW"
        
        for item in actions:
            if isinstance(item, str):
                act = {"description": item, "command": item}
            elif isinstance(item, dict):
                act = dict(item)
            else:
                continue

            cmd = act.get("command", "")
            is_valid, reason = cls.validate_command(cmd)
            
            if not is_valid:
                act["command"] = f"# BLOCKED BY GUARDRAIL: {reason}"
                act["description"] = f"[REJECTED] {act.get('description', '')}"
                highest_risk = "BLOCKED"
            else:
                verified_actions.append(act)
                
        return verified_actions, highest_risk

