import re
from typing import List, Tuple, Any

class CommandGuardrail:
    """
    KRONOS PC Control Safety Engine for Professor.
    Guarantees full administrative freedom to control the Windows PC via natural language prompts,
    while protecting against catastrophic self-destruct accidents (e.g., formatting system drives,
    wiping C:\\Windows, deleting boot records).
    """
    
    # Strictly prohibited catastrophic self-destruct operations
    DENY_LIST = [
        r"(?<!Format-)\bformat(?:\.exe|\.com)?\s+[a-zA-Z]:",
        r"\bFormat-Volume\b",
        r"\bInitialize-Disk\b",
        r"\bClear-Disk\b",
        r"\bdiskpart(?:\.exe)?\b",
        r"\bvssadmin(?:\.exe)?\s+delete",
        r"\bbcdedit(?:\.exe)?\s+/delete",
        r"\breg(?:\.exe)?\s+delete\s+.*system",
        r"\bRemove-Item\s+.*(?:c:\\windows|[a-zA-Z]:\\?)",
        r"\brmdir(?:\.exe)?\s+.*(?:c:\\windows|[a-zA-Z]:\\?)",
        r"\bdel(?:ete)?(?:\.exe)?\s+.*(?:c:\\windows|[a-zA-Z]:\\?)",
        r"\bcipher(?:\.exe)?\s+/w",
        r"Set-NetFirewallProfile.*-Enabled\s+False",
        r"\bnet(?:\.exe)?\s+user\s+.*\/add",
        r"downloadstring",
        r"invoke-webrequest.*\.exe",
        r"\bpowershell(?:\.exe)?\s+.*-(?:e|enc|encodedcommand)\b",
        r"(?:Stop-Process|taskkill).*(?:svchost|csrss|lsass|smss|wininit|winlogon|services\.exe)",
        r"downloadstring.*\|\s*(?:iex|powershell)",
        r"\bcurl\b.*\|\s*(?:iex|powershell)",
        r"\bwget\b.*\|\s*(?:iex|powershell)"
    ]

    @classmethod
    def validate_command(cls, command: str) -> Tuple[bool, str]:
        """
        Validates an individual command against safety rules.
        Allows full administrative Windows control while blocking catastrophic self-destruct patterns.
        Returns: (is_allowed, reason)
        """
        if not command or not isinstance(command, str):
            return False, "Empty or invalid command specification"

        cmd_clean = command.strip()
        if not cmd_clean:
            return False, "Empty command string"
        
        # Check Deny List for catastrophic self-destruct patterns
        for pattern in cls.DENY_LIST:
            if re.search(pattern, cmd_clean, re.IGNORECASE):
                return False, f"Prohibited instruction pattern detected: {pattern}"

        return True, "Passed safety validation"

    @classmethod
    def sanitize_plan(cls, actions: List[Any]) -> Tuple[List[dict], str]:
        """
        Sanitizes a list of actions and returns verified actions.
        Ensures dangerous self-destruct commands are neutralized while
        preserving all legitimate system administration and control commands.
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
