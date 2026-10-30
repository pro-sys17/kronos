"""
KRONOS Autonomous Skills Engine
Specialized problem-solving domain playbooks for Windows sysadmin & endpoint healing.
"""

from typing import Dict, Any, List, Optional
import re

class SkillPlaybook:
    def __init__(
        self,
        skill_id: str,
        name: str,
        description: str,
        triggers: List[str],
        guidance: str,
        default_actions: List[Dict[str, str]],
        default_verification: str
    ):
        self.skill_id = skill_id
        self.name = name
        self.description = description
        self.triggers = triggers
        self.guidance = guidance
        self.default_actions = default_actions
        self.default_verification = default_verification

    def matches(self, query: str) -> bool:
        q = query.lower()
        for t in self.triggers:
            if re.search(r"\b" + re.escape(t) + r"\b", q, re.IGNORECASE) or t.lower() in q:
                return True
        return False


SKILLS: List[SkillPlaybook] = [
    SkillPlaybook(
        skill_id="SKILL-CRASH-BSOD",
        name="BSOD & System Crash Root-Cause Analyzer",
        description="Diagnoses kernel panics, bugchecks, minidumps, and driver crash logs.",
        triggers=[
            "bsod", "blue screen", "crash", "restarted unexpectedly", "bugcheck", 
            "kernel", "freeze", "hang ho gaya", "band ho gaya", "minidump", "event 41"
        ],
        guidance=(
            "The user is dealing with system crashes or BSOD.\n"
            "- Check Event Log for Event ID 41 (Kernel-Power) and Event ID 1001 (BugCheck).\n"
            "- Query C:\\Windows\\Minidump for recent .dmp files.\n"
            "- Check for recently failing drivers with Get-CimInstance Win32_PnPEntity -Filter \"ConfigManagerErrorCode != 0\".\n"
            "- Output must be concise and tabular."
        ),
        default_actions=[
            {
                "description": "Inspect recent Kernel-Power & BugCheck events (Event ID 41/1001)",
                "command": "Get-WinEvent -FilterHashtable @{LogName='System'; Id=41,1001} -MaxEvents 5 -ErrorAction SilentlyContinue | Select-Object TimeCreated, Id, @{N='Detail';E={$_.Message.Split(\"`n\")[0]}} | Format-Table -AutoSize"
            },
            {
                "description": "Scan for recently generated crash minidumps",
                "command": "Get-ChildItem -Path 'C:\\Windows\\Minidump' -Filter *.dmp -ErrorAction SilentlyContinue | Select-Object Name, Length, LastWriteTime | Format-Table -AutoSize"
            },
            {
                "description": "Identify hardware devices reporting driver error codes",
                "command": "Get-CimInstance Win32_PnPEntity -Filter 'ConfigManagerErrorCode != 0' -ErrorAction SilentlyContinue | Select-Object Name, DeviceID, ConfigManagerErrorCode | Format-Table -AutoSize"
            }
        ],
        default_verification="(Get-CimInstance Win32_PnPEntity -Filter 'ConfigManagerErrorCode != 0' -ErrorAction SilentlyContinue).Count -ge 0"
    ),

    SkillPlaybook(
        skill_id="SKILL-PERF-OPTIMIZER",
        name="Performance & Resource Leak Surgeon",
        description="Pinpoints CPU/RAM hogs, disk queue saturation, and thermal throttling.",
        triggers=[
            "slow", "lag", "hang", "freeze", "cpu", "ram", "memory", "100% disk", 
            "task manager", "heavy", "stuck", "laptop garam", "overheating", "fan loud", "speed up"
        ],
        guidance=(
            "The user has performance degradation, high CPU, or memory bottlenecks.\n"
            "- Identify top 5 CPU consuming processes using Get-Process sorted by CPU.\n"
            "- Identify top 5 working set (RAM) consuming processes in MB.\n"
            "- Check free physical memory percentage and drive space.\n"
            "- Safe cleanup: user temp folder purge."
        ),
        default_actions=[
            {
                "description": "Identify top 5 CPU-intensive processes",
                "command": "Get-Process | Sort-Object CPU -Descending | Select-Object -First 5 ProcessName, Id, @{N='CPU(s)';E={[math]::Round($_.CPU,1)}}, @{N='RAM(MB)';E={[math]::Round($_.WorkingSet64/1MB,1)}} | Format-Table -AutoSize"
            },
            {
                "description": "Identify top 5 Memory-intensive processes",
                "command": "Get-Process | Sort-Object WorkingSet64 -Descending | Select-Object -First 5 ProcessName, Id, @{N='RAM(MB)';E={[math]::Round($_.WorkingSet64/1MB,1)}} | Format-Table -AutoSize"
            },
            {
                "description": "Display storage volumes with free space capacity",
                "command": "Get-PSDrive -PSProvider FileSystem | Select-Object Name, @{N='Used(GB)';E={[math]::Round($_.Used/1GB,2)}}, @{N='Free(GB)';E={[math]::Round($_.Free/1GB,2)}} | Format-Table -AutoSize"
            }
        ],
        default_verification="$true"
    ),

    SkillPlaybook(
        skill_id="SKILL-NETWORK-SURGEON",
        name="Deep Network Surgeon & Latency Healer",
        description="DNS benchmark, Winsock rebuild, Wi-Fi driver power fix, packet loss triage.",
        triggers=[
            "wifi", "internet", "dns", "ping", "disconnect", "packet loss", "no internet", 
            "net nahi chal raha", "slow internet", "wifi dropping", "limited access", "ip conflict"
        ],
        guidance=(
            "The user is experiencing network connectivity, DNS, or adapter dropouts.\n"
            "- Flush DNS and reset ARP cache.\n"
            "- Test DNS resolution against Cloudflare (1.1.1.1) and Google (8.8.8.8).\n"
            "- Check network adapter status and active link speeds.\n"
            "- If needed, reset Winsock and TCP/IP stack."
        ),
        default_actions=[
            {
                "description": "Flush local DNS resolver cache",
                "command": "Clear-DnsClientCache; Write-Output 'DNS Cache Flushed'"
            },
            {
                "description": "Measure latency & connectivity to Cloudflare (1.1.1.1) and Google (8.8.8.8)",
                "command": "Test-NetConnection -ComputerName 1.1.1.1 -InformationLevel Detailed | Select-Object ComputerName, PingSucceeded, RoundTripTime | Format-Table -AutoSize"
            },
            {
                "description": "Verify physical & wireless network adapter link states",
                "command": "Get-NetAdapter -ErrorAction SilentlyContinue | Select-Object Name, InterfaceDescription, Status, LinkSpeed | Format-Table -AutoSize"
            }
        ],
        default_verification="(Test-Connection -ComputerName 1.1.1.1 -Count 1 -Quiet) -eq $true"
    ),

    SkillPlaybook(
        skill_id="SKILL-UPDATE-HEALER",
        name="Windows Update Corrupted Cache Healer",
        description="Resolves stuck update downloads, error codes 0x80070002, 0x80240034, and BITS hang.",
        triggers=[
            "update", "windows update", "0x80", "download stuck", "update fail", 
            "kb update", "installing 0%", "bits", "softwaredistribution", "pending update"
        ],
        guidance=(
            "The user has Windows Update failures or wants update diagnostics.\n"
            "- If viewing updates: use Get-HotFix | Select-Object -First 10 HotFixID, Description, InstalledOn | Format-Table -AutoSize.\n"
            "- If repairing stuck updates: stop wuauserv and BITS, reset state, restart cleanly."
        ),
        default_actions=[
            {
                "description": "Inspect latest 10 installed Windows Hotfix patches",
                "command": "Get-HotFix | Sort-Object InstalledOn -Descending -ErrorAction SilentlyContinue | Select-Object -First 10 HotFixID, Description, InstalledOn | Format-Table -AutoSize"
            },
            {
                "description": "Verify health status of Windows Update and BITS services",
                "command": "Get-Service -Name wuauserv, BITS, cryptsvc, trustedinstaller -ErrorAction SilentlyContinue | Select-Object Name, DisplayName, Status, StartType | Format-Table -AutoSize"
            }
        ],
        default_verification="(Get-Service wuauserv -ErrorAction SilentlyContinue).Status -ne 'Faulted'"
    ),

    SkillPlaybook(
        skill_id="SKILL-SECURITY-HUNTER",
        name="Malware & Stealth Persistence Hunter",
        description="Audits suspicious listening ports, autoruns, and anomalous scheduled tasks.",
        triggers=[
            "virus", "malware", "hacked", "ports", "listening", "suspicious", "autorun", 
            "startup", "trojan", "miner", "crypto", "spyware", "security audit"
        ],
        guidance=(
            "The user requests a security check or persistence audit.\n"
            "- List active listening TCP ports and associated process names.\n"
            "- Inspect registry Run & RunOnce autostart keys.\n"
            "- Identify scheduled tasks running from suspicious directories (e.g. Temp or AppData).\n"
            "- Never delete critical files; only identify and report findings."
        ),
        default_actions=[
            {
                "description": "Audit active listening TCP ports and owning processes",
                "command": "Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue | Select-Object -First 10 LocalAddress, LocalPort, OwningProcess | Format-Table -AutoSize"
            },
            {
                "description": "Inspect user and machine autorun registry startup programs",
                "command": "Get-ItemProperty 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Run' -ErrorAction SilentlyContinue | Format-List"
            },
            {
                "description": "Scan scheduled tasks executing out of user AppData or Temp folders",
                "command": "Get-ScheduledTask -ErrorAction SilentlyContinue | Where-Object { $_.Actions.Execute -match 'AppData|Temp' } | Select-Object -First 5 TaskName, TaskPath | Format-Table -AutoSize"
            }
        ],
        default_verification="$true"
    ),

    SkillPlaybook(
        skill_id="SKILL-HARDWARE-INSPECTOR",
        name="Hardware & S.M.A.R.T. Health Inspector",
        description="Inspects battery wear, physical drive health, memory specs, and BIOS info.",
        triggers=[
            "battery", "battery health", "disk health", "smart", "hard disk", "ssd", 
            "specs", "specification", "ram slot", "processor", "bios", "hardware", "recent files"
        ],
        guidance=(
            "The user wants hardware health, specifications, or recent files.\n"
            "- For recent files: Get-ChildItem -Path ([Environment]::GetFolderPath('Recent')) -File -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 10 BaseName, LastWriteTime | Format-Table -AutoSize.\n"
            "- For battery health: generate battery report or query Win32_Battery.\n"
            "- For disk health: Get-PhysicalDisk | Select-Object DeviceId, FriendlyName, MediaType, OperationalStatus, HealthStatus.\n"
            "- For specs: query Win32_Processor, Win32_OperatingSystem cleanly."
        ),
        default_actions=[
            {
                "description": "Inspect physical drive health status & media type (SSD/HDD)",
                "command": "Get-PhysicalDisk -ErrorAction SilentlyContinue | Select-Object DeviceId, FriendlyName, MediaType, OperationalStatus, HealthStatus | Format-Table -AutoSize"
            },
            {
                "description": "Retrieve comprehensive CPU, RAM, and OS hardware profile",
                "command": "Get-CimInstance Win32_OperatingSystem | Select-Object Caption, Version, OSArchitecture, TotalVisibleMemorySize, FreePhysicalMemory | Format-List"
            }
        ],
        default_verification="$true"
    )
]

class SkillsRegistry:
    """
    Central router and guidance engine for KRONOS Problem-Solving Skills.
    """

    @classmethod
    def match_skill(cls, query: str) -> Optional[SkillPlaybook]:
        for skill in SKILLS:
            if skill.matches(query):
                return skill
        return None

    @classmethod
    def get_skill_by_id(cls, skill_id: str) -> Optional[SkillPlaybook]:
        for skill in SKILLS:
            if skill.skill_id.lower() == skill_id.lower():
                return skill
        return None

    @classmethod
    def get_all_skills(cls) -> List[SkillPlaybook]:
        return SKILLS

    @classmethod
    def build_system_context(cls, query: str) -> str:
        skill = cls.match_skill(query)
        if not skill:
            return ""
        return (
            f"\n[ACTIVE PROBLEM-SOLVING SKILL: {skill.name}]\n"
            f"Skill Objective: {skill.description}\n"
            f"Expert Playbook Guidance:\n{skill.guidance}\n"
        )

