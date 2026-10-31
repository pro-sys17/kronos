"""
KRONOS Advanced Skills Engine (Level 2 Controlled Autonomy)
Intent-aware, ranked problem-solving domain playbooks for Windows sysadmin & endpoint healing.
Each skill specifies diagnostic procedures, permitted registered tools, root causes, and verification.
"""

from typing import Dict, Any, List, Optional, Tuple
import re

class SkillPlaybook:
    def __init__(
        self,
        skill_id: str,
        name: str,
        description: str,
        supported_intents: List[str],
        natural_triggers: List[str],
        example_queries: List[str],
        required_system_context: List[str],
        diagnostic_procedure: List[str],
        permitted_tools: List[str],
        remediation_tools: List[str],
        potential_root_causes: List[str],
        risk_level: str,
        confirmation_required: bool,
        verification_steps: str,
        recovery_procedure: str
    ):
        self.skill_id = skill_id
        self.name = name
        self.description = description
        self.supported_intents = supported_intents
        self.natural_triggers = natural_triggers
        self.example_queries = example_queries
        self.required_system_context = required_system_context
        self.diagnostic_procedure = diagnostic_procedure
        self.permitted_tools = permitted_tools
        self.remediation_tools = remediation_tools
        self.potential_root_causes = potential_root_causes
        self.risk_level = risk_level.upper()
        self.confirmation_required = confirmation_required
        self.verification_steps = verification_steps
        self.recovery_procedure = recovery_procedure

    def calculate_relevance(self, query: str, intent: Optional[str] = None) -> float:
        """
        Calculates ranked relevance score (0.0 to 100.0) based on intent and lexical matching.
        """
        score = 0.0
        q_clean = query.lower().strip()

        # Intent alignment
        if intent and intent.upper() in [i.upper() for i in self.supported_intents]:
            score += 25.0

        # Trigger matching
        for trigger in self.natural_triggers:
            t = trigger.lower()
            if re.search(r"\b" + re.escape(t) + r"\b", q_clean):
                score += 35.0
                break
            elif t in q_clean:
                score += 15.0

        # Example query similarity
        for ex in self.example_queries:
            if ex.lower() in q_clean or q_clean in ex.lower():
                score += 20.0
                break

        return min(100.0, score)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "skill_id": self.skill_id,
            "name": self.name,
            "description": self.description,
            "supported_intents": self.supported_intents,
            "diagnostic_procedure": self.diagnostic_procedure,
            "permitted_tools": self.permitted_tools,
            "remediation_tools": self.remediation_tools,
            "potential_root_causes": self.potential_root_causes,
            "risk_level": self.risk_level,
            "confirmation_required": self.confirmation_required,
            "verification_steps": self.verification_steps,
            "recovery_procedure": self.recovery_procedure
        }


# ==============================================================================
# SKILLS CATALOG — 13 MODULAR DOMAINS
# ==============================================================================

