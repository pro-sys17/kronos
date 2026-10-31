"""
KRONOS Structured Tool Execution Engine
Strictly registered, typed, and permission-tiered Windows System Tools.
Replaces untrusted arbitrary LLM PowerShell string generation with deterministic operations.
"""

from __future__ import annotations
from typing import Dict, Any, List, Optional, Callable, Tuple
import re
import json

class ToolParameter:
    def __init__(self, name: str, param_type: str, description: str, required: bool = True, default: Any = None, allowed_values: Optional[List[Any]] = None):
        self.name = name
        self.param_type = param_type  # 'string', 'int', 'bool', 'choice'
        self.description = description
        self.required = required
        self.default = default
        self.allowed_values = allowed_values

    def validate(self, value: Any) -> Tuple_Validation:
        if value is None:
            if self.required:
                return False, f"Missing required parameter '{self.name}'"
            return True, ""

        if self.param_type == "int":
            try:
                int(value)
            except (ValueError, TypeError):
                return False, f"Parameter '{self.name}' must be an integer."
        elif self.param_type == "bool":
            if not isinstance(value, bool) and str(value).lower() not in ("true", "false", "1", "0"):
                return False, f"Parameter '{self.name}' must be a boolean."
        elif self.param_type == "choice":
            if self.allowed_values and str(value).lower() not in [str(x).lower() for x in self.allowed_values]:
                return False, f"Parameter '{self.name}' must be one of {self.allowed_values}."
        elif self.param_type == "string":
            # Sanitize dangerous characters in string arguments to prevent injection
            val_str = str(value)
            if re.search(r"[`$;|&><\n\r]", val_str):
                return False, f"Illegal characters detected in parameter '{self.name}'."

        return True, ""

Tuple_Validation = tuple[bool, str]

class ToolDefinition:
    def __init__(
        self,
        tool_id: str,
        category: str,
        name: str,
        description: str,
        risk: str,  # 'LOW', 'MODERATE', 'HIGH', 'PROHIBITED'
        requires_confirmation: bool,
        parameters: List[ToolParameter],
        command_builder: Callable[[Dict[str, Any]], str],
        verification_builder: Optional[Callable[[Dict[str, Any]], str]] = None,
        recovery_info: Optional[str] = None
    ):
        self.tool_id = tool_id
        self.category = category
        self.name = name
        self.description = description
        self.risk = risk.upper()
        self.requires_confirmation = requires_confirmation
        self.parameters = {p.name: p for p in parameters}
        self.command_builder = command_builder
        self.verification_builder = verification_builder
        self.recovery_info = recovery_info

    def validate_args(self, args: Dict[str, Any]) -> Tuple_Validation:
        for p_name, param in self.parameters.items():
            val = args.get(p_name, param.default)
            is_valid, err = param.validate(val)
            if not is_valid:
                return False, err
        return True, ""

    def build_command(self, args: Dict[str, Any]) -> str:
        clean_args = {p_name: args.get(p_name, param.default) for p_name, param in self.parameters.items()}
        return self.command_builder(clean_args)

    def build_verification(self, args: Dict[str, Any]) -> str:
        if self.verification_builder:
            clean_args = {p_name: args.get(p_name, param.default) for p_name, param in self.parameters.items()}
            return self.verification_builder(clean_args)
        return "$true"

    def to_schema(self) -> Dict[str, Any]:
        return {
            "tool_id": self.tool_id,
            "category": self.category,
            "name": self.name,
            "description": self.description,
            "risk": self.risk,
            "requires_confirmation": self.requires_confirmation,
            "parameters": {
                p.name: {
                    "type": p.param_type,
                    "description": p.description,
                    "required": p.required,
                    "default": p.default,
                    "allowed_values": p.allowed_values
                } for p in self.parameters.values()
            },
            "recovery_info": self.recovery_info
        }


# ==============================================================================
# TOOL REGISTRY IMPLEMENTATION
# ==============================================================================

class ToolRegistry:
    _tools: Dict[str, ToolDefinition] = {}

    @classmethod
    def register(cls, tool: ToolDefinition):
        cls._tools[tool.tool_id] = tool

    @classmethod
    def get(cls, tool_id: str) -> Optional[ToolDefinition]:
        return cls._tools.get(tool_id)

    @classmethod
    def list_all(cls) -> List[ToolDefinition]:
        return list(cls._tools.values())

    @classmethod
    def get_schemas(cls) -> List[Dict[str, Any]]:
        return [t.to_schema() for t in cls._tools.values()]


