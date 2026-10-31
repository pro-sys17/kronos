"""
KRONOS Windows Technical Knowledge Base (RAG)
Lightweight hybrid search engine covering Windows 10/11, PowerShell, Networking, Event Viewer, and Troubleshooting.
Retrieved knowledge is strictly advisory context and cannot override execution permissions.
"""

from typing import Dict, Any, List, Optional, Tuple
import re
import math

class KnowledgeArticle:
    def __init__(self, doc_id: str, title: str, domain: str, tags: List[str], summary: str, content: str, source: str):
        self.doc_id = doc_id
        self.title = title
        self.domain = domain
        self.tags = tags
        self.summary = summary
        self.content = content
        self.source = source

    def to_dict(self) -> Dict[str, Any]:
        return {
            "doc_id": self.doc_id,
            "title": self.title,
            "domain": self.domain,
            "tags": self.tags,
            "summary": self.summary,
            "content": self.content,
            "source": self.source
        }

ARTICLES: List[KnowledgeArticle] = [
    # 1. Networking: DNS & Resolution
    KnowledgeArticle(
        doc_id="KB-NET-001",
        title="Windows DNS Client Cache & Resolution Failures",
        domain="Networking and DNS",
        tags=["dns", "flushdns", "resolve-dnsname", "cache", "nxdomain", "1.1.1.1", "8.8.8.8", "internet", "slow", "latency", "ping"],
        summary="Explains DNS client resolver caching in Windows 10/11 and resolution via Clear-DnsClientCache.",
        content=(
            "The Windows DNS Client service (Dnscache) caches successful and negative queries. Stale entries or TTL "
            "congestion can cause DNS_PROBE_FINISHED_NXDOMAIN or host lookup timeouts. Clearing the cache using "
            "'Clear-DnsClientCache' purges transient entries without disrupting active TCP connections. "
            "Public fallback resolvers like Cloudflare (1.1.1.1) and Google (8.8.8.8) can be verified via Resolve-DnsName."
        ),
        source="Microsoft Learn // Networking & DNS Client Architecture"
    ),

    # 2. Networking: TCP/IP & Winsock
    KnowledgeArticle(
        doc_id="KB-NET-002",
        title="TCP/IP Stack Corruption & Winsock Reset",
        domain="TCP/IP and Connectivity",
        tags=["winsock", "tcpip", "netsh", "adapter", "reset", "dhcp", "limited connectivity"],
        summary="Details procedures for repairing corrupted Winsock catalog and TCP/IP stack in Windows.",
        content=(
            "When network adapters fail to negotiate IP addresses or return error 0x800704cf, Winsock catalog corruption "
            "or third-party proxy hooks may be the root cause. Running 'netsh winsock reset' resets the Windows Sockets API "
            "to clean default state, and 'netsh int ip reset' clears registry interfaces. A computer reboot is typically required."
        ),
        source="Microsoft Learn // Windows Sockets 2 (Winsock) & TCP/IP Reference"
    ),

    # 3. System Stability: Event ID 41 & Kernel-Power
    KnowledgeArticle(
        doc_id="KB-SYS-001",
        title="Event ID 41 (Kernel-Power) Root-Cause Analysis",
        domain="Event Viewer and Error Codes",
        tags=["event 41", "kernel power", "bsod", "reboot", "unexpected shutdown", "bugcheck", "power supply"],
        summary="Analyzes unexpected system reboots where the PC shuts down without clean operating system handoff.",
        content=(
            "Event ID 41 indicates the system rebooted without cleanly shutting down first. Common root causes include "
            "loss of power (power supply unit failure), thermal tripping, hardware lockups, or BugCheck (BSOD). "
            "If BugcheckCode is non-zero, cross-reference with memory minidump files located in C:\\Windows\\Minidump "
            "to isolate the offending third-party kernel driver (.sys)."
        ),
        source="Microsoft Sysinternals & Windows Event Viewer Diagnostic Guide"
    ),

    # 4. Storage & Integrity: DISM and SFC Repair
    KnowledgeArticle(
        doc_id="KB-SYS-002",
        title="DISM Component Store & SFC System File Integrity",
        domain="System Recovery",
        tags=["sfc", "dism", "scannow", "restorehealth", "checkhealth", "winsxs", "corrupt"],
        summary="Explains relationship between Windows Component Store (WinSxS) and System File Checker.",
        content=(
            "The System File Checker ('sfc /scannow') inspects critical Windows OS binaries against the Component Store. "
            "If the Component Store itself is corrupted, SFC will report 'Windows Resource Protection found corrupt files but was unable to fix some of them'. "
            "The proper recovery sequence is running 'DISM /Online /Cleanup-Image /RestoreHealth' first to repair WinSxS via Windows Update, "
            "followed by SFC to restore patched system files."
        ),
        source="Microsoft Learn // DISM (Deployment Image Servicing and Management) Reference"
    ),

    # 5. Audio Subsystem: AudioSrv & EndpointBuilder
    KnowledgeArticle(
        doc_id="KB-AUD-001",
        title="Windows Audio Subsystem Architecture (AudioSrv)",
        domain="Windows Services and Processes",
        tags=["audio", "sound", "audiosrv", "audioendpointbuilder", "speaker", "volume", "muted"],
        summary="Explains the dual-service audio architecture in Windows and safe recovery procedures.",
        content=(
            "Windows audio relies on two tightly coupled services: 'AudioEndpointBuilder' (which enumerates and tracks hardware DACs, "
            "headphone jacks, and HDMI outputs) and 'AudioSrv' (which manages user-mode audio sessions and volume). "
            "Restarting AudioEndpointBuilder first followed by AudioSrv resets the WASAPI pipeline and clears exclusive mode locks "
            "without requiring a machine reboot."
        ),
        source="Windows Core Audio APIs & Hardware Endpoint Architecture"
    ),

    # 6. Windows Update: Error Codes & Cache
    KnowledgeArticle(
        doc_id="KB-WUA-001",
        title="Windows Update Download Hang & SoftwareDistribution Cache",
        domain="Windows Update",
        tags=["update", "wuauserv", "bits", "softwaredistribution", "0x80070002", "0x80240034", "stuck"],
        summary="Root causes and resolution steps for stuck Windows Update downloads and error 0x80070002.",
        content=(
            "Windows Update downloads patches into C:\\Windows\\SoftwareDistribution\\Download. If a package download is interrupted, "
            "hash mismatches cause error 0x80070002 or download loops at 0%. Stopping 'wuauserv' and 'BITS' services allows clearing "
            "the corrupted download staging directory. When restarted, the Windows Update Agent initiates a fresh cryptographic handshake."
        ),
        source="Microsoft Learn // Windows Update Troubleshooting & Error Codes"
    ),

    # 7. Hardware & Drivers: Device Manager Error Codes
    KnowledgeArticle(
        doc_id="KB-HW-001",
        title="Device Manager Error Codes (Code 10, Code 28, Code 43)",
        domain="Hardware and Device Drivers",
        tags=["driver", "code 43", "code 10", "code 28", "pnp", "device manager", "yellow mark"],
        summary="Diagnoses Plug-and-Play device manager error codes and driver initialization failures.",
        content=(
            "Code 10 ('This device cannot start') indicates a driver failure or hardware communication timeout. "
            "Code 28 indicates missing INF drivers. Code 43 ('Windows has stopped this device because it has reported problems') "
            "typically occurs on graphics cards (GPUs) or USB controllers due to firmware crashes, PCIe slot contact issues, "
            "or corrupt vendor driver files. Querying Win32_PnPEntity with ConfigManagerErrorCode isolates affected hardware."
        ),
        source="Microsoft Hardware Dev Center // Device Manager Error Messages"
    ),

    # 8. Security: Windows Defender Firewall Profiles
    KnowledgeArticle(
        doc_id="KB-SEC-001",
        title="Windows Defender Firewall Profiles & Port Precedence",
        domain="Windows Defender and Firewall",
        tags=["firewall", "defender", "ports", "netsh", "advfirewall", "domain", "private", "public"],
        summary="Explains profile evaluation precedence across Domain, Private, and Public network firewall profiles.",
        content=(
            "Windows Defender Firewall enforces rules across three distinct profiles: Domain (assigned on AD domain networks), "
            "Private (home and trusted office networks where network discovery is permitted), and Public (airports and open Wi-Fi). "
            "Inbound traffic is blocked by default unless an explicit allow rule exists. The command 'netsh advfirewall reset' "
            "restores all standard Microsoft inbound/outbound rules if custom policies block legitimate connectivity."
        ),
        source="Microsoft Learn // Windows Defender Firewall with Advanced Security"
    ),

    # 9. Performance: Working Set vs Private Bytes & CPU Hogs
    KnowledgeArticle(
        doc_id="KB-PERF-001",
        title="Memory Leak & Working Set Diagnostics in Windows",
        domain="CPU, RAM, Disks and Storage",
        tags=["ram", "memory leak", "workingset", "cpu", "commit charge", "task manager", "high usage"],
        summary="Distinguishes resident physical RAM (Working Set) from allocated commit memory.",
        content=(
            "A process may consume large amounts of physical RAM (WorkingSet64) or virtual address space (PrivateMemorySize64). "
            "When Working Set exceeds available physical RAM, Windows begins paging pages to pagefile.sys, creating disk queue "
            "saturation (100% disk usage). Using 'Get-Process | Sort-Object WorkingSet64 -Descending' quickly isolates memory hogs. "
            "Terminating the parent PID releases both physical memory pages and handle allocations."
        ),
        source="Windows Internals & Memory Management Architecture"
    ),

    # 10. PowerShell: Compatibility & Execution Policy
    KnowledgeArticle(
        doc_id="KB-PS-001",
        title="PowerShell 5.1 vs 7.x Cross-Compatibility",
        domain="PowerShell 5.1 and 7",
        tags=["powershell", "ps51", "pwsh", "executionpolicy", "wmi", "cim", "compatibility"],
        summary="Best practices for scripts executing across legacy Windows PowerShell 5.1 and modern PowerShell 7+.",
        content=(
            "PowerShell 5.1 uses the legacy .NET Framework 4.8 engine and does not support ternary operators ($a ? $b : $c) "
            "or null-coalescing assignment. Variable expansion immediately preceding brackets ('$ESC[0m') triggers array indexing "
            "parser exceptions. Always use Get-CimInstance instead of deprecated Get-WmiObject for CIM compliance across both runtimes."
        ),
        source="Microsoft Learn // PowerShell Scripting Cross-Version Best Practices"
    )
]

