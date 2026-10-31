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
        r"\bdiskpart(?:\.exe)?\b",
        r"\bvssadmin(?:\.exe)?\s+delete",
        r"\bbcdedit(?:\.exe)?\s+/delete",
        r"\breg(?:\.exe)?\s+delete\s+.*system",
        r"\breg(?:\.exe)?\s+add\b",
        r"\bRemove-Item\s+.*(?:c:\\windows|[a-zA-Z]:\\?)",
        r"\brmdir(?:\.exe)?\s+.*(?:c:\\windows|[a-zA-Z]:\\?)",
        r"\bdel(?:ete)?(?:\.exe)?\s+.*(?:c:\\windows|[a-zA-Z]:\\?)",
        r"\bcipher(?:\.exe)?\s+/w",
        r"Set-NetFirewallProfile.*-Enabled\s+False",
        r"\bnet(?:\.exe)?\s+user\s+.*\/add",
        r"downloadstring",
        r"invoke-webrequest.*\.exe",
        r"\bpowershell(?:\.exe)?\s+.*-(?:e|enc|encodedcommand)\b",
        r"\b(?:Invoke-Expression|iex)\b",
        r"\bStart-Process\b",
        r"\bcmd(?:\.exe)?\s+(?:/c|/k)\b",
        r"\bcertutil(?:\.exe)?\b",
        r"\bSet-ExecutionPolicy\b",
        r"\b(?:Stop-Computer|Restart-Computer)\b",
        r"\bcurl\b.*\|\s*(?:iex|powershell)",
        r"\bwget\b.*\|\s*(?:iex|powershell)",
        r"\bexit\s+\d+",
        r"\bexit\b",
        r"(?:Stop-Process|taskkill).*(?:svchost|csrss|lsass|smss|wininit|winlogon|services\.exe)"
    ]
    
    # Safe system maintenance whitelist patterns
    ALLOW_LIST = [
        r"^Restart-Service\s+[a-zA-Z0-9_\-]+(\s+-Force)?(?:;\s*.*)?$",
        r"^Start-Service\s+[a-zA-Z0-9_\-]+(?:;\s*.*)?$",
        r"^Stop-Service\s+[a-zA-Z0-9_\-]+(\s+-Force)?(?:;\s*.*)?$",
        r"^netsh\s+(?:advfirewall|winsock|int\s+ip)\s+",
        r"^ipconfig\s+/(?:flushdns|release|renew)(?:;\s*.*)?$",
        r"^Clear-DnsClientCache(?:;\s*.*)?$",
        r"^sfc\s+/scanfile=.*$",
        r"^DISM\s+/Online\s+",
        r"^Remove-Item\s+-Path\s+[\"']?\$env:TEMP\\.*[\"']?(?:\s+-Recurse)?(?:\s+-Force)?(?:\s+-ErrorAction\s+\w+)?(?:;\s*.*)?$",
        r"^Clear-RecycleBin\s+-Force$",
        r"^Get-Service(?:\s+.*)?$",
        r"^Test-NetConnection\s+",
        r"^Get-CimInstance\s+",
        r"^Get-Process\s+",
        r"^Get-PSDrive\s+",
        r"^Get-NetAdapter\s+",
        r"^Resolve-DnsName\s+",
        r"^Get-NetTCPConnection\s+",
        r"^Get-WinEvent\s+",
        r"^\$startTime\s*=\s*\(Get-Date\)\.AddHours.*",
        r"^Get-PnpDevice\s+",
        r"^\$errs\s*=\s*@\(Get-PnpDevice.*",
        r"^Get-ChildItem\s+",
        r"^Get-NetIPAddress\s+",
        r"^Stop-Process\s+-Id\s+\d+(\s+-Force)?(?:;\s*.*)?$",
        r"^if\s*\([^)]+\)\s*\{\s*(?:Enable|Disable)-NetAdapter\s+",
        r"^Set-NetFirewallProfile\s+-Profile\s+['\"][^'\"]+['\"]\s+-Enabled\s+['\"][^'\"]+['\"](?:;\s*.*)?$",
        r"^if\s*\(Test-Path\s+['\"][^'\"]+['\"]\)\s*\{\s*Remove-Item\s+-Path\s+",
        r"^powercfg\s+",
        r"^Show-[a-zA-Z0-9]+TUI$",
        r"^Install-KronosGlobalCLI$",
        r"^Toggle-VoiceEngine$",
        r"^\$true$",
        r"^Write-Output\s+.*$"
    ]

    @classmethod
    def validate_command(cls, command: str) -> Tuple[bool, str]:
        """
        Validates an individual command against security rules.
        Enforces:
        1. Explicit Deny List check (blocks destructive/injection patterns)
        2. Strict Allow List check (rejects arbitrary unwhitelisted shell strings)
        Returns: (is_allowed, reason)
        """
        if not command or not isinstance(command, str):
            return False, "Empty or invalid command specification"

        cmd_clean = command.strip()
        if not cmd_clean:
            return False, "Empty command string"
        
        # 1. Check Deny List
        for pattern in cls.DENY_LIST:
            if re.search(pattern, cmd_clean, re.IGNORECASE):
                return False, f"Prohibited instruction pattern detected: {pattern}"

        # 2. Strict Allow List Enforcement
        matched_allow = False
        for pattern in cls.ALLOW_LIST:
            if re.search(pattern, cmd_clean, re.IGNORECASE):
                matched_allow = True
                break

        if not matched_allow:
            return False, "Command does not match strict system maintenance allowlist"

        return True, "Passed security validation"

    @classmethod
    def sanitize_plan(cls, actions: List[Any]) -> Tuple[List[dict], str]:
        """
        Sanitizes a list of actions and returns filtered actions + highest risk level.
        Rejects non-conforming or arbitrary shell instructions.
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