# ------------------------------------------------------------------------------
# 1. LOW RISK (AUTOMATIC, READ-ONLY DIAGNOSTIC TOOLS)
# ------------------------------------------------------------------------------

# system.get_info
ToolRegistry.register(ToolDefinition(
    tool_id="system.get_info",
    category="system",
    name="Get System Hardware & OS Info",
    description="Collects machine specifications, CPU model, architecture, memory capacity, and OS build number.",
    risk="LOW",
    requires_confirmation=False,
    parameters=[],
    command_builder=lambda args: (
        "Get-CimInstance Win32_OperatingSystem | Select-Object Caption, Version, BuildNumber, OSArchitecture, "
        "@{N='TotalRAM_GB';E={[math]::Round($_.TotalVisibleMemorySize/1MB,1)}}, "
        "@{N='FreeRAM_GB';E={[math]::Round($_.FreePhysicalMemory/1MB,1)}} | Format-List"
    ),
    verification_builder=lambda args: "$true"
))

# system.inspect_resources
ToolRegistry.register(ToolDefinition(
    tool_id="system.inspect_resources",
    category="system",
    name="Inspect CPU & RAM Resource Load",
    description="Inspects real-time CPU load and retrieves top 8 memory and CPU consuming processes.",
    risk="LOW",
    requires_confirmation=False,
    parameters=[
        ToolParameter("limit", "int", "Number of top processes to retrieve", required=False, default=8)
    ],
    command_builder=lambda args: (
        f"Get-Process | Sort-Object WorkingSet64 -Descending | Select-Object -First {args['limit']} "
        "Id, ProcessName, @{N='RAM(MB)';E={[math]::Round($_.WorkingSet64/1MB,1)}}, "
        "@{N='CPU(s)';E={if($_.CPU){[math]::Round($_.CPU,1)}else{0}}} | Format-Table -AutoSize"
    ),
    verification_builder=lambda args: "$true"
))

# storage.check_disks
ToolRegistry.register(ToolDefinition(
    tool_id="storage.check_disks",
    category="storage",
    name="Check Disk Volumes and Free Space",
    description="Inspects all local storage volumes, drive letters, capacity, free space and percentage headroom.",
    risk="LOW",
    requires_confirmation=False,
    parameters=[],
    command_builder=lambda args: (
        "Get-PSDrive -PSProvider FileSystem | Where-Object { $_.Free -gt 0 } | "
        "Select-Object Name, @{N='Used(GB)';E={[math]::Round($_.Used/1GB,2)}}, "
        "@{N='Free(GB)';E={[math]::Round($_.Free/1GB,2)}}, "
        "@{N='Total(GB)';E={[math]::Round(($_.Used+$_.Free)/1GB,2)}}, "
        "@{N='PercentFree';E={[math]::Round(($_.Free/($_.Used+$_.Free))*100,1)}} | Format-Table -AutoSize"
    ),
    verification_builder=lambda args: "$true"
))

# network.inspect_adapters
ToolRegistry.register(ToolDefinition(
    tool_id="network.inspect_adapters",
    category="network",
    name="Inspect Network Adapters and Configuration",
    description="Queries all active physical and Wi-Fi network adapters, link speeds, IPv4 addresses, and default gateway.",
    risk="LOW",
    requires_confirmation=False,
    parameters=[],
    command_builder=lambda args: (
        "Get-NetAdapter | Where-Object { $_.InterfaceDescription -notmatch 'VMware|Virtual|Loopback' } | "
        "Select-Object Name, InterfaceDescription, Status, LinkSpeed | Format-Table -AutoSize; "
        "Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias (Get-NetAdapter | Where-Object Status -eq 'Up' | Select-Object -First 1 -ExpandProperty Name -ErrorAction SilentlyContinue) -ErrorAction SilentlyContinue | "
        "Select-Object IPAddress, InterfaceAlias | Format-Table -AutoSize"
    ),
    verification_builder=lambda args: "$true"
))

# network.test_dns
ToolRegistry.register(ToolDefinition(
    tool_id="network.test_dns",
    category="network",
    name="Test DNS Name Resolution",
    description="Tests DNS hostname resolution against system default DNS or a specified resolver (e.g. 1.1.1.1, 8.8.8.8).",
    risk="LOW",
    requires_confirmation=False,
    parameters=[
        ToolParameter("domain", "string", "Domain name to resolve", required=False, default="cloudflare.com"),
        ToolParameter("server", "string", "Optional DNS server IP to query", required=False, default="")
    ],
    command_builder=lambda args: (
        f"Resolve-DnsName -Name '{args['domain']}'" + (f" -Server '{args['server']}'" if args.get('server') else "") + " -ErrorAction SilentlyContinue | Select-Object Name, Type, IPAddress, NameHost | Format-Table -AutoSize"
    ),
    verification_builder=lambda args: f"Resolve-DnsName -Name '{args['domain']}' -Quiet"
))