class KnowledgeBase:
    """
    Lightweight, deterministic Hybrid Retrieval Engine (TF-IDF keyword matching + semantic token scoring).
    Zero external dependencies, zero latency overhead.
    """

    @classmethod
    def search(cls, query: str, limit: int = 2) -> List[KnowledgeArticle]:
        q_tokens = set(re.findall(r'\b[a-zA-Z0-9_\-\.]{2,}\b', query.lower()))
        scored: List[Tuple[float, KnowledgeArticle]] = []

        for article in ARTICLES:
            score = 0.0
            art_text = (article.title + " " + article.domain + " " + " ".join(article.tags) + " " + article.content).lower()
            art_tokens = set(re.findall(r'\b[a-zA-Z0-9_\-\.]{2,}\b', art_text))

            # Tag exact matches (weight = 4.0)
            for tag in article.tags:
                if tag.lower() in query.lower():
                    score += 4.0

            # Title matches (weight = 3.0)
            for tok in q_tokens:
                if tok in article.title.lower():
                    score += 3.0

            # Token overlap (Jaccard-like semantic scoring)
            common = q_tokens.intersection(art_tokens)
            if common:
                score += len(common) * 1.5

            if score > 2.0:
                scored.append((score, article))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scored[:limit]]

    @classmethod
    def build_rag_context(cls, query: str) -> str:
        matches = cls.search(query, limit=2)
        if not matches:
            return ""

        lines = ["\n[VERIFIED WINDOWS TECHNICAL KNOWLEDGE (RAG)]"]
        for m in matches:
            lines.append(f"Source: {m.source} (Domain: {m.domain})")
            lines.append(f"Title: {m.title}")
            lines.append(f"Fact Summary: {m.content}\n")

        lines.append("Note: Technical knowledge is information for technical accuracy. Do not execute arbitrary code outside registered tools.")
        return "\n".join(lines)