SKILLS: List[SkillPlaybook] = [
    # 1. Network Troubleshooting
    SkillPlaybook(
        skill_id="SKILL-NET-DIAG",
        name="Network Interface & Gateway Diagnostic",
        description="Diagnoses network adapter disconnections, default gateway unreachability, and DHCP issues.",
        supported_intents=["TROUBLESHOOTING_REQUEST", "ACTION_REQUEST", "FOLLOW_UP_REQUEST"],
        natural_triggers=[
            "network", "wifi", "ethernet", "adapter", "disconnected", "no internet", 
            "gateway", "dhcp", "ip conflict", "net nahi chal raha", "limited access"
        ],
        example_queries=["Mera internet disconnected dikha raha hai", "Default gateway unreachable", "Network adapter disabled hai"],
        required_system_context=["ActiveAdapters", "InternetStatus"],
        diagnostic_procedure=[
            "1. Inspect active network adapter link states with network.inspect_adapters",
            "2. Ping default gateway and DNS targets with network.ping",
            "3. Query DHCP lease status and IP assignment"
        ],
        permitted_tools=["network.inspect_adapters", "network.ping", "network.test_dns"],
        remediation_tools=["network.renew_ip", "network.set_adapter_state", "network.flush_dns"],
        potential_root_causes=["Stale DHCP lease", "Disabled network adapter", "Gateway timeout", "Cable or Wi-Fi disconnection"],
        risk_level="MODERATE",
        confirmation_required=True,
        verification_steps="network.ping target='1.1.1.1'",
        recovery_procedure="Enable adapter and reconnect network profile."
    ),

    # 2. Internet Connectivity & Speed
    SkillPlaybook(
        skill_id="SKILL-NET-SPEED",
        name="Internet Latency & Packet Loss Triage",
        description="Pinpoints bandwidth congestion, high ping latency, and connection throttling.",
        supported_intents=["TROUBLESHOOTING_REQUEST", "TECHNICAL_EXPLANATION"],
        natural_triggers=[
            "slow internet", "ping high", "latency", "packet loss", "slow net", 
            "internet slow hai", "download speed kam hai", "buffer", "lag in games"
        ],
        example_queries=["Mera internet slow hai", "High ping in online games", "Websites opening very slow"],
        required_system_context=["ActiveAdapters", "InternetStatus"],
        diagnostic_procedure=[
            "1. Probe ICMP roundtrip latency to 1.1.1.1 and 8.8.8.8 using network.ping",
            "2. Inspect active bandwidth-consuming background processes using system.inspect_resources",
            "3. Audit listening TCP sockets and network sockets using network.list_ports"
        ],
        permitted_tools=["network.ping", "network.inspect_adapters", "system.inspect_resources", "network.list_ports"],
        remediation_tools=["network.flush_dns", "network.renew_ip"],
        potential_root_causes=["Background update download", "DNS server slow", "Wi-Fi channel interference"],
        risk_level="LOW",
        confirmation_required=False,
        verification_steps="network.ping target='1.1.1.1'",
        recovery_procedure="No settings changed during latency audit."
    ),

    # 3. DNS Problems & Resolution
    SkillPlaybook(
        skill_id="SKILL-NET-DNS",
        name="DNS Cache & Resolution Resolver",
        description="Diagnoses host lookup failures (DNS_PROBE_FINISHED_NXDOMAIN) and resolves DNS cache congestion.",
        supported_intents=["TROUBLESHOOTING_REQUEST", "ACTION_REQUEST", "TECHNICAL_EXPLANATION"],
        natural_triggers=[
            "dns", "nxdomain", "server not found", "cannot resolve", "domain name", 
            "dns flush", "flushdns", "site nahi khul rahi", "dns problem"
        ],
        example_queries=["DNS flush karo", "Server not found error in browser", "DNS resolution failed"],
        required_system_context=["ActiveAdapters"],
        diagnostic_procedure=[
            "1. Test domain resolution against local DNS using network.test_dns",
            "2. Compare resolution against Cloudflare public resolver (1.1.1.1)",
            "3. Clear local DNS client cache if corrupted records detected"
        ],
        permitted_tools=["network.test_dns", "network.ping"],
        remediation_tools=["network.flush_dns"],
        potential_root_causes=["Stale DNS cache entry", "ISP DNS outage", "Corrupted resolver service"],
        risk_level="MODERATE",
        confirmation_required=True,
        verification_steps="network.test_dns domain='cloudflare.com'",
        recovery_procedure="DNS records repopulate dynamically."
    ),

    # 4. CPU and RAM Diagnostics
    SkillPlaybook(
        skill_id="SKILL-SYS-RESOURCES",
        name="CPU & RAM Resource Bottleneck Surgeon",
        description="Identifies rogue processes consuming 100% CPU, memory leaks, and thermal throttling.",
        supported_intents=["TROUBLESHOOTING_REQUEST", "SYSTEM_INFO_REQUEST", "ACTION_REQUEST"],
        natural_triggers=[
            "cpu", "ram", "memory", "100%", "high usage", "laptop garam", "fan loud", 
            "freeze", "lag", "hang ho raha hai", "task manager", "speed up"
        ],
        example_queries=["CPU 100% used hai", "RAM kitni free hai", "Laptop freeze ho raha hai"],
        required_system_context=["TotalMemoryGB", "OSVersion"],
        diagnostic_procedure=[
            "1. Inspect real-time CPU & RAM consumption using system.inspect_resources",
            "2. Identify runaway processes exceeding thresholds",
            "3. Query recent Event Log crash events if system locked up"
        ],
        permitted_tools=["system.inspect_resources", "system.get_info", "eventlog.query_errors"],
        remediation_tools=["process.terminate", "storage.clean_temp"],
        potential_root_causes=["Runaway background task", "Browser memory leak", "Antivirus scan lock"],
        risk_level="MODERATE",
        confirmation_required=True,
        verification_steps="system.inspect_resources limit=5",
        recovery_procedure="Terminated applications can be relaunched manually."
    ),

    # 5. Disk and Storage Issues
    SkillPlaybook(
        skill_id="SKILL-STORAGE-HEADROOM",
        name="Disk Space & Storage Capacity Optimizer",
        description="Analyzes partition headroom, locates large files, and purges user temp files.",
        supported_intents=["TROUBLESHOOTING_REQUEST", "SYSTEM_INFO_REQUEST", "ACTION_REQUEST"],
        natural_triggers=[
            "disk", "storage", "c drive", "drive full", "space", "low disk space", 
            "cleanup", "temp", "junk", "disk bhar gaya", "space khali karo"
        ],
        example_queries=["C drive me space kam hai", "Clean temp files", "Check disk space"],
        required_system_context=["Drives"],
        diagnostic_procedure=[
            "1. Check volume capacities and percentage free headroom using storage.check_disks",
            "2. Safe purge of user temp files using storage.clean_temp",
            "3. Verify recovered space"
        ],
        permitted_tools=["storage.check_disks", "file.search"],
        remediation_tools=["storage.clean_temp"],
        potential_root_causes=["Windows temp files buildup", "Browser download cache", "Log file accumulation"],
        risk_level="MODERATE",
        confirmation_required=True,
        verification_steps="storage.check_disks",
        recovery_procedure="Temp files are permanently cleaned; user documents are never modified."
    ),

    # 6. Windows Services
    SkillPlaybook(
        skill_id="SKILL-SVC-MANAGER",
        name="Windows Service Supervisor & Health Manager",
        description="Inspects service runtimes, diagnoses startup failure, and safely restarts crashed daemons.",
        supported_intents=["TROUBLESHOOTING_REQUEST", "ACTION_REQUEST", "SYSTEM_INFO_REQUEST"],
        natural_triggers=[
            "service", "services", "audiocore", "wuauserv", "spooler", "bits", 
            "stopped service", "service chalu karo", "service restart karo"
        ],
        example_queries=["Windows Update service check karo", "Restart Spooler service", "Service status kya hai"],
        required_system_context=[],
        diagnostic_procedure=[
            "1. Query target service status and startup type using service.get_status",
            "2. Audit recent service crash events in Event Log with eventlog.query_errors",
            "3. Restart target service safely using service.restart"
        ],
        permitted_tools=["service.get_status", "eventlog.query_errors"],
        remediation_tools=["service.restart", "service.start", "service.stop"],
        potential_root_causes=["Service deadlock", "Unsatisfied dependency", "Process crash"],
        risk_level="MODERATE",
        confirmation_required=True,
        verification_steps="service.get_status",
        recovery_procedure="Rollback snapshot created before service restarts."
    ),

    # 7. Audio Troubleshooting
    SkillPlaybook(
        skill_id="SKILL-AUDIO-REPAIR",
        name="Audio Subsystem Deep Diagnostic & Reset",
        description="Fixes audio crackling, muted playback devices, and AudioSrv desynchronization.",
        supported_intents=["TROUBLESHOOTING_REQUEST", "ACTION_REQUEST"],
        natural_triggers=[
            "audio", "sound", "speaker", "volume", "mic", "earphone", "headphone", 
            "aawaz nahi aa rahi", "sound nahi aa rahi", "speaker band hai", "sound crackle"
        ],
        example_queries=["Speaker se aawaz nahi aa rahi", "Audio restart karo", "Sound not working"],
        required_system_context=[],
        diagnostic_procedure=[
            "1. Inspect AudioSrv and AudioEndpointBuilder status using service.get_status",
            "2. Scan for audio device driver errors using hardware.audit_devices",
            "3. Restart the core audio stack using audio.restart_subsystem"
        ],
        permitted_tools=["service.get_status", "hardware.audit_devices"],
        remediation_tools=["audio.restart_subsystem"],
        potential_root_causes=["AudioSrv stopped", "Endpoint builder desynchronization", "Exclusive mode lock"],
        risk_level="MODERATE",
        confirmation_required=True,
        verification_steps="service.get_status service_name='AudioSrv'",
        recovery_procedure="Audio services re-initialize default sound playback endpoints."
    ),

    # 8. Startup Optimization
    SkillPlaybook(
        skill_id="SKILL-STARTUP-OPT",
        name="Startup & Boot Performance Optimizer",
        description="Audits autorun entries, background boot delays, and high-impact startup items.",
        supported_intents=["TROUBLESHOOTING_REQUEST", "SYSTEM_INFO_REQUEST"],
        natural_triggers=[
            "startup", "boot", "slow boot", "start hone me time lagta hai", 
            "boot time", "autorun", "startup apps"
        ],
        example_queries=["Laptop start hone me bohot time leta hai", "Check startup apps", "Optimize boot"],
        required_system_context=["OSVersion", "TotalMemoryGB"],
        diagnostic_procedure=[
            "1. Inspect top processes and CPU load on startup using system.inspect_resources",
            "2. Query system specifications using system.get_info"
        ],
        permitted_tools=["system.inspect_resources", "system.get_info"],
        remediation_tools=["storage.clean_temp"],
        potential_root_causes=["Too many autostart programs", "Mechanical HDD fragmentation", "Corrupt temp cache"],
        risk_level="LOW",
        confirmation_required=False,
        verification_steps="system.get_info",
        recovery_procedure="No modifications made."
    ),

    # 9. Driver Diagnostics
    SkillPlaybook(
        skill_id="SKILL-DRIVER-AUDIT",
        name="Plug-and-Play & Device Driver Inspector",
        description="Scans device manager for hardware Code 10/28/43 errors and malfunctioning drivers.",
        supported_intents=["TROUBLESHOOTING_REQUEST", "SYSTEM_INFO_REQUEST"],
        natural_triggers=[
            "driver", "device", "yellow mark", "code 43", "code 10", "code 28", 
            "hardware error", "usb not working", "bluetooth nahi chal raha"
        ],
        example_queries=["Driver check karo", "Device manager me error aa raha hai", "USB port not detected"],
        required_system_context=[],
        diagnostic_procedure=[
            "1. Audit all Plug-and-Play devices for Degraded or Error status using hardware.audit_devices",
            "2. Query recent hardware crash events in System event log"
        ],
        permitted_tools=["hardware.audit_devices", "eventlog.query_errors"],
        remediation_tools=[],
        potential_root_causes=["Missing device driver", "Hardware failure", "Power-saving state lock"],
        risk_level="LOW",
        confirmation_required=False,
        verification_steps="hardware.audit_devices",
        recovery_procedure="Read-only diagnostic audit."
    ),

    # 10. Windows Defender and Firewall
    SkillPlaybook(
        skill_id="SKILL-SEC-FIREWALL",
        name="Windows Defender & Firewall Profile Cockpit",
        description="Inspects active security shield profiles, listening ports, and blocked outbound connections.",
        supported_intents=["TROUBLESHOOTING_REQUEST", "ACTION_REQUEST", "SYSTEM_INFO_REQUEST"],
        natural_triggers=[
            "firewall", "defender", "port", "ports", "antivirus", "blocked connection", 
            "firewall turn off", "firewall turn on", "security check"
        ],
        example_queries=["Firewall status check karo", "Listening ports dikhao", "Enable firewall"],
        required_system_context=[],
        diagnostic_procedure=[
            "1. Audit listening network ports using network.list_ports",
            "2. Check Defender Antivirus service status using service.get_status service_name='WinDefend'",
            "3. Update firewall state if requested with firewall.set_profile"
        ],
        permitted_tools=["network.list_ports", "service.get_status"],
        remediation_tools=["firewall.set_profile", "firewall.reset_rules"],
        potential_root_causes=["Blocked incoming port", "Firewall profile disabled", "WinDefend stopped"],
        risk_level="HIGH",
        confirmation_required=True,
        verification_steps="service.get_status service_name='WinDefend'",
        recovery_procedure="Firewall can be reset to factory defaults with firewall.reset_rules."
    ),

    # 11. Application Troubleshooting
    SkillPlaybook(
        skill_id="SKILL-APP-KILL",
        name="Hung Application & Unresponsive Process Terminus",
        description="Diagnoses hanging GUI programs and safely terminates unresponsive process threads.",
        supported_intents=["ACTION_REQUEST", "TROUBLESHOOTING_REQUEST"],
        natural_triggers=[
            "kill", "close", "terminate", "not responding", "hang", "band karo", 
            "chrome band karo", "force close", "kill process"
        ],
        example_queries=["Chrome kill kar do", "App not responding force close karo", "Kill process by PID"],
        required_system_context=[],
        diagnostic_procedure=[
            "1. Inspect target process PID and resource usage using system.inspect_resources",
            "2. Terminate rogue process using process.terminate"
        ],
        permitted_tools=["system.inspect_resources"],
        remediation_tools=["process.terminate"],
        potential_root_causes=["Deadlocked thread", "Infinite loop", "GPU process freeze"],
        risk_level="MODERATE",
        confirmation_required=True,
        verification_steps="system.inspect_resources limit=5",
        recovery_procedure="App can be relaunched by user."
    ),

    # 12. Windows Update
    SkillPlaybook(
        skill_id="SKILL-WUA-HEALER",
        name="Windows Update Cache & BITS Healer",
        description="Resolves stuck update downloads, error codes 0x80070002, and BITS service failure.",
        supported_intents=["TROUBLESHOOTING_REQUEST", "ACTION_REQUEST"],
        natural_triggers=[
            "update", "windows update", "0x80", "download stuck", "update fail", 
            "kb update", "installing 0%", "bits", "softwaredistribution"
        ],
        example_queries=["Windows update stuck hai 0%", "Error 0x80070002 fix karo", "Update service restart karo"],
        required_system_context=[],
        diagnostic_procedure=[
            "1. Verify wuauserv and BITS service status using service.get_status",
            "2. Audit recent Update error events in Event Log with eventlog.query_errors",
            "3. Restart Windows Update service cleanly using service.restart"
        ],
        permitted_tools=["service.get_status", "eventlog.query_errors"],
        remediation_tools=["service.restart", "storage.clean_temp"],
        potential_root_causes=["SoftwareDistribution cache lock", "BITS stopped", "Corrupted package download"],
        risk_level="MODERATE",
        confirmation_required=True,
        verification_steps="service.get_status service_name='wuauserv'",
        recovery_procedure="Rollback snapshot saved before service restart."
    ),

    # 13. System Stability & Integrity
    SkillPlaybook(
        skill_id="SKILL-STABILITY-SFC",
        name="System File Integrity & Component Store Repair",
        description="Diagnoses corrupt OS binaries, DISM component store corruption, and BSOD bugchecks.",
        supported_intents=["TROUBLESHOOTING_REQUEST", "ACTION_REQUEST"],
        natural_triggers=[
            "bsod", "blue screen", "crash", "bugcheck", "sfc", "dism", "corrupt", 
            "system files", "event 41", "kernel power", "restarted unexpectedly"
        ],
        example_queries=["Blue screen aaya tha", "Check system file corruption", "Run DISM check"],
        required_system_context=["OSVersion", "Architecture"],
        diagnostic_procedure=[
            "1. Audit recent Kernel-Power & BugCheck events in Event Log with eventlog.query_errors",
            "2. Scan Component Store health using system.run_dism_check",
            "3. If corruption detected, run system.run_dism_restore with administrator confirmation"
        ],
        permitted_tools=["eventlog.query_errors", "system.run_dism_check", "hardware.audit_devices"],
        remediation_tools=["system.run_dism_restore"],
        potential_root_causes=["Corrupt DLL or driver", "Unexpected power loss", "Storage block error"],
        risk_level="HIGH",
        confirmation_required=True,
        verification_steps="system.run_dism_check",
        recovery_procedure="System restore point and service snapshot saved prior to repair."
    )
]