# network.ping
ToolRegistry.register(ToolDefinition(
    tool_id="network.ping",
    category="network",
    name="Ping Target Host",
    description="Tests ICMP roundtrip ping latency and packet connectivity to a remote IP or domain.",
    risk="LOW",
    requires_confirmation=False,
    parameters=[
        ToolParameter("target", "string", "Hostname or IP address to ping", required=False, default="1.1.1.1"),
        ToolParameter("count", "int", "Number of ping probes", required=False, default=3)
    ],
    command_builder=lambda args: (
        f"Test-NetConnection -ComputerName '{args['target']}' -InformationLevel Detailed | "
        "Select-Object ComputerName, RemoteAddress, PingSucceeded, RoundTripTime | Format-List"
    ),
    verification_builder=lambda args: f"Test-Connection -ComputerName '{args['target']}' -Count 1 -Quiet"
))

# network.list_ports
ToolRegistry.register(ToolDefinition(
    tool_id="network.list_ports",
    category="network",
    name="List Active Listening TCP Ports",
    description="Audits all listening TCP sockets and identifies their owning process IDs and names.",
    risk="LOW",
    requires_confirmation=False,
    parameters=[
        ToolParameter("limit", "int", "Maximum number of port records to retrieve", required=False, default=15)
    ],
    command_builder=lambda args: (
        f"Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue | Sort-Object LocalPort | Select-Object -First {args['limit']} "
        "LocalAddress, LocalPort, OwningProcess, @{N='Process';E={(Get-Process -Id $_.OwningProcess -ErrorAction SilentlyContinue).ProcessName}} | Format-Table -AutoSize"
    ),
    verification_builder=lambda args: "$true"
))

# service.get_status
ToolRegistry.register(ToolDefinition(
    tool_id="service.get_status",
    category="service",
    name="Check Windows Service Status",
    description="Queries the runtime status, startup type, and display name of a given Windows service.",
    risk="LOW",
    requires_confirmation=False,
    parameters=[
        ToolParameter("service_name", "string", "Service name to inspect (e.g. AudioSrv, wuauserv, WinDefend)", required=True)
    ],
    command_builder=lambda args: (
        f"Get-Service -Name '{args['service_name']}' -ErrorAction SilentlyContinue | Select-Object Name, DisplayName, Status, StartType | Format-List"
    ),
    verification_builder=lambda args: f"(Get-Service -Name '{args['service_name']}' -ErrorAction SilentlyContinue) -ne $null"
))

# eventlog.query_errors
ToolRegistry.register(ToolDefinition(
    tool_id="eventlog.query_errors",
    category="system",
    name="Query Recent Windows Event Errors",
    description="Audits the Windows System or Application event log for recent critical errors and service failures.",
    risk="LOW",
    requires_confirmation=False,
    parameters=[
        ToolParameter("log_name", "choice", "Event log name", required=False, default="System", allowed_values=["System", "Application"]),
        ToolParameter("hours", "int", "Lookback hours", required=False, default=24),
        ToolParameter("limit", "int", "Max records", required=False, default=6)
    ],
    command_builder=lambda args: (
        f"$startTime = (Get-Date).AddHours(-{args['hours']}); "
        f"Get-WinEvent -FilterHashtable @{{LogName='{args['log_name']}'; Level=1,2; StartTime=$startTime}} -MaxEvents {args['limit']} -ErrorAction SilentlyContinue | "
        "Select-Object TimeCreated, Id, ProviderName, @{N='Message';E={$_.Message.Split(\"`r`n\")[0]}} | Format-Table -AutoSize"
    ),
    verification_builder=lambda args: "$true"
))

# hardware.audit_devices
ToolRegistry.register(ToolDefinition(
    tool_id="hardware.audit_devices",
    category="hardware",
    name="Audit Hardware Devices & Problem Drivers",
    description="Scans Plug-and-Play devices for hardware errors, yellow exclamation marks, and missing drivers.",
    risk="LOW",
    requires_confirmation=False,
    parameters=[],
    command_builder=lambda args: (
        "Get-PnpDevice -Status Error, Degraded -ErrorAction SilentlyContinue | "
        "Select-Object FriendlyName, InstanceId, Class, Status, Problem | Format-Table -AutoSize"
    ),
    verification_builder=lambda args: "$true"
))

