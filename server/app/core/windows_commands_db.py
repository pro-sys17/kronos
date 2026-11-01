"""
KRONOS Windows Master Commands & Tools Database
Contains 250+ Windows System Commands, GUI Applets, Management Consoles,
Modern Settings URIs, Diagnostic Utilities, and Extensible Custom Commands.
"""

from __future__ import annotations
import os
import json
import re
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

# ==============================================================================
# MASTER CATALOG OF 250+ WINDOWS SYSTEM COMMANDS & TOOLS
# ==============================================================================

WINDOWS_MASTER_CATALOG: Dict[str, List[Dict[str, str]]] = {
    "system_diagnostics": [
        {"cmd": "msinfo32", "type": "GUI", "alias": "systeminfo gui, msinfo, system information", "desc": "Windows System Information (Hardware, Components, Drivers)"},
        {"cmd": "dxdiag", "type": "GUI", "alias": "directx, directx diagnostic, gpu info", "desc": "DirectX Diagnostic Tool (GPU, Sound, Display Driver Details)"},
        {"cmd": "winver", "type": "GUI", "alias": "about windows, windows version, os build", "desc": "About Windows / OS Version & Build Dialog"},
        {"cmd": "msconfig", "type": "GUI", "alias": "system config, boot config", "desc": "System Configuration Utility (Boot, Services, Tools)"},
        {"cmd": "systeminfo", "type": "CLI", "alias": "sysinfo, specs cli", "desc": "Detailed Machine Specifications, OS Build, BIOS & Hotfixes"},
        {"cmd": "perfmon", "type": "GUI", "alias": "performance monitor, perf mon", "desc": "Performance Monitor (Realtime Hardware Counter Graphs)"},
        {"cmd": "resmon", "type": "GUI", "alias": "resource monitor, res mon", "desc": "Resource Monitor (CPU, Memory, Disk, Network Processes)"},
        {"cmd": "taskmgr", "type": "GUI", "alias": "task manager, taskmgr.exe, task monitor", "desc": "Windows Task Manager (Processes, Performance, Startup, Users)"},
        {"cmd": "eventvwr.msc", "type": "MMC", "alias": "event viewer, logs, windows logs", "desc": "Windows Event Viewer (System, Application & Security Logs)"},
        {"cmd": "perfmon /rel", "type": "GUI", "alias": "reliability monitor, crash history", "desc": "Reliability History Monitor (System Stability Index & Crashes)"},
        {"cmd": "psr.exe", "type": "GUI", "alias": "problem steps recorder, psr, step recorder", "desc": "Problem Steps Recorder (Screenshots & Step-by-Step Logging)"},
        {"cmd": "sigverif.exe", "type": "GUI", "alias": "file signature verification, sigverif", "desc": "File Signature Verification Utility (Unsigned Driver Check)"},
        {"cmd": "verifier.exe", "type": "GUI", "alias": "driver verifier, verifier", "desc": "Driver Verifier Manager (Kernel Stress Testing)"},
        {"cmd": "mdsched.exe", "type": "GUI", "alias": "memory diagnostic, mdsched, ram test", "desc": "Windows Memory Diagnostic Tool (Reboot & Deep RAM Check)"},
        {"cmd": "msdt.exe", "type": "GUI", "alias": "support diagnostics, msdt", "desc": "Microsoft Support Diagnostic Tool (Troubleshooter Engine)"},
        {"cmd": "sysdm.cpl", "type": "CPL", "alias": "system properties, sysdm", "desc": "System Properties (Computer Name, Hardware, Advanced, Remote)"},
        {"cmd": "systempropertiesadvanced", "type": "GUI", "alias": "advanced system properties, env vars, environment variables", "desc": "Advanced System Properties (Environment Variables & Virtual Memory)"},
        {"cmd": "systempropertiesperformance", "type": "GUI", "alias": "performance options, visual effects", "desc": "Visual Effects, Processor Scheduling & Virtual Memory Paging"},
        {"cmd": "systempropertiesdataexecutionprevention", "type": "GUI", "alias": "dep settings, data execution prevention", "desc": "Data Execution Prevention (DEP) Kernel Memory Protection"},
        {"cmd": "systempropertieshardware", "type": "GUI", "alias": "hardware properties", "desc": "Hardware Properties & Driver Installation Policy"},
        {"cmd": "systempropertiesprotection", "type": "GUI", "alias": "system protection, restore points, system restore", "desc": "System Protection, Restore Points & Shadow Copies"},
        {"cmd": "systempropertiesremote", "type": "GUI", "alias": "remote settings", "desc": "Remote Desktop & Remote Assistance Settings"},
        {"cmd": "systempropertiescomputername", "type": "GUI", "alias": "computer name settings, workgroup", "desc": "Computer Name, Workgroup & Domain Properties"},
        {"cmd": "fltmc.exe", "type": "CLI", "alias": "filter drivers, fltmc", "desc": "Filter Driver Control (Inspect Installed Filesystem Filter Drivers)"},
        {"cmd": "powercfg /devicequery wake_armed", "type": "CLI", "alias": "wake devices, wake armed", "desc": "Query Hardware Devices Configured to Wake Computer from Sleep"},
        {"cmd": "powercfg /availablesleepstates", "type": "CLI", "alias": "sleep states, standby modes", "desc": "Inspect Available System Sleep States (S0, S3, Modern Standby)"},
        {"cmd": "powercfg /requests", "type": "CLI", "alias": "power requests, sleep blockers", "desc": "Display Drivers & Applications Preventing Machine from Sleeping"},
        {"cmd": "powercfg /systempowerreport", "type": "CLI", "alias": "system power report", "desc": "Generate HTML Modern Standby & System Power Diagnostic Report"},
        {"cmd": "openfiles.exe", "type": "CLI", "alias": "open files cli, lock files", "desc": "Display and Disconnect Open Files and Network File Locks"},
        {"cmd": "wmic bios get serialnumber,smbiosbiosversion", "type": "CLI", "alias": "bios serial, bios version", "desc": "Query Motherboard BIOS Serial Number and SMBIOS Firmware Version"},
        {"cmd": "wmic cpu get name,maxclockspeed,numberofcores", "type": "CLI", "alias": "cpu specs, cpu cores", "desc": "Query Processor Name, Max Clock Speed, and Physical Core Count"},
        {"cmd": "wmic memorychip get capacity,speed,manufacturer", "type": "CLI", "alias": "ram specs, ram speed", "desc": "Query Installed RAM Modules, Capacity, Bus Speed & Vendor"},
        {"cmd": "wmic baseboard get product,manufacturer,version", "type": "CLI", "alias": "motherboard info", "desc": "Query Motherboard Product Name, Manufacturer & Revision"}
    ],
    "control_panel_applets": [
        {"cmd": "ncpa.cpl", "type": "CPL", "alias": "network connections, network adapters, ncpa, adapters gui", "desc": "Network Connections (Ethernet, Wi-Fi Adapters, IPv4 DNS Properties)"},
        {"cmd": "appwiz.cpl", "type": "CPL", "alias": "programs and features, uninstall programs, add remove, appwiz", "desc": "Programs and Features (Uninstall / Repair Desktop Applications)"},
        {"cmd": "firewall.cpl", "type": "CPL", "alias": "windows firewall, defender firewall, firewall gui", "desc": "Windows Defender Firewall Status & Quick Profile Control"},
        {"cmd": "mmsys.cpl", "type": "CPL", "alias": "sound settings, audio popup, sound properties, mmsys, audio settings", "desc": "Sound Properties (Playback Devices, Recording Microphones, Levels)"},
        {"cmd": "desk.cpl", "type": "CPL", "alias": "display settings, resolution popup, desk", "desc": "Display Settings & Monitor Resolution Control"},
        {"cmd": "powercfg.cpl", "type": "CPL", "alias": "power options, power plans, sleep settings, powercfg", "desc": "Power Options (High Performance, Balanced, Battery Sleep Plans)"},
        {"cmd": "inetcpl.cpl", "type": "CPL", "alias": "internet properties, internet options, proxy gui, inetcpl", "desc": "Internet Properties (Security Zones, LAN Proxy, Certificates)"},
        {"cmd": "intl.cpl", "type": "CPL", "alias": "region settings, language format, intl, locale", "desc": "Region & Language Formats, Number & Currency Settings"},
        {"cmd": "timedate.cpl", "type": "CPL", "alias": "date and time, clock settings, timezone, timedate", "desc": "Date and Time Properties, Additional Clocks & Internet Time"},
        {"cmd": "main.cpl", "type": "CPL", "alias": "mouse settings, mouse properties, pointer speed, main", "desc": "Mouse Properties (Button Configuration, Pointers, Wheel Speed)"},
        {"cmd": "keybrd.cpl", "type": "CPL", "alias": "keyboard settings, keyboard properties, keybrd", "desc": "Keyboard Properties (Repeat Delay, Repeat Rate, Cursor Blink)"},
        {"cmd": "hdwwiz.cpl", "type": "CPL", "alias": "add hardware wizard, device wizard, hdwwiz", "desc": "Add Hardware Wizard (Install Legacy Drivers)"},
        {"cmd": "wscui.cpl", "type": "CPL", "alias": "security and maintenance, action center, wscui", "desc": "Security and Maintenance Center (Antivirus, SmartScreen Alerts)"},
        {"cmd": "telephon.cpl", "type": "CPL", "alias": "phone and modem, telephon", "desc": "Phone and Modem Location & Dialing Rules"},
        {"cmd": "bthprops.cpl", "type": "CPL", "alias": "bluetooth settings, bluetooth cpl, bthprops", "desc": "Bluetooth Devices & Wireless Comms Settings"},
        {"cmd": "joy.cpl", "type": "CPL", "alias": "game controller, joystick, gamepad test, joy", "desc": "Game Controllers (Test USB Gamepad Calibration & Vibrations)"},
        {"cmd": "colorcpl", "type": "CPL", "alias": "color management, icc profiles, colorcpl", "desc": "Color Management (Monitor ICC Profiles & Display Calibration)"},
        {"cmd": "tabletpc.cpl", "type": "CPL", "alias": "pen and touch, stylus settings, tabletpc", "desc": "Pen and Touch Input Settings"},
        {"cmd": "control fonts", "type": "GUI", "alias": "fonts folder, installed fonts", "desc": "Windows Fonts Directory (Install, Preview & Delete Typefaces)"},
        {"cmd": "control printers", "type": "GUI", "alias": "printers folder, devices and printers", "desc": "Devices and Printers Classic Control Hub"},
        {"cmd": "control admintools", "type": "GUI", "alias": "administrative tools, admin tools", "desc": "Administrative Tools Master Directory"},
        {"cmd": "control schedtasks", "type": "GUI", "alias": "scheduled tasks folder", "desc": "Scheduled Tasks Explorer Hub"},
        {"cmd": "control netconnections", "type": "GUI", "alias": "network connections folder", "desc": "Network Connections Classic Folder"},
        {"cmd": "control userpasswords", "type": "GUI", "alias": "user passwords basic", "desc": "Classic User Accounts Overview Dialog"},
        {"cmd": "control color", "type": "GUI", "alias": "color appearance classic", "desc": "Classic Color and Appearance Window Scheme"},
        {"cmd": "control mouse", "type": "GUI", "alias": "mouse classic", "desc": "Classic Mouse Configuration Hub"},
        {"cmd": "control keyboard", "type": "GUI", "alias": "keyboard classic", "desc": "Classic Keyboard Hardware Hub"},
        {"cmd": "control international", "type": "GUI", "alias": "international settings", "desc": "International Regional Standards Hub"},
        {"cmd": "control datetime", "type": "GUI", "alias": "date time classic", "desc": "Date and Time Classic Control Console"},
        {"cmd": "control folders", "type": "GUI", "alias": "folder options, file explorer options", "desc": "File Explorer Options (Show Hidden Files, File Extensions)"},
        {"cmd": "stiknp.cpl", "type": "CPL", "alias": "scanners and cameras", "desc": "Scanners and Cameras Properties Applet"},
        {"cmd": "directx.cpl", "type": "CPL", "alias": "directx cpl", "desc": "DirectX Diagnostic Control Panel Applet"}
    ],
    "management_consoles": [
        {"cmd": "devmgmt.msc", "type": "MMC", "alias": "device manager, devmgmt, drivers manager", "desc": "Device Manager (Driver Updates, Hardware Hierarchy, Problem Devices)"},
        {"cmd": "diskmgmt.msc", "type": "MMC", "alias": "disk management, diskmgmt, partitions gui, partition manager", "desc": "Disk Management (Format Volumes, Shrink/Extend Partitions, VHDs)"},
        {"cmd": "services.msc", "type": "MMC", "alias": "services console, windows services, services", "desc": "Windows Services Controller (Start, Stop, Automatic/Manual Triggers)"},
        {"cmd": "compmgmt.msc", "type": "MMC", "alias": "computer management, compmgmt", "desc": "Computer Management Console (Master Hub for System Tools)"},
        {"cmd": "taskschd.msc", "type": "MMC", "alias": "task scheduler, taskschd, scheduled jobs", "desc": "Task Scheduler (Automated Scheduled Scripts & Background Triggers)"},
        {"cmd": "gpedit.msc", "type": "MMC", "alias": "group policy editor, gpedit, local policies", "desc": "Local Group Policy Editor (Windows Admin Policies & Restrictions)"},
        {"cmd": "secpol.msc", "type": "MMC", "alias": "local security policy, secpol, audit policy", "desc": "Local Security Policy (User Rights Assignment, Audit Logs, Hardening)"},
        {"cmd": "lusrmgr.msc", "type": "MMC", "alias": "local users and groups, lusrmgr, local users", "desc": "Local Users and Groups Manager (Account Admin & Group Memberships)"},
        {"cmd": "certmgr.msc", "type": "MMC", "alias": "certificate manager user, certmgr, certificates", "desc": "Certificates Manager - Current User (Personal, Trusted Authorities)"},
        {"cmd": "certlm.msc", "type": "MMC", "alias": "certificate manager machine, certlm", "desc": "Certificates Manager - Local Computer System"},
        {"cmd": "fsmgmt.msc", "type": "MMC", "alias": "shared folders, fsmgmt, smb shares", "desc": "Shared Folders (Active Network Shares, Open Files & Sessions)"},
        {"cmd": "wf.msc", "type": "MMC", "alias": "firewall advanced security, wf.msc, wf", "desc": "Windows Defender Firewall with Advanced Security (Inbound/Outbound Rules)"},
        {"cmd": "printmanagement.msc", "type": "MMC", "alias": "print management, printer spooler", "desc": "Print Management Console (Printer Drivers, Ports & Queues)"},
        {"cmd": "tpm.msc", "type": "MMC", "alias": "tpm management, tpm chip, tpm", "desc": "Trusted Platform Module Management (TPM Chip Specs & Status)"},
        {"cmd": "wmimgmt.msc", "type": "MMC", "alias": "wmi management, wmimgmt", "desc": "WMI Management Console (Windows Management Instrumentation)"},
        {"cmd": "rsop.msc", "type": "MMC", "alias": "resultant policy, rsop", "desc": "Resultant Set of Policy (Verify Applied Active GPO Policies)"},
        {"cmd": "virtmgmt.msc", "type": "MMC", "alias": "hyperv manager, virtmgmt, virtual machines", "desc": "Hyper-V Manager (Manage Virtual Machines & Virtual Networks)"},
        {"cmd": "comexp.msc", "type": "MMC", "alias": "component services, comexp, dcom", "desc": "Component Services (DCOM Configuration & COM+ Applications)"},
        {"cmd": "azman.msc", "type": "MMC", "alias": "authorization manager, azman", "desc": "Authorization Manager (Role-Based Access Control Snap-in)"},
        {"cmd": "cliconfg.exe", "type": "GUI", "alias": "sql client config, cliconfg", "desc": "SQL Server Client Network Utility (TCP/IP & Named Pipes)"},
        {"cmd": "odbcad32.exe", "type": "GUI", "alias": "odbc administrator, odbc data sources", "desc": "ODBC Data Source Administrator (DSNs & Database Drivers)"},
        {"cmd": "gpmc.msc", "type": "MMC", "alias": "group policy management console, gpmc", "desc": "Group Policy Management Console (Enterprise Domain GPOs)"},
        {"cmd": "gpme.msc", "type": "MMC", "alias": "group policy editor snapin, gpme", "desc": "Group Policy Management Editor Snap-in"},
        {"cmd": "iis.msc", "type": "MMC", "alias": "iis manager, web server manager", "desc": "Internet Information Services (IIS) 6.0/10.0 Web Manager"},
        {"cmd": "dnsmgmt.msc", "type": "MMC", "alias": "dns manager console, dnsmgmt", "desc": "DNS Server Management Console Snap-in"},
        {"cmd": "dhcpmgmt.msc", "type": "MMC", "alias": "dhcp manager console, dhcpmgmt", "desc": "DHCP Server Management Console Snap-in"},
        {"cmd": "dfsmgmt.msc", "type": "MMC", "alias": "dfs management console, dfsmgmt", "desc": "Distributed File System (DFS) Namespace & Replication Hub"}
    ],
    "modern_settings_uris": [
        {"cmd": "ms-settings:", "type": "URI", "alias": "settings, modern settings", "desc": "Windows Modern Settings Dashboard"},
        {"cmd": "ms-settings:windowsupdate", "type": "URI", "alias": "windows update, update check", "desc": "Windows Update (Check for Security Patches & Feature Updates)"},
        {"cmd": "ms-settings:network", "type": "URI", "alias": "network settings modern", "desc": "Network & Internet Overview and Airplane Mode"},
        {"cmd": "ms-settings:network-wifi", "type": "URI", "alias": "wifi settings, wifi settings modern", "desc": "Wi-Fi Networks, Hardware Properties & Known Networks"},
        {"cmd": "ms-settings:network-status", "type": "URI", "alias": "network status modern", "desc": "Network Connection Status & Data Usage Limits"},
        {"cmd": "ms-settings:network-ethernet", "type": "URI", "alias": "ethernet settings modern", "desc": "Ethernet Adapter Settings, IP & DNS Assignments"},
        {"cmd": "ms-settings:network-vpn", "type": "URI", "alias": "vpn settings modern", "desc": "VPN Connections (Add / Configure Virtual Private Networks)"},
        {"cmd": "ms-settings:network-proxy", "type": "URI", "alias": "proxy settings modern", "desc": "Proxy Server Settings & Automatic Proxy Detection"},
        {"cmd": "ms-settings:network-dialup", "type": "URI", "alias": "dialup settings modern", "desc": "Dial-Up & Broadband Connection Setup"},
        {"cmd": "ms-settings:network-mobilehotspot", "type": "URI", "alias": "hotspot settings modern, mobile hotspot", "desc": "Mobile Hotspot (Share Cellular / Wi-Fi Connection)"},
        {"cmd": "ms-settings:network-airplanemode", "type": "URI", "alias": "airplane mode modern", "desc": "Airplane Mode Hardware Radios Control"},
        {"cmd": "ms-settings:bluetooth", "type": "URI", "alias": "bluetooth settings, bluetooth modern", "desc": "Bluetooth & Other Wireless Devices Pair Cockpit"},
        {"cmd": "ms-settings:printers", "type": "URI", "alias": "printers modern", "desc": "Printers & Scanners Management Dashboard"},
        {"cmd": "ms-settings:mouse", "type": "URI", "alias": "mouse modern", "desc": "Mouse Pointer Speed & Primary Button Settings"},
        {"cmd": "ms-settings:typing", "type": "URI", "alias": "typing settings modern", "desc": "Typing Settings (Touch Keyboard, Autocorrect, Text Predictions)"},
        {"cmd": "ms-settings:pen", "type": "URI", "alias": "pen modern, surface pen", "desc": "Pen & Windows Ink Shortcuts & Handwriting Input"},
        {"cmd": "ms-settings:autoplay", "type": "URI", "alias": "autoplay modern", "desc": "AutoPlay Defaults for Flash Drives & Memory Cards"},
        {"cmd": "ms-settings:usb", "type": "URI", "alias": "usb settings modern", "desc": "USB Connection Notifications & Battery Optimization"},
        {"cmd": "ms-settings:appsfeatures", "type": "URI", "alias": "apps and features modern, installed apps", "desc": "Installed Modern Store Apps & Desktop Applications"},
        {"cmd": "ms-settings:defaultapps", "type": "URI", "alias": "default apps modern", "desc": "Default Applications Configuration"},
        {"cmd": "ms-settings:optionalfeatures", "type": "URI", "alias": "optional features modern", "desc": "Optional Windows Features (SSH, RSAT, Graphics Tools)"},
        {"cmd": "ms-settings:startupapps", "type": "URI", "alias": "startup apps modern", "desc": "Startup Apps (Toggle Background Startup Programs & Impact)"},
        {"cmd": "ms-settings:storagesense", "type": "URI", "alias": "storage sense, disk usage modern", "desc": "Storage Breakdown & Storage Sense Automated Temp Cleaning"},
        {"cmd": "ms-settings:display", "type": "URI", "alias": "display modern, night light settings", "desc": "Display Brightness, Night Light, Multiple Monitors & HDR"},
        {"cmd": "ms-settings:sound", "type": "URI", "alias": "sound modern", "desc": "Sound Output, Spatial Audio & Volume Mixer"},
        {"cmd": "ms-settings:notifications", "type": "URI", "alias": "notifications modern, focus assist", "desc": "Notifications, App Banners & Do Not Disturb / Focus Assist"},
        {"cmd": "ms-settings:batterysaver", "type": "URI", "alias": "battery modern, battery usage", "desc": "Battery Usage Per App & Battery Saver Thresholds"},
        {"cmd": "ms-settings:powersleep", "type": "URI", "alias": "power sleep modern", "desc": "Power, Sleep & Screen Timeout Rules"},
        {"cmd": "ms-settings:multitasking", "type": "URI", "alias": "multitasking modern, snap windows", "desc": "Multitasking, Snap Windows, Virtual Desktops & Alt+Tab"},
        {"cmd": "ms-settings:project", "type": "URI", "alias": "project screen modern, miractast", "desc": "Projecting to This PC (Miracast Wireless Display Receiver)"},
        {"cmd": "ms-settings:clipboard", "type": "URI", "alias": "clipboard history modern", "desc": "Clipboard History (Win + V) & Cloud Sync"},
        {"cmd": "ms-settings:remotedesktop", "type": "URI", "alias": "remote desktop modern", "desc": "Remote Desktop Server Enablement & Connection Ports"},
        {"cmd": "ms-settings:privacy", "type": "URI", "alias": "privacy modern", "desc": "Windows Privacy, Camera, Microphone & Location Permissions"},
        {"cmd": "ms-settings:windowsdefender", "type": "URI", "alias": "windows security modern, defender", "desc": "Windows Security (Virus & Threat Protection, Firewall, Device Security)"},
        {"cmd": "ms-settings:activation", "type": "URI", "alias": "activation modern, license status", "desc": "Windows Product Key & Digital License Activation Status"},
        {"cmd": "ms-settings:recovery", "type": "URI", "alias": "recovery modern, reset pc", "desc": "Recovery Options, Advanced Startup & Reset This PC"},
        {"cmd": "ms-settings:about", "type": "URI", "alias": "about pc modern", "desc": "About PC (Processor, Installed RAM, Device ID, Windows Edition)"},
        {"cmd": "ms-settings:colors", "type": "URI", "alias": "dark mode, theme colors", "desc": "Personalization Colors (Dark Mode / Light Mode Switcher & Accent)"},
        {"cmd": "ms-settings:taskbar", "type": "URI", "alias": "taskbar settings modern", "desc": "Taskbar Alignment, Corner Icons & Auto-Hide Behaviors"},
        {"cmd": "ms-settings:developers", "type": "URI", "alias": "developer mode modern", "desc": "Developer Mode (Sideload Apps, Remote Diagnostics, End Task)"},
        {"cmd": "ms-settings:crossdevice", "type": "URI", "alias": "phone link modern, cross device", "desc": "Phone Link & Mobile Device Synchronization Hub"},
        {"cmd": "ms-settings:speech", "type": "URI", "alias": "speech modern", "desc": "Speech Recognition, Microphone Setup & Text-to-Speech Voices"},
        {"cmd": "ms-settings:regionlanguage", "type": "URI", "alias": "languages modern", "desc": "Preferred Languages, Windows Display Language & Language Packs"},
        {"cmd": "ms-settings:dateandtime", "type": "URI", "alias": "date time modern", "desc": "Date & Time Auto-Sync via time.windows.com NTP"},
        {"cmd": "ms-settings:easeofaccess-magnifier", "type": "URI", "alias": "magnifier modern", "desc": "Accessibility Magnifier Options & Fullscreen Zoom Factor"},
        {"cmd": "ms-settings:easeofaccess-narrator", "type": "URI", "alias": "narrator modern", "desc": "Accessibility Narrator Screen Reader Settings"}
    ],
    "network_admin": [
        {"cmd": "ipconfig /all", "type": "CLI", "alias": "ipconfig, ip details", "desc": "Display Full TCP/IP Network Configuration & DHCP/DNS Servers"},
        {"cmd": "ipconfig /flushdns", "type": "CLI", "alias": "flush dns, clear dns", "desc": "Flush and Purge the DNS Client Resolver Cache"},
        {"cmd": "ipconfig /displaydns", "type": "CLI", "alias": "display dns, show dns cache", "desc": "Display All Cached DNS Host Records and Time-To-Live"},
        {"cmd": "ipconfig /release", "type": "CLI", "alias": "release ip", "desc": "Release Current IPv4 Lease from DHCP Server"},
        {"cmd": "ipconfig /renew", "type": "CLI", "alias": "renew ip", "desc": "Renew IPv4 Address Lease from DHCP Server"},
        {"cmd": "netstat -ano", "type": "CLI", "alias": "netstat ports, open ports cli", "desc": "Display All Active Listening Connections with PID Association"},
        {"cmd": "netstat -ab", "type": "CLI", "alias": "netstat binaries", "desc": "Display Active TCP Connections with Owning Executable Names"},
        {"cmd": "netstat -e", "type": "CLI", "alias": "netstat stats, ethernet stats", "desc": "Display Ethernet Statistics (Bytes Sent/Received, Packet Errors)"},
        {"cmd": "ping 8.8.8.8", "type": "CLI", "alias": "ping google, ping test", "desc": "Send ICMP Echo Requests to Verify Network Latency"},
        {"cmd": "tracert 8.8.8.8", "type": "CLI", "alias": "traceroute, tracert", "desc": "Trace Route Network Hops to Remote Destination"},
        {"cmd": "pathping 8.8.8.8", "type": "CLI", "alias": "pathping", "desc": "Comprehensive Route Tracing with Per-Hop Packet Loss Analysis"},
        {"cmd": "nslookup", "type": "CLI", "alias": "nslookup, dns query", "desc": "Query Domain Name Servers for DNS Resource Records"},
        {"cmd": "route print", "type": "CLI", "alias": "route table, ip routing", "desc": "Print IP Routing Table, Network Destinations & Gateways"},
        {"cmd": "arp -a", "type": "CLI", "alias": "arp table, mac arp", "desc": "Display Address Resolution Protocol Cache (IP to MAC mapping)"},
        {"cmd": "getmac /v", "type": "CLI", "alias": "getmac, mac address", "desc": "Display Physical MAC Addresses of All Network Adapters"},
        {"cmd": "nbtstat -n", "type": "CLI", "alias": "nbtstat names", "desc": "Display Local NetBIOS Names Registered by Machine"},
        {"cmd": "nbtstat -c", "type": "CLI", "alias": "nbtstat cache", "desc": "Display NetBIOS Name Cache with Remote IP Resolutions"},
        {"cmd": "net view", "type": "CLI", "alias": "net view, view network", "desc": "Inspect Shared Computers and Resources on Local Subnet"},
        {"cmd": "net share", "type": "CLI", "alias": "net share, smb shares", "desc": "List All Active Local Network Shares and Administrative IPC$ Drives"},
        {"cmd": "net use", "type": "CLI", "alias": "net use, mapped drives", "desc": "Display Active SMB Network Shares and Mapped Drive Letters"},
        {"cmd": "net session", "type": "CLI", "alias": "net session, smb sessions", "desc": "List All Active Network Sessions Connected to Local Machine"},
        {"cmd": "net time", "type": "CLI", "alias": "net time, domain time", "desc": "Synchronize Time with Domain Time Server"},
        {"cmd": "netsh wlan show profiles", "type": "CLI", "alias": "wifi profiles, saved wifi", "desc": "List All Saved Wi-Fi SSIDs on Machine"},
        {"cmd": "netsh wlan show interfaces", "type": "CLI", "alias": "wifi signal, link speed", "desc": "Inspect Wi-Fi Adapter State, Signal %, Channel & BSSID"},
        {"cmd": "netsh wlan show networks mode=bssid", "type": "CLI", "alias": "wifi scan cli, nearby wifi", "desc": "Scan and Display All Nearby Wi-Fi Networks, SSIDs & Channels"},
        {"cmd": "netsh wlan show wlanreport", "type": "CLI", "alias": "wlan report, wifi report", "desc": "Generate HTML Wi-Fi Diagnostics Report & Drop-off Analysis"},
        {"cmd": "netsh int ip reset", "type": "CLI", "alias": "reset ip stack", "desc": "Reset TCP/IP Protocol Stack to Out-of-Box Factory State"},
        {"cmd": "netsh winsock reset", "type": "CLI", "alias": "reset winsock, winsock fix", "desc": "Reset Windows Sockets (Winsock) Catalog Layer"},
        {"cmd": "netsh advfirewall reset", "type": "CLI", "alias": "reset firewall cli", "desc": "Reset Windows Defender Firewall Rules to Factory Default"},
        {"cmd": "netsh interface ipv4 show subinterfaces", "type": "CLI", "alias": "mtu size cli", "desc": "Display MTU Sizes and Interface Speeds for All Adapters"},
        {"cmd": "netsh interface ipv4 show addresses", "type": "CLI", "alias": "ip addresses cli", "desc": "Display Detailed IPv4 Addresses, Subnets & Gateways"},
        {"cmd": "bitsadmin /list /allusers", "type": "CLI", "alias": "bitsadmin jobs, bits jobs", "desc": "List All Background Intelligent Transfer Service (BITS) Download Jobs"},
        {"cmd": "hostname", "type": "CLI", "alias": "computer hostname", "desc": "Print Machine NetBIOS / DNS Hostname"},
        {"cmd": "qprocess", "type": "CLI", "alias": "query processes", "desc": "Quickly Query Local and Remote Terminal Session Processes"},
        {"cmd": "qwinsta", "type": "CLI", "alias": "query sessions", "desc": "Display Information About Active Remote Desktop Sessions"},
        {"cmd": "curl -I https://www.google.com", "type": "CLI", "alias": "curl test, http test", "desc": "Test HTTP/HTTPS Web Connectivity and Inspect Response Headers"}
    ],
    "storage_filesystem": [
        {"cmd": "sfc /scannow", "type": "CLI", "alias": "sfc scan, repair system files", "desc": "System File Checker: Scan and Repair Corrupted Windows System Files"},
        {"cmd": "dism /online /cleanup-image /checkhealth", "type": "CLI", "alias": "dism check", "desc": "Check if Windows Component Store Image has Been Flagged Corrupt"},
        {"cmd": "dism /online /cleanup-image /scanhealth", "type": "CLI", "alias": "dism scan", "desc": "Scan Windows Image for Component Store Corruption"},
        {"cmd": "dism /online /cleanup-image /restorehealth", "type": "CLI", "alias": "dism restore, dism repair", "desc": "Repair Windows Component Store Using Official Windows Update Source"},
        {"cmd": "chkdsk C: /f", "type": "CLI", "alias": "chkdsk, check disk repair", "desc": "Check Disk & Fix Volume File System Errors on Next Reboot"},
        {"cmd": "cleanmgr.exe", "type": "GUI", "alias": "disk cleanup, cleanmgr", "desc": "Windows Disk Cleanup Tool (Delete Temporary Files & Old Updates)"},
        {"cmd": "defrag C: /O", "type": "CLI", "alias": "defrag, optimize drive", "desc": "Optimize Drives: Issue TRIM to SSDs or Defragment Mechanical HDDs"},
        {"cmd": "diskpart", "type": "CLI", "alias": "diskpart cli", "desc": "Disk Partitioning Command Line Utility"},
        {"cmd": "fsutil volume diskfree C:", "type": "CLI", "alias": "disk free cli", "desc": "Query Total and Free Storage Space on Volume"},
        {"cmd": "fsutil dirty query C:", "type": "CLI", "alias": "check dirty bit, dirty volume", "desc": "Query Volume Dirty Bit (Indicates Unsaved Changes / File System Damage)"},
        {"cmd": "fsutil fsinfo drives", "type": "CLI", "alias": "list drive letters", "desc": "Enumerate All Mounted Drive Letters on Computer"},
        {"cmd": "fsutil fsinfo volumeinfo C:", "type": "CLI", "alias": "volume info cli", "desc": "Inspect File System Type, NTFS Flags, Serial Number & Cluster Size"},
        {"cmd": "fsutil behavior query DisableDeleteNotify", "type": "CLI", "alias": "check trim, ssd trim status", "desc": "Check SSD TRIM Notification State (0 = Enabled, 1 = Disabled)"},
        {"cmd": "mountvol", "type": "CLI", "alias": "mountvol cli, volume guids", "desc": "List All Mounted Volume GUIDs and Volume Mount Points"},
        {"cmd": "vssadmin list shadows", "type": "CLI", "alias": "list shadow copies, vss list", "desc": "List All Active Volume Shadow Copies and Restore Point Snapshots"},
        {"cmd": "vssadmin list providers", "type": "CLI", "alias": "vss providers", "desc": "List Registered Volume Shadow Copy Hardware/Software Providers"},
        {"cmd": "vssadmin list writers", "type": "CLI", "alias": "vss writers", "desc": "Inspect Volume Shadow Copy Writers and Check for Failed State"},
        {"cmd": "reagentc /info", "type": "CLI", "alias": "winre info, recovery partition status", "desc": "Windows Recovery Environment (WinRE) Status, BCD GUID & Image Path"},
        {"cmd": "bcdedit /enum", "type": "CLI", "alias": "bcdedit enum, boot config", "desc": "Enumerate Boot Configuration Data (BCD) OS Boot Loaders"},
        {"cmd": "manage-bde -status", "type": "CLI", "alias": "bitlocker status, manage-bde", "desc": "Inspect BitLocker Encryption Status, Protection Level & Method"},
        {"cmd": "robocopy", "type": "CLI", "alias": "robocopy cli", "desc": "Robust Multi-Threaded File Copy Engine with Resume Support"},
        {"cmd": "tree /f /a", "type": "CLI", "alias": "directory tree", "desc": "Display Graphical Directory Hierarchy and File Tree"},
        {"cmd": "compact /c /s:C:\\Temp", "type": "CLI", "alias": "ntfs compact", "desc": "NTFS Transparent File & Folder Compression"},
        {"cmd": "cipher /w:C:", "type": "CLI", "alias": "cipher wipe", "desc": "Wipe and Overwrite Free Unallocated Space on Drive"},
        {"cmd": "icacls", "type": "CLI", "alias": "file permissions, icacls", "desc": "Display and Modify File and Folder Security Access Control Lists (ACLs)"},
        {"cmd": "takeown /f <file>", "type": "CLI", "alias": "take ownership", "desc": "Take Ownership of Locked Administrator Files or Folders"}
    ],
    "process_services": [
        {"cmd": "tasklist /v", "type": "CLI", "alias": "tasklist, running tasks", "desc": "List All Active Tasks with Memory Usage and Window Titles"},
        {"cmd": "tasklist /svc", "type": "CLI", "alias": "tasklist services", "desc": "List Process PIDs and the Windows Services Hosted by Them"},
        {"cmd": "tasklist /m", "type": "CLI", "alias": "tasklist dlls, loaded modules", "desc": "List Processes and All Loaded DLL Dynamic Libraries"},
        {"cmd": "taskkill /f /im <name>", "type": "CLI", "alias": "kill process name", "desc": "Forcefully Terminate Process by Executable Name"},
        {"cmd": "taskkill /f /pid <pid>", "type": "CLI", "alias": "kill process pid", "desc": "Forcefully Terminate Process by Process ID (PID)"},
        {"cmd": "sc query type= service", "type": "CLI", "alias": "query services cli", "desc": "Query Windows Service Controller for Service States"},
        {"cmd": "sc queryex", "type": "CLI", "alias": "query extended services", "desc": "Query Extended Service Status Including Owning Process PIDs"},
        {"cmd": "sc start <service>", "type": "CLI", "alias": "start service cli", "desc": "Send Start Signal to a Windows Service"},
        {"cmd": "sc stop <service>", "type": "CLI", "alias": "stop service cli", "desc": "Send Stop Signal to a Running Windows Service"},
        {"cmd": "sc qc <service>", "type": "CLI", "alias": "service config cli", "desc": "Query Service Binary Path, Startup Type & Account Credentials"},
        {"cmd": "schtasks /query /fo TABLE", "type": "CLI", "alias": "query scheduled tasks", "desc": "Display All Scheduled Tasks in Clean Table Format"},
        {"cmd": "driverquery /v", "type": "CLI", "alias": "list drivers cli", "desc": "List All Installed Kernel and Hardware Device Drivers"},
        {"cmd": "powercfg /batteryreport", "type": "CLI", "alias": "battery report, battery health", "desc": "Generate Comprehensive HTML Battery Health & Cycle Life Report"},
        {"cmd": "powercfg /energy", "type": "CLI", "alias": "energy report", "desc": "Generate HTML Energy Efficiency & Power Drain Analysis"},
        {"cmd": "wmic process get caption,commandline,processid", "type": "CLI", "alias": "process commandlines", "desc": "Display Processes with Exact Command Line Launch Arguments"},
        {"cmd": "wmic service get name,displayname,state,startmode", "type": "CLI", "alias": "wmic services list", "desc": "Display Full WMI Service Inventory with Start Mode & Status"}
    ],
    "security_admin": [
        {"cmd": "whoami /all", "type": "CLI", "alias": "whoami, user privileges", "desc": "Display Current User Name, Security Identifiers (SIDs) & Privileges"},
        {"cmd": "whoami /priv", "type": "CLI", "alias": "whoami privileges", "desc": "Display Assigned User Rights & Privileges (e.g. SeDebugPrivilege)"},
        {"cmd": "whoami /groups", "type": "CLI", "alias": "whoami groups", "desc": "Display Security Group Memberships and Mandatory SIDs"},
        {"cmd": "gpupdate /force", "type": "CLI", "alias": "gpupdate, refresh policy", "desc": "Force Immediate Refresh of Computer & User Group Policy Objects"},
        {"cmd": "gpresult /r", "type": "CLI", "alias": "gpresult, gpo status", "desc": "Display Resultant Set of Policy (RSoP) Summary in Terminal"},
        {"cmd": "net user", "type": "CLI", "alias": "list users, net user", "desc": "List All Local User Accounts Registered on This Machine"},
        {"cmd": "net localgroup administrators", "type": "CLI", "alias": "list admins, local admins", "desc": "List All Accounts with Administrator Privileges"},
        {"cmd": "net localgroup", "type": "CLI", "alias": "list local groups", "desc": "Enumerate All Local Security Groups on the System"},
        {"cmd": "net accounts", "type": "CLI", "alias": "password policy, net accounts", "desc": "Display Password Expiration, Lockout Thresholds & Length Policy"},
        {"cmd": "netplwiz", "type": "GUI", "alias": "netplwiz, user accounts gui", "desc": "Advanced User Accounts Dialog (Manage Auto-Login & Groups)"},
        {"cmd": "auditpol /get /category:*", "type": "CLI", "alias": "audit policy cli", "desc": "Audit Security Subcategories (Logon, Object Access, Privilege Use)"},
        {"cmd": "dsregcmd /status", "type": "CLI", "alias": "azure ad status, dsregcmd", "desc": "Inspect Azure AD Join Status, Workplace Join & Primary Refresh Token"},
        {"cmd": "certutil -dump", "type": "CLI", "alias": "certutil, certificates cli", "desc": "Certificate Utility: Dump and Verify Installed Security Certificates"},
        {"cmd": "certutil -store my", "type": "CLI", "alias": "my certificates", "desc": "Display Personal User Security Certificates Store"},
        {"cmd": "certutil -store root", "type": "CLI", "alias": "root certificates", "desc": "Display Trusted Root Certification Authorities Store"},
        {"cmd": "certutil -urlcache * delete", "type": "CLI", "alias": "purge crl cache", "desc": "Purge Windows Certificate Revocation List (CRL) Cache"},
        {"cmd": "klist", "type": "CLI", "alias": "kerberos tickets, klist", "desc": "List Cached Kerberos Authentication Tickets"},
        {"cmd": "klist purge", "type": "CLI", "alias": "purge tickets", "desc": "Purge and Flush Cached Kerberos Authentication Tickets"}
    ],
    "builtin_utilities": [
        {"cmd": "regedit.exe", "type": "GUI", "alias": "registry, registry editor, regedit", "desc": "Windows Registry Editor (Inspect & Modify HKLM, HKCU Keys)"},
        {"cmd": "control.exe", "type": "GUI", "alias": "control panel, control", "desc": "Classic Windows Control Panel Master View"},
        {"cmd": "calc.exe", "type": "GUI", "alias": "calculator, calc", "desc": "Windows Desktop Calculator"},
        {"cmd": "notepad.exe", "type": "GUI", "alias": "notepad, text editor", "desc": "Windows Notepad Editor"},
        {"cmd": "mspaint.exe", "type": "GUI", "alias": "paint, mspaint", "desc": "Windows Paint Graphics Studio"},
        {"cmd": "write.exe", "type": "GUI", "alias": "wordpad, write", "desc": "WordPad Rich Text Document Editor"},
        {"cmd": "explorer.exe", "type": "GUI", "alias": "explorer, file explorer", "desc": "Windows File Explorer"},
        {"cmd": "cmd.exe", "type": "CLI", "alias": "cmd, command prompt", "desc": "Windows Command Prompt Shell"},
        {"cmd": "powershell.exe", "type": "CLI", "alias": "powershell, powershell shell", "desc": "Windows PowerShell 5.1 Automation Console"},
        {"cmd": "wt.exe", "type": "GUI", "alias": "windows terminal, wt", "desc": "Modern Windows Terminal (Multi-Tab PowerShell & WSL)"},
        {"cmd": "cleanmgr.exe", "type": "GUI", "alias": "cleanmgr, disk cleaner", "desc": "Disk Cleanup Dialog for Temp Files and Previous Installations"},
        {"cmd": "dfrgui.exe", "type": "GUI", "alias": "defragmenter gui, dfrgui", "desc": "Drive Defragmenter and Optimizer"},
        {"cmd": "snippingtool.exe", "type": "GUI", "alias": "snipping tool, screenshot tool, snip", "desc": "Windows Snipping Tool & Screen Capture Utility"},
        {"cmd": "mstsc.exe", "type": "GUI", "alias": "remote desktop, rdp client, mstsc", "desc": "Remote Desktop Connection Client"},
        {"cmd": "quickassist.exe", "type": "GUI", "alias": "quick assist, remote help", "desc": "Microsoft Quick Assist Remote Support Screen Sharing"},
        {"cmd": "magnify.exe", "type": "GUI", "alias": "magnifier, zoom screen", "desc": "Screen Magnifier Accessibility Utility"},
        {"cmd": "osk.exe", "type": "GUI", "alias": "on screen keyboard, virtual keyboard", "desc": "On-Screen Virtual Keyboard"},
        {"cmd": "charmap.exe", "type": "GUI", "alias": "character map, charmap", "desc": "Character Map (Search Unicode Characters and Glyphs)"},
        {"cmd": "eudcedit.exe", "type": "GUI", "alias": "character editor, eudcedit", "desc": "Private Character Editor (Custom Glyph Vector Tool)"},
        {"cmd": "mrt.exe", "type": "GUI", "alias": "mrt, malicious software removal", "desc": "Microsoft Malicious Software Removal Tool (On-Demand Deep Scan)"},
        {"cmd": "msra.exe", "type": "GUI", "alias": "remote assistance, msra", "desc": "Windows Remote Assistance (Invite Someone to Help Connect)"},
        {"cmd": "optionalfeatures.exe", "type": "GUI", "alias": "optional features, windows features", "desc": "Turn Windows Features On or Off (WSL, Hyper-V, Sandbox, IIS)"},
        {"cmd": "shutdown /i", "type": "GUI", "alias": "shutdown gui, remote shutdown", "desc": "Remote & Local Graphical Shutdown / Restart Dialog"},
        {"cmd": "control userpasswords2", "type": "GUI", "alias": "userpasswords2, user passwords", "desc": "Legacy User Accounts Management Window"},
        {"cmd": "tabcal.exe", "type": "GUI", "alias": "digitizer calibration, tabcal", "desc": "Digitizer and Stylus Pen Calibration Tool"},
        {"cmd": "shell:::{ED7BA470-8E54-465E-825C-99712043E01C}", "type": "GUI", "alias": "god mode, godmode", "desc": "Windows Master Control Panel (God Mode: 200+ Control Applets in One List)"}
    ]
}