class SkillsRegistry:
    """
    Ranked Skill Matcher and Diagnostic Context Provider.
    """

    @classmethod
    def match_skill(cls, query: str, intent: Optional[str] = None) -> Optional[SkillPlaybook]:
        scored_skills: List[Tuple[float, SkillPlaybook]] = []

        for skill in SKILLS:
            score = skill.calculate_relevance(query, intent=intent)
            if score >= 30.0:
                scored_skills.append((score, skill))

        if not scored_skills:
            return None

        # Sort descending by relevance score
        scored_skills.sort(key=lambda x: x[0], reverse=True)
        return scored_skills[0][1]

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
    def build_system_context(cls, query: str, intent: Optional[str] = None) -> str:
        skill = cls.match_skill(query, intent=intent)
        if not skill:
            return ""

        context_lines = [
            f"[MATCHED EXPERT DIAGNOSTIC PLAYBOOK: {skill.name} ({skill.skill_id})]",
            f"Objective: {skill.description}",
            f"Risk Level: {skill.risk_level} (Confirmation Required: {skill.confirmation_required})",
            "Permitted Diagnostic Tools: " + ", ".join(skill.permitted_tools),
            "Remediation Tools: " + ", ".join(skill.remediation_tools),
            "Diagnostic Steps: " + " | ".join(skill.diagnostic_procedure),
            "Potential Root Causes: " + ", ".join(skill.potential_root_causes),
            f"Verification: {skill.verification_steps}",
            f"Recovery Info: {skill.recovery_procedure}"
        ]
        return "\n".join(context_lines)