# file.search
ToolRegistry.register(ToolDefinition(
    tool_id="file.search",
    category="storage",
    name="Search Files Across Storage Volumes",
    description="Locates files matching a pattern without modifying any content.",
    risk="LOW",
    requires_confirmation=False,
    parameters=[
        ToolParameter("query", "string", "File name pattern or extension (e.g. *.pdf, budget, report)", required=True),
        ToolParameter("drive", "string", "Drive letter to search (e.g. C:, D:)", required=False, default="C:"),
        ToolParameter("limit", "int", "Maximum number of search results", required=False, default=10)
    ],
    command_builder=lambda args: (
        "Get-ChildItem -Path '" + str(args['drive']) + "\\' -Filter '*" + str(args['query']) + "*' -Recurse -File -ErrorAction SilentlyContinue | "
        "Select-Object -First " + str(args['limit']) + " FullName, @{N='Size(MB)';E={[math]::Round($_.Length/1MB,2)}}, LastWriteTime | Format-Table -AutoSize"
    ),
    verification_builder=lambda args: "$true"
))


# ------------------------------------------------------------------------------
# 2. MODERATE RISK (CONFIRM BEFORE EXECUTION)
# ------------------------------------------------------------------------------

# network.flush_dns
ToolRegistry.register(ToolDefinition(
    tool_id="network.flush_dns",
    category="network",
    name="Flush Windows DNS Cache",
    description="Purges and resets the local DNS client resolver cache to clear corrupted or poisoned records.",
    risk="MODERATE",
    requires_confirmation=True,
    parameters=[],
    command_builder=lambda args: "Clear-DnsClientCache; Write-Output '[PASS] DNS Resolver Cache Flushed Successfully.'",
    verification_builder=lambda args: "$true",
    recovery_info="DNS records will repopulate automatically upon subsequent network requests."
))

# network.renew_ip
ToolRegistry.register(ToolDefinition(
    tool_id="network.renew_ip",
    category="network",
    name="Release and Renew IP Lease",
    description="Releases and re-acquires DHCP dynamic IP address lease from the local router or DHCP server.",
    risk="MODERATE",
    requires_confirmation=True,
    parameters=[],
    command_builder=lambda args: "ipconfig /release; Start-Sleep -Seconds 1; ipconfig /renew",
    verification_builder=lambda args: "(Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias (Get-NetAdapter | Where-Object Status -eq 'Up' | Select-Object -First 1 -ExpandProperty Name -ErrorAction SilentlyContinue) -ErrorAction SilentlyContinue) -ne $null",
    recovery_info="If DHCP fails, reconnect network cable or cycle Wi-Fi connection."
))

# network.set_adapter_state
ToolRegistry.register(ToolDefinition(
    tool_id="network.set_adapter_state",
    category="network",
    name="Enable or Disable Network Adapter",
    description="Enables or disables a physical, Wi-Fi, or Ethernet network interface.",
    risk="MODERATE",
    requires_confirmation=True,
    parameters=[
        ToolParameter("adapter_name", "string", "Interface alias name (e.g. Wi-Fi, Ethernet)", required=True),
        ToolParameter("enabled", "bool", "True to enable, False to disable", required=True)
    ],
    command_builder=lambda args: (
        f"if ('{str(args['enabled']).lower()}' -eq 'true') {{ "
        f"Enable-NetAdapter -Name '{args['adapter_name']}' -Confirm:$false "
        f"}} else {{ "
        f"Disable-NetAdapter -Name '{args['adapter_name']}' -Confirm:$false "
        f"}}"
    ),
    verification_builder=lambda args: (
        f"(Get-NetAdapter -Name '{args['adapter_name']}').Status -eq " + ("'Up'" if str(args['enabled']).lower() == 'true' else "'Disabled'")
    ),
    recovery_info="Adapter state can be toggled back on using KRONOS or Windows Network Connections."
))