# ==============================================================================
# CUSTOM COMMANDS LOADER (TXT & JSON FILES)
# ==============================================================================

CUSTOM_COMMANDS_FILE_PATHS = [
    Path.cwd() / "custom_commands.json",
    Path.cwd() / "custom_commands.txt",
    Path.cwd().parent / "client" / "custom_commands.json",
    Path.cwd().parent / "client" / "custom_commands.txt",
    Path(__file__).resolve().parents[2] / "client" / "custom_commands.json",
    Path(__file__).resolve().parents[2] / "client" / "custom_commands.txt"
]

def load_custom_commands() -> List[Dict[str, str]]:
    """
    Dynamically loads custom user commands from custom_commands.json or custom_commands.txt.
    Supports user expansion on the fly without server restart!
    """
    custom_list: List[Dict[str, str]] = []
    seen_triggers = set()

    for file_path in CUSTOM_COMMANDS_FILE_PATHS:
        if not file_path.exists():
            continue

        try:
            if file_path.suffix.lower() == ".json":
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        for item in data:
                            if isinstance(item, dict) and "trigger" in item and "command" in item:
                                trig = item["trigger"].strip().lower()
                                if trig and trig not in seen_triggers:
                                    seen_triggers.add(trig)
                                    custom_list.append({
                                        "cmd": item["command"],
                                        "type": "CUSTOM",
                                        "alias": trig,
                                        "desc": item.get("description", "Custom user command")
                                    })
            elif file_path.suffix.lower() == ".txt":
                with open(file_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith("#"):
                            continue
                        # Format: trigger = command | description
                        if "=" in line:
                            trigger, rest = line.split("=", 1)
                            trig = trigger.strip().lower()
                            cmd = rest.strip()
                            desc = "Custom user command"
                            if "|" in cmd:
                                cmd, desc = cmd.split("|", 1)
                            if trig and trig not in seen_triggers:
                                seen_triggers.add(trig)
                                custom_list.append({
                                    "cmd": cmd.strip(),
                                    "type": "CUSTOM",
                                    "alias": trig,
                                    "desc": desc.strip()
                                })
        except Exception:
            pass

    return custom_list

def get_total_commands_count() -> int:
    """Returns the total number of commands across all categories + custom commands."""
    total = sum(len(items) for items in WINDOWS_MASTER_CATALOG.values())
    total += len(load_custom_commands())
    return total

def get_categorized_commands_summary() -> str:
    """
    Returns a comprehensive, formatted multi-category string summary of all available tools
    and commands for display to the user.
    """
    total = get_total_commands_count()
    lines = [
        f"KRONOS MASTER WINDOWS COMMANDS CATALOG ({total}+ Loaded Commands):",
        "",
        "1. SYSTEM & DIAGNOSTICS:",
        "   - msinfo32 (System Information) • dxdiag (DirectX Diagnostics)",
        "   - winver (Windows Version) • msconfig (System Configuration)",
        "   - systeminfo (Machine Specs CLI) • perfmon (Performance Monitor)",
        "   - resmon (Resource Monitor) • taskmgr (Task Manager)",
        "   - eventvwr.msc (Event Logs) • perfmon /rel (Reliability Monitor)",
        "   - sysdm.cpl (System Properties) • systempropertiesadvanced (Env Vars)",
        "",
        "2. CONTROL PANEL APPLETS (.cpl):",
        "   - ncpa.cpl (Network Connections) • appwiz.cpl (Uninstall Programs)",
        "   - firewall.cpl (Windows Firewall) • mmsys.cpl (Sound & Audio Devices)",
        "   - desk.cpl (Display Settings) • powercfg.cpl (Power Plans & Sleep)",
        "   - inetcpl.cpl (Internet & Proxy) • joy.cpl (Game Controllers / USB Gamepad)",
        "   - timedate.cpl (Date & Time) • intl.cpl (Region & Language Formats)",
        "   - main.cpl (Mouse Properties) • wscui.cpl (Security & Maintenance)",
        "",
        "3. MANAGEMENT CONSOLES (.msc):",
        "   - devmgmt.msc (Device Manager) • diskmgmt.msc (Disk & Partition Manager)",
        "   - services.msc (Windows Services) • compmgmt.msc (Computer Management)",
        "   - taskschd.msc (Task Scheduler) • gpedit.msc (Local Group Policy)",
        "   - secpol.msc (Security Policy) • lusrmgr.msc (Local Users & Groups)",
        "   - certmgr.msc (Certificates) • wf.msc (Advanced Security Firewall)",
        "   - fsmgmt.msc (Shared Folders) • tpm.msc (TPM Chip Security)",
        "",
        "4. MODERN SETTINGS URIs (ms-settings:):",
        "   - ms-settings: (Settings Home) • ms-settings:windowsupdate (Windows Update)",
        "   - ms-settings:network (Network & Internet) • ms-settings:network-wifi (Wi-Fi)",
        "   - ms-settings:bluetooth (Bluetooth) • ms-settings:appsfeatures (Apps)",
        "   - ms-settings:storagesense (Storage Sense) • ms-settings:display (Display)",
        "   - ms-settings:sound (Sound) • ms-settings:privacy (Privacy & Permissions)",
        "   - ms-settings:windowsdefender (Security) • ms-settings:recovery (Reset PC)",
        "",
        "5. NETWORK & CONNECTIVITY CLI:",
        "   - ipconfig /all (IP Config) • ipconfig /flushdns (Flush DNS Cache)",
        "   - netstat -ano (Listening Ports & PIDs) • ping (Ping Host)",
        "   - tracert (Trace Route) • pathping (Packet Loss Hops)",
        "   - nslookup (DNS Lookup) • route print (IP Route Table)",
        "   - arp -a (ARP Cache) • getmac /v (Adapter MAC Addresses)",
        "   - netsh wlan show profiles (Wi-Fi SSIDs) • netsh winsock reset",
        "",
        "6. STORAGE & REPAIR CLI:",
        "   - sfc /scannow (System File Checker) • dism /online /cleanup-image /restorehealth",
        "   - chkdsk C: /f (Check Disk) • defrag C: /O (Optimize SSD/HDD)",
        "   - diskpart (Partition Utility) • robocopy (Multi-threaded Copy)",
        "   - cleanmgr.exe (Disk Cleanup) • tree (Directory Tree Graph)",
        "",
        "7. SECURITY & ACCOUNTS:",
        "   - whoami /all (User Token & Privileges) • gpupdate /force (Refresh GPO)",
        "   - net user (User Accounts) • net localgroup administrators (Admin List)",
        "   - netplwiz (Advanced User Accounts) • certutil (Certificates Dump)",
        "",
        "8. POPUP UTILITIES & GOD MODE:",
        "   - regedit.exe (Registry Editor) • control.exe (Control Panel)",
        "   - snippingtool.exe (Snipping Tool) • mstsc.exe (Remote Desktop)",
        "   - shutdown /i (Remote Shutdown GUI) • God Mode (200+ Tools in 1 List)"
    ]

    custom_cmds = load_custom_commands()
    if custom_cmds:
        lines.append("")
        lines.append(f"9. USER CUSTOM COMMANDS ({len(custom_cmds)} Loaded from custom_commands.txt):")
        for c in custom_cmds:
            lines.append(f"   - {c['alias']} -> {c['cmd']} ({c['desc']})")

    lines.append("")
    lines.append("Tip: Kisi bhi tool ko kholne ke liye seedhe bolein: 'open <tool>' (jaise 'open ncpa.cpl', 'open god mode', 'open devmgmt').")
    return "\n".join(lines)

def match_command_or_app(problem: str) -> Optional[Tuple[str, str, str]]:
    """
    Matches user natural prompt against the master catalog + custom commands.
    Returns: (command_to_execute, action_description, friendly_summary)
    """
    raw_p = problem.strip().lower()

    # Clean leading verbs for accurate keyword matching
    clean_p = re.sub(r'^(open|kholo|chalu|run|launch|start|show|dikhao)\s+', '', raw_p).strip()
    clean_p = re.sub(r'\s+(kholo|chalu karo|start karo|run karo|open karo)$', '', clean_p).strip()

    # 1. Custom user commands check first (user overrides)
    for custom in load_custom_commands():
        alias = custom["alias"]
        if alias and (raw_p == alias or clean_p == alias or f"/{alias}" == raw_p):
            cmd = custom["cmd"]
            if not cmd.lower().startswith("start-process") and not cmd.lower().startswith("get-") and not cmd.lower().startswith("invoke-"):
                cmd = f"Start-Process '{cmd}'"
            return (cmd, f"Launch Custom Tool: {custom['desc']}", f"Custom tool '{alias}' launch kar raha hoon, Professor.")

    # 2. Check God Mode
    if any(k in raw_p for k in ["god mode", "godmode", "master control panel"]):
        return (
            "Start-Process 'explorer.exe' -ArgumentList 'shell:::{ED7BA470-8E54-465E-825C-99712043E01C}'",
            "Open Windows God Mode Master Control Panel",
            "Windows Master God Mode khol diya gaya, Professor! Isme 200+ control applets ek sath milenge."
        )

    # 3. Check exact command names in all categories
    for category, items in WINDOWS_MASTER_CATALOG.items():
        for item in items:
            cmd_target = item["cmd"]
            aliases = [a.strip().lower() for a in item["alias"].split(",") if a.strip()]
            aliases.append(cmd_target.lower())
            base_cmd = cmd_target.split()[0].lower()
            aliases.append(base_cmd)
            # Remove extension (.msc, .cpl, .exe)
            no_ext = re.sub(r'\.(msc|cpl|exe)$', '', base_cmd)
            if no_ext != base_cmd:
                aliases.append(no_ext)

            for a in aliases:
                if not a:
                    continue
                # Match against cleaned prompt or raw prompt
                if clean_p == a or raw_p == a or raw_p == f"open {a}" or raw_p == f"kholo {a}" or raw_p == f"run {a}":
                    desc = item["desc"]
                    if item["type"] in ["GUI", "CPL", "MMC", "URI"]:
                        exec_cmd = f"Start-Process '{cmd_target}'"
                    else:
                        exec_cmd = cmd_target

                    return (
                        exec_cmd,
                        f"Launch {desc}",
                        f"{desc} khol diya gaya, Professor."
                    )

    return None