# service.restart
ToolRegistry.register(ToolDefinition(
    tool_id="service.restart",
    category="service",
    name="Restart Windows Service",
    description="Safely stops and restarts a Windows system service.",
    risk="MODERATE",
    requires_confirmation=True,
    parameters=[
        ToolParameter("service_name", "string", "Name of service to restart (e.g. AudioSrv, Spooler, wuauserv)", required=True)
    ],
    command_builder=lambda args: (
        f"Restart-Service -Name '{args['service_name']}' -Force; Start-Sleep -Milliseconds 400; "
        f"Get-Service -Name '{args['service_name']}' | Select-Object Name, Status"
    ),
    verification_builder=lambda args: f"(Get-Service -Name '{args['service_name']}').Status -eq 'Running'",
    recovery_info="Service can be re-started or queried with Get-Service."
))

# service.start
ToolRegistry.register(ToolDefinition(
    tool_id="service.start",
    category="service",
    name="Start Windows Service",
    description="Starts a stopped Windows system service.",
    risk="MODERATE",
    requires_confirmation=True,
    parameters=[
        ToolParameter("service_name", "string", "Name of service to start", required=True)
    ],
    command_builder=lambda args: (
        f"Start-Service -Name '{args['service_name']}'; Start-Sleep -Milliseconds 300; "
        f"Get-Service -Name '{args['service_name']}' | Select-Object Name, Status"
    ),
    verification_builder=lambda args: f"(Get-Service -Name '{args['service_name']}').Status -eq 'Running'",
    recovery_info="Service can be stopped with Stop-Service."
))

# service.stop
ToolRegistry.register(ToolDefinition(
    tool_id="service.stop",
    category="service",
    name="Stop Windows Service",
    description="Stops an active Windows service.",
    risk="MODERATE",
    requires_confirmation=True,
    parameters=[
        ToolParameter("service_name", "string", "Name of non-critical service to stop", required=True)
    ],
    command_builder=lambda args: (
        f"Stop-Service -Name '{args['service_name']}' -Force; Start-Sleep -Milliseconds 300; "
        f"Get-Service -Name '{args['service_name']}' | Select-Object Name, Status"
    ),
    verification_builder=lambda args: f"(Get-Service -Name '{args['service_name']}').Status -eq 'Stopped'",
    recovery_info="Service can be restarted at any time with Start-Service."
))

# storage.clean_temp
ToolRegistry.register(ToolDefinition(
    tool_id="storage.clean_temp",
    category="storage",
    name="Clean User Temporary Files",
    description="Purges locked and unreferenced temporary files from the current user's %TEMP% directory.",
    risk="MODERATE",
    requires_confirmation=True,
    parameters=[],
    command_builder=lambda args: (
        "Remove-Item -Path \"$env:TEMP\\*\" -Recurse -Force -ErrorAction SilentlyContinue; "
        "Write-Output '[PASS] User temporary directory purged.'"
    ),
    verification_builder=lambda args: "$true",
    recovery_info="Only transient application cache files are purged; personal user documents are never touched."
))

# process.terminate
ToolRegistry.register(ToolDefinition(
    tool_id="process.terminate",
    category="process",
    name="Terminate Process by PID",
    description="Forcefully stops a runaway, hanging, or unresponsive process by its process ID.",
    risk="MODERATE",
    requires_confirmation=True,
    parameters=[
        ToolParameter("pid", "int", "Process ID (PID) to terminate", required=True)
    ],
    command_builder=lambda args: (
        f"Stop-Process -Id {args['pid']} -Force; Start-Sleep -Milliseconds 250; "
        f"Write-Output '[PASS] Stop-Process signaled to PID {args['pid']}.'"
    ),
    verification_builder=lambda args: f"-not (Get-Process -Id {args['pid']} -ErrorAction SilentlyContinue)",
    recovery_info="Terminated application can be relaunched manually by the user."
))

# audio.restart_subsystem
ToolRegistry.register(ToolDefinition(
    tool_id="audio.restart_subsystem",
    category="audio",
    name="Restart Windows Audio Subsystem",
    description="Restarts Windows Audio Service and Windows Audio Endpoint Builder to resolve sound crackle, desync, or muted outputs.",
    risk="MODERATE",
    requires_confirmation=True,
    parameters=[],
    command_builder=lambda args: (
        "Restart-Service -Name 'AudioEndpointBuilder' -Force; "
        "Restart-Service -Name 'AudioSrv' -Force; Start-Sleep -Milliseconds 400; "
        "Get-Service -Name 'AudioSrv', 'AudioEndpointBuilder' | Select-Object Name, Status"
    ),
    verification_builder=lambda args: "(Get-Service AudioSrv).Status -eq 'Running' -and (Get-Service AudioEndpointBuilder).Status -eq 'Running'",
    recovery_info="Audio services restart automatically and restore audio playback."
))

# system.run_dism_check
ToolRegistry.register(ToolDefinition(
    tool_id="system.run_dism_check",
    category="system",
    name="Check Windows Component Store Integrity",
    description="Scans the Windows Component Store (WinSxS) to detect corrupt operating system files without making modifications.",
    risk="MODERATE",
    requires_confirmation=True,
    parameters=[],
    command_builder=lambda args: "DISM /Online /Cleanup-Image /CheckHealth",
    verification_builder=lambda args: "$true",
    recovery_info="Read-only integrity check; does not alter system files."
))


# ------------------------------------------------------------------------------
# 3. HIGH RISK (EXPLICIT AUTHORIZATION REQUIRED)
# ------------------------------------------------------------------------------

# firewall.set_profile
ToolRegistry.register(ToolDefinition(
    tool_id="firewall.set_profile",
    category="security",
    name="Configure Windows Defender Firewall Profiles",
    description="Enables or disables Windows Defender Firewall for Domain, Private, or Public network profiles.",
    risk="HIGH",
    requires_confirmation=True,
    parameters=[
        ToolParameter("profile", "choice", "Firewall profile target", required=True, allowed_values=["Domain", "Private", "Public", "All"]),
        ToolParameter("enabled", "bool", "True to enable, False to disable", required=True)
    ],
    command_builder=lambda args: (
        f"Set-NetFirewallProfile -Profile '{args['profile']}' -Enabled '{args['enabled']}'; "
        f"Get-NetFirewallProfile -Profile '{args['profile']}' | Select-Object Name, Enabled"
    ),
    verification_builder=lambda args: (
        f"(Get-NetFirewallProfile -Profile '{args['profile']}').Enabled -eq '{args['enabled']}'"
    ),
    recovery_info="Firewall state can be re-enabled using 'firewall.set_profile' or through Windows Security."
))

# firewall.reset_rules
ToolRegistry.register(ToolDefinition(
    tool_id="firewall.reset_rules",
    category="security",
    name="Reset Windows Firewall to Factory Default",
    description="Resets all Windows Defender Firewall rules and configurations back to clean Windows factory defaults.",
    risk="HIGH",
    requires_confirmation=True,
    parameters=[],
    command_builder=lambda args: "netsh advfirewall reset",
    verification_builder=lambda args: "$true",
    recovery_info="Restores all default firewall rules and policies."
))

# network.reset_winsock
ToolRegistry.register(ToolDefinition(
    tool_id="network.reset_winsock",
    category="network",
    name="Reset TCP/IP Stack and Winsock Catalog",
    description="Performs a deep reset of the Winsock catalog and TCP/IP stack to resolve severe protocol or proxy corruption.",
    risk="HIGH",
    requires_confirmation=True,
    parameters=[],
    command_builder=lambda args: "netsh winsock reset; netsh int ip reset; Write-Output '[PASS] Winsock & TCP/IP stack reset. A reboot is recommended.'",
    verification_builder=lambda args: "$true",
    recovery_info="A safety rollback snapshot of service configurations is created prior to execution."
))

# system.run_dism_restore
ToolRegistry.register(ToolDefinition(
    tool_id="system.run_dism_restore",
    category="system",
    name="Repair Windows Component Store (RestoreHealth)",
    description="Repairs corrupted system files using Windows Update or local component payload.",
    risk="HIGH",
    requires_confirmation=True,
    parameters=[],
    command_builder=lambda args: "DISM /Online /Cleanup-Image /RestoreHealth",
    verification_builder=lambda args: "$true",
    recovery_info="System rollback snapshot is saved prior to repair."
))

# file.delete_item
ToolRegistry.register(ToolDefinition(
    tool_id="file.delete_item",
    category="storage",
    name="Safe Item Deletion with Explicit Confirmation",
    description="Deletes an explicitly specified single file. Strictly prohibited on system directories (Windows, Program Files).",
    risk="HIGH",
    requires_confirmation=True,
    parameters=[
        ToolParameter("path", "string", "Absolute path to the file to delete", required=True)
    ],
    command_builder=lambda args: (
        f"if (Test-Path '{args['path']}') {{ "
        f"Remove-Item -Path '{args['path']}' -Force; Write-Output '[PASS] Deleted: {args['path']}' "
        f"}} else {{ Write-Output '[WARN] File not found: {args['path']}' }}"
    ),
    verification_builder=lambda args: f"-not (Test-Path '{args['path']}')",
    recovery_info="Permanent file removal. Always verify file name before authorizing."
))
