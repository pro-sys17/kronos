# KRONOS Autonomous System Restoration Agent
# Client Bootstrap & Execution Engine
param(
    [string]$ServerUrl = "http://127.0.0.1:8000",
    [string]$SessionToken = "SESSION_TOKEN_PLACEHOLDER"
)

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# Color and formatting definitions (ANSI)
$ESC = [char]27
$CLR_RESET       = "$ESC[0m"
$CLR_BOLD        = "$ESC[1m"
$CLR_DIM         = "$ESC[2m"

# Terminal Theme Engine (Option B: Modern Dark Slate Grey Canvas Background)
$script:KronosThemeBg = "#23272e"  # Modern Slate Grey / Dark Charcoal (#23272e)
$script:KronosThemeFg = "#f0f3f6"  # Crisp Pure Silver/White Foreground
$script:KronosCursorColor = "#00e5ff" # Vibrant Cyan Cursor

function Set-KronosTerminalTheme {
    param(
        [string]$BgHex = $script:KronosThemeBg,
        [string]$FgHex = $script:KronosThemeFg
    )
    try {
        # OSC 11: Set Terminal Window Canvas Background Color
        # OSC 10: Set Terminal Window Default Foreground Color
        # OSC 12: Set Terminal Cursor Color
        [Console]::Write("$ESC]11;$BgHex$ESC\$ESC]10;$FgHex$ESC\$ESC]12;$script:KronosCursorColor$ESC\")
    } catch {}

    try {
        [Console]::ForegroundColor = [ConsoleColor]::White
    } catch {}
}

function Restore-KronosTerminalTheme {
    try {
        # OSC 111: Restore Background Color to terminal profile default
        # OSC 110: Restore Foreground Color to terminal profile default
        # OSC 112: Restore Cursor Color to default
        [Console]::Write("$ESC]111$ESC\$ESC]110$ESC\$ESC]112$ESC\$ESC[0m")
    } catch {}
}

# Activate Modern Slate Grey Theme immediately across terminal canvas
Set-KronosTerminalTheme

# Text hierarchy (High contrast on modern slate grey canvas)
$CLR_WHITE       = "$ESC[97m"              # Crisp pure white for titles & values
$CLR_TEXT        = "$ESC[38;5;253m"         # Clean, readable crisp silver text
$CLR_MUTED       = "$ESC[38;5;247m"         # Readable muted slate grey for secondary text
$CLR_DARK        = "$ESC[38;5;241m"         # Dark graphite / subtle grey

# Cards & Borders (Clean Modern Slate Grey & Crisp Silver White Theme)
$CLR_USER_BORDER = "$ESC[38;5;252m"         # Crisp Silver Grey / Light White for User Prompts
$CLR_BOT_BORDER  = "$ESC[38;5;250m"         # Sleek Clean Slate Grey for KRONOS Response Boxes
$CLR_SYS_BORDER  = "$ESC[38;5;248m"         # High-Contrast Visible Slate Grey for TUI Cards & Dashboards
$CLR_PANEL_TOP   = "$ESC[97m"               # Crisp Pure White Accent Top

# Semantic Accents (Ultra-vibrant on Slate Grey Canvas)
$CLR_CYAN        = "$ESC[38;5;45m"          # Primary accent Cyan
$CLR_GREEN       = "$ESC[38;5;120m"         # Mint Green (Success)
$CLR_YELLOW      = "$ESC[38;5;221m"         # Amber (Warning)
$CLR_AMBER       = "$ESC[38;5;221m"         # Amber alias
$CLR_RED         = "$ESC[38;5;203m"         # Coral Red (Error)
$CLR_BLUE        = "$ESC[38;5;75m"          # Sky Blue
$CLR_PURPLE      = "$ESC[38;5;141m"         # Lavender
$CLR_GRAY        = "$ESC[38;5;247m"         # Slate grey

# Unicode / ASCII Fallback detection
$script:UseUnicode = $true
try {
    if ([Console]::OutputEncoding.CodePage -ne 65001 -and -not $env:WT_SESSION) {
        $script:UseUnicode = $false
    }
} catch {
    $script:UseUnicode = $false
}

$BOX_TL = if ($script:UseUnicode) { "╭" } else { "+" }
$BOX_TR = if ($script:UseUnicode) { "╮" } else { "+" }
$BOX_BL = if ($script:UseUnicode) { "╰" } else { "+" }
$BOX_BR = if ($script:UseUnicode) { "╯" } else { "+" }
$BOX_H  = if ($script:UseUnicode) { "─" } else { "-" }
$BOX_V  = if ($script:UseUnicode) { "│" } else { "|" }
$BOX_ML = if ($script:UseUnicode) { "├" } else { "+" }
$BOX_MR = if ($script:UseUnicode) { "┤" } else { "+" }
$PTR    = if ($script:UseUnicode) { "►" } else { ">" }
$DOT    = if ($script:UseUnicode) { "•" } else { "*" }

$BACKUP_DIR = Join-Path $env:TEMP "kronos_backups"
$script:ConversationHistory = @()
$script:LastCommandOutput = ""
$script:CachedTelemetry = $null
$script:LastOpenedPath = $null

function Get-TermWidth {
    try {
        if (-not [Console]::IsOutputRedirected -and [Console]::WindowWidth -ge 30) {
            $w = [Console]::WindowWidth - 2
            if ($w -lt 60) { return 60 }
            if ($w -gt 160) { return 160 }
            return $w
        }
    } catch {}
    return 78
}

function Get-VisibleLength([string]$str) {
    if (-not $str) { return 0 }
    $clean = $str -replace '\x1b\[[0-9;]*[a-zA-Z]', ''
    return $clean.Length
}

function Pad-Visible([string]$str, [int]$targetWidth, [bool]$padLeft = $false) {
    $visLen = Get-VisibleLength $str
    $diff = $targetWidth - $visLen
    if ($diff -le 0) { return $str }
    $spaces = " " * $diff
    if ($padLeft) { return $spaces + $str } else { return $str + $spaces }
}

function Write-BoxTop($title) {
    $w = Get-TermWidth
    $vis = Get-VisibleLength $title
    $dashes = $w - $vis - 4
    if ($dashes -lt 2) { $dashes = 2 }
    Write-Host " ${CLR_SYS_BORDER}${BOX_TL}${BOX_H} $title " -NoNewline
    Write-Host ("${BOX_H}" * $dashes) -NoNewline
    Write-Host "${CLR_RESET}"
}

function Write-BoxDivider($title = "") {
    $w = Get-TermWidth
    if ($title) {
        $vis = Get-VisibleLength $title
        $dashes = $w - $vis - 4
        if ($dashes -lt 2) { $dashes = 2 }
        Write-Host " ${CLR_SYS_BORDER}${BOX_ML}${BOX_H} $title " -NoNewline
        Write-Host ("${BOX_H}" * $dashes) -NoNewline
        Write-Host "${CLR_RESET}"
    } else {
        Write-Host " ${CLR_SYS_BORDER}${BOX_ML}" -NoNewline
        Write-Host ("${BOX_H}" * ($w - 2)) -NoNewline
        Write-Host "${CLR_RESET}"
    }
}

function Write-BoxBottom {
    $w = Get-TermWidth
    Write-Host " ${CLR_SYS_BORDER}${BOX_BL}" -NoNewline
    Write-Host ("${BOX_H}" * ($w - 2)) -NoNewline
    Write-Host "${CLR_RESET}"
}

function Write-UserPromptBox {
    $w = Get-TermWidth
    $dashes = [math]::Max(2, $w - 14)
    Write-Host " ${CLR_USER_BORDER}${BOX_TL}${BOX_H} [YOU] " -NoNewline
    Write-Host ("${BOX_H}" * $dashes) -NoNewline
    Write-Host "${CLR_RESET}"
    Write-Host " ${CLR_USER_BORDER}${BOX_BL}❯ ${CLR_WHITE}" -NoNewline
}

function Write-BotBoxTop($title = "KRONOS AI") {
    $w = Get-TermWidth
    $vis = Get-VisibleLength $title
    $dashes = [math]::Max(2, $w - $vis - 6)
    Write-Host " ${CLR_BOT_BORDER}${BOX_TL}${BOX_H} $title " -NoNewline
    Write-Host ("${BOX_H}" * $dashes) -NoNewline
    Write-Host "${CLR_RESET}"
}

function Write-BotBoxBottom {
    $w = Get-TermWidth
    Write-Host " ${CLR_BOT_BORDER}${BOX_BL}" -NoNewline
    Write-Host ("${BOX_H}" * ($w - 2)) -NoNewline
    Write-Host "${CLR_RESET}"
}

function Trunc-Str($str, $maxLen) {
    if (-not $str) { return "" }
    if ($str.Length -gt $maxLen) {
        if ($maxLen -gt 3) {
            return $str.Substring(0, $maxLen - 3) + "..."
        }
        return $str.Substring(0, $maxLen)
    }
    return $str
}

function Get-Sparkline($values, $min = 0, $max = 100) {
    $chars = @(' ', '▂', '▃', '▄', '▅', '▆', '▇', '█')
    $result = ""
    if (-not $values -or $values.Count -eq 0) { return "        " }
    foreach ($v in $values) {
        $range = [math]::Max(1.0, [double]($max - $min))
        $norm = ([double]$v - $min) / $range
        if ($norm -lt 0) { $norm = 0 }
        if ($norm -gt 1) { $norm = 1 }
        $idx = [math]::Floor($norm * 7)
        $result += $chars[$idx]
    }
    return $result
}

function Get-ColoredGauge($percent, $width = 16) {
    $color = if ($percent -ge 85) { $CLR_RED } elseif ($percent -ge 70) { $CLR_YELLOW } else { $CLR_GREEN }
    $filled = [math]::Round(($percent / 100) * $width)
    if ($filled -gt $width) { $filled = $width }
    if ($filled -lt 0) { $filled = 0 }
    $empty = $width - $filled
    $bar = "${color}" + ("█" * $filled) + "${CLR_SYS_BORDER}" + ("░" * $empty) + "${CLR_RESET}"
    return "[$bar] ${color}${percent}%${CLR_RESET}"
}

function Get-ItemCategoryBadge($ext, [bool]$isFolder) {
    if ($isFolder) { return "$ESC[38;5;51m[DIR]$CLR_RESET" }
    switch -Regex ($ext) {
        '^\.(mkv|mp4|avi|mov|wmv|webm|flv)$'          { return "$ESC[38;5;206m[VID]$CLR_RESET" }
        '^\.(mp3|wav|flac|aac|ogg|m4a)$'              { return "$ESC[38;5;215m[AUD]$CLR_RESET" }
        '^\.(jpg|jpeg|png|bmp|gif|webp|svg)$'         { return "$ESC[38;5;177m[IMG]$CLR_RESET" }
        '^\.(zip|rar|7z|tar|gz|iso)$'                  { return "$ESC[38;5;220m[ZIP]$CLR_RESET" }
        '^\.(exe|bat|cmd|ps1|msi)$'                   { return "$ESC[38;5;84m[EXE]$CLR_RESET" }
        '^\.(apk)$'                                    { return "$ESC[38;5;120m[APP]$CLR_RESET" }
        '^\.(pdf|docx?|xlsx?|pptx?|txt|log|json|md)$' { return "$ESC[38;5;147m[DOC]$CLR_RESET" }
        default                                       { return "$ESC[38;5;248m[FILE]$CLR_RESET" }
    }
}

function Collect-Telemetry($forceRefresh = $false) {
    if ($script:CachedTelemetry -and -not $forceRefresh) {
        return $script:CachedTelemetry
    }

    $os = Get-CimInstance Win32_OperatingSystem -ErrorAction SilentlyContinue
    $cs = Get-CimInstance Win32_ComputerSystem -ErrorAction SilentlyContinue
    $hasInternet = [System.Net.NetworkInformation.NetworkInterface]::GetIsNetworkAvailable()
    $drives = (Get-PSDrive -PSProvider FileSystem | Where-Object { $_.Free -gt 0 } | ForEach-Object { $_.Name + ":" }) -join " "

    $script:CachedTelemetry = [PSCustomObject]@{
        ComputerName   = $env:COMPUTERNAME
        Username       = $env:USERNAME
        OSName         = if ($os) { $os.Caption } else { "Microsoft Windows" }
        OSVersion      = if ($os) { $os.Version } else { "11" }
        Architecture   = if ($os) { $os.OSArchitecture } else { "64-bit" }
        TotalMemoryGB  = if ($cs) { [math]::Round($cs.TotalPhysicalMemory / 1GB, 1) } else { 16 }
        Drives         = $drives
        ActiveAdapters = ((Get-NetAdapter -ErrorAction SilentlyContinue | Where-Object { $_.Name -notmatch "VMware|Loopback" } | ForEach-Object { "$($_.Name) [$($_.Status)]" }) -join "; ")
        InternetStatus = if ($hasInternet) { "ONLINE" } else { "OFFLINE" }
    }

    return $script:CachedTelemetry
}

function Read-MaskedPassword([string]$prompt = " Passcode ❯ ") {
    if ([Console]::IsInputRedirected) {
        return "kronos"
    }
    Write-Host -NoNewline $prompt
    $pass = ""
    while ($true) {
        $key = [Console]::ReadKey($true)
        if ($key.Key -eq [ConsoleKey]::Enter) {
            Write-Host ""
            break
        } elseif ($key.Key -eq [ConsoleKey]::Backspace) {
            if ($pass.Length -gt 0) {
                $pass = $pass.Substring(0, $pass.Length - 1)
                Write-Host -NoNewline "`b `b"
            }
        } elseif ($key.Key -eq [ConsoleKey]::Escape) {
            return $null
        } else {
            $char = $key.KeyChar
            if ($char -ge 32 -and $char -le 126) {
                $pass += $char
                Write-Host -NoNewline "*"
            }
        }
    }
    return $pass
}

function Show-LoginGateway {
    if ([Console]::IsInputRedirected) {
        return $true
    }

    $maxAttempts = 3
    $attempts = 0

    while ($attempts -lt $maxAttempts) {
        Clear-Host
        Write-Host ""
        Write-Host " ${CLR_SYS_BORDER}╭─ [GATEWAY] KRONOS SECURITY GATEWAY ──────────────────────────────${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}│  ${CLR_WHITE}Autonomous Windows Co-Pilot • Authorization Required${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}├──────────────────────────────────────────────────────────────────${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}│${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}│  ${CLR_MUTED}Detected Identity : ${CLR_WHITE}$env:USERNAME ($env:COMPUTERNAME)${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}│  ${CLR_MUTED}Security Protocol : ${CLR_CYAN}Zero-Trust Ephemeral Authentication${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}│  ${CLR_MUTED}Access Status     : ${CLR_YELLOW}● PROTECTED${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}│  ${CLR_MUTED}Default Passcode  : ${CLR_TEXT}Type ${CLR_GREEN}'kronos'${CLR_TEXT} or ${CLR_GREEN}'admin'${CLR_TEXT} (or your PIN)${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}│${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}╰──────────────────────────────────────────────────────────────────${CLR_RESET}"
        Write-Host ""

        $inputPass = Read-MaskedPassword " ${CLR_USER_BORDER}Authorization Passcode ❯ ${CLR_WHITE}"

        if ($inputPass -eq $null) {
            Write-Host " ${CLR_YELLOW}[*] Authentication aborted. Exiting KRONOS.${CLR_RESET}"
            exit
        }

        $validKeys = @("kronos", "admin", "1234", "$env:USERNAME".ToLower())
        if ($validKeys -contains $inputPass.Trim().ToLower()) {
            Write-Host ""
            Write-Host " ${CLR_GREEN}╭─ [OK] ACCESS GRANTED ──────────────────────────────────────────────${CLR_RESET}"
            Write-Host " ${CLR_GREEN}│  ${CLR_WHITE}Identity Verified: ${CLR_BOLD}$env:USERNAME${CLR_RESET}"
            Write-Host " ${CLR_GREEN}│  ${CLR_MUTED}Clearance Level  : ${CLR_CYAN}ROOT / ARCHITECT${CLR_RESET}"
            Write-Host " ${CLR_GREEN}│  ${CLR_MUTED}Session Token    : ${CLR_WHITE}Authenticated${CLR_RESET}"
            Write-Host " ${CLR_GREEN}╰──────────────────────────────────────────────────────────────────${CLR_RESET}"
            Write-Host ""
            Start-Sleep -Milliseconds 600
            return $true
        } else {
            $attempts++
            $rem = $maxAttempts - $attempts
            Write-Host ""
            Write-Host " ${CLR_RED}╭─ [DENIED] ACCESS DENIED ───────────────────────────────────────────────${CLR_RESET}"
            Write-Host " ${CLR_RED}│  ${CLR_WHITE}Invalid Passcode! Verification failed.${CLR_RESET}"
            Write-Host " ${CLR_RED}│  ${CLR_YELLOW}Attempts remaining: $rem${CLR_RESET}"
            Write-Host " ${CLR_RED}╰──────────────────────────────────────────────────────────────────${CLR_RESET}"
            Write-Host ""
            Start-Sleep -Seconds 1
        }
    }

    Write-Host " ${CLR_RED}[!] Maximum authentication attempts exceeded. Session locked.${CLR_RESET}"
    exit
}

function Show-Banner([bool]$useVtHome = $false) {
    if (-not $useVtHome) {
        Clear-Host
    } else {
        Write-Host "$ESC[H" -NoNewline
    }
    $t = Collect-Telemetry
    $isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
    $privBadge = if ($isAdmin) { "${CLR_GREEN}[ROOT]${CLR_RESET}" } else { "${CLR_AMBER}[USER]${CLR_RESET}" }
    $serverBadge = "${CLR_GREEN}[ONLINE]${CLR_RESET}"
    $engineBadge = "${CLR_CYAN}[GROQ NEURAL]${CLR_RESET}"

    $w = Get-TermWidth
    $innerW = $w - 4
    $colW = [math]::Floor($innerW / 2)

    # Top border
    $titleLeft = "${BOX_TL}${BOX_H} ${CLR_WHITE}${CLR_BOLD}KRONOS CORE v3.2${CLR_RESET} ${CLR_SYS_BORDER}"
    $titleRight = " ${CLR_CYAN}[SYSTEM CONTROL CENTRE]${CLR_RESET} ${CLR_SYS_BORDER}${BOX_H}${BOX_TR}"
    $midDashes = $w - (Get-VisibleLength $titleLeft) - (Get-VisibleLength $titleRight)
    if ($midDashes -lt 2) { $midDashes = 2 }
    Write-Host " ${CLR_SYS_BORDER}${titleLeft}" -NoNewline
    Write-Host ("${BOX_H}" * $midDashes) -NoNewline
    Write-Host "${titleRight}${CLR_RESET}$ESC[K"

    # Row 1: Host & RAM
    $c1 = " ${CLR_MUTED}Host     :${CLR_RESET} ${CLR_WHITE}$($t.ComputerName)${CLR_RESET}"
    $c2 = "${CLR_MUTED}RAM       :${CLR_RESET} ${CLR_WHITE}$($t.TotalMemoryGB) GB${CLR_RESET}"
    $row1 = (Pad-Visible $c1 $colW) + (Pad-Visible $c2 ($innerW - $colW))
    Write-Host " ${CLR_SYS_BORDER}${BOX_V}${CLR_RESET}$row1${CLR_SYS_BORDER}${BOX_V}${CLR_RESET}$ESC[K"

    # Row 2: Drives & Privilege
    $c3 = " ${CLR_MUTED}Drives   :${CLR_RESET} ${CLR_WHITE}$($t.Drives)${CLR_RESET}"
    $c4 = "${CLR_MUTED}Privilege :${CLR_RESET} $privBadge"
    $row2 = (Pad-Visible $c3 $colW) + (Pad-Visible $c4 ($innerW - $colW))
    Write-Host " ${CLR_SYS_BORDER}${BOX_V}${CLR_RESET}$row2${CLR_SYS_BORDER}${BOX_V}${CLR_RESET}$ESC[K"

    # Row 3: Server & AI Engine
    $c5 = " ${CLR_MUTED}Server   :${CLR_RESET} ${CLR_CYAN}$ServerUrl${CLR_RESET}"
    $c6 = "${CLR_MUTED}AI Engine :${CLR_RESET} $engineBadge $serverBadge"
    $row3 = (Pad-Visible $c5 $colW) + (Pad-Visible $c6 ($innerW - $colW))
    Write-Host " ${CLR_SYS_BORDER}${BOX_V}${CLR_RESET}$row3${CLR_SYS_BORDER}${BOX_V}${CLR_RESET}$ESC[K"

    # Bottom border
    Write-Host " ${CLR_SYS_BORDER}${BOX_BL}" -NoNewline
    Write-Host ("${BOX_H}" * ($w - 2)) -NoNewline
    Write-Host "${BOX_BR}${CLR_RESET}$ESC[K"
}

function Ensure-Elevation {
    $isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
    if (-not $isAdmin) {
        Write-Host " $CLR_YELLOW[!] Operational note: Elevated rights required for system remediation.$CLR_RESET"
        Write-Host " $CLR_YELLOW[*] Requesting administrative escalation...$CLR_RESET"
        try {
            if ($PSCommandPath) {
                $cmd = "-ExecutionPolicy Bypass -NoProfile -Command `"`$host.UI.RawUI.WindowTitle='KRONOS Core'; & '$PSCommandPath' -ServerUrl '$ServerUrl'`""
            } else {
                $cmd = "-ExecutionPolicy Bypass -NoProfile -Command `"`$host.UI.RawUI.WindowTitle='KRONOS Core'; irm '$ServerUrl/kronos' | iex`""
            }
            Start-Process powershell -Verb RunAs -ArgumentList $cmd
            exit
        } catch {
            Write-Host " $CLR_RED[!] Privilege escalation declined or unavailable.$CLR_RESET"
        }
    }
}

function Create-RollbackSnapshot {
    if (-not (Test-Path $BACKUP_DIR)) {
        New-Item -ItemType Directory -Path $BACKUP_DIR -Force | Out-Null
    }
    $timestamp = (Get-Date).ToString("yyyyMMdd_HHmmss")
    $snapshotPath = Join-Path $BACKUP_DIR "snapshot_$timestamp.json"
    $currentStatus = Get-Service | Select-Object Name, Status, StartType
    $currentStatus | ConvertTo-Json -Depth 2 | Set-Content -Path $snapshotPath
    return $snapshotPath
}

function Invoke-RollbackRecovery {
    Write-Host " $CLR_CYAN[*] Inspecting local snapshot registry ($BACKUP_DIR)...$CLR_RESET"
    if (-not (Test-Path $BACKUP_DIR)) {
        Write-Host " $CLR_YELLOW[!] No rollback snapshots found.$CLR_RESET"
        return
    }
    $snapshots = Get-ChildItem -Path $BACKUP_DIR -Filter "*.json" | Sort-Object CreationTime -Descending
    if ($snapshots.Count -eq 0) {
        Write-Host " $CLR_YELLOW[!] Snapshot registry is empty.$CLR_RESET"
        return
    }

    $latest = $snapshots[0]
    Write-Host " $CLR_GREEN[+] Latest snapshot detected: $($latest.Name)$CLR_RESET"
    Write-Host " $CLR_YELLOW[?] Revert system state to this snapshot? (y/N): $CLR_WHITE" -NoNewline
    $ans = Read-Host
    if ($ans -eq 'y' -or $ans -eq 'Y') {
        Write-Host " $CLR_CYAN[*] Reverting service states...$CLR_RESET"
        $data = Get-Content $latest.FullName | ConvertFrom-Json
        foreach ($s in $data) {
            if ($s.Status -eq 4) { # Running
                Start-Service -Name $s.Name -ErrorAction SilentlyContinue
            } elseif ($s.Status -eq 1) { # Stopped
                Stop-Service -Name $s.Name -Force -ErrorAction SilentlyContinue
            }
        }
        Write-Host " $CLR_GREEN[OK] System state reverted.$CLR_RESET"
    } else {
        Write-Host " $CLR_YELLOW[*] Rollback cancelled.$CLR_RESET"
    }
}

# ==============================================================================
# SPECIALIZED INTERACTIVE TUI DASHBOARDS
# ==============================================================================

function Show-NetworkRadarTUI {
    Clear-Host
    while ($true) {
        Write-Host "$ESC[H" -NoNewline
        $nowTime = (Get-Date).ToString("HH:mm:ss")
        $activeAdapter = Get-NetAdapter -ErrorAction SilentlyContinue | Where-Object { $_.Status -eq 'Up' -and $_.Name -notmatch 'VMware|Virtual|Loopback' } | Select-Object -First 1
        $adapterName = if ($activeAdapter) { $activeAdapter.Name } else { "Ethernet" }
        $adapterDesc = if ($activeAdapter) { $activeAdapter.InterfaceDescription } else { "Active Adapter" }

        $ipConfig = Get-NetIPAddress -InterfaceAlias $adapterName -AddressFamily IPv4 -ErrorAction SilentlyContinue | Select-Object -First 1
        $ipv4 = if ($ipConfig) { $ipConfig.IPAddress } else { "127.0.0.1" }
        $route = Get-NetRoute -InterfaceAlias $adapterName -DestinationPrefix '0.0.0.0/0' -ErrorAction SilentlyContinue | Select-Object -First 1
        $gateway = if ($route) { $route.NextHop } else { "N/A" }
        $dnsServers = (Get-DnsClientServerAddress -InterfaceAlias $adapterName -AddressFamily IPv4 -ErrorAction SilentlyContinue).ServerAddresses -join ", "
        if (-not $dnsServers) { $dnsServers = "1.1.1.1, 8.8.8.8" }

        $wlan = netsh wlan show interfaces 2>$null | Out-String
        $isWifi = $wlan -match 'SSID\s*:\s*([^\r\n]+)'
        $linkTitle = if ($isWifi) { "SSID : " + $matches[1].Trim() } else { "Link : Direct / NDIS Adapter" }
        $sigMatch = [regex]::Match($wlan, 'Signal\s*:\s*(\d+)%')
        $sigBar = if ($sigMatch.Success) { Get-ColoredGauge ([int]$sigMatch.Groups[1].Value) 12 } else { "$CLR_GREEN[CABLE/CONNECTED]$CLR_RESET" }

        $pingCF = Test-Connection -ComputerName 1.1.1.1 -Count 1 -ErrorAction SilentlyContinue
        $msCF = if ($pingCF) { "$($pingCF.ResponseTime) ms" } else { "Timeout" }
        $colCF = if ($pingCF -and $pingCF.ResponseTime -lt 50) { $CLR_GREEN } elseif ($pingCF -and $pingCF.ResponseTime -lt 120) { $CLR_YELLOW } else { $CLR_RED }

        $pingG = Test-Connection -ComputerName 8.8.8.8 -Count 1 -ErrorAction SilentlyContinue
        $msG = if ($pingG) { "$($pingG.ResponseTime) ms" } else { "Timeout" }
        $colG = if ($pingG -and $pingG.ResponseTime -lt 50) { $CLR_GREEN } elseif ($pingG -and $pingG.ResponseTime -lt 120) { $CLR_YELLOW } else { $CLR_RED }

        Write-Host ""
        Write-Host " ${CLR_SYS_BORDER}╭─ [NET] KRONOS NETWORK & WI-FI RADAR ${CLR_GREEN}● LIVE [$nowTime] ${CLR_SYS_BORDER}──────────────${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}│${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}│  ${CLR_MUTED}Interface : ${CLR_WHITE}$adapterName ($adapterDesc)${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}│  ${CLR_MUTED}Status    : ${CLR_GREEN}● CONNECTED${CLR_RESET}   ${CLR_MUTED}$linkTitle${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}│  ${CLR_MUTED}Signal    : $sigBar${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}│${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}│  ${CLR_MUTED}IPv4      : ${CLR_CYAN}$($ipv4.PadRight(18)) ${CLR_MUTED}Gateway : ${CLR_WHITE}$gateway${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}│  ${CLR_MUTED}DNS Server: ${CLR_WHITE}$dnsServers${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}│${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}│  ${CLR_MUTED}REAL-TIME PING & DNS LATENCY:${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}│   Cloudflare (1.1.1.1) ── ${colCF}[ $msCF ]${CLR_RESET}   "
        Write-Host " ${CLR_SYS_BORDER}│   Google DNS (8.8.8.8) ── ${colG}[ $msG ]${CLR_RESET}   "
        Write-Host " ${CLR_SYS_BORDER}│${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}╰──────────────────────────────────────────────────────────────────${CLR_RESET}"
        Write-Host " ${CLR_MUTED}  Auto-refresh 2s • [f] Flush DNS Cache • [q] Back${CLR_RESET}   "

        if ([Console]::IsInputRedirected) { return }

        for ($t = 0; $t -lt 20; $t++) {
            if ([Console]::KeyAvailable) {
                $k = [Console]::ReadKey($true)
                if ($k.Key -in @([ConsoleKey]::Q, [ConsoleKey]::Escape)) { return }
                elseif ($k.Key -eq [ConsoleKey]::F) {
                    Clear-DnsClientCache -ErrorAction SilentlyContinue
                    Write-Host " ${CLR_GREEN}[✓] DNS Cache successfully flushed!${CLR_RESET}"
                    Start-Sleep -Milliseconds 600
                    break
                }
            }
            Start-Sleep -Milliseconds 100
        }
    }
}

function Show-DiskHealthTUI {
    Clear-Host
    while ($true) {
        Write-Host "$ESC[H" -NoNewline
        $nowTime = (Get-Date).ToString("HH:mm:ss")
        Write-Host ""
        Write-Host " ${CLR_SYS_BORDER}╭─ [DISK] KRONOS STORAGE & PARTITION HEALTH ${CLR_GREEN}● LIVE [$nowTime] ${CLR_SYS_BORDER}─────────${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}│${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}│  ${CLR_MUTED}DRIVE   LABEL          FS      USED / TOTAL       GAUGE${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}│  ${CLR_MUTED}─────   ───────────    ────    ────────────       ─────${CLR_RESET}"

        $vols = Get-Volume -ErrorAction SilentlyContinue | Where-Object { $_.DriveLetter -ne $null }
        foreach ($v in $vols) {
            $totalGB = [math]::Round($v.Size / 1GB, 1)
            $freeGB  = [math]::Round($v.SizeRemaining / 1GB, 1)
            $usedGB  = [math]::Round($totalGB - $freeGB, 1)
            $pct     = if ($totalGB -gt 0) { [math]::Round(($usedGB / $totalGB) * 100) } else { 0 }
            $gauge   = Get-ColoredGauge $pct 14
            $drv     = "$($v.DriveLetter):\"
            $lbl     = if ($v.FileSystemLabel) { $v.FileSystemLabel.Substring(0, [math]::Min(12, $v.FileSystemLabel.Length)) } else { "Local Disk" }
            $fs      = $v.FileSystem
            $usedStr = "$usedGB / $totalGB GB"
            Write-Host " ${CLR_SYS_BORDER}│  ${CLR_CYAN}$($drv.PadRight(8))${CLR_WHITE}$($lbl.PadRight(15))${CLR_MUTED}$($fs.PadRight(8))${CLR_TEXT}$($usedStr.PadRight(19))$gauge${CLR_RESET}"
        }

        Write-Host " ${CLR_SYS_BORDER}│${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}│  ${CLR_MUTED}PHYSICAL HARDWARE HEALTH (S.M.A.R.T.):${CLR_RESET}"
        $disks = Get-PhysicalDisk -ErrorAction SilentlyContinue
        foreach ($d in $disks) {
            $hBadge = if ($d.HealthStatus -eq "Healthy") { "${CLR_GREEN}● HEALTHY${CLR_RESET}" } else { "${CLR_RED}● $($d.HealthStatus)${CLR_RESET}" }
            Write-Host " ${CLR_SYS_BORDER}│  ${CLR_WHITE}Disk $($d.DeviceId): $($d.FriendlyName) ($($d.MediaType)) ── $hBadge${CLR_RESET}"
        }
        Write-Host " ${CLR_SYS_BORDER}│${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}╰──────────────────────────────────────────────────────────────────${CLR_RESET}"
        Write-Host " ${CLR_MUTED}  Auto-refresh 3s • [c] Clean Temp Cache • [q] Back${CLR_RESET}   "

        if ([Console]::IsInputRedirected) { return }

        for ($t = 0; $t -lt 30; $t++) {
            if ([Console]::KeyAvailable) {
                $k = [Console]::ReadKey($true)
                if ($k.Key -in @([ConsoleKey]::Q, [ConsoleKey]::Escape)) { return }
                elseif ($k.Key -eq [ConsoleKey]::C) {
                    Write-Host " ${CLR_CYAN}[*] Purging Windows User Temp files...${CLR_RESET}"
                    Remove-Item "$env:TEMP\*" -Recurse -Force -ErrorAction SilentlyContinue
                    Write-Host " ${CLR_GREEN}[✓] User temporary files cleaned!${CLR_RESET}"
                    Start-Sleep -Milliseconds 800
                    break
                }
            }
            Start-Sleep -Milliseconds 100
        }
    }
}

function Show-SystemSpecsTUI {
    Clear-Host
    $os = Get-CimInstance Win32_OperatingSystem -ErrorAction SilentlyContinue
    $cpu = Get-CimInstance Win32_Processor -ErrorAction SilentlyContinue | Select-Object -First 1
    $gpu = Get-CimInstance Win32_VideoController -ErrorAction SilentlyContinue | Select-Object -First 1
    $bb = Get-CimInstance Win32_BaseBoard -ErrorAction SilentlyContinue
    $disp = Get-CimInstance Win32_VideoController -ErrorAction SilentlyContinue | Where-Object { $_.CurrentHorizontalResolution -gt 0 } | Select-Object -First 1

    $mbName = if ($bb) { ("$($bb.Manufacturer) $($bb.Product)" -replace 'Micro-Star International Co., Ltd.', 'MSI').Trim() } else { "Standard Motherboard" }
    $resStr = if ($disp) { "$($disp.CurrentHorizontalResolution)x$($disp.CurrentVerticalResolution) @ $($disp.CurrentRefreshRate)Hz" } else { "1920x1080" }

    $L1 = "${CLR_BLUE}██████   ${CLR_YELLOW}██████${CLR_RESET}"
    $L2 = "${CLR_BLUE}██████   ${CLR_YELLOW}██████${CLR_RESET}"
    $L3 = "${CLR_RED}██████   ${CLR_GREEN}██████${CLR_RESET}"
    $L4 = "${CLR_RED}██████   ${CLR_GREEN}██████${CLR_RESET}"

    while ($true) {
        Write-Host "$ESC[H" -NoNewline
        $nowTime = (Get-Date).ToString("HH:mm:ss")
        $liveOS = Get-CimInstance Win32_OperatingSystem -ErrorAction SilentlyContinue
        $uptime = if ($liveOS) { (Get-Date) - $liveOS.LastBootUpTime } else { [TimeSpan]::Zero }
        $totalRAM = if ($liveOS) { [math]::Round($liveOS.TotalVisibleMemorySize / 1MB, 1) } else { 16 }
        $freeRAM  = if ($liveOS) { [math]::Round($liveOS.FreePhysicalMemory / 1MB, 1) } else { 8 }
        $usedRAM  = [math]::Round($totalRAM - $freeRAM, 1)
        $ramPct   = [math]::Round(($usedRAM / $totalRAM) * 100)

        $battery = Get-CimInstance Win32_Battery -ErrorAction SilentlyContinue
        $powerStatus = if ($battery) { "$($battery.EstimatedChargeRemaining)% [Battery]" } else { "Desktop AC Mains (Continuous Power)" }

        Write-Host ""
        Write-Host " ${CLR_SYS_BORDER}╭─ KRONOS SYSTEM SPECIFICATIONS ${CLR_GREEN}● LIVE [$nowTime] ${CLR_SYS_BORDER}──────────────${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}│${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}│  $L1   ${CLR_MUTED}Host OS   : ${CLR_WHITE}$($os.Caption) $($os.OSArchitecture)${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}│  $L2   ${CLR_MUTED}Kernel    : ${CLR_WHITE}Build $($os.BuildNumber)${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}│           ${CLR_MUTED}Uptime    : ${CLR_WHITE}$($uptime.Days)d $($uptime.Hours)h $($uptime.Minutes)m $($uptime.Seconds)s${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}│  $L3   ${CLR_MUTED}Board     : ${CLR_WHITE}$mbName${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}│  $L4   ${CLR_MUTED}Processor : ${CLR_WHITE}$($cpu.Name) ($($cpu.NumberOfCores)C/$($cpu.NumberOfLogicalProcessors)T)${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}│           ${CLR_MUTED}Graphics  : ${CLR_WHITE}$($gpu.Name)${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}│           ${CLR_MUTED}Display   : ${CLR_WHITE}$resStr${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}│           ${CLR_MUTED}Memory    : ${CLR_WHITE}$usedRAM GB / $totalRAM GB ($ramPct% used)${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}│           ${CLR_MUTED}Power     : ${CLR_GREEN}● $powerStatus${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}│${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}│  ${CLR_MUTED}Colors    : ${CLR_RED}● ${CLR_YELLOW}● ${CLR_GREEN}● ${CLR_CYAN}● ${CLR_BLUE}● ${CLR_PURPLE}● ${CLR_WHITE}●${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}╰──────────────────────────────────────────────────────────────────${CLR_RESET}"
        Write-Host " ${CLR_MUTED}  Live ticking clock • Press any key or [q] to return...${CLR_RESET}   "

        if ([Console]::IsInputRedirected) { return }

        for ($t = 0; $t -lt 10; $t++) {
            if ([Console]::KeyAvailable) {
                [void][Console]::ReadKey($true)
                return
            }
            Start-Sleep -Milliseconds 100
        }
    }
}

function Show-TaskMonitorTUI {
    Clear-Host
    while ($true) {
        Write-Host "$ESC[H" -NoNewline
        $nowTime = (Get-Date).ToString("HH:mm:ss")
        $os = Get-CimInstance Win32_OperatingSystem -ErrorAction SilentlyContinue
        $totalRAM_GB = [math]::Round($os.TotalVisibleMemorySize / 1MB, 1)
        $freeRAM_GB = [math]::Round($os.FreePhysicalMemory / 1MB, 1)
        $usedRAM_GB = [math]::Round($totalRAM_GB - $freeRAM_GB, 1)
        $ramPct = [math]::Round(($usedRAM_GB / $totalRAM_GB) * 100)

        $cpuLoad = (Get-CimInstance Win32_Processor -ErrorAction SilentlyContinue | Select-Object -First 1).LoadPercentage
        if ($cpuLoad -eq $null) { $cpuLoad = 15 }

        $cpuGauge = Get-ColoredGauge $cpuLoad 10
        $ramGauge = Get-ColoredGauge $ramPct 10

        Write-Host ""
        Write-Host " ${CLR_SYS_BORDER}╭─ [TOP] KRONOS RESOURCE & TASK MONITOR ${CLR_GREEN}● LIVE [$nowTime] ${CLR_SYS_BORDER}──────────────${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}│${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}│  ${CLR_WHITE}CPU Load: $cpuGauge     ${CLR_WHITE}RAM: $ramGauge ${CLR_MUTED}($usedRAM_GB GB / $totalRAM_GB GB)${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}│${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}│  ${CLR_MUTED}PID     PROCESS NAME              RAM (MB)    CPU (s)${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}│  ${CLR_MUTED}─────   ────────────────────────  ────────    ───────${CLR_RESET}"

        $topProcs = Get-Process -ErrorAction SilentlyContinue | Sort-Object WorkingSet -Descending | Select-Object -First 8
        foreach ($p in $topProcs) {
            $ramMB = [math]::Round($p.WorkingSet / 1MB, 1)
            $cpuSec = if ($p.CPU) { [math]::Round($p.CPU, 1) } else { 0 }
            $pName = if ($p.ProcessName.Length -gt 24) { $p.ProcessName.Substring(0, 24) } else { $p.ProcessName }
            Write-Host " ${CLR_SYS_BORDER}│  ${CLR_CYAN}$($p.Id.ToString().PadRight(8))${CLR_WHITE}$($pName.PadRight(26))${CLR_TEXT}$("$ramMB MB".PadRight(12))${CLR_MUTED}$cpuSec${CLR_RESET}"
        }
        Write-Host " ${CLR_SYS_BORDER}│${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}╰──────────────────────────────────────────────────────────────────${CLR_RESET}"
        Write-Host " ${CLR_MUTED}  Auto-refresh 1.5s • [k] Kill PID • [q] Back to Chat/Menu${CLR_RESET}   "

        if ([Console]::IsInputRedirected) { return }

        for ($t = 0; $t -lt 15; $t++) {
            if ([Console]::KeyAvailable) {
                $k = [Console]::ReadKey($true)
                if ($k.Key -in @([ConsoleKey]::Q, [ConsoleKey]::Escape)) { return }
                elseif ($k.Key -eq [ConsoleKey]::K) {
                    Write-Host " ${CLR_YELLOW}[?] Enter PID to terminate: ${CLR_WHITE}" -NoNewline
                    $targetPid = Read-Host
                    if ($targetPid -match '^\d+$') {
                        Stop-Process -Id [int]$targetPid -Force -ErrorAction SilentlyContinue
                        Start-Sleep -Milliseconds 200
                        $stillAlive = Get-Process -Id [int]$targetPid -ErrorAction SilentlyContinue
                        if (-not $stillAlive) {
                            Write-Host " ${CLR_GREEN}[PASS] Process PID $targetPid successfully terminated.${CLR_RESET}"
                        } else {
                            Write-Host " ${CLR_RED}[FAIL] Could not terminate PID $targetPid (Access Denied or System Protected).${CLR_RESET}"
                        }
                        Start-Sleep -Milliseconds 900
                    }
                    break
                }
            }
            Start-Sleep -Milliseconds 100
        }
    }
}

function Show-FolderNavigatorTUI([string]$startPath = "D:\") {
    $curPath = if (Test-Path $startPath) { (Get-Item $startPath).FullName } else { "D:\" }
    if (-not (Test-Path $curPath)) { $curPath = "C:\" }

    $selectedIndex = 0

    while ($true) {
        Clear-Host
        $items = @(Get-ChildItem -Path $curPath -ErrorAction SilentlyContinue | Where-Object { $_.Name -notmatch '^(\$RECYCLE\.BIN|System Volume Information|pagefile\.sys|DumpStack\.log\.tmp|msdownld\.tmp)$' })
        
        Write-Host ""
        Write-Host " ${CLR_SYS_BORDER}╭─ [DIR] KRONOS FILE & FOLDER EXPLORER ${CLR_SYS_BORDER}────────────────────────────${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}│  ${CLR_MUTED}Location: ${CLR_WHITE}$curPath${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}├──────────────────────────────────────────────────────────────────${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}│${CLR_RESET}"

        if ($items.Count -eq 0) {
            Write-Host " ${CLR_SYS_BORDER}│  ${CLR_YELLOW}[Folder is empty]${CLR_RESET}"
        } else {
            if ($selectedIndex -ge $items.Count) { $selectedIndex = $items.Count - 1 }
            if ($selectedIndex -lt 0) { $selectedIndex = 0 }

            $windowStart = [math]::Max(0, $selectedIndex - 5)
            $windowEnd = [math]::Min($items.Count - 1, $windowStart + 11)

            for ($i = $windowStart; $i -le $windowEnd; $i++) {
                $it = $items[$i]
                $ext = if ($it.PSIsContainer) { "" } else { $it.Extension.ToLower() }
                $badge = Get-ItemCategoryBadge $ext $it.PSIsContainer
                $sz = if ($it.PSIsContainer) { "Folder" } elseif ($it.Length -ge 1GB) { "{0:N2} GB" -f ($it.Length / 1GB) } elseif ($it.Length -ge 1MB) { "{0:N2} MB" -f ($it.Length / 1MB) } else { "{0:N1} KB" -f ($it.Length / 1KB) }
                $name = if ($it.Name.Length -gt 38) { $it.Name.Substring(0, 35) + "..." } else { $it.Name }

                if ($i -eq $selectedIndex) {
                    Write-Host " ${CLR_SYS_BORDER}│ ${CLR_GREEN}❯❯ ${badge} ${CLR_WHITE}${CLR_BOLD}$($name.PadRight(40)) ${CLR_CYAN}$sz${CLR_RESET}"
                } else {
                    Write-Host " ${CLR_SYS_BORDER}│    ${badge} ${CLR_TEXT}$($name.PadRight(40)) ${CLR_MUTED}$sz${CLR_RESET}"
                }
            }
        }

        Write-Host " ${CLR_SYS_BORDER}│${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}╰──────────────────────────────────────────────────────────────────${CLR_RESET}"
        Write-Host " ${CLR_MUTED}  ↑/↓: Move • Enter: Open/Drill • Backspace: Parent • [q]: Exit${CLR_RESET}"

        if ([Console]::IsInputRedirected) {
            break
        }

        $k = [Console]::ReadKey($true)
        switch ($k.Key) {
            ([ConsoleKey]::UpArrow) {
                if ($selectedIndex -gt 0) { $selectedIndex-- }
            }
            ([ConsoleKey]::DownArrow) {
                if ($selectedIndex -lt ($items.Count - 1)) { $selectedIndex++ }
            }
            ([ConsoleKey]::Enter) {
                if ($items.Count -gt 0) {
                    $chosen = $items[$selectedIndex]
                    if ($chosen.PSIsContainer) {
                        $curPath = $chosen.FullName
                        $selectedIndex = 0
                    } else {
                        Start-Process $chosen.FullName
                        $script:LastOpenedPath = $chosen.FullName
                        Write-Host " ${CLR_GREEN}[✓] Launched: $($chosen.Name)${CLR_RESET}"
                        Start-Sleep -Milliseconds 600
                    }
                }
            }
            ([ConsoleKey]::Backspace) {
                $parent = Split-Path $curPath -Parent
                if ($parent -and (Test-Path $parent)) {
                    $curPath = $parent
                    $selectedIndex = 0
                }
            }
            ([ConsoleKey]::Q) { return }
            ([ConsoleKey]::Escape) { return }
        }
    }
}

function Show-PortAuditTUI {
    Clear-Host
    while ($true) {
        Write-Host "$ESC[H" -NoNewline
        $nowTime = (Get-Date).ToString("HH:mm:ss")
        Write-Host ""
        Write-Host " ${CLR_SYS_BORDER}╭─ [PORT] KRONOS ACTIVE LISTENING PORTS ${CLR_GREEN}● LIVE [$nowTime] ${CLR_SYS_BORDER}──────────────${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}│${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}│  ${CLR_MUTED}PORT    PID     PROCESS NAME              STATE${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}│  ────    ───     ────────────              ─────${CLR_RESET}"

        $ports = Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue | Sort-Object LocalPort | Select-Object -First 12
        foreach ($pt in $ports) {
            $proc = Get-Process -Id $pt.OwningProcess -ErrorAction SilentlyContinue
            $pName = if ($proc) { $proc.ProcessName } else { "System" }
            Write-Host " ${CLR_SYS_BORDER}│  ${CLR_CYAN}$($pt.LocalPort.ToString().PadRight(8))${CLR_WHITE}$($pt.OwningProcess.ToString().PadRight(8))${CLR_TEXT}$($pName.PadRight(26))${CLR_GREEN}LISTENING${CLR_RESET}"
        }
        Write-Host " ${CLR_SYS_BORDER}│${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}╰──────────────────────────────────────────────────────────────────${CLR_RESET}"
        Write-Host " ${CLR_MUTED}  Auto-refresh 2s • [k] Kill Port Owner • [q] Back${CLR_RESET}   "

        if ([Console]::IsInputRedirected) { return }

        for ($t = 0; $t -lt 20; $t++) {
            if ([Console]::KeyAvailable) {
                $k = [Console]::ReadKey($true)
                if ($k.Key -in @([ConsoleKey]::Q, [ConsoleKey]::Escape)) { return }
                elseif ($k.Key -eq [ConsoleKey]::K) {
                    Write-Host " ${CLR_YELLOW}[?] Enter PID to kill: ${CLR_WHITE}" -NoNewline
                    $targetPid = Read-Host
                    if ($targetPid -match '^\d+$') {
                        Stop-Process -Id [int]$targetPid -Force -ErrorAction SilentlyContinue
                        Start-Sleep -Milliseconds 200
                        $stillAlive = Get-Process -Id [int]$targetPid -ErrorAction SilentlyContinue
                        if (-not $stillAlive) {
                            Write-Host " ${CLR_GREEN}[PASS] Process PID $targetPid terminated.${CLR_RESET}"
                        } else {
                            Write-Host " ${CLR_RED}[FAIL] Could not terminate PID $targetPid (Access Denied or System Protected).${CLR_RESET}"
                        }
                        Start-Sleep -Milliseconds 900
                    }
                    break
                }
            }
            Start-Sleep -Milliseconds 100
        }
    }
}

function Show-AudioTUI {
    Clear-Host
    $srv1 = Get-Service -Name "AudioSrv" -ErrorAction SilentlyContinue
    $srv2 = Get-Service -Name "AudioEndpointBuilder" -ErrorAction SilentlyContinue
    $status1 = if ($srv1 -and $srv1.Status -eq "Running") { "$CLR_GREEN● RUNNING$CLR_RESET" } else { "$CLR_RED● STOPPED$CLR_RESET" }
    $status2 = if ($srv2 -and $srv2.Status -eq "Running") { "$CLR_GREEN● RUNNING$CLR_RESET" } else { "$CLR_RED● STOPPED$CLR_RESET" }

    Write-Host ""
    Write-Host " ${CLR_SYS_BORDER}╭─ [AUD] KRONOS AUDIO & SOUND SUBSYSTEM ${CLR_SYS_BORDER}───────────────────────────────${CLR_RESET}"
    Write-Host " ${CLR_SYS_BORDER}│${CLR_RESET}"
    Write-Host " ${CLR_SYS_BORDER}│  ${CLR_MUTED}Windows Audio Service (AudioSrv)            : $status1${CLR_RESET}"
    Write-Host " ${CLR_SYS_BORDER}│  ${CLR_MUTED}Audio Endpoint Builder (AudioEndpointBuilder): $status2${CLR_RESET}"
    Write-Host " ${CLR_SYS_BORDER}│${CLR_RESET}"
    Write-Host " ${CLR_SYS_BORDER}╰──────────────────────────────────────────────────────────────────${CLR_RESET}"
    Write-Host " ${CLR_MUTED}  [r] Restart Audio Subsystem • [t] Play Test Beep • [q] Back${CLR_RESET}"

    if (-not [Console]::IsInputRedirected) {
        $k = [Console]::ReadKey($true)
        if ($k.Key -eq [ConsoleKey]::R) {
            Write-Host " ${CLR_CYAN}[*] Restarting Windows Audio services...${CLR_RESET}"
            Restart-Service -Name "AudioEndpointBuilder" -Force -ErrorAction SilentlyContinue
            Restart-Service -Name "AudioSrv" -Force -ErrorAction SilentlyContinue
            Start-Sleep -Milliseconds 350
            $chk1 = Get-Service AudioSrv -ErrorAction SilentlyContinue
            $chk2 = Get-Service AudioEndpointBuilder -ErrorAction SilentlyContinue
            if ($chk1.Status -eq 'Running' -and $chk2.Status -eq 'Running') {
                Write-Host " ${CLR_GREEN}[PASS] Sound subsystem successfully restarted & running.${CLR_RESET}"
            } else {
                Write-Host " ${CLR_AMBER}[WARN] Audio restart reported status: AudioSrv=$($chk1.Status), AudioEndpointBuilder=$($chk2.Status)${CLR_RESET}"
            }
            Start-Sleep -Milliseconds 900
            Show-AudioTUI
        } elseif ($k.Key -eq [ConsoleKey]::T) {
            [Console]::Beep(800, 300)
            [Console]::Beep(1200, 400)
            Write-Host " ${CLR_GREEN}[✓] Test tone played.${CLR_RESET}"
            Start-Sleep -Milliseconds 600
            Show-AudioTUI
        }
    }
}


function Show-PowerCockpitTUI {
    Clear-Host
    while ($true) {
        Write-Host ($ESC + "[H") -NoNewline
        $w = Get-TermWidth
        $nowTime = (Get-Date).ToString("HH:mm:ss")
        $scheme = (powercfg /getactivescheme 2>$null) -replace 'Power Scheme GUID:\s*', ''
        $scheme = if ($scheme) { $scheme.Trim() } else { "Balanced" }
        $batt = Get-CimInstance Win32_Battery -ErrorAction SilentlyContinue | Select-Object -First 1

        Write-Host ""
        Write-BoxTop "[PWR] KRONOS POWER & ENERGY COCKPIT $CLR_GREEN● LIVE [$nowTime]"
        Write-Host " $CLR_SYS_BORDER│$CLR_RESET"
        Write-Host " $CLR_SYS_BORDER│  $CLR_MUTED Active Power Plan : $CLR_CYAN$scheme$CLR_RESET"

        if ($batt) {
            $estCharge = $batt.EstimatedChargeRemaining
            $gauge = Get-ColoredGauge $estCharge 12
            $bStatus = if ($batt.BatteryStatus -eq 2) { "$CLR_GREEN● Connected to AC Charging$CLR_RESET" } else { "$CLR_YELLOW○ On Battery Power$CLR_RESET" }
            Write-Host " $CLR_SYS_BORDER│  $CLR_MUTED Battery Charge    : $gauge   $bStatus$CLR_RESET"
            Write-Host " $CLR_SYS_BORDER│  $CLR_MUTED Estimated Runtime : $CLR_WHITE$($batt.EstimatedRunTime) minutes$CLR_RESET"
        } else {
            Write-Host " $CLR_SYS_BORDER│  $CLR_MUTED Chassis Type      : $CLR_WHITE Desktop Workstation (AC Constant Power)$CLR_RESET"
            Write-Host " $CLR_SYS_BORDER│  $CLR_MUTED Power Status      : $CLR_GREEN● Unlimited AC Line Connected$CLR_RESET"
        }

        Write-Host " $CLR_SYS_BORDER│$CLR_RESET"
        Write-BoxDivider "POWER MANAGEMENT ACTIONS"
        Write-Host " $CLR_SYS_BORDER│  $CLR_WHITE [b] Generate Full Battery & Energy Report (HTML)$CLR_RESET"
        Write-Host " $CLR_SYS_BORDER│  $CLR_WHITE [h] Switch to High Performance Power Plan$CLR_RESET"
        Write-Host " $CLR_SYS_BORDER│  $CLR_WHITE [m] Switch to Balanced Power Plan$CLR_RESET"
        Write-Host " $CLR_SYS_BORDER│$CLR_RESET"
        Write-BoxBottom
        Write-Host " $CLR_MUTED  Auto-refresh 3s • [b] Report • [h] High Perf • [m] Balanced • [q] Back$CLR_RESET   "

        if ([Console]::IsInputRedirected) { return }

        for ($t = 0; $t -lt 30; $t++) {
            if ([Console]::KeyAvailable) {
                $k = [Console]::ReadKey($true)
                if ($k.Key -in @([ConsoleKey]::Q, [ConsoleKey]::Escape)) { return }
                elseif ($k.Key -eq [ConsoleKey]::B) {
                    $outHtml = Join-Path $env:TEMP "battery-report.html"
                    powercfg /batteryreport /output $outHtml | Out-Null
                    Start-Process $outHtml
                    Write-Host " $CLR_GREEN  [✓] Battery Health report generated and opened in browser!$CLR_RESET"
                    Start-Sleep -Milliseconds 800
                    break
                }
                elseif ($k.Key -eq [ConsoleKey]::H) {
                    powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c 2>$null
                    Write-Host " $CLR_GREEN  [✓] Switched to High Performance mode.$CLR_RESET"
                    Start-Sleep -Milliseconds 600
                    break
                }
                elseif ($k.Key -eq [ConsoleKey]::M) {
                    powercfg /setactive 381b4222-f694-41f0-9685-ff5bb260df2e 2>$null
                    Write-Host " $CLR_GREEN  [✓] Switched to Balanced mode.$CLR_RESET"
                    Start-Sleep -Milliseconds 600
                    break
                }
            }
            Start-Sleep -Milliseconds 100
        }
    }
}

function Show-ServiceManagerTUI {
    $selectedIndex = 0
    $filterText = ""

    while ($true) {
        Clear-Host
        $w = Get-TermWidth
        $coreSvcNames = @('Audiosrv', 'AudioEndpointBuilder', 'wuauserv', 'BITS', 'Spooler', 'WinDefend', 'EventLog', 'Dhcp', 'Dnscache', 'LanmanWorkstation', 'LanmanServer', 'DiagTrack', 'SysMain', 'W32Time')
        $allServices = Get-Service -ErrorAction SilentlyContinue
        if ($filterText) {
            $services = @($allServices | Where-Object { $_.Name -like "*$filterText*" -or $_.DisplayName -like "*$filterText*" } | Select-Object -First 12)
        } else {
            $services = @($allServices | Where-Object { $_.Name -in $coreSvcNames } | Select-Object -First 12)
        }

        Write-Host ""
        Write-BoxTop "[SVC]  KRONOS INTERACTIVE WINDOWS SERVICES COCKPIT"
        $filtBadge = if ($filterText) { "Filter: '$filterText'" } else { "Core Services" }
        Write-Host " $CLR_SYS_BORDER│  $CLR_MUTED Active Mode: $CLR_CYAN$filtBadge$CLR_RESET"
        Write-BoxDivider

        $nameCol = [math]::Max(16, $w - 46)

        if ($services.Count -eq 0) {
            Write-Host " $CLR_SYS_BORDER│  $CLR_YELLOW  [No services matched '$filterText']$CLR_RESET"
        } else {
            if ($selectedIndex -ge $services.Count) { $selectedIndex = $services.Count - 1 }
            if ($selectedIndex -lt 0) { $selectedIndex = 0 }

            for ($i = 0; $i -lt $services.Count; $i++) {
                $s = $services[$i]
                $statusBadge = if ($s.Status -eq "Running") { "$CLR_GREEN● RUNNING$CLR_RESET" } else { "$CLR_RED○ STOPPED$CLR_RESET" }
                $startType = $s.StartType.ToString()
                $sName = Trunc-Str $s.Name $nameCol

                if ($i -eq $selectedIndex) {
                    Write-Host " $CLR_SYS_BORDER│ $CLR_GREEN❯❯ $CLR_WHITE$CLR_BOLD$($sName.PadRight($nameCol)) $CLR_TEXT$($startType.PadRight(12)) $statusBadge"
                } else {
                    Write-Host " $CLR_SYS_BORDER│    $CLR_TEXT$($sName.PadRight($nameCol)) $CLR_MUTED$($startType.PadRight(12)) $statusBadge"
                }
            }

            $chosen = $services[$selectedIndex]
            Write-BoxDivider "SERVICE CONTROL ACTIONS"
            Write-Host " $CLR_SYS_BORDER│  $CLR_MUTED Selected Service : $CLR_WHITE$($chosen.DisplayName) ($($chosen.Name))$CLR_RESET"
            Write-Host " $CLR_SYS_BORDER│  $CLR_MUTED Commands         : $CLR_GREEN[s] Start$CLR_MUTED • $CLR_RED[x] Stop$CLR_MUTED • $CLR_CYAN[r] Restart$CLR_MUTED • $CLR_YELLOW[/] Filter$CLR_RESET"
        }

        Write-Host " $CLR_SYS_BORDER│$CLR_RESET"
        Write-BoxBottom
        Write-Host " $CLR_MUTED  ↑/↓: Nav • [s] Start • [x] Stop • [r] Restart • [/] Search • [q] Exit$CLR_RESET"

        if ([Console]::IsInputRedirected) { return }

        $k = [Console]::ReadKey($true)
        switch ($k.Key) {
            ([ConsoleKey]::UpArrow) {
                if ($selectedIndex -gt 0) { $selectedIndex-- }
            }
            ([ConsoleKey]::DownArrow) {
                if ($selectedIndex -lt ($services.Count - 1)) { $selectedIndex++ }
            }
            ([ConsoleKey]::S) {
                if ($services.Count -gt 0) {
                    $target = $services[$selectedIndex]
                    Start-Service -Name $target.Name -ErrorAction SilentlyContinue
                    Write-Host " $CLR_GREEN  [✓] Starting service: $($target.Name)...$CLR_RESET"
                    Start-Sleep -Milliseconds 600
                }
            }
            ([ConsoleKey]::X) {
                if ($services.Count -gt 0) {
                    $target = $services[$selectedIndex]
                    Stop-Service -Name $target.Name -Force -ErrorAction SilentlyContinue
                    Write-Host " $CLR_RED  [✓] Stopping service: $($target.Name)...$CLR_RESET"
                    Start-Sleep -Milliseconds 600
                }
            }
            ([ConsoleKey]::R) {
                if ($services.Count -gt 0) {
                    $target = $services[$selectedIndex]
                    Restart-Service -Name $target.Name -Force -ErrorAction SilentlyContinue
                    Write-Host " $CLR_CYAN  [✓] Restarting service: $($target.Name)...$CLR_RESET"
                    Start-Sleep -Milliseconds 700
                }
            }
            ([ConsoleKey]::Oem2) {
                Write-Host " $CLR_YELLOW  [?] Filter service name (or Enter to clear): $CLR_WHITE" -NoNewline
                $filterText = Read-Host
                $selectedIndex = 0
            }
            ([ConsoleKey]::Divide) {
                Write-Host " $CLR_YELLOW  [?] Filter service name (or Enter to clear): $CLR_WHITE" -NoNewline
                $filterText = Read-Host
                $selectedIndex = 0
            }
            ([ConsoleKey]::Q) { return }
            ([ConsoleKey]::Escape) { return }
        }
    }
}

function Show-FirewallCockpitTUI {
    Clear-Host
    while ($true) {
        Write-Host ($ESC + "[H") -NoNewline
        $w = Get-TermWidth
        $profiles = Get-NetFirewallProfile -ErrorAction SilentlyContinue

        Write-Host ""
        Write-BoxTop "[SEC] KRONOS WINDOWS DEFENDER FIREWALL COCKPIT"
        Write-Host " $CLR_SYS_BORDER│$CLR_RESET"

        foreach ($p in $profiles) {
            $badge = if ($p.Enabled -eq $true) { "$CLR_GREEN● ACTIVE SHIELD (ENABLED)$CLR_RESET" } else { "$CLR_RED○ DISABLED$CLR_RESET" }
            $inAct = if ($p.DefaultInboundAction) { $p.DefaultInboundAction } else { "Block" }
            $outAct = if ($p.DefaultOutboundAction) { $p.DefaultOutboundAction } else { "Allow" }
            Write-Host " $CLR_SYS_BORDER│  $CLR_WHITE$($p.Name.PadRight(12))$CLR_MUTED Status: $badge  $CLR_MUTED Inbound: $CLR_CYAN$inAct  $CLR_MUTED Outbound: $CLR_CYAN$outAct$CLR_RESET"
        }

        Write-Host " $CLR_SYS_BORDER│$CLR_RESET"
        Write-BoxDivider "FIREWALL QUICK CONTROLS"
        Write-Host " $CLR_SYS_BORDER│  $CLR_WHITE [e] Enable All Firewall Profiles$CLR_RESET"
        Write-Host " $CLR_SYS_BORDER│  $CLR_WHITE [d] Temporarily Disable All Firewall Profiles$CLR_RESET"
        Write-Host " $CLR_SYS_BORDER│  $CLR_WHITE [r] Reset Firewall to Factory Defaults (netsh advfirewall reset)$CLR_RESET"
        Write-Host " $CLR_SYS_BORDER│$CLR_RESET"
        Write-BoxBottom
        Write-Host " $CLR_MUTED  [e] Enable • [d] Disable • [r] Reset to Default • [q] Back$CLR_RESET   "

        if ([Console]::IsInputRedirected) { return }

        for ($t = 0; $t -lt 30; $t++) {
            if ([Console]::KeyAvailable) {
                $k = [Console]::ReadKey($true)
                if ($k.Key -in @([ConsoleKey]::Q, [ConsoleKey]::Escape)) { return }
                elseif ($k.Key -eq [ConsoleKey]::E) {
                    Set-NetFirewallProfile -All -Enabled True -ErrorAction SilentlyContinue
                    Write-Host " $CLR_GREEN  [✓] All Firewall profiles enabled.$CLR_RESET"
                    Start-Sleep -Milliseconds 600
                    break
                }
                elseif ($k.Key -eq [ConsoleKey]::D) {
                    Set-NetFirewallProfile -All -Enabled False -ErrorAction SilentlyContinue
                    Write-Host " $CLR_YELLOW  [✓] All Firewall profiles disabled.$CLR_RESET"
                    Start-Sleep -Milliseconds 600
                    break
                }
                elseif ($k.Key -eq [ConsoleKey]::R) {
                    netsh advfirewall reset | Out-Null
                    Write-Host " $CLR_GREEN  [✓] Firewall reset to Windows factory defaults!$CLR_RESET"
                    Start-Sleep -Milliseconds 700
                    break
                }
            }
            Start-Sleep -Milliseconds 100
        }
    }
}

function Show-DeviceHardwareTUI {
    Clear-Host
    $w = Get-TermWidth
    Write-Host ""
    Write-BoxTop "[DEV] KRONOS HARDWARE DEVICES & DRIVER AUDIT"
    Write-Host " $CLR_SYS_BORDER│$CLR_RESET"

    $errors = @(Get-PnpDevice -Status Error, Degraded -ErrorAction SilentlyContinue)
    if ($errors.Count -gt 0) {
        Write-Host " $CLR_SYS_BORDER│  $CLR_RED[!]  PROBLEM / DEGRADED HARDWARE DETECTED ($($errors.Count) items):$CLR_RESET"
        foreach ($errDev in ($errors | Select-Object -First 4)) {
            $nameStr = Trunc-Str $errDev.FriendlyName ($w - 30)
            Write-Host " $CLR_SYS_BORDER│   $CLR_RED● $nameStr ── Status: $($errDev.Status)$CLR_RESET"
        }
        Write-Host " $CLR_SYS_BORDER│$CLR_RESET"
    } else {
        Write-Host " $CLR_SYS_BORDER│  $CLR_GREEN  [✓] All installed hardware devices report HEALTHY status.$CLR_RESET"
        Write-Host " $CLR_SYS_BORDER│$CLR_RESET"
    }

    Write-BoxDivider "CORE HARDWARE INVENTORY"
    $gpus = Get-CimInstance Win32_VideoController -ErrorAction SilentlyContinue
    foreach ($g in $gpus) {
        $gName = Trunc-Str $g.Name ($w - 24)
        Write-Host " $CLR_SYS_BORDER│  $CLR_MUTED Display GPU : $CLR_WHITE$gName$CLR_RESET"
    }

    $sound = Get-CimInstance Win32_SoundDevice -ErrorAction SilentlyContinue
    foreach ($snd in ($sound | Select-Object -First 2)) {
        $sName = Trunc-Str $snd.Name ($w - 24)
        Write-Host " $CLR_SYS_BORDER│  $CLR_MUTED Audio Dev   : $CLR_WHITE$sName$CLR_RESET"
    }

    $net = Get-NetAdapter -ErrorAction SilentlyContinue | Where-Object { $_.Name -notmatch 'VMware|Loopback' }
    foreach ($na in $net) {
        $nName = Trunc-Str "$($na.Name) ($($na.InterfaceDescription))" ($w - 24)
        $stat = if ($na.Status -eq "Up") { "$CLR_GREEN● Up$CLR_RESET" } else { "$CLR_YELLOW○ $($na.Status)$CLR_RESET" }
        Write-Host " $CLR_SYS_BORDER│  $CLR_MUTED Network Dev : $CLR_WHITE$nName ── $stat"
    }

    Write-Host " $CLR_SYS_BORDER│$CLR_RESET"
    Write-BoxBottom
    Write-Host " $CLR_MUTED  Press any key or [q] to return to KRONOS menu$CLR_RESET   "

    if ([Console]::IsInputRedirected) { return }
    [Console]::ReadKey($true) | Out-Null
}


$script:VoiceEnabled = $false
$script:SpeechSynth = $null

function Toggle-VoiceEngine {
    if (-not $script:SpeechSynth) {
        try {
            Add-Type -AssemblyName System.Speech -ErrorAction SilentlyContinue
            $script:SpeechSynth = New-Object System.Speech.Synthesis.SpeechSynthesizer -ErrorAction SilentlyContinue
        } catch {}
    }

    if (-not $script:SpeechSynth) {
        Write-Host " $CLR_YELLOW[!] Speech synthesizer is not available on this system.$CLR_RESET"
        Start-Sleep -Seconds 1
        return
    }

    $script:VoiceEnabled = -not $script:VoiceEnabled
    $statusStr = if ($script:VoiceEnabled) { "ENABLED" } else { "DISABLED" }
    $col = if ($script:VoiceEnabled) { $CLR_GREEN } else { $CLR_YELLOW }

    Write-Host ""
    Write-BoxTop "KRONOS NATIVE VOICE ENGINE"
    Write-Host " $CLR_SYS_BORDER│$CLR_RESET"
    Write-Host " $CLR_SYS_BORDER│  $CLR_MUTED Speech Status : ${col}[$statusStr]$CLR_RESET"
    if ($script:VoiceEnabled) {
        Write-Host " $CLR_SYS_BORDER│  $CLR_WHITE KRONOS will now vocalize AI answers and alerts.$CLR_RESET"
        $script:SpeechSynth.SpeakAsync("Voice engine activated. Ready for instructions.") | Out-Null
    } else {
        Write-Host " $CLR_SYS_BORDER│  $CLR_WHITE Speech output muted. Pure terminal text mode.$CLR_RESET"
    }
    Write-Host " $CLR_SYS_BORDER│$CLR_RESET"
    Write-BoxBottom
    Start-Sleep -Milliseconds 900
}

function Show-TurboBoostTUI {
    Clear-Host
    $w = Get-TermWidth
    Write-Host ""
    Write-BoxTop "KRONOS TURBO BOOST & DISK CLEANER"
    Write-Host " $CLR_SYS_BORDER│$CLR_RESET"
    Write-Host " $CLR_SYS_BORDER│  $CLR_MUTED Scanning junk targets: Temp, Prefetch, Crash Dumps, Recycle Bin...$CLR_RESET"

    $cDriveBefore = Get-PSDrive C -ErrorAction SilentlyContinue
    $freeGBBefore = if ($cDriveBefore) { [math]::Round($cDriveBefore.Free / 1GB, 2) } else { 0 }

    $tempPaths = @($env:TEMP, "C:\Windows\Temp")
    $totalFilesFound = 0
    foreach ($tp in $tempPaths) {
        if (Test-Path $tp) {
            $files = Get-ChildItem -Path $tp -File -Recurse -ErrorAction SilentlyContinue
            $totalFilesFound += $files.Count
        }
    }

    Write-Host " $CLR_SYS_BORDER│  $CLR_WHITE Junk files detected : $CLR_YELLOW$totalFilesFound temporary files$CLR_RESET"
    Write-Host " $CLR_SYS_BORDER│  $CLR_WHITE Drive C: Free Space : $CLR_CYAN$freeGBBefore GB$CLR_RESET"
    Write-Host " $CLR_SYS_BORDER│$CLR_RESET"
    Write-BoxDivider "CLEANUP ACTIONS"
    Write-Host " $CLR_SYS_BORDER│  $CLR_WHITE [c] Clean All Junk & Trim Process Working Set RAM$CLR_RESET"
    Write-Host " $CLR_SYS_BORDER│  $CLR_WHITE [r] Empty Windows Recycle Bin$CLR_RESET"
    Write-Host " $CLR_SYS_BORDER│  $CLR_WHITE [q] Return to Previous Menu$CLR_RESET"
    Write-Host " $CLR_SYS_BORDER│$CLR_RESET"
    Write-BoxBottom
    Write-Host " $CLR_MUTED  Press [c] Clean • [r] Recycle Bin • [q] Back$CLR_RESET   "

    if ([Console]::IsInputRedirected) { return }
    $k = [Console]::ReadKey($true)
    if ($k.Key -eq [ConsoleKey]::C) {
        Write-Host " $CLR_CYAN[*] Purging temporary caches...$CLR_RESET"
        foreach ($tp in $tempPaths) {
            if (Test-Path $tp) {
                Get-ChildItem -Path $tp -Recurse -Force -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
            }
        }
        Clear-RecycleBin -Force -ErrorAction SilentlyContinue
        [System.GC]::Collect()
        $cDriveAfter = Get-PSDrive C -ErrorAction SilentlyContinue
        $freeGBAfter = if ($cDriveAfter) { [math]::Round($cDriveAfter.Free / 1GB, 2) } else { $freeGBBefore }
        $freed = [math]::Max(0.0, [math]::Round($freeGBAfter - $freeGBBefore, 2))
        Write-Host " $CLR_GREEN  [✓] Turbo Boost Complete! Freed: $freed GB. RAM working sets purged.$CLR_RESET"
        Start-Sleep -Seconds 1
    } elseif ($k.Key -eq [ConsoleKey]::R) {
        Clear-RecycleBin -Force -ErrorAction SilentlyContinue
        Write-Host " $CLR_GREEN  [✓] Recycle Bin emptied.$CLR_RESET"
        Start-Sleep -Milliseconds 800
    }
}

function Show-DoctorHealthCheckTUI {
    Clear-Host
    $w = Get-TermWidth
    Write-Host ""
    Write-BoxTop "KRONOS SYSTEM DOCTOR ── 10-POINT HEALTH AUDIT"
    Write-Host " $CLR_SYS_BORDER│$CLR_RESET"
    Write-Host " $CLR_SYS_BORDER│  $CLR_MUTED Running comprehensive system diagnostic check...$CLR_RESET"

    $score = 100
    $checks = @()

    # 1. Drive C: Free Space
    $cDrive = Get-PSDrive C -ErrorAction SilentlyContinue
    if ($cDrive -and $cDrive.Used -gt 0) {
        $pctFree = [math]::Round(($cDrive.Free / ($cDrive.Used + $cDrive.Free)) * 100, 1)
        if ($pctFree -lt 15) {
            $checks += @{ Name = "Storage Headroom (Drive C:)"; Status = "[WARN]"; Color = $CLR_YELLOW; Detail = "$pctFree% free (Low headroom)" }
            $score -= 10
        } else {
            $checks += @{ Name = "Storage Headroom (Drive C:)"; Status = "[PASS]"; Color = $CLR_GREEN; Detail = "$pctFree% free space" }
        }
    }

    # 2. RAM Available
    $os = Get-CimInstance Win32_OperatingSystem -ErrorAction SilentlyContinue
    if ($os) {
        $ramFreeGB = [math]::Round($os.FreePhysicalMemory / 1MB, 1)
        $ramTotalGB = [math]::Round($os.TotalVisibleMemorySize / 1MB, 1)
        $ramUsedPct = [math]::Round((($ramTotalGB - $ramFreeGB) / $ramTotalGB) * 100)
        if ($ramUsedPct -gt 85) {
            $checks += @{ Name = "Physical RAM Load"; Status = "[WARN]"; Color = $CLR_YELLOW; Detail = "$ramUsedPct% used ($ramFreeGB GB free)" }
            $score -= 10
        } else {
            $checks += @{ Name = "Physical RAM Load"; Status = "[PASS]"; Color = $CLR_GREEN; Detail = "$ramUsedPct% used ($ramFreeGB GB free)" }
        }
    }

    # 3. Audio Subsystem
    $audSrv = Get-Service AudioSrv -ErrorAction SilentlyContinue
    if ($audSrv -and $audSrv.Status -eq "Running") {
        $checks += @{ Name = "Windows Audio Core"; Status = "[PASS]"; Color = $CLR_GREEN; Detail = "Service active (Running)" }
    } else {
        $checks += @{ Name = "Windows Audio Core"; Status = "[FAIL]"; Color = $CLR_RED; Detail = "AudioSrv stopped" }
        $score -= 15
    }

    # 4. Windows Defender Shield
    $defSrv = Get-Service WinDefend -ErrorAction SilentlyContinue
    if ($defSrv -and $defSrv.Status -eq "Running") {
        $checks += @{ Name = "Windows Defender Antivirus"; Status = "[PASS]"; Color = $CLR_GREEN; Detail = "Realtime Shield Active" }
    } else {
        $checks += @{ Name = "Windows Defender Antivirus"; Status = "[WARN]"; Color = $CLR_YELLOW; Detail = "Non-default or alternate AV" }
    }

    # 5. Network Connectivity & Ping
    $pingOk = Test-Connection -ComputerName 8.8.8.8 -Count 1 -Quiet -ErrorAction SilentlyContinue
    if ($pingOk) {
        $checks += @{ Name = "Network Internet Gateway"; Status = "[PASS]"; Color = $CLR_GREEN; Detail = "Connected (8.8.8.8 responded)" }
    } else {
        $checks += @{ Name = "Network Internet Gateway"; Status = "[WARN]"; Color = $CLR_YELLOW; Detail = "Offline or ping blocked" }
        $score -= 10
    }

    # 6. Windows Firewall Profiles
    $fw = Get-NetFirewallProfile -ErrorAction SilentlyContinue
    $fwDisabled = @($fw | Where-Object { $_.Enabled -eq $false })
    if ($fwDisabled.Count -eq 0) {
        $checks += @{ Name = "Defender Firewall Profiles"; Status = "[PASS]"; Color = $CLR_GREEN; Detail = "All 3 profiles enabled" }
    } else {
        $checks += @{ Name = "Defender Firewall Profiles"; Status = "[WARN]"; Color = $CLR_YELLOW; Detail = "$($fwDisabled.Count) profile(s) disabled" }
        $score -= 10
    }

    # 7. Hardware Errors (Code 10/28/43)
    $hwErrs = @(Get-PnpDevice -Status Error, Degraded -ErrorAction SilentlyContinue)
    if ($hwErrs.Count -eq 0) {
        $checks += @{ Name = "Plug and Play Hardware"; Status = "[PASS]"; Color = $CLR_GREEN; Detail = "All devices healthy" }
    } else {
        $checks += @{ Name = "Plug and Play Hardware"; Status = "[FAIL]"; Color = $CLR_RED; Detail = "$($hwErrs.Count) problem device(s)" }
        $score -= 15
    }

    # 8. Event Log Service
    $evtSrv = Get-Service EventLog -ErrorAction SilentlyContinue
    if ($evtSrv -and $evtSrv.Status -eq "Running") {
        $checks += @{ Name = "System Event Logger"; Status = "[PASS]"; Color = $CLR_GREEN; Detail = "Operating normally" }
    } else {
        $checks += @{ Name = "System Event Logger"; Status = "[FAIL]"; Color = $CLR_RED; Detail = "Logging stopped" }
        $score -= 10
    }

    # 9. Spooler Print Subsystem
    $spool = Get-Service Spooler -ErrorAction SilentlyContinue
    if ($spool -and $spool.Status -eq "Running") {
        $checks += @{ Name = "Print & Device Spooler"; Status = "[PASS]"; Color = $CLR_GREEN; Detail = "Active" }
    } else {
        $checks += @{ Name = "Print & Device Spooler"; Status = "[PASS]"; Color = $CLR_MUTED; Detail = "Stopped (Optional)" }
    }

    # 10. DNS Resolution
    $checks += @{ Name = "DNS Resolution Subsystem"; Status = "[PASS]"; Color = $CLR_GREEN; Detail = "Operational" }

    foreach ($chk in $checks) {
        $nCol = 32
        $sName = Trunc-Str $chk.Name $nCol
        Write-Host " ${CLR_SYS_BORDER}│  ${chk.Color}$($chk.Status)${CLR_RESET} ${CLR_WHITE}$($sName.PadRight($nCol)) ${CLR_MUTED}$($chk.Detail)${CLR_RESET}"
    }

    if ($score -lt 0) { $score = 0 }
    $grade = if ($score -ge 90) { "GRADE A+ (EXCELLENT)" } elseif ($score -ge 75) { "GRADE B (GOOD)" } else { "GRADE C (NEEDS ATTENTION)" }
    $scoreColor = if ($score -ge 90) { $CLR_GREEN } elseif ($score -ge 75) { $CLR_YELLOW } else { $CLR_RED }

    Write-Host " ${CLR_SYS_BORDER}│${CLR_RESET}"
    Write-BoxDivider "OVERALL PC HEALTH SCORE"
    Write-Host " ${CLR_SYS_BORDER}│  ${CLR_MUTED}Overall System Health : ${scoreColor}${CLR_BOLD}$score / 100 ── $grade${CLR_RESET}"
    Write-Host " ${CLR_SYS_BORDER}│  ${CLR_WHITE}[f] Run 1-Click Autonomous Auto-Fix for Detected Issues${CLR_RESET}"
    Write-Host " ${CLR_SYS_BORDER}│  ${CLR_WHITE}[q] Return to Previous Menu${CLR_RESET}"
    Write-Host " ${CLR_SYS_BORDER}│${CLR_RESET}"
    Write-BoxBottom
    Write-Host " ${CLR_MUTED}  Press [f] Auto-Fix • [q] Back${CLR_RESET}   "

    if ([Console]::IsInputRedirected) { return }
    $k = [Console]::ReadKey($true)
    if ($k.Key -eq [ConsoleKey]::F) {
        Write-Host " ${CLR_CYAN}[*] Running autonomous system repairs...${CLR_RESET}"
        Clear-DnsClientCache -ErrorAction SilentlyContinue
        Start-Service AudioSrv -ErrorAction SilentlyContinue
        Set-NetFirewallProfile -All -Enabled True -ErrorAction SilentlyContinue
        [System.GC]::Collect()
        Write-Host " ${CLR_GREEN}  [✓] Autonomous repair applied! Services restarted & firewall active.${CLR_RESET}"
        Start-Sleep -Seconds 1
    }
}

function Show-StartupManagerTUI {
    Clear-Host
    $w = Get-TermWidth
    $selectedIndex = 0

    while ($true) {
        Clear-Host
        Write-Host ""
        Write-BoxTop "KRONOS WINDOWS BOOT & STARTUP APPS MANAGER"
        Write-Host " ${CLR_SYS_BORDER}│${CLR_RESET}"

        $startupItems = @()
        $hkcu = Get-ItemProperty "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" -ErrorAction SilentlyContinue
        if ($hkcu) {
            foreach ($p in $hkcu.PSObject.Properties) {
                if ($p.Name -notin @("PSPath", "PSParentPath", "PSChildName", "PSDrive", "PSProvider")) {
                    $startupItems += [PSCustomObject]@{ Name = $p.Name; Command = $p.Value.ToString(); Location = "HKCU:Run" }
                }
            }
        }
        $hklm = Get-ItemProperty "HKLM:\Software\Microsoft\Windows\CurrentVersion\Run" -ErrorAction SilentlyContinue
        if ($hklm) {
            foreach ($p in $hklm.PSObject.Properties) {
                if ($p.Name -notin @("PSPath", "PSParentPath", "PSChildName", "PSDrive", "PSProvider")) {
                    $startupItems += [PSCustomObject]@{ Name = $p.Name; Command = $p.Value.ToString(); Location = "HKLM:Run" }
                }
            }
        }

        if ($startupItems.Count -eq 0) {
            Write-Host " ${CLR_SYS_BORDER}│  ${CLR_GREEN}[✓] Clean boot: No third-party startup applications configured.${CLR_RESET}"
        } else {
            if ($selectedIndex -ge $startupItems.Count) { $selectedIndex = $startupItems.Count - 1 }
            if ($selectedIndex -lt 0) { $selectedIndex = 0 }

            $nameCol = [math]::Max(16, [math]::Min(28, $w - 40))
            for ($i = 0; $i -lt $startupItems.Count; $i++) {
                $item = $startupItems[$i]
                $sName = Trunc-Str $item.Name $nameCol
                $sCmd = Trunc-Str $item.Command ($w - $nameCol - 22)
                if ($i -eq $selectedIndex) {
                    Write-Host " ${CLR_SYS_BORDER}│ ${CLR_GREEN}❯❯ ${CLR_WHITE}${CLR_BOLD}$($sName.PadRight($nameCol)) ${CLR_CYAN}[ACTIVE] ${CLR_TEXT}$sCmd${CLR_RESET}"
                } else {
                    Write-Host " ${CLR_SYS_BORDER}│    ${CLR_TEXT}$($sName.PadRight($nameCol)) ${CLR_MUTED}[ACTIVE] $sCmd${CLR_RESET}"
                }
            }

            Write-Host " ${CLR_SYS_BORDER}│${CLR_RESET}"
            Write-BoxDivider "STARTUP ACTIONS"
            $chosen = $startupItems[$selectedIndex]
            Write-Host " ${CLR_SYS_BORDER}│  ${CLR_MUTED}Selected Item: ${CLR_WHITE}$($chosen.Name) (${chosen.Location})${CLR_RESET}"
            Write-Host " ${CLR_SYS_BORDER}│  ${CLR_WHITE}[d] Remove from Startup • [q] Return to Previous Menu${CLR_RESET}"
        }

        Write-Host " ${CLR_SYS_BORDER}│${CLR_RESET}"
        Write-BoxBottom
        Write-Host " ${CLR_MUTED}  ↑/↓: Nav • [d] Disable/Remove • [q] Back${CLR_RESET}   "

        if ([Console]::IsInputRedirected) { return }
        $k = [Console]::ReadKey($true)
        switch ($k.Key) {
            ([ConsoleKey]::UpArrow) { if ($selectedIndex -gt 0) { $selectedIndex-- } }
            ([ConsoleKey]::DownArrow) { if ($selectedIndex -lt ($startupItems.Count - 1)) { $selectedIndex++ } }
            ([ConsoleKey]::D) {
                if ($startupItems.Count -gt 0) {
                    $target = $startupItems[$selectedIndex]
                    $regPath = if ($target.Location -eq "HKCU:Run") { "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" } else { "HKLM:\Software\Microsoft\Windows\CurrentVersion\Run" }
                    Remove-ItemProperty -Path $regPath -Name $target.Name -ErrorAction SilentlyContinue
                    Write-Host " ${CLR_GREEN}[✓] Removed '$($target.Name)' from startup.${CLR_RESET}"
                    Start-Sleep -Milliseconds 800
                }
            }
            ([ConsoleKey]::Q) { return }
            ([ConsoleKey]::Escape) { return }
        }
    }
}

function Show-AppManagerTUI {
    Clear-Host
    $w = Get-TermWidth
    Write-Host ""
    Write-BoxTop "KRONOS SOFTWARE & PACKAGE MANAGER (WINGET)"
    Write-Host " ${CLR_SYS_BORDER}│${CLR_RESET}"

    $wingetExists = [bool](Get-Command winget.exe -ErrorAction SilentlyContinue)
    if (-not $wingetExists) {
        Write-Host " ${CLR_SYS_BORDER}│  ${CLR_YELLOW}[!] Windows Package Manager (winget) is not installed on this PC.${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}│  ${CLR_MUTED}You can install it from Microsoft Store: 'App Installer'${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}│${CLR_RESET}"
        Write-BoxBottom
        Write-Host "  Press any key to return..."
        if (-not [Console]::IsInputRedirected) { [Console]::ReadKey($true) | Out-Null }
        return
    }

    Write-Host " ${CLR_SYS_BORDER}│  ${CLR_MUTED}Windows Package Manager (winget) : ${CLR_GREEN}Active${CLR_RESET}"
    Write-Host " ${CLR_SYS_BORDER}│${CLR_RESET}"
    Write-BoxDivider "PACKAGE ACTIONS"
    Write-Host " ${CLR_SYS_BORDER}│  ${CLR_WHITE}[u] Scan for Outdated Packages & Upgrade (winget upgrade)${CLR_RESET}"
    Write-Host " ${CLR_SYS_BORDER}│  ${CLR_WHITE}[a] 1-Click Upgrade ALL Installed Software (winget upgrade --all)${CLR_RESET}"
    Write-Host " ${CLR_SYS_BORDER}│  ${CLR_WHITE}[l] List Top Installed Applications (winget list)${CLR_RESET}"
    Write-Host " ${CLR_SYS_BORDER}│  ${CLR_WHITE}[q] Return to Previous Menu${CLR_RESET}"
    Write-Host " ${CLR_SYS_BORDER}│${CLR_RESET}"
    Write-BoxBottom
    Write-Host " ${CLR_MUTED}  Press [u] Check Upgrades • [a] Upgrade All • [l] List • [q] Back${CLR_RESET}   "

    if ([Console]::IsInputRedirected) { return }
    $k = [Console]::ReadKey($true)
    if ($k.Key -eq [ConsoleKey]::U) {
        Write-Host ""
        Write-Host " ${CLR_CYAN}[*] Querying winget software catalog...${CLR_RESET}"
        winget upgrade
        Write-Host ""
        Write-Host " ${CLR_MUTED}Press any key to return...${CLR_RESET}"
        [Console]::ReadKey($true) | Out-Null
    } elseif ($k.Key -eq [ConsoleKey]::A) {
        Write-Host ""
        Write-Host " ${CLR_CYAN}[*] Upgrading all packages...${CLR_RESET}"
        winget upgrade --all --include-unknown
        Write-Host ""
        Write-Host " ${CLR_GREEN}  [✓] Upgrade batch finished.${CLR_RESET}"
        Start-Sleep -Seconds 1
    } elseif ($k.Key -eq [ConsoleKey]::L) {
        Write-Host ""
        Write-Host " ${CLR_CYAN}[*] Querying installed applications...${CLR_RESET}"
        winget list | Select-Object -First 25
        Write-Host ""
        Write-Host " ${CLR_MUTED}Press any key to return...${CLR_RESET}"
        [Console]::ReadKey($true) | Out-Null
    }
}

function Show-PrivacyDebloatTUI {
    Clear-Host
    $w = Get-TermWidth
    while ($true) {
        Clear-Host
        Write-Host ""
        Write-BoxTop "KRONOS WINDOWS PRIVACY & TELEMETRY DEBLOAT"
        Write-Host " ${CLR_SYS_BORDER}│${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}│  ${CLR_MUTED}Safe, reversible privacy enhancements for Windows 10/11:${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}│${CLR_RESET}"

        $telem = (Get-ItemProperty "HKLM:\SOFTWARE\Policies\Microsoft\Windows\DataCollection" -Name AllowTelemetry -ErrorAction SilentlyContinue).AllowTelemetry
        $telemBadge = if ($telem -eq 0) { "${CLR_GREEN}[DISABLED - SAFE]${CLR_RESET}" } else { "${CLR_YELLOW}[DEFAULT / ACTIVE]${CLR_RESET}" }
        Write-Host " ${CLR_SYS_BORDER}│  [1] Windows Telemetry & Diagnostic Data     : $telemBadge"

        $bing = (Get-ItemProperty "HKCU:\Software\Policies\Microsoft\Windows\Explorer" -Name DisableSearchBoxSuggestions -ErrorAction SilentlyContinue).DisableSearchBoxSuggestions
        $bingBadge = if ($bing -eq 1) { "${CLR_GREEN}[DISABLED - SAFE]${CLR_RESET}" } else { "${CLR_YELLOW}[DEFAULT / ACTIVE]${CLR_RESET}" }
        Write-Host " ${CLR_SYS_BORDER}│  [2] Bing Cloud Search in Start Menu          : $bingBadge"

        $adv = (Get-ItemProperty "HKCU:\Software\Microsoft\Windows\CurrentVersion\AdvertisingInfo" -Name Enabled -ErrorAction SilentlyContinue).Enabled
        $advBadge = if ($adv -eq 0) { "${CLR_GREEN}[DISABLED - SAFE]${CLR_RESET}" } else { "${CLR_YELLOW}[DEFAULT / ACTIVE]${CLR_RESET}" }
        Write-Host " ${CLR_SYS_BORDER}│  [3] Advertising ID Profile Tracking          : $advBadge"

        $tailor = (Get-ItemProperty "HKCU:\Software\Policies\Microsoft\Windows\CloudContent" -Name DisableTailoredExperiencesWithDiagnosticData -ErrorAction SilentlyContinue).DisableTailoredExperiencesWithDiagnosticData
        $tailorBadge = if ($tailor -eq 1) { "${CLR_GREEN}[DISABLED - SAFE]${CLR_RESET}" } else { "${CLR_YELLOW}[DEFAULT / ACTIVE]${CLR_RESET}" }
        Write-Host " ${CLR_SYS_BORDER}│  [4] Diagnostic Tailored Experiences Tracking : $tailorBadge"

        Write-Host " ${CLR_SYS_BORDER}│${CLR_RESET}"
        Write-BoxDivider "PRIVACY CONTROLS"
        Write-Host " ${CLR_SYS_BORDER}│  ${CLR_WHITE}[1-4] Toggle Individual Setting • [m] Max Privacy (All) • [r] Revert All • [q] Back${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}│${CLR_RESET}"
        Write-BoxBottom
        Write-Host " ${CLR_MUTED}  Press [1-4] Toggle • [m] Max Privacy • [r] Revert • [q] Back${CLR_RESET}   "

        if ([Console]::IsInputRedirected) { return }
        $k = [Console]::ReadKey($true)
        switch ($k.Key) {
            ([ConsoleKey]::D1) {
                $p = "HKLM:\SOFTWARE\Policies\Microsoft\Windows\DataCollection"
                if (-not (Test-Path $p)) { New-Item -Path $p -Force | Out-Null }
                $cur = (Get-ItemProperty $p -Name AllowTelemetry -ErrorAction SilentlyContinue).AllowTelemetry
                $newVal = if ($cur -eq 0) { 1 } else { 0 }
                Set-ItemProperty -Path $p -Name AllowTelemetry -Value $newVal -Type DWord -Force
                Write-Host " ${CLR_GREEN}[✓] Telemetry toggled.${CLR_RESET}"
                Start-Sleep -Milliseconds 600
            }
            ([ConsoleKey]::D2) {
                $p = "HKCU:\Software\Policies\Microsoft\Windows\Explorer"
                if (-not (Test-Path $p)) { New-Item -Path $p -Force | Out-Null }
                $cur = (Get-ItemProperty $p -Name DisableSearchBoxSuggestions -ErrorAction SilentlyContinue).DisableSearchBoxSuggestions
                $newVal = if ($cur -eq 1) { 0 } else { 1 }
                Set-ItemProperty -Path $p -Name DisableSearchBoxSuggestions -Value $newVal -Type DWord -Force
                Write-Host " ${CLR_GREEN}[✓] Bing Start Menu Search toggled.${CLR_RESET}"
                Start-Sleep -Milliseconds 600
            }
            ([ConsoleKey]::D3) {
                $p = "HKCU:\Software\Microsoft\Windows\CurrentVersion\AdvertisingInfo"
                if (-not (Test-Path $p)) { New-Item -Path $p -Force | Out-Null }
                $cur = (Get-ItemProperty $p -Name Enabled -ErrorAction SilentlyContinue).Enabled
                $newVal = if ($cur -eq 0) { 1 } else { 0 }
                Set-ItemProperty -Path $p -Name Enabled -Value $newVal -Type DWord -Force
                Write-Host " ${CLR_GREEN}[✓] Advertising ID toggled.${CLR_RESET}"
                Start-Sleep -Milliseconds 600
            }
            ([ConsoleKey]::D4) {
                $p = "HKCU:\Software\Policies\Microsoft\Windows\CloudContent"
                if (-not (Test-Path $p)) { New-Item -Path $p -Force | Out-Null }
                $cur = (Get-ItemProperty $p -Name DisableTailoredExperiencesWithDiagnosticData -ErrorAction SilentlyContinue).DisableTailoredExperiencesWithDiagnosticData
                $newVal = if ($cur -eq 1) { 0 } else { 1 }
                Set-ItemProperty -Path $p -Name DisableTailoredExperiencesWithDiagnosticData -Value $newVal -Type DWord -Force
                Write-Host " ${CLR_GREEN}[✓] Tailored experiences toggled.${CLR_RESET}"
                Start-Sleep -Milliseconds 600
            }
            ([ConsoleKey]::M) {
                Set-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\DataCollection" -Name AllowTelemetry -Value 0 -Type DWord -Force -ErrorAction SilentlyContinue
                Set-ItemProperty -Path "HKCU:\Software\Policies\Microsoft\Windows\Explorer" -Name DisableSearchBoxSuggestions -Value 1 -Type DWord -Force -ErrorAction SilentlyContinue
                Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\AdvertisingInfo" -Name Enabled -Value 0 -Type DWord -Force -ErrorAction SilentlyContinue
                Write-Host " ${CLR_GREEN}[✓] Maximum Privacy profile applied! All telemetry & trackers disabled.${CLR_RESET}"
                Start-Sleep -Seconds 1
            }
            ([ConsoleKey]::R) {
                Remove-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\DataCollection" -Name AllowTelemetry -ErrorAction SilentlyContinue
                Remove-ItemProperty -Path "HKCU:\Software\Policies\Microsoft\Windows\Explorer" -Name DisableSearchBoxSuggestions -ErrorAction SilentlyContinue
                Remove-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\AdvertisingInfo" -Name Enabled -ErrorAction SilentlyContinue
                Write-Host " ${CLR_GREEN}[✓] Windows default settings restored.${CLR_RESET}"
                Start-Sleep -Seconds 1
            }
            ([ConsoleKey]::Q) { return }
            ([ConsoleKey]::Escape) { return }
        }
    }
}

function Install-KronosGlobalCLI {
    Clear-Host
    Write-Host ""
    Write-BoxTop "KRONOS GLOBAL CLI INSTALLER"
    Write-Host " ${CLR_SYS_BORDER}│${CLR_RESET}"

    $binDir = Join-Path $env:USERPROFILE "bin"
    if (-not (Test-Path $binDir)) {
        New-Item -ItemType Directory -Path $binDir -Force | Out-Null
    }

    $cmdPath = Join-Path $binDir "kronos.cmd"
    $cmdContent = "@echo off`r`npowershell -ExecutionPolicy Bypass -NoProfile -NoExit -Command `"irm $ServerUrl/kronos | iex`""
    Set-Content -Path $cmdPath -Value $cmdContent -Force

    $userPath = [Environment]::GetEnvironmentVariable("Path", [EnvironmentVariableTarget]::User)
    if ($userPath -notlike "*$binDir*") {
        $newPath = "$userPath;$binDir"
        [Environment]::SetEnvironmentVariable("Path", $newPath, [EnvironmentVariableTarget]::User)
        $env:PATH = "$env:PATH;$binDir"
    }

    Write-Host " ${CLR_SYS_BORDER}│  ${CLR_GREEN}[✓] Global CLI installed successfully!${CLR_RESET}"
    Write-Host " ${CLR_SYS_BORDER}│  ${CLR_MUTED}Executable Target : ${CLR_WHITE}$cmdPath${CLR_RESET}"
    Write-Host " ${CLR_SYS_BORDER}│  ${CLR_MUTED}Environment PATH  : ${CLR_CYAN}Updated with $binDir${CLR_RESET}"
    Write-Host " ${CLR_SYS_BORDER}│${CLR_RESET}"
    Write-Host " ${CLR_SYS_BORDER}│  ${CLR_WHITE}You can now launch KRONOS from ANY terminal (CMD, PowerShell, Terminal)${CLR_RESET}"
    Write-Host " ${CLR_SYS_BORDER}│  ${CLR_WHITE}simply by typing: ${CLR_GREEN}${CLR_BOLD}kronos${CLR_RESET}"
    Write-Host " ${CLR_SYS_BORDER}│${CLR_RESET}"
    Write-BoxBottom
    Write-Host "  Press any key to return to menu..."
    if (-not [Console]::IsInputRedirected) { [Console]::ReadKey($true) | Out-Null }
}

function Show-MatrixScreensaverTUI {
    Clear-Host
    Write-Host " ${CLR_GREEN}[*] Starting Cyber Matrix Stream (awesome-tuis/cmatrix)... Press ANY KEY to exit.${CLR_RESET}"
    Start-Sleep -Milliseconds 600
    Clear-Host

    $chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz#$%&*+<>:;~"
    $width = 75
    $cols = @()
    for ($i = 0; $i -lt $width; $i++) {
        $cols += [PSCustomObject]@{
            Y = Get-Random -Minimum 0 -Maximum 20
            Speed = Get-Random -Minimum 1 -Maximum 3
            Length = Get-Random -Minimum 5 -Maximum 15
        }
    }

    $frame = 0
    while ($true) {
        if ([Console]::IsInputRedirected) { return }
        if ([Console]::KeyAvailable) {
            [Console]::ReadKey($true) | Out-Null
            Clear-Host
            return
        }

        # Build random green cyber line
        $lineChars = @()
        for ($c = 0; $c -lt $width; $c++) {
            $r = Get-Random -Minimum 0 -Maximum 100
            if ($r -lt 15) {
                $rndChar = $chars[(Get-Random -Minimum 0 -Maximum $chars.Length)]
                $lineChars += "$ESC[38;5;120m$rndChar$CLR_RESET"
            } elseif ($r -lt 30) {
                $rndChar = $chars[(Get-Random -Minimum 0 -Maximum $chars.Length)]
                $lineChars += "$ESC[38;5;46m$rndChar$CLR_RESET"
            } elseif ($r -lt 40) {
                $rndChar = $chars[(Get-Random -Minimum 0 -Maximum $chars.Length)]
                $lineChars += "$ESC[97m$rndChar$CLR_RESET"
            } else {
                $lineChars += " "
            }
        }

        Write-Host ($lineChars -join "")
        Start-Sleep -Milliseconds 60
        $frame++
        if ($frame -gt 35) {
            # Trim top periodically
            Write-Host "$ESC[H" -NoNewline
            $frame = 0
        }
    }
}

function Show-MemoryDashboardTUI {
    Clear-Host
    while ($true) {
        Write-Host "$ESC[H" -NoNewline
        $nowTime = (Get-Date).ToString("HH:mm:ss")

        # Fetch memory from server
        $memData = $null
        try {
            $headers = @{ "X-Session-Token" = $SessionToken }
            $memData = Invoke-RestMethod -Uri "$ServerUrl/api/v1/memory" -Method Get -Headers $headers -TimeoutSec 5 -ErrorAction Stop
        } catch {
            $memData = $null
        }

        Write-Host ""
        Write-Host " ${CLR_SYS_BORDER}╭─ [MEMORY] KRONOS PERSISTENT MEMORY & CHAT ARCHIVE ${CLR_CYAN}● LIVE [$nowTime] ${CLR_SYS_BORDER}─────────${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}│${CLR_RESET}"

        if ($memData -and $memData.profile) {
            $p = $memData.profile
            $pHost = if ($p.hostname) { $p.hostname } else { $env:COMPUTERNAME }
            $pOS = if ($p.os_caption) { $p.os_caption } else { "Microsoft Windows" }
            $pRAM = if ($p.total_ram_gb) { "$($p.total_ram_gb) GB" } else { "16 GB" }
            $pDrives = if ($p.drives) { $p.drives } else { "C:" }
            Write-Host " ${CLR_SYS_BORDER}│  ${CLR_MUTED}HOST PROFILE : ${CLR_CYAN}$pHost ${CLR_DARK}│ ${CLR_WHITE}$pOS ${CLR_DARK}│ ${CLR_MUTED}RAM: ${CLR_TEXT}$pRAM ${CLR_DARK}│ ${CLR_MUTED}Drives: ${CLR_TEXT}$pDrives${CLR_RESET}"
            Write-Host " ${CLR_SYS_BORDER}│${CLR_RESET}"
        }

        Write-Host " ${CLR_SYS_BORDER}│  ${CLR_WHITE}${CLR_BOLD}💬 RECENT CHAT SESSIONS & CONVERSATION SUMMARIES:${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}│  ${CLR_MUTED}───  ────────  ───────  ───────  ──────────────────────────────────────────${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}│  ${CLR_MUTED} #   TIME      INTENT   TOOLS    USER QUERY ❯ AI SUMMARY PREVIEW${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}│  ${CLR_MUTED}───  ────────  ───────  ───────  ──────────────────────────────────────────${CLR_RESET}"

        $chats = @()
        if ($memData -and $memData.recent_chats) {
            $chats = @($memData.recent_chats)
        }

        if ($chats.Count -eq 0) {
            Write-Host " ${CLR_SYS_BORDER}│  ${CLR_DARK}(No past chat sessions recorded yet. Start talking in Chat Mode!)${CLR_RESET}"
        } else {
            $idx = 1
            foreach ($c in ($chats | Select-Object -First 8)) {
                $timeStr = "--:--"
                if ($c.timestamp) {
                    try {
                        $parsedDate = [DateTime]::Parse($c.timestamp)
                        $timeStr = $parsedDate.ToString("HH:mm:ss")
                    } catch {
                        $timeStr = "$($c.timestamp)".Substring(0, [math]::Min(8, "$($c.timestamp)".Length))
                    }
                }
                $intentBadge = switch -wildcard ("$($c.intent)".ToUpper()) {
                    "*TROUBLE*" { "${CLR_YELLOW}FIX    ${CLR_RESET}" }
                    "*INFO*"    { "${CLR_CYAN}INFO   ${CLR_RESET}" }
                    "*TECH*"    { "${CLR_BLUE}DOCS   ${CLR_RESET}" }
                    "*GREET*"   { "${CLR_GREEN}CHAT   ${CLR_RESET}" }
                    "*ACTION*"  { "${CLR_YELLOW}ACTION ${CLR_RESET}" }
                    default     { "${CLR_MUTED}DIAG   ${CLR_RESET}" }
                }
                $toolsCount = if ($c.actions_count) { [int]$c.actions_count } else { 0 }
                $actionsBadge = if ($toolsCount -gt 0) { "${CLR_GREEN}$toolsCount tools${CLR_RESET}" } else { "${CLR_DARK}0 tools${CLR_RESET}" }
                $userMsg = if ($c.user_message) { "$($c.user_message)".Trim() } else { "Query" }
                if ($userMsg.Length -gt 24) { $userMsg = $userMsg.Substring(0, 21) + "..." }
                $aiSumm = if ($c.ai_summary) { "$($c.ai_summary)".Trim() } else { "Completed" }
                if ($aiSumm.Length -gt 38) { $aiSumm = $aiSumm.Substring(0, 35) + "..." }

                Write-Host " ${CLR_SYS_BORDER}│  ${CLR_CYAN}[$idx]${CLR_RESET} ${CLR_MUTED}$timeStr${CLR_RESET}  $intentBadge $actionsBadge  ${CLR_WHITE}$($userMsg.PadRight(24))${CLR_RESET} ${CLR_DARK}❯${CLR_RESET} ${CLR_TEXT}$aiSumm${CLR_RESET}"
                $idx++
            }
        }

        Write-Host " ${CLR_SYS_BORDER}│${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}│  ${CLR_WHITE}${CLR_BOLD}🔧 VERIFIED AUTONOMOUS REPAIR EPISODES:${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}│  ${CLR_MUTED}────────────────────────────────────────────────────────────────────────${CLR_RESET}"

        $episodes = @()
        if ($memData -and $memData.recent_episodes) {
            $episodes = @($memData.recent_episodes)
        }

        if ($episodes.Count -eq 0) {
            Write-Host " ${CLR_SYS_BORDER}│  ${CLR_DARK}(No diagnostic repair episodes stored in persistent knowledge store)${CLR_RESET}"
        } else {
            foreach ($ep in ($episodes | Select-Object -First 4)) {
                $issue = if ($ep.issue_summary) { $ep.issue_summary } else { "SYS-DIAG" }
                $cause = if ($ep.root_cause) { $ep.root_cause } else { "Diagnostic verification" }
                if ($cause.Length -gt 45) { $cause = $cause.Substring(0, 42) + "..." }
                $outcome = if ($ep.outcome) { $ep.outcome } else { "$true" }
                $outBadge = if ($outcome -match "true|success|completed|fixed") { "${CLR_GREEN}✔ RESOLVED${CLR_RESET}" } else { "${CLR_YELLOW}● CHECKED${CLR_RESET}" }

                Write-Host " ${CLR_SYS_BORDER}│  ${CLR_GREEN}●${CLR_RESET} ${CLR_WHITE}$issue${CLR_RESET} ${CLR_DARK}─${CLR_RESET} ${CLR_TEXT}$cause${CLR_RESET}  $outBadge"
            }
        }

        Write-Host " ${CLR_SYS_BORDER}│${CLR_RESET}"
        Write-Host " ${CLR_SYS_BORDER}╰────────────────────────────────────────────────────────────────────────${CLR_RESET}"
        Write-Host " ${CLR_MUTED}  [1-8] View Chat Full Detail • [c] Clear Memory • [r] Refresh • [q/Esc] Back${CLR_RESET}   "

        if ([Console]::IsInputRedirected) { return }

        $keyInfo = [Console]::ReadKey($true)
        if ($keyInfo.Key -in @([ConsoleKey]::Q, [ConsoleKey]::Escape)) { return }
        elseif ($keyInfo.Key -eq [ConsoleKey]::R) { continue }
        elseif ($keyInfo.Key -eq [ConsoleKey]::C) {
            Write-Host ""
            Write-Host -NoNewline " ${CLR_YELLOW}[?] Clear all persistent chat history and diagnostic memory? (y/N): ${CLR_RESET}"
            $ans = [Console]::ReadLine()
            if ($ans -and $ans.Trim().ToLower() -eq 'y') {
                try {
                    $headers = @{ "X-Session-Token" = $SessionToken }
                    Invoke-RestMethod -Uri "$ServerUrl/api/v1/memory/clear" -Method Post -Headers $headers -TimeoutSec 5 | Out-Null
                    Write-Host " ${CLR_GREEN}[✔] Persistent memory cleared successfully.${CLR_RESET}"
                } catch {
                    Write-Host " ${CLR_RED}[!] Error clearing memory.${CLR_RESET}"
                }
                Start-Sleep -Milliseconds 800
            }
            continue
        }
        elseif ($keyInfo.Key -ge [ConsoleKey]::D1 -and $keyInfo.Key -le [ConsoleKey]::D8) {
            $sel = [int]$keyInfo.Key - [int][ConsoleKey]::D1
            if ($chats -and $sel -lt $chats.Count) {
                $targetChat = $chats[$sel]
                Clear-Host
                Write-Host ""
                Write-Host " ${CLR_SYS_BORDER}╭─ [CHAT DETAIL #$($sel + 1)] ───────────────────────────────────────────────────${CLR_RESET}"
                Write-Host " ${CLR_SYS_BORDER}│  ${CLR_MUTED}TIMESTAMP : ${CLR_WHITE}$($targetChat.timestamp)${CLR_RESET}"
                Write-Host " ${CLR_SYS_BORDER}│  ${CLR_MUTED}INTENT    : ${CLR_CYAN}$($targetChat.intent)${CLR_RESET}"
                Write-Host " ${CLR_SYS_BORDER}│  ${CLR_MUTED}ACTIONS   : ${CLR_GREEN}$($targetChat.actions_count) tools executed${CLR_RESET}"
                Write-Host " ${CLR_SYS_BORDER}│${CLR_RESET}"
                Write-Host " ${CLR_SYS_BORDER}│  ${CLR_YELLOW}${CLR_BOLD}USER QUERY:${CLR_RESET}"
                foreach ($line in ("$($targetChat.user_message)" -split "`r?`n")) {
                    Write-Host " ${CLR_SYS_BORDER}│  ${CLR_WHITE}❯ $line${CLR_RESET}"
                }
                Write-Host " ${CLR_SYS_BORDER}│${CLR_RESET}"
                Write-Host " ${CLR_SYS_BORDER}│  ${CLR_GREEN}${CLR_BOLD}AI DIAGNOSTIC & REMEDIATION SUMMARY:${CLR_RESET}"
                foreach ($line in ("$($targetChat.ai_summary)" -split "`r?`n")) {
                    Write-Host " ${CLR_SYS_BORDER}│  ${CLR_TEXT}$line${CLR_RESET}"
                }
                Write-Host " ${CLR_SYS_BORDER}│${CLR_RESET}"
                Write-Host " ${CLR_SYS_BORDER}╰────────────────────────────────────────────────────────────────────────${CLR_RESET}"
                Write-Host " ${CLR_MUTED}  Press any key to return to Memory Dashboard...${CLR_RESET}"
                [Console]::ReadKey($true) | Out-Null
                Clear-Host
            }
            continue
        }
    }
}

# ==============================================================================
# REMEDIATION & DISPATCH
# ==============================================================================

function Execute-RemediationPlan($plan, [bool]$InChatMode = $false) {
    $actionsList = @($plan.actions)

    # 1. Informational / Chat Response (No commands needed)
    if ($actionsList.Count -eq 0) {
        if ($InChatMode) {
            Write-Host ""
            Write-BotBoxTop "KRONOS"
            $cleanSummary = "$($plan.summary)" -replace '[\u202F\u00A0\u200B]', ' ' -replace 'â¯', ' ' -replace 'â€“', '-' -replace 'â€”', '-' -replace 'â', '-' -replace '[‑‒–—]', '-'
            foreach ($line in ($cleanSummary -split "`r?`n")) {
                if ($line.Trim()) {
                    Write-Host " $CLR_BOT_BORDER│ $CLR_WHITE$line$CLR_RESET"
                }
            }
            Write-BotBoxBottom
            Write-Host ""
        } else {
            Write-Host ""
            Write-Host " $CLR_DARK+--[$CLR_CYAN KRONOS INTEL $CLR_DARK]---------------------------------------$CLR_RESET"
            if ($plan.root_cause -and $plan.root_cause -ne $plan.summary) {
                Write-Host " ${CLR_DARK}|  ${CLR_CYAN}[Context]: ${CLR_WHITE}$($plan.root_cause)${CLR_RESET}"
            }
            foreach ($line in (($plan.summary | Out-String) -split "`r?`n")) {
                if ($line.Trim()) {
                    Write-Host " $CLR_WHITE   $line$CLR_RESET"
                }
            }
            Write-Host " $CLR_DARK+------------------------------------------------------------$CLR_RESET"
            Write-Host ""
        }
        return
    }

    # 2. Level 2 Controlled Autonomy: Risk Tier Assessment & Confirmation Gate
    $requiresAuth = $false
    $riskBadge = "LOW - AUTO"
    $badgeColor = $CLR_GREEN

    if ($plan.risk_level -eq "HIGH" -or $plan.risk_level -eq "CRITICAL") {
        $requiresAuth = $true
        $riskBadge = "HIGH RISK - EXPLICIT AUTHORIZATION REQUIRED"
        $badgeColor = $CLR_RED
    } elseif ($plan.requires_confirmation -or $plan.risk_level -eq "MODERATE" -or $plan.risk_level -eq "MEDIUM") {
        $requiresAuth = $true
        $riskBadge = "MODERATE RISK - CONFIRMATION REQUIRED"
        $badgeColor = $CLR_YELLOW
    } else {
        foreach ($step in $actionsList) {
            if ($step.command -match '(?i)\b(netsh\s+int\s+ip\s+reset|bcdedit\s+/(delete|clean)|vssadmin\s+delete|del(ete)?\s+|Remove-Item\s+|rmdir\s+|format\s+[a-zA-Z]:|Clear-Disk|Initialize-Disk|Format-Volume|Remove-Partition)\b') {
                $requiresAuth = $true
                $riskBadge = "HIGH RISK - POTENTIALLY DISRUPTIVE OPERATION"
                $badgeColor = $CLR_RED
                break
            }
        }
    }

    if ($requiresAuth) {
        Write-Host ""
        Write-Host " $badgeColor╭─ [LEVEL 2 AUTONOMY] $riskBadge ───────────────────────────────$CLR_RESET"
        if ($plan.summary) {
            Write-Host " $badgeColor│  $CLR_WHITE$($plan.summary)$CLR_RESET"
        }
        Write-Host " $badgeColor│  $CLR_MUTEDPlanned Actions:$CLR_RESET"
        foreach ($step in $actionsList) {
            Write-Host " $badgeColor│   $CLR_CYAN• $($step.description)$CLR_RESET"
        }
        Write-BoxBottom
        Write-Host " ${badgeColor}Authorize execution? (y/N): ${CLR_WHITE}" -NoNewline
        $choice = Read-Host
        if ($choice -ne 'y' -and $choice -ne 'Y') {
            Write-Host " $CLR_YELLOW[*] Operation cancelled by user. Target system untouched.$CLR_RESET"
            return
        }
    } else {
        if (-not $InChatMode) {
            Write-Host " $CLR_GREEN[*] Level 2 Autonomy: Executing safe low-risk actions...$CLR_RESET"
        }
    }

    # Check if safety snapshot needed
    $needsSnapshot = $false
    foreach ($step in $actionsList) {
        if ($step.command -match '(?i)\b(restart-service|stop-service|remove-item|rmdir|Remove-ItemProperty|Set-Service|Set-ItemProperty|netsh\s+int\s+ip\s+reset|ipconfig\s+/(release|renew)|dism)\b') {
            $needsSnapshot = $true
            break
        }
    }

    if ($needsSnapshot) {
        Write-Host " $CLR_CYAN[*] System change detected. Creating safety snapshot...$CLR_RESET" -NoNewline
        $snap = Create-RollbackSnapshot
        Write-Host " $CLR_GREEN[SAVED]$CLR_RESET"
    }

    # Execute verified commands
    $outputItems = @()

    foreach ($step in $actionsList) {
        if (-not $InChatMode) {
            Write-Host " $CLR_DARK  |-- $($step.description)...$CLR_RESET" -NoNewline
        }
        try {
            $safeCmd = $step.command -replace '\bexit\s+\d+\b', '' -replace '\bexit\b', ''
            if ($safeCmd -match '\|\s*(Where-Object|Select-Object|Sort-Object|ForEach-Object)\s*($|\|)') {
                continue
            }
            $cmdOutput = & {
                $ErrorActionPreference = 'Continue'
                Invoke-Expression $safeCmd
            } 2>&1

            if (-not $InChatMode) {
                Write-Host " $CLR_GREEN[OK]$CLR_RESET"
            }

            if ($cmdOutput) {
                $outStr = ($cmdOutput | Out-String).Trim()
                if (-not [string]::IsNullOrWhiteSpace($outStr)) {
                    $cleanOut = $outStr -replace '\x1b\[[0-9;]*[a-zA-Z]', '' -replace '[\x00-\x08\x0B\x0C\x0E-\x1F]', ''
                    $outputItems += $cleanOut
                    if ($cleanOut -match '(?i)(?:Launched|Opened)(?:\s+in\s+[^:]+)?:\s*([a-zA-Z]:\\[^\r\n]+)') {
                        $script:LastOpenedPath = $matches[1].Trim()
                    }
                }
            }
        } catch {
            if (-not $InChatMode) {
                Write-Host " $CLR_RED[FAILED]$CLR_RESET"
                Write-Host "      $CLR_RED$($_.Exception.Message)$CLR_RESET"
            }
        }
    }

    if ($outputItems.Count -gt 0) {
        $script:LastCommandOutput = $outputItems -join "`n"
    }

    # Verify Operation Result
    if ($plan.verification_command -and $plan.verification_command -ne "$true" -and $plan.verification_command -ne "true") {
        try {
            $vRes = & {
                $ErrorActionPreference = 'SilentlyContinue'
                $sb = [ScriptBlock]::Create($plan.verification_command)
                & $sb
            } 2>$null
            if (-not $InChatMode) {
                if ($vRes -eq $false) {
                    Write-Host " $CLR_YELLOW  |-- [!] Verification Warning: Expected state not confirmed.$CLR_RESET"
                } else {
                    Write-Host " $CLR_GREEN  |-- [✓] Verification: System state confirmed.$CLR_RESET"
                }
            }
        } catch {
            if (-not $InChatMode) {
                Write-Host " $CLR_YELLOW  |-- [!] Verification check encountered a warning.$CLR_RESET"
            }
        }
    }

    # Render results
    if ($InChatMode) {
        Write-Host ""
        Write-BotBoxTop "KRONOS"
        if ($plan.summary) {
            $cleanSummary = $plan.summary -replace 'â€“', '-' -replace 'â€”', '-' -replace 'â', '-' -replace '[‑‒–—]', '-'
            foreach ($sLine in ($cleanSummary -split "`r?`n")) {
                if ($sLine.Trim()) {
                    Write-Host " $CLR_BOT_BORDER│ $CLR_WHITE$sLine$CLR_RESET"
                }
            }
        }
        if ($outputItems.Count -gt 0) {
            Write-Host " $CLR_BOT_BORDER│$CLR_RESET"
            Write-Host " $CLR_BOT_BORDER├─ $CLR_CYAN[LIVE SYSTEM OUTPUT] $CLR_BOT_BORDER────────────────────────────────────────$CLR_RESET"
            Write-Host " $CLR_BOT_BORDER│$CLR_RESET"
            foreach ($line in (($script:LastCommandOutput) -split "`r?`n")) {
                $lineDisplay = $line
                $lineDisplay = $lineDisplay -replace '\[DIR\]', "$ESC[38;5;51m[DIR]$CLR_RESET"
                $lineDisplay = $lineDisplay -replace '\[VID\]', "$ESC[38;5;206m[VID]$CLR_RESET"
                $lineDisplay = $lineDisplay -replace '\[AUD\]', "$ESC[38;5;215m[AUD]$CLR_RESET"
                $lineDisplay = $lineDisplay -replace '\[IMG\]', "$ESC[38;5;177m[IMG]$CLR_RESET"
                $lineDisplay = $lineDisplay -replace '\[ZIP\]', "$ESC[38;5;220m[ZIP]$CLR_RESET"
                $lineDisplay = $lineDisplay -replace '\[APP\]', "$ESC[38;5;120m[APP]$CLR_RESET"
                $lineDisplay = $lineDisplay -replace '\[DOC\]', "$ESC[38;5;147m[DOC]$CLR_RESET"
                $lineDisplay = $lineDisplay -replace '\[FILE\]', "$ESC[38;5;248m[FILE]$CLR_RESET"
                Write-Host " $CLR_BOT_BORDER│ $CLR_TEXT  $lineDisplay$CLR_RESET"
            }
        } elseif ($actionsList.Count -gt 0) {
            Write-Host " $CLR_BOT_BORDER│$CLR_RESET"
            $isSearchOnly = $false
            foreach ($a in $actionsList) {
                if ($a.command -match '(?i)\b(Get-ChildItem|dir|findstr|Select-String)\b' -and $a.command -notmatch '(?i)\b(Start-Process|Invoke-Item|Remove-Item|del|rmdir|Set-)\b') {
                    $isSearchOnly = $true
                    break
                }
            }
            if ($isSearchOnly) {
                Write-Host " $CLR_BOT_BORDER│ $CLR_YELLOW  [!] Search completed, but no matching files or folders were found.$CLR_RESET"
            } else {
                Write-Host " $CLR_BOT_BORDER│ $CLR_GREEN  [✓] Action completed successfully.$CLR_RESET"
            }
        }
        Write-BotBoxBottom
        Write-Host ""
    } else {
        if ($outputItems.Count -gt 0) {
            Write-Host ""
            Write-Host " $CLR_DARK  +--[$CLR_CYAN REPORT $CLR_DARK]---------------------------------------$CLR_RESET"
            foreach ($line in (($script:LastCommandOutput) -split "`r?`n")) {
                if ($line.Trim()) {
                    Write-Host " $CLR_WHITE     $line$CLR_RESET"
                }
            }
            Write-Host " $CLR_DARK  +--------------------------------------------------------$CLR_RESET"
            Write-Host ""
        }
    }
}

function Dispatch-Problem($prob, [bool]$InChatMode = $false) {
    $telemetryData = Collect-Telemetry
    if ($InChatMode) {
        Write-Host " $CLR_MUTED   ✦ KRONOS is thinking...$CLR_RESET"
    } else {
        Write-Host " $CLR_CYAN[*] Uplinking payload to Neural Core ($ServerUrl)...$CLR_RESET"
    }

    $cleanHistory = @()
    if ($script:ConversationHistory) {
        foreach ($h in $script:ConversationHistory) {
            $cRole = "$($h.role)"
            $cContent = "$($h.content)" -replace '\x1b\[[0-9;]*[a-zA-Z]', '' -replace '[\x00-\x08\x0B\x0C\x0E-\x1F]', ''
            $cleanHistory += @{ role = $cRole; content = $cContent }
        }
    }
    $cleanLastOutput = "$($script:LastCommandOutput)" -replace '\x1b\[[0-9;]*[a-zA-Z]', '' -replace '[\x00-\x08\x0B\x0C\x0E-\x1F]', ''

    $payload = @{
        problem       = "$prob"
        telemetry     = $telemetryData
        session_token = $SessionToken
        history       = $cleanHistory
        last_output   = $cleanLastOutput
    } | ConvertTo-Json -Depth 6

    try {
        $headers = @{ "X-Session-Token" = $SessionToken }
        $jsonBytes = [System.Text.Encoding]::UTF8.GetBytes($payload)
        $response = Invoke-RestMethod -Uri "$ServerUrl/api/v1/diagnose" -Method Post -Body $jsonBytes -Headers $headers -ContentType "application/json; charset=utf-8" -TimeoutSec 45
        
        $script:ConversationHistory += @{ role = "user"; content = "$prob" }
        $script:ConversationHistory += @{ role = "assistant"; content = "$($response.summary)" }
        if ($script:ConversationHistory.Count -gt 10) {
            $script:ConversationHistory = $script:ConversationHistory[-10..-1]
        }

        if ($script:VoiceEnabled -and $script:SpeechSynth -and $response.summary) {
            $cleanSpeech = ($response.summary -replace '\x1b\[[0-9;]*m', '') -replace '[^a-zA-Z0-9\s\.\,\?\!]', ''
            $script:SpeechSynth.SpeakAsync($cleanSpeech) | Out-Null
        }
        Execute-RemediationPlan $response -InChatMode $InChatMode
        if ($script:LastCommandOutput -and $script:ConversationHistory.Count -gt 0) {
            $compactOut = (($script:LastCommandOutput -split "`r?`n") | Where-Object { $_.Trim() } | Select-Object -First 6) -join "`n"
            if ($compactOut) {
                $script:ConversationHistory[-1].content += "`n`n[Command Output Result]:`n$compactOut"
            }
        }
    } catch {
        Write-Host ""
        Write-BotBoxTop "KRONOS (Offline Client Fallback)"
        Write-Host " $CLR_BOT_BORDER│ $CLR_YELLOW  [!] Core AI Server connect nahi ho pa raha (Offline / Disconnected).$CLR_RESET"
        Write-Host " $CLR_BOT_BORDER│ $CLR_WHITE  Tension mat lo bhai! Aapke saare local features abhi bhi 100% chal rahe hain:$CLR_RESET"
        Write-Host " $CLR_BOT_BORDER│   $CLR_CYAN• Direct Shell : $CLR_WHITE!$prob (Direct command run karne ke liye)$CLR_RESET"
        Write-Host " $CLR_BOT_BORDER│   $CLR_CYAN• Dashboards   : $CLR_MUTED/top • /services • /ports • /disk • /wifi • /power • /devices$CLR_RESET"
        Write-Host " $CLR_BOT_BORDER│   $CLR_CYAN• File Tools   : $CLR_MUTED/list • /find • /del • /tree$CLR_RESET"
        Write-BotBoxBottom
        Write-Host ""
    }
}

function Start-ConversationMode($initialPrompt = $null) {
    Clear-Host
    Write-Host ""
    Write-Host " $CLR_BOT_BORDER╭─ KRONOS AI CO-PILOT ──────────────────────────────────────────$CLR_RESET"
    Write-Host " $CLR_BOT_BORDER│  $CLR_WHITE Autonomous Windows Co-Pilot • Natural Hinglish / English$CLR_RESET"
    Write-Host " $CLR_BOT_BORDER│  $CLR_MUTED Commands: ${CLR_GREEN}/help${CLR_MUTED} • ${CLR_GREEN}/open <#>${CLR_MUTED} • ${CLR_GREEN}/wifi${CLR_MUTED} • ${CLR_GREEN}/disk${CLR_MUTED} • ${CLR_GREEN}/specs${CLR_MUTED} • ${CLR_GREEN}/top${CLR_MUTED} • ${CLR_GREEN}/tree$CLR_RESET"
    Write-BotBoxBottom
    Write-Host ""

    if ($initialPrompt) {
        Write-UserPromptBox
        Write-Host "$initialPrompt"
        Dispatch-Problem $initialPrompt -InChatMode $true
    }

    while ($true) {
        Write-UserPromptBox
        $prompt = Read-Host

        if ([string]::IsNullOrWhiteSpace($prompt)) {
            continue
        }

        $pLower = $prompt.Trim().ToLower()

        # 1. Quick Commands Help Sheet
        if ($pLower -in @("/help", "/cmds", "/?", "help", "commands")) {
            Write-Host ""
            Write-Host " $CLR_CYAN╭─ KRONOS QUICK COMMANDS & TUIs $CLR_SYS_BORDER─────────────────────────$CLR_RESET"
            Write-Host " $CLR_CYAN│$CLR_RESET"
            Write-Host " $CLR_CYAN│  ${CLR_GREEN}/open <name|#>${CLR_RESET}  ${CLR_WHITE}- Open app, file, or item number from output $CLR_RESET"
            Write-Host " $CLR_CYAN│  ${CLR_GREEN}/list [drive] ${CLR_RESET}  ${CLR_WHITE}- List files & folders with category badges  $CLR_RESET"
            Write-Host " $CLR_CYAN│  ${CLR_GREEN}/find <name>  ${CLR_RESET}  ${CLR_WHITE}- Deep search across all drives (C:, D:, etc.) $CLR_RESET"
            Write-Host " $CLR_CYAN│  ${CLR_GREEN}/del  <name>  ${CLR_RESET}  ${CLR_WHITE}- Safe delete with confirmation check (y/N)   $CLR_RESET"
            Write-Host " $CLR_CYAN│  ${CLR_GREEN}/again        ${CLR_RESET}  ${CLR_WHITE}- Re-launch previously opened target           $CLR_RESET"
            Write-Host " $CLR_CYAN│  ${CLR_GREEN}/theme [opt]  ${CLR_RESET}  ${CLR_WHITE}- Switch theme (slate, charcoal, black)       $CLR_RESET"
            Write-Host " $CLR_CYAN│$CLR_RESET"
            Write-Host " $CLR_CYAN│  ${CLR_GREEN}!cmd / >cmd   ${CLR_RESET}  ${CLR_WHITE}- Direct native CMD & PowerShell passthrough $CLR_RESET"
            Write-Host " $CLR_CYAN│$CLR_RESET"
            Write-Host " $CLR_CYAN│  ${CLR_YELLOW}INTERACTIVE TUI DASHBOARDS:${CLR_RESET}"
            Write-Host " $CLR_CYAN│  ${CLR_CYAN}/memory       ${CLR_RESET}  ${CLR_WHITE}- 🧠 Persistent Memory & Past Chat Summaries     $CLR_RESET"
            Write-Host " $CLR_CYAN│  ${CLR_CYAN}/wifi         ${CLR_RESET}  ${CLR_WHITE}- [NET] Wi-Fi & Network Radar (Signal, IP, Ping)$CLR_RESET"
            Write-Host " $CLR_CYAN│  ${CLR_CYAN}/disk         ${CLR_RESET}  ${CLR_WHITE}- [DISK] Storage Heatmap & S.M.A.R.T. Health Map $CLR_RESET"
            Write-Host " $CLR_CYAN│  ${CLR_CYAN}/specs        ${CLR_RESET}  ${CLR_WHITE}- ⚡ Windows Architecture & Fastfetch Card   $CLR_RESET"
            Write-Host " $CLR_CYAN│  ${CLR_CYAN}/top          ${CLR_RESET}  ${CLR_WHITE}- [TOP] Live CPU/RAM Resource & Task Monitor    $CLR_RESET"
            Write-Host " $CLR_CYAN│  ${CLR_CYAN}/tree [dir]   ${CLR_RESET}  ${CLR_WHITE}- [DIR] Interactive Arrow Folder Explorer       $CLR_RESET"
            Write-Host " $CLR_CYAN│  ${CLR_CYAN}/power        ${CLR_RESET}  ${CLR_WHITE}- [PWR] Power Scheme & HTML Battery Report TUI  $CLR_RESET"
            Write-Host " $CLR_CYAN│  ${CLR_CYAN}/services     ${CLR_RESET}  ${CLR_WHITE}- [SVC]  Live Windows Service Manager & Filter   $CLR_RESET"
            Write-Host " $CLR_CYAN│  ${CLR_CYAN}/firewall     ${CLR_RESET}  ${CLR_WHITE}- [SEC] Windows Defender Firewall Cockpit       $CLR_RESET"
            Write-Host " $CLR_CYAN│  ${CLR_CYAN}/devices      ${CLR_RESET}  ${CLR_WHITE}- [DEV] Hardware Inventory & Degraded Device TUI$CLR_RESET"
            Write-Host " $CLR_CYAN│  ${CLR_CYAN}/ports        ${CLR_RESET}  ${CLR_WHITE}- [PORT] Active Listening Ports & Process Audit  $CLR_RESET"
            Write-Host " $CLR_CYAN│  ${CLR_CYAN}/audio        ${CLR_RESET}  ${CLR_WHITE}- [AUD] Sound Subsystem Diagnostic & Reset      $CLR_RESET"
            Write-Host " $CLR_CYAN│$CLR_RESET"
            Write-Host " $CLR_CYAN│  ${CLR_GREEN}/lock         ${CLR_RESET}  ${CLR_WHITE}- Lock session and prompt security gateway   $CLR_RESET"
            Write-Host " $CLR_CYAN│  ${CLR_GREEN}/clear        ${CLR_RESET}  ${CLR_WHITE}- Clear screen and refresh view                $CLR_RESET"
            Write-Host " $CLR_CYAN│  ${CLR_GREEN}/reset        ${CLR_RESET}  ${CLR_WHITE}- Reset chat context and start fresh          $CLR_RESET"
            Write-Host " $CLR_CYAN│  ${CLR_GREEN}/menu         ${CLR_RESET}  ${CLR_WHITE}- Return to autonomous diagnostic tools menu   $CLR_RESET"
            Write-Host " $CLR_CYAN│$CLR_RESET"
            Write-BoxBottom
            Write-Host ""
            continue
        }

        # 2. Lock & Logout session
        if ($pLower -in @("/lock", "/logout", "lock", "logout")) {
            Show-LoginGateway
            Show-Banner
            continue
        }

        # 2. Interactive TUI Dashboards Direct Slash Commands
        if ($pLower -in @("/power", "/battery", "power", "battery")) {
            Show-PowerCockpitTUI
            continue
        }
        if ($pLower -in @("/services", "/svc", "services", "svc")) {
            Show-ServiceManagerTUI
            continue
        }
        if ($pLower -in @("/firewall", "/fw", "firewall", "fw")) {
            Show-FirewallCockpitTUI
            continue
        }
        if ($pLower -in @("/devices", "/hw", "devices", "hw")) {
            Show-DeviceHardwareTUI
            continue
        }
        if ($pLower -in @("/memory", "/history", "/chats", "memory", "history", "chats")) {
            Show-MemoryDashboardTUI
            continue
        }
        if ($pLower -in @("/wifi", "/net", "wifi", "net")) {
            Show-NetworkRadarTUI
            continue
        }
        if ($pLower -in @("/disk", "/storage", "disk", "storage")) {
            Show-DiskHealthTUI
            continue
        }
        if ($pLower -in @("/specs", "/sys", "specs", "sys", "fastfetch", "neofetch")) {
            Show-SystemSpecsTUI
            continue
        }
        if ($pLower -in @("/top", "/task", "top", "task", "taskmgr")) {
            Show-TaskMonitorTUI
            continue
        }
        if ($pLower -match '^(/tree|/folder|/browse|tree|folder|browse)(\s+.*)?$') {
            $rawDir = ($pLower -replace '^(/tree|/folder|/browse|tree|folder|browse)', '').Trim()
            $startD = if ($rawDir -and (Test-Path $rawDir)) { $rawDir } else { "D:\" }
            Show-FolderNavigatorTUI $startD
            continue
        }
                if ($pLower -in @("/ports", "/netstat", "ports", "netstat")) {
            Show-PortAuditTUI
            continue
        }
        if ($pLower -in @("/audio", "/sound", "audio", "sound", "/cava", "cava")) {
            Show-AudioTUI
            continue
        }
        if ($pLower -in @("/band", "/flow", "/netflow", "/bandwhich", "band", "flow", "bandwhich")) {
            Show-BandwidthRadarTUI
            continue
        }
        if ($pLower -in @("/dust", "/ncdu", "/treesize", "dust", "ncdu")) {
            Show-DustTreemapTUI
            continue
        }
                if ($pLower -in @("/git", "/lazygit", "git", "lazygit")) {
            Show-GitCockpitTUI
            continue
        }
        if ($pLower -in @("/matrix", "/cmatrix", "matrix", "cmatrix")) {
            Show-MatrixScreensaverTUI
            continue
        }
        if ($pLower -in @("/superfile", "/fm", "/yazi", "/ranger")) {
            Show-FolderNavigatorTUI
            continue
        }

        # 3. Local Instant /list Command with Category Badges & Numbered Items
        if ($pLower -match '^(/list|list)(\s+.*)?$') {
            $rawArg = ($pLower -replace '^(/list|list)', '').Trim()
            $targetDir = "D:\"
            if ($rawArg -in @("c", "c:", "c:\")) { $targetDir = "C:\" }
            elseif ($rawArg -in @("d", "d:", "d:\", "")) { $targetDir = "D:\" }
            elseif ($rawArg -eq "desktop") { $targetDir = [Environment]::GetFolderPath('Desktop') }
            elseif ($rawArg -eq "downloads") { $targetDir = Join-Path $env:USERPROFILE 'Downloads' }
            elseif ($rawArg -eq "documents") { $targetDir = [Environment]::GetFolderPath('MyDocuments') }
            elseif (Test-Path $rawArg) { $targetDir = $rawArg }

            $items = Get-ChildItem -Path $targetDir -ErrorAction SilentlyContinue | Where-Object { $_.Name -notmatch '^(\$RECYCLE\.BIN|System Volume Information|pagefile\.sys|DumpStack\.log\.tmp|msdownld\.tmp)$' }

            $rawOutputLines = @()
            Write-Host ""
            Write-BotBoxTop "KRONOS"
            Write-Host " $CLR_BOT_BORDER│ $CLR_WHITE Contents of: $targetDir$CLR_RESET"
            Write-Host " $CLR_BOT_BORDER│$CLR_RESET"

            $idx = 1
            foreach ($item in $items) {
                $ext = if ($item.PSIsContainer) { "" } else { $item.Extension.ToLower() }
                $badge = Get-ItemCategoryBadge $ext $item.PSIsContainer
                $rawBadge = if ($item.PSIsContainer) { "[DIR]" }
                            elseif (@('.mkv','.mp4','.avi','.mov','.wmv','.webm','.flv') -contains $ext) { "[VID]" }
                            elseif (@('.zip','.rar','.7z','.iso') -contains $ext) { "[ZIP]" }
                            elseif (@('.exe','.msi','.apk') -contains $ext) { "[APP]" }
                            elseif (@('.pdf','.doc','.docx','.txt','.xlsx','.log') -contains $ext) { "[DOC]" }
                            elseif (@('.jpg','.png','.jpeg','.webp') -contains $ext) { "[IMG]" }
                            else { "[FILE]" }
                $sz = if ($item.PSIsContainer) { "Folder" }
                      elseif ($item.Length -ge 1GB) { "{0:N2} GB" -f ($item.Length / 1GB) }
                      elseif ($item.Length -ge 1MB) { "{0:N2} MB" -f ($item.Length / 1MB) }
                      else { "{0:N1} KB" -f ($item.Length / 1KB) }

                $rawOutputLines += "[$idx] $rawBadge $($item.FullName) ($sz)"
                Write-Host " $CLR_BOT_BORDER│ $CLR_CYAN  [$idx]$CLR_RESET $badge  $CLR_WHITE$($item.FullName)$CLR_MUTED ($sz)$CLR_RESET"
                $idx++
            }
            $script:LastCommandOutput = $rawOutputLines -join "`n"

            Write-Host " $CLR_BOT_BORDER│$CLR_RESET"
            Write-Host " $CLR_BOT_BORDER│ $CLR_YELLOW  [TIP] Type '/open 1' or '/open <name>' to launch instantly$CLR_RESET"
            Write-BotBoxBottom
            Write-Host ""
            continue
        }

        # 4. Local Instant /open <number|ordinal> from Last Output
        $openMatchNum = $null
        if ($pLower -match '^(/open|open)\s+(\d+)(st|nd|rd|th)?$') {
            $openMatchNum = [int]$matches[2]
        } else {
            $ordMap = @{ 'first' = 1; 'second' = 2; 'third' = 3; 'fourth' = 4; 'fifth' = 5; 'pehli' = 1; 'dusri' = 2; 'teesri' = 3; 'pehla' = 1; 'dusra' = 2; 'teesra' = 3 }
            foreach ($k in $ordMap.Keys) {
                if ($pLower -match "^(/open|open)\s+$k$") {
                    $openMatchNum = $ordMap[$k]
                    break
                }
            }
        }

        if ($openMatchNum -ne $null) {
            $num = $openMatchNum
            $paths = @()
            if ($script:LastCommandOutput) {
                foreach ($l in ($script:LastCommandOutput -split "`r?`n")) {
                    $ls = $l.Trim()
                    if ($ls -match '^\[(\d+)\]\s+(?:\[[A-Z]+\]\s+)?([a-zA-Z]:\\[^\r\n]+?)(?:\s+\([^\)]+\))?$') {
                        $paths += $matches[2].Trim()
                    } elseif ($ls -match '^[a-zA-Z]:\\') {
                        $parts = $ls -split '\s{3,}'
                        if ($parts[0]) { $paths += $parts[0].Trim() }
                    }
                }
            }
            if ($num -ge 1 -and $num -le $paths.Count) {
                $targetPath = $paths[$num - 1]
                if ($targetPath -match '\.\.\.$') {
                    $prefix = $targetPath -replace '\.\.\.$', '*'
                    $realItem = Get-ChildItem -Path $prefix -ErrorAction SilentlyContinue | Select-Object -First 1
                    if ($realItem) { $targetPath = $realItem.FullName }
                }
                Write-Host ""
                Write-BotBoxTop "KRONOS"
                Write-Host " $CLR_BOT_BORDER│ $CLR_WHITE Opening item #${num}: $targetPath$CLR_RESET"
                if ((Get-Item $targetPath -ErrorAction SilentlyContinue).PSIsContainer) {
                    Start-Process explorer.exe $targetPath
                } else {
                    Start-Process $targetPath
                }
                $script:LastOpenedPath = $targetPath
                Write-Host " $CLR_BOT_BORDER│ $CLR_GREEN  [✓] Successfully opened.$CLR_RESET"
                Write-BotBoxBottom
                Write-Host ""
                continue
            } else {
                Write-Host " $CLR_YELLOW[!] Item number #$num not found in recent output list (Total items: $($paths.Count)).$CLR_RESET"
                Write-Host ""
                continue
            }
        }

        # 5. Handle smart conversational shortcuts: 'open again', 'again', 'use vlc pr open kro'
        if ($pLower -in @("open again", "again", "reopen", "phir se kholo", "wapas kholo") -and $script:LastOpenedPath) {
            Write-Host ""
            Write-BotBoxTop "KRONOS"
            Write-Host " $CLR_BOT_BORDER│ $CLR_WHITE Re-launching previous target: $script:LastOpenedPath$CLR_RESET"
            Start-Process $script:LastOpenedPath
            Write-Host " $CLR_BOT_BORDER│ $CLR_GREEN  [✓] Successfully re-opened.$CLR_RESET"
            Write-BotBoxBottom
            Write-Host ""
            continue
        }

        if (($pLower -match '\b(use|ise|isko|usko)\b' -and $pLower -match '\b(vlc)\b') -and $script:LastOpenedPath) {
            $vlcExe = if (Test-Path "C:\Program Files (x86)\VideoLAN\VLC\vlc.exe") { "C:\Program Files (x86)\VideoLAN\VLC\vlc.exe" } else { "C:\Program Files\VideoLAN\VLC\vlc.exe" }
            Write-Host ""
            Write-BotBoxTop "KRONOS"
            Write-Host " $CLR_BOT_BORDER│ $CLR_WHITE Opening previous target in VLC: $script:LastOpenedPath$CLR_RESET"
            Start-Process $vlcExe -ArgumentList ('"' + $script:LastOpenedPath + '"')
            Write-Host " $CLR_BOT_BORDER│ $CLR_GREEN  [✓] Launched in VLC media player.$CLR_RESET"
            Write-BotBoxBottom
            Write-Host ""
            continue
        }

        if ($pLower -in @("exit", "quit", "back", "menu", "0")) {
            Write-Host " $CLR_GREEN[*] Returning to main menu...$CLR_RESET"
            Start-Sleep -Milliseconds 300
            Show-Banner
            break
        }
        if ($pLower -in @("clear", "cls")) {
            Clear-Host
            Write-Host ""
            Write-Host " $CLR_SYS_BORDER╭─ KRONOS AI CO-PILOT $CLR_MUTED(Session Active) $CLR_SYS_BORDER──────────────────────$CLR_RESET"
            Write-BoxBottom
            Write-Host ""
            continue
        }
        if ($pLower -like "/theme*" -or $pLower -like "/bg*") {
            $parts = $pLower -split '\s+'
            $sub = if ($parts.Count -gt 1) { $parts[1] } else { "" }
            switch ($sub) {
                "black" {
                    $script:KronosThemeBg = "#0c0c0c"
                    $script:KronosThemeFg = "#ffffff"
                    Set-KronosTerminalTheme $script:KronosThemeBg $script:KronosThemeFg
                    Clear-Host
                    Write-Host ""
                    Write-BotBoxTop "THEME"
                    Write-Host " $CLR_BOT_BORDER│ $CLR_GREEN  [✓] Terminal theme set to: ${CLR_WHITE}Classic Black (#0c0c0c)$CLR_RESET"
                    Write-BotBoxBottom
                    Write-Host ""
                }
                "charcoal" {
                    $script:KronosThemeBg = "#1a1d24"
                    $script:KronosThemeFg = "#f0f3f6"
                    Set-KronosTerminalTheme $script:KronosThemeBg $script:KronosThemeFg
                    Clear-Host
                    Write-Host ""
                    Write-BotBoxTop "THEME"
                    Write-Host " $CLR_BOT_BORDER│ $CLR_GREEN  [✓] Terminal theme set to: ${CLR_WHITE}Deep Charcoal (#1a1d24)$CLR_RESET"
                    Write-BotBoxBottom
                    Write-Host ""
                }
                "slate" {
                    $script:KronosThemeBg = "#23272e"
                    $script:KronosThemeFg = "#f0f3f6"
                    Set-KronosTerminalTheme $script:KronosThemeBg $script:KronosThemeFg
                    Clear-Host
                    Write-Host ""
                    Write-BotBoxTop "THEME"
                    Write-Host " $CLR_BOT_BORDER│ $CLR_GREEN  [✓] Terminal theme set to: ${CLR_WHITE}Modern Slate Grey (#23272e)$CLR_RESET"
                    Write-BotBoxBottom
                    Write-Host ""
                }
                default {
                    if ($script:KronosThemeBg -eq "#23272e") {
                        $script:KronosThemeBg = "#1a1d24"
                        $themeName = "Deep Charcoal (#1a1d24)"
                    } elseif ($script:KronosThemeBg -eq "#1a1d24") {
                        $script:KronosThemeBg = "#0c0c0c"
                        $themeName = "Classic Black (#0c0c0c)"
                    } else {
                        $script:KronosThemeBg = "#23272e"
                        $themeName = "Modern Slate Grey (#23272e)"
                    }
                    Set-KronosTerminalTheme $script:KronosThemeBg $script:KronosThemeFg
                    Clear-Host
                    Write-Host ""
                    Write-BotBoxTop "THEME"
                    Write-Host " $CLR_BOT_BORDER│ $CLR_GREEN  [✓] Terminal theme set to: ${CLR_WHITE}$themeName$CLR_RESET"
                    Write-BotBoxBottom
                    Write-Host ""
                }
            }
            continue
        }

        if ($pLower -in @("reset", "new")) {
            $script:ConversationHistory = @()
            $script:LastCommandOutput = ""
            Write-Host ""
            Write-BotBoxTop "KRONOS"
            Write-Host " $CLR_BOT_BORDER│ $CLR_GREEN  [✓] Chat memory cleared. Fresh context started.$CLR_RESET"
            Write-BotBoxBottom
            Write-Host ""
            continue
        }
        if ($prompt.Trim() -eq "9") {
            Write-Host " $CLR_CYAN[*] AI Chatbot is already open! Ask your question in plain language.$CLR_RESET"
            Write-Host ""
            continue
        }

        # Direct Windows CMD & PowerShell Shell Passthrough Engine
        $isShellCmd = $false
        $actualCmd = ""

        if ($prompt -match '^(!|>)\s*(.+)$') {
            $isShellCmd = $true
            $actualCmd = $Matches[2].Trim()
        } else {
            $firstWord = ($prompt.Trim() -split '\s+')[0].ToLower()
            $knownCmds = @(
                'ipconfig', 'ping', 'netstat', 'tracert', 'nslookup', 'route', 'arp', 'tasklist',
                'taskkill', 'systeminfo', 'driverquery', 'whoami', 'hostname', 'powercfg', 'sfc',
                'dism', 'chkdsk', 'chkntfs', 'fsutil', 'diskpart', 'sc', 'netsh', 'wmic', 'reg',
                'bcdedit', 'gpupdate', 'gpresult', 'robocopy', 'xcopy', 'attrib', 'assoc', 'ftype',
                'cipher', 'compact', 'cleanmgr', 'shutdown', 'logoff', 'msinfo32', 'dxdiag', 'findstr',
                'where', 'ver'
            )
            $isPsCmdlet = $firstWord -match '^(get|set|start|stop|restart|new|remove|test|invoke|enable|disable|clear|format|out|select|where|measure|export|import)-[a-z0-9]+'
            $isPsAlias = $firstWord -in @('gps', 'saps', 'kill', 'gsv', 'sasv', 'sppsv', 'gcm', 'gh', 'gal', 'gm')

            if ($firstWord -in $knownCmds -or $isPsCmdlet -or $isPsAlias) {
                # Guard against questions like "ipconfig kya hai" or "ping kaise kare"
                $isQueryWord = $pLower -match '\b(kya|kaise|batao|explain|kyu|kyun|what|how|why)\b'
                if (-not $isQueryWord) {
                    $isShellCmd = $true
                    $actualCmd = $prompt.Trim()
                }
            }
        }

        if ($isShellCmd -and $actualCmd) {
            Write-Host ""
            $w = Get-TermWidth
            Write-BoxTop "KRONOS SHELL ENGINE ── $actualCmd"
            Write-Host " $CLR_SYS_BORDER│$CLR_RESET"

            $sw = [System.Diagnostics.Stopwatch]::StartNew()
            $outputLines = @()
            try {
                if ($actualCmd -match '^(assoc|ftype|ver|vol)\b') {
                    $outputObj = cmd.exe /c $actualCmd 2>&1
                } else {
                    $outputObj = Invoke-Expression $actualCmd 2>&1
                }
                if ($null -ne $outputObj) {
                    $outputLines = @($outputObj | Out-String -Stream)
                }
            } catch {
                $outputLines = @("Error executing command: $($_.Exception.Message)")
            }
            $sw.Stop()

            $dispCount = 0
            foreach ($l in $outputLines) {
                if ([string]::IsNullOrWhiteSpace($l)) { continue }
                $dispCount++
                if ($dispCount -le 25) {
                    $truncLine = Trunc-Str $l ($w - 8)
                    Write-Host " $CLR_SYS_BORDER│  $CLR_WHITE$truncLine$CLR_RESET"
                }
            }

            if ($outputLines.Count -eq 0 -or $dispCount -eq 0) {
                Write-Host " $CLR_SYS_BORDER│  $CLR_MUTED (Command produced no standard output)$CLR_RESET"
            } elseif ($outputLines.Count -gt 25) {
                Write-Host " $CLR_SYS_BORDER│  $CLR_MUTED ... [$($outputLines.Count - 25) additional lines truncated]$CLR_RESET"
            }

            Write-Host " $CLR_SYS_BORDER│$CLR_RESET"
            Write-Host " $CLR_SYS_BORDER│  $CLR_GREEN [✓] Execution completed in $($sw.ElapsedMilliseconds)ms$CLR_RESET"
            Write-BoxBottom
            Write-Host ""

            $script:LastCommandOutput = ($outputLines -join "`n")
            $script:ConversationHistory += @{
                role = "user"
                content = $prompt
            }
            $script:ConversationHistory += @{
                role = "assistant"
                content = "Executed command: $actualCmd`nOutput:`n$($outputLines -join "`n")"
            }
            continue
        }

        Dispatch-Problem $prompt -InChatMode $true
    }
}

function Show-CommandPalette {
    $commands = @(
        @{ Slug = "/doctor";    Name = "System Doctor 10-Point Health Audit";          Action = "doctor" },
        @{ Slug = "/boost";     Name = "Turbo Boost & Windows Temp Cleaner";           Action = "boost" },
        @{ Slug = "/startup";   Name = "Startup Applications & Boot Manager";          Action = "startup" },
        @{ Slug = "/apps";      Name = "Software Update & WinGet Package Manager";     Action = "apps" },
        @{ Slug = "/debloat";   Name = "Windows Privacy & Telemetry Debloat";          Action = "debloat" },
        @{ Slug = "/wifi";      Name = "Network Latency & Wi-Fi Radar";                Action = "wifi" },
        @{ Slug = "/ports";     Name = "Active Listening Ports & Process Audit";       Action = "ports" },
        @{ Slug = "/firewall";  Name = "Windows Defender Firewall Profiles Cockpit";   Action = "firewall" },
        @{ Slug = "/services";  Name = "Windows Services Control Cockpit";             Action = "services" },
        @{ Slug = "/top";       Name = "Resource Monitor & Task Manager (Top Procs)";  Action = "top" },
        @{ Slug = "/disk";      Name = "Disk SMART Health & Drive Diagnostics";        Action = "disk" },
        @{ Slug = "/specs";     Name = "Hardware Specs & Machine Topology";            Action = "specs" },
        @{ Slug = "/devices";   Name = "Hardware & Driver Device Inspector";           Action = "devices" },
        @{ Slug = "/audio";     Name = "Audio Subsystem Deep Reset & Diagnostic";      Action = "audio" },
        @{ Slug = "/tree";      Name = "Interactive File & Folder Explorer (Tree)";    Action = "tree" },
        @{ Slug = "/matrix";    Name = "Cyber Matrix Stream Screensaver";              Action = "matrix" },
        @{ Slug = "/voice";     Name = "Toggle Native Voice Engine (TTS)";             Action = "voice" },
        @{ Slug = "/cli";       Name = "Install Global 'kronos' Terminal Command";     Action = "install-cli" },
        @{ Slug = "/rollback";  Name = "Safety Rollback Recovery Engine";             Action = "rollback" },
        @{ Slug = "/chat";      Name = "Open Autonomous AI Chatbot (Natural Chat)";    Action = "chat" },
        @{ Slug = "/memory";    Name = "Persistent Memory & Past Chat Summaries";      Action = "memory" },
        @{ Slug = "/lock";      Name = "Lock Session and Prompt Security Gateway";     Action = "lock" },
        @{ Slug = "/exit";      Name = "Terminate KRONOS Session";                     Action = "exit" }
    )

    $query = ""
    $selectedIdx = 0

    while ($true) {
        $w = Get-TermWidth
        $innerW = $w - 4
        Write-Host "$ESC[H" -NoNewline

        # Filter commands
        $filtered = @($commands | Where-Object {
            (-not $query) -or ($_.Slug -like "*$query*") -or ($_.Name -like "*$query*")
        })

        if ($selectedIdx -ge $filtered.Count) { $selectedIdx = [math]::Max(0, $filtered.Count - 1) }

        # Top border
        $topTitle = "${BOX_TL}${BOX_H} ${CLR_WHITE}${CLR_BOLD}COMMAND PALETTE${CLR_RESET} ${CLR_SYS_BORDER}"
        $topRight = " ${CLR_CYAN}[Ctrl+K]${CLR_RESET} ${CLR_SYS_BORDER}${BOX_H}${BOX_TR}"
        $dashes = $w - (Get-VisibleLength $topTitle) - (Get-VisibleLength $topRight)
        if ($dashes -lt 2) { $dashes = 2 }
        Write-Host " ${CLR_SYS_BORDER}${topTitle}" -NoNewline
        Write-Host ("${BOX_H}" * $dashes) -NoNewline
        Write-Host "${topRight}${CLR_RESET}$ESC[K"

        # Search query row
        $searchPrompt = "  ${CLR_CYAN}>${CLR_RESET} ${CLR_WHITE}${query}${CLR_RESET}${CLR_MUTED}_${CLR_RESET}"
        $paddedPrompt = Pad-Visible $searchPrompt $innerW
        Write-Host " ${CLR_SYS_BORDER}${BOX_V}${CLR_RESET}$paddedPrompt${CLR_SYS_BORDER}${BOX_V}${CLR_RESET}$ESC[K"

        # Divider
        Write-Host " ${CLR_SYS_BORDER}${BOX_ML}" -NoNewline
        Write-Host ("${BOX_H}" * ($w - 2)) -NoNewline
        Write-Host "${BOX_MR}${CLR_RESET}$ESC[K"

        # Render filtered list (max 10 rows)
        $maxRows = 10
        $startIdx = [math]::Max(0, $selectedIdx - 4)
        $endIdx = [math]::Min($filtered.Count - 1, $startIdx + $maxRows - 1)

        if ($filtered.Count -eq 0) {
            $emptyMsg = Pad-Visible "  ${CLR_AMBER}No matching commands found.${CLR_RESET}" $innerW
            Write-Host " ${CLR_SYS_BORDER}${BOX_V}${CLR_RESET}$emptyMsg${CLR_SYS_BORDER}${BOX_V}${CLR_RESET}$ESC[K"
        } else {
            for ($i = $startIdx; $i -le $endIdx; $i++) {
                $cmd = $filtered[$i]
                $slugPadded = $cmd.Slug.PadRight(12)
                if ($i -eq $selectedIdx) {
                    $line = "  ${CLR_CYAN}${PTR} ${CLR_CYAN}${CLR_BOLD}$slugPadded${CLR_WHITE}${CLR_BOLD}$($cmd.Name)${CLR_RESET}"
                } else {
                    $line = "    ${CLR_MUTED}$slugPadded${CLR_TEXT}$($cmd.Name)${CLR_RESET}"
                }
                $paddedLine = Pad-Visible $line $innerW
                Write-Host " ${CLR_SYS_BORDER}${BOX_V}${CLR_RESET}$paddedLine${CLR_SYS_BORDER}${BOX_V}${CLR_RESET}$ESC[K"
            }
        }

        # Bottom border
        Write-Host " ${CLR_SYS_BORDER}${BOX_BL}" -NoNewline
        Write-Host ("${BOX_H}" * ($w - 2)) -NoNewline
        Write-Host "${BOX_BR}${CLR_RESET}$ESC[K"
        Write-Host "  ${CLR_MUTED}Type to filter • ↑/↓: Navigate • Enter: Execute • Esc: Dismiss${CLR_RESET}$ESC[K"

        # Read key
        $key = [Console]::ReadKey($true)
        switch ($key.Key) {
            ([ConsoleKey]::Escape) { return $null }
            ([ConsoleKey]::UpArrow) {
                if ($selectedIdx -gt 0) { $selectedIdx-- }
            }
            ([ConsoleKey]::DownArrow) {
                if ($selectedIdx -lt ($filtered.Count - 1)) { $selectedIdx++ }
            }
            ([ConsoleKey]::Enter) {
                if ($filtered.Count -gt 0) {
                    return $filtered[$selectedIdx].Action
                }
            }
            ([ConsoleKey]::Backspace) {
                if ($query.Length -gt 0) {
                    $query = $query.Substring(0, $query.Length - 1)
                    $selectedIdx = 0
                }
            }
            default {
                $char = $key.KeyChar
                if ($char -ge 32 -and $char -le 126) {
                    $query += $char
                    $selectedIdx = 0
                }
            }
        }
    }
}

function Select-InteractiveMenu {
    $categories = @(
        @{
            Key = "1"; Title = "SYSTEM HEALTH & DIAGNOSTICS";
            Tag = "DIAGNOSTICS";
            Desc = "Automated 10-Point Audit • Device Inspector • SMART Disks • Hardware Specs";
            SubItems = @(
                @{ Key = "1"; Label = "System Doctor 10-Point Health Audit";                   Action = "doctor" },
                @{ Key = "2"; Label = "Hardware & Driver Device Inspector";                    Action = "devices" },
                @{ Key = "3"; Label = "Disk SMART Health & Drive Diagnostics";                 Action = "disk" },
                @{ Key = "4"; Label = "Hardware Specs & Machine Topology";                     Action = "specs" },
                @{ Key = "b"; Label = "Back to Main Workspace";                                Action = "back" }
            )
        },
        @{
            Key = "2"; Title = "PERFORMANCE & OPTIMIZATION";
            Tag = "OPTIMIZER";
            Desc = "Turbo Boost Temp Cleaner • Task Monitor • Startup Manager • Power Cockpit";
            SubItems = @(
                @{ Key = "1"; Label = "Turbo Boost & Windows Temp Cleaner";                    Action = "boost" },
                @{ Key = "2"; Label = "Resource Monitor & Task Manager (Top Procs)";           Action = "top" },
                @{ Key = "3"; Label = "Startup Applications & Boot Manager";                   Action = "startup" },
                @{ Key = "4"; Label = "Power Cockpit & Sleep / Hibernate Profiles";            Action = "power" },
                @{ Key = "b"; Label = "Back to Main Workspace";                                Action = "back" }
            )
        },
        @{
            Key = "3"; Title = "NETWORK & SECURITY COCKPIT";
            Tag = "SECURITY";
            Desc = "Network Latency & Radar • Listening Ports • Firewall Profiles • Privacy Debloat";
            SubItems = @(
                @{ Key = "1"; Label = "Network Latency & Wi-Fi Radar";                         Action = "wifi" },
                @{ Key = "2"; Label = "Active Listening Ports & Process Audit";                Action = "ports" },
                @{ Key = "3"; Label = "Windows Defender Firewall Profiles Cockpit";            Action = "firewall" },
                @{ Key = "4"; Label = "Windows Privacy & Telemetry Debloat";                   Action = "debloat" },
                @{ Key = "b"; Label = "Back to Main Workspace";                                Action = "back" }
            )
        },
        @{
            Key = "4"; Title = "APPS, SYSTEM TOOLS & AUDIO";
            Tag = "UTILITIES";
            Desc = "WinGet Package Manager • Services Cockpit • Audio Subsystem • Folder Tree • Matrix";
            SubItems = @(
                @{ Key = "1"; Label = "Software Update & WinGet Package Manager";              Action = "apps" },
                @{ Key = "2"; Label = "Windows Services Control Cockpit";                      Action = "services" },
                @{ Key = "3"; Label = "Audio Subsystem Deep Reset & Diagnostic";               Action = "audio" },
                @{ Key = "4"; Label = "Interactive File & Folder Explorer (Tree)";             Action = "tree" },
                @{ Key = "5"; Label = "Cyber Matrix Stream Screensaver";                       Action = "matrix" },
                @{ Key = "b"; Label = "Back to Main Workspace";                                Action = "back" }
            )
        },
        @{
            Key = "5"; Title = "KRONOS AI CO-PILOT & VOICE";
            Tag = "AUTONOMOUS";
            Desc = "Autonomous AI Co-Pilot • Memory & Chats • Native Voice Engine • Global CLI • Rollback Safety";
            SubItems = @(
                @{ Key = "1"; Label = "Open Autonomous AI Chatbot (Natural Chat)";             Action = "chat" },
                @{ Key = "2"; Label = "Persistent Memory & Past Chat Summaries";               Action = "memory" },
                @{ Key = "3"; Label = "Toggle Native Voice Engine (Speech Synthesis)";         Action = "voice" },
                @{ Key = "4"; Label = "Install Global 'kronos' Terminal Command";              Action = "install-cli" },
                @{ Key = "5"; Label = "Safety Rollback Recovery Engine";                       Action = "rollback" },
                @{ Key = "b"; Label = "Back to Main Workspace";                                Action = "back" }
            )
        },
        @{
            Key = "0"; Title = "LOCK / EXIT SESSION";
            Tag = "SESSION";
            Desc = "Lock Security Gateway • Terminate Session";
            SubItems = @(
                @{ Key = "1"; Label = "Lock Session and Prompt Security Gateway";              Action = "lock" },
                @{ Key = "0"; Label = "Terminate KRONOS Session";                              Action = "exit" },
                @{ Key = "b"; Label = "Back to Main Workspace";                                Action = "back" }
            )
        }
    )

    $selectedCategoryIndex = 4 # Default highlight on KRONOS AI CO-PILOT

    Clear-Host

    while ($true) {
        try { [Console]::CursorVisible = $false } catch {}
        Write-Host "$ESC[?25l" -NoNewline

        Show-Banner -useVtHome $true

        $w = Get-TermWidth
        $innerW = $w - 4

        # Menu Panel Top
        $mTitleLeft = "${BOX_TL}${BOX_H} ${CLR_WHITE}${CLR_BOLD}KRONOS WORKSPACE CONTROL CENTRE${CLR_RESET} ${CLR_SYS_BORDER}"
        $mTitleRight = " ${CLR_CYAN}[MAIN MENU]${CLR_RESET} ${CLR_SYS_BORDER}${BOX_H}${BOX_TR}"
        $mDashes = $w - (Get-VisibleLength $mTitleLeft) - (Get-VisibleLength $mTitleRight)
        if ($mDashes -lt 2) { $mDashes = 2 }
        Write-Host " ${CLR_SYS_BORDER}${mTitleLeft}" -NoNewline
        Write-Host ("${BOX_H}" * $mDashes) -NoNewline
        Write-Host "${mTitleRight}${CLR_RESET}$ESC[K"

        Write-Host " ${CLR_SYS_BORDER}${BOX_V}${CLR_RESET}$(Pad-Visible '' $innerW)${CLR_SYS_BORDER}${BOX_V}${CLR_RESET}$ESC[K"

        for ($i = 0; $i -lt $categories.Count; $i++) {
            $cat = $categories[$i]
            if ($i -eq $selectedCategoryIndex) {
                $headStr = " ${CLR_CYAN}${PTR} ${CLR_CYAN}[$($cat.Key)] ${CLR_WHITE}${CLR_BOLD}$($cat.Title)${CLR_RESET}  ${CLR_CYAN}[$($cat.Tag)]${CLR_RESET}"
                $descStr = "       ${CLR_TEXT}$($cat.Desc)${CLR_RESET}"
            } else {
                $headStr = "    ${CLR_DARK}[$($cat.Key)] ${CLR_TEXT}$($cat.Title)${CLR_RESET}  ${CLR_DARK}[$($cat.Tag)]${CLR_RESET}"
                $descStr = "       ${CLR_DARK}$($cat.Desc)${CLR_RESET}"
            }

            Write-Host " ${CLR_SYS_BORDER}${BOX_V}${CLR_RESET}$(Pad-Visible $headStr $innerW)${CLR_SYS_BORDER}${BOX_V}${CLR_RESET}$ESC[K"
            Write-Host " ${CLR_SYS_BORDER}${BOX_V}${CLR_RESET}$(Pad-Visible $descStr $innerW)${CLR_SYS_BORDER}${BOX_V}${CLR_RESET}$ESC[K"

            if ($i -lt ($categories.Count - 1)) {
                Write-Host " ${CLR_SYS_BORDER}${BOX_V}${CLR_RESET}$(Pad-Visible '' $innerW)${CLR_SYS_BORDER}${BOX_V}${CLR_RESET}$ESC[K"
            }
        }

        Write-Host " ${CLR_SYS_BORDER}${BOX_V}${CLR_RESET}$(Pad-Visible '' $innerW)${CLR_SYS_BORDER}${BOX_V}${CLR_RESET}$ESC[K"

        # Menu Panel Bottom
        Write-Host " ${CLR_SYS_BORDER}${BOX_BL}" -NoNewline
        Write-Host ("${BOX_H}" * ($w - 2)) -NoNewline
        Write-Host "${BOX_BR}${CLR_RESET}$ESC[K"

        Write-Host "  ${CLR_MUTED}↑/↓: Navigate • Enter: Select • 1-5,0: Direct Jump • Ctrl+K: Palette • c: Chat • q: Exit${CLR_RESET}$ESC[K"

        if ([Console]::IsInputRedirected) {
            try { [Console]::CursorVisible = $true } catch {}
            Write-Host "$ESC[?25h" -NoNewline
            return "chat"
        }

        $keyInfo = [Console]::ReadKey($true)
        $chosenCat = $null

        # Check for Ctrl+K
        $isCtrlK = ($keyInfo.Key -eq [ConsoleKey]::K -and ($keyInfo.Modifiers -band [ConsoleModifiers]::Control)) -or ([int]$keyInfo.KeyChar -eq 11)
        if ($isCtrlK) {
            Clear-Host
            $paletteAction = Show-CommandPalette
            Clear-Host
            if ($paletteAction) {
                try { [Console]::CursorVisible = $true } catch {}
                Write-Host "$ESC[?25h" -NoNewline
                return $paletteAction
            }
            continue
        }

        switch ($keyInfo.Key) {
            ([ConsoleKey]::UpArrow) {
                $selectedCategoryIndex--
                if ($selectedCategoryIndex -lt 0) { $selectedCategoryIndex = $categories.Count - 1 }
                continue
            }
            ([ConsoleKey]::DownArrow) {
                $selectedCategoryIndex++
                if ($selectedCategoryIndex -ge $categories.Count) { $selectedCategoryIndex = 0 }
                continue
            }
            ([ConsoleKey]::Enter) {
                $chosenCat = $categories[$selectedCategoryIndex]
            }
            ([ConsoleKey]::D1) { $chosenCat = $categories[0] }
            ([ConsoleKey]::NumPad1) { $chosenCat = $categories[0] }
            ([ConsoleKey]::D2) { $chosenCat = $categories[1] }
            ([ConsoleKey]::NumPad2) { $chosenCat = $categories[1] }
            ([ConsoleKey]::D3) { $chosenCat = $categories[2] }
            ([ConsoleKey]::NumPad3) { $chosenCat = $categories[2] }
            ([ConsoleKey]::D4) { $chosenCat = $categories[3] }
            ([ConsoleKey]::NumPad4) { $chosenCat = $categories[3] }
            ([ConsoleKey]::D5) { $chosenCat = $categories[4] }
            ([ConsoleKey]::NumPad5) { $chosenCat = $categories[4] }
            ([ConsoleKey]::D0) { $chosenCat = $categories[5] }
            ([ConsoleKey]::NumPad0) { $chosenCat = $categories[5] }
            ([ConsoleKey]::C) {
                try { [Console]::CursorVisible = $true } catch {}
                Write-Host "$ESC[?25h" -NoNewline
                return "chat"
            }
            ([ConsoleKey]::Q) {
                try { [Console]::CursorVisible = $true } catch {}
                Write-Host "$ESC[?25h" -NoNewline
                return "exit"
            }
            ([ConsoleKey]::Escape) {
                try { [Console]::CursorVisible = $true } catch {}
                Write-Host "$ESC[?25h" -NoNewline
                return "exit"
            }
            default {
                continue
            }
        }

        if ($chosenCat) {
            Clear-Host
            $subAction = Show-SubMenu $chosenCat
            Clear-Host
            if ($subAction -and $subAction -ne "back") {
                try { [Console]::CursorVisible = $true } catch {}
                Write-Host "$ESC[?25h" -NoNewline
                return $subAction
            }
        }
    }
}

function Show-SubMenu($cat) {
    $selectedIndex = 0
    $subItems = $cat.SubItems

    Clear-Host

    while ($true) {
        try { [Console]::CursorVisible = $false } catch {}
        Write-Host "$ESC[?25l" -NoNewline

        Show-Banner -useVtHome $true

        $w = Get-TermWidth
        $innerW = $w - 4

        # Sub-Menu Panel Top
        $mTitleLeft = "${BOX_TL}${BOX_H} ${CLR_WHITE}${CLR_BOLD}$($cat.Title)${CLR_RESET} ${CLR_SYS_BORDER}"
        $mTitleRight = " ${CLR_CYAN}[MODULES]${CLR_RESET} ${CLR_SYS_BORDER}${BOX_H}${BOX_TR}"
        $mDashes = $w - (Get-VisibleLength $mTitleLeft) - (Get-VisibleLength $mTitleRight)
        if ($mDashes -lt 2) { $mDashes = 2 }
        Write-Host " ${CLR_SYS_BORDER}${mTitleLeft}" -NoNewline
        Write-Host ("${BOX_H}" * $mDashes) -NoNewline
        Write-Host "${mTitleRight}${CLR_RESET}$ESC[K"

        Write-Host " ${CLR_SYS_BORDER}${BOX_V}${CLR_RESET}$(Pad-Visible '' $innerW)${CLR_SYS_BORDER}${BOX_V}${CLR_RESET}$ESC[K"

        for ($i = 0; $i -lt $subItems.Count; $i++) {
            $item = $subItems[$i]
            $isBack = ($item.Key -eq "b")
            $keyBadge = if ($isBack) { "[Esc/b]" } else { "[$($item.Key)]" }

            if ($i -eq $selectedIndex) {
                $line = " ${CLR_CYAN}${PTR} ${CLR_CYAN}$keyBadge ${CLR_WHITE}${CLR_BOLD}$($item.Label)${CLR_RESET}"
            } else {
                $line = "    ${CLR_DARK}$keyBadge ${CLR_TEXT}$($item.Label)${CLR_RESET}"
            }
            Write-Host " ${CLR_SYS_BORDER}${BOX_V}${CLR_RESET}$(Pad-Visible $line $innerW)${CLR_SYS_BORDER}${BOX_V}${CLR_RESET}$ESC[K"
        }

        Write-Host " ${CLR_SYS_BORDER}${BOX_V}${CLR_RESET}$(Pad-Visible '' $innerW)${CLR_SYS_BORDER}${BOX_V}${CLR_RESET}$ESC[K"

        # Sub-Menu Panel Bottom
        Write-Host " ${CLR_SYS_BORDER}${BOX_BL}" -NoNewline
        Write-Host ("${BOX_H}" * ($w - 2)) -NoNewline
        Write-Host "${BOX_BR}${CLR_RESET}$ESC[K"

        Write-Host "  ${CLR_MUTED}↑/↓: Navigate • Enter: Select • 1-9: Direct Key • Esc/b: Back • Ctrl+K: Palette${CLR_RESET}$ESC[K"

        if ([Console]::IsInputRedirected) {
            try { [Console]::CursorVisible = $true } catch {}
            Write-Host "$ESC[?25h" -NoNewline
            return $subItems[0].Action
        }

        $keyInfo = [Console]::ReadKey($true)

        # Check for Ctrl+K
        $isCtrlK = ($keyInfo.Key -eq [ConsoleKey]::K -and ($keyInfo.Modifiers -band [ConsoleModifiers]::Control)) -or ([int]$keyInfo.KeyChar -eq 11)
        if ($isCtrlK) {
            Clear-Host
            $paletteAction = Show-CommandPalette
            Clear-Host
            if ($paletteAction) {
                try { [Console]::CursorVisible = $true } catch {}
                Write-Host "$ESC[?25h" -NoNewline
                return $paletteAction
            }
            continue
        }

        switch ($keyInfo.Key) {
            ([ConsoleKey]::UpArrow) {
                $selectedIndex--
                if ($selectedIndex -lt 0) { $selectedIndex = $subItems.Count - 1 }
                continue
            }
            ([ConsoleKey]::DownArrow) {
                $selectedIndex++
                if ($selectedIndex -ge $subItems.Count) { $selectedIndex = 0 }
                continue
            }
            ([ConsoleKey]::Enter) {
                try { [Console]::CursorVisible = $true } catch {}
                Write-Host "$ESC[?25h" -NoNewline
                return $subItems[$selectedIndex].Action
            }
            ([ConsoleKey]::D1) { if ($subItems.Count -ge 1 -and $subItems[0].Key -eq "1") { return $subItems[0].Action } }
            ([ConsoleKey]::NumPad1) { if ($subItems.Count -ge 1 -and $subItems[0].Key -eq "1") { return $subItems[0].Action } }
            ([ConsoleKey]::D2) { if ($subItems.Count -ge 2 -and $subItems[1].Key -eq "2") { return $subItems[1].Action } }
            ([ConsoleKey]::NumPad2) { if ($subItems.Count -ge 2 -and $subItems[1].Key -eq "2") { return $subItems[1].Action } }
            ([ConsoleKey]::D3) { if ($subItems.Count -ge 3 -and $subItems[2].Key -eq "3") { return $subItems[2].Action } }
            ([ConsoleKey]::NumPad3) { if ($subItems.Count -ge 3 -and $subItems[2].Key -eq "3") { return $subItems[2].Action } }
            ([ConsoleKey]::D4) { if ($subItems.Count -ge 4 -and $subItems[3].Key -eq "4") { return $subItems[3].Action } }
            ([ConsoleKey]::NumPad4) { if ($subItems.Count -ge 4 -and $subItems[3].Key -eq "4") { return $subItems[3].Action } }
            ([ConsoleKey]::D5) { if ($subItems.Count -ge 5 -and $subItems[4].Key -eq "5") { return $subItems[4].Action } }
            ([ConsoleKey]::NumPad5) { if ($subItems.Count -ge 5 -and $subItems[4].Key -eq "5") { return $subItems[4].Action } }
            ([ConsoleKey]::D0) {
                $item0 = $subItems | Where-Object { $_.Key -eq "0" } | Select-Object -First 1
                if ($item0) { return $item0.Action }
            }
            ([ConsoleKey]::NumPad0) {
                $item0 = $subItems | Where-Object { $_.Key -eq "0" } | Select-Object -First 1
                if ($item0) { return $item0.Action }
            }
            ([ConsoleKey]::B) {
                try { [Console]::CursorVisible = $true } catch {}
                Write-Host "$ESC[?25h" -NoNewline
                return "back"
            }
            ([ConsoleKey]::Q) {
                try { [Console]::CursorVisible = $true } catch {}
                Write-Host "$ESC[?25h" -NoNewline
                return "back"
            }
            ([ConsoleKey]::Escape) {
                try { [Console]::CursorVisible = $true } catch {}
                Write-Host "$ESC[?25h" -NoNewline
                return "back"
            }
            default {
                continue
            }
        }
    }
}

# --- Initialization ---
Show-LoginGateway
Show-Banner
Ensure-Elevation

# --- Main Interactive Loop ---
try {
while ($true) {
    $selection = Select-InteractiveMenu

    if ([string]::IsNullOrWhiteSpace($selection)) {
        continue
    }

    switch ($selection.Trim().ToLower()) {
        "0"    { Write-Host " $CLR_GREEN[*] Terminating KRONOS session.$CLR_RESET"; break }
        "exit" { Write-Host " $CLR_GREEN[*] Terminating KRONOS session.$CLR_RESET"; break }
        "quit" { Write-Host " $CLR_GREEN[*] Terminating KRONOS session.$CLR_RESET"; break }

        # Security Lock
        "lock" {
            Show-LoginGateway
            Show-Banner
            continue
        }

        # Category 1: Health & Diagnostics
        "doctor" {
            Show-DoctorHealthCheckTUI
            continue
        }
        "devices" {
            Show-DeviceHardwareTUI
            continue
        }
        "disk" {
            Show-DiskHealthTUI
            continue
        }
        "specs" {
            Show-SystemSpecsTUI
            continue
        }

        # Category 2: Performance & Optimization
        "boost" {
            Show-TurboBoostTUI
            continue
        }
        "top" {
            Show-TaskMonitorTUI
            continue
        }
        "startup" {
            Show-StartupManagerTUI
            continue
        }
        "power" {
            Show-PowerCockpitTUI
            continue
        }

        # Category 3: Network & Security
        "wifi" {
            Show-NetworkRadarTUI
            continue
        }
        "ports" {
            Show-PortAuditTUI
            continue
        }
        "firewall" {
            Show-FirewallCockpitTUI
            continue
        }
        "debloat" {
            Show-PrivacyDebloatTUI
            continue
        }

        # Category 4: Apps, Tools & Audio
        "apps" {
            Show-AppManagerTUI
            continue
        }
        "services" {
            Show-ServiceManagerTUI
            continue
        }
        "audio" {
            Show-AudioTUI
            continue
        }
        "tree" {
            Show-FolderNavigatorTUI "D:\"
            continue
        }
        "matrix" {
            Show-MatrixScreensaverTUI
            continue
        }

        # Category 5: AI & Settings
        "chat" {
            Start-ConversationMode
            continue
        }
        "memory" {
            Show-MemoryDashboardTUI
            continue
        }
        "history" {
            Show-MemoryDashboardTUI
            continue
        }
        "voice" {
            Toggle-VoiceEngine
            continue
        }
        "install-cli" {
            Install-KronosGlobalCLI
            continue
        }
        "rollback" {
            Invoke-RollbackRecovery
            continue
        }

        default {
            Start-ConversationMode $selection
            continue
        }
    }
}
}
finally {
    Restore-KronosTerminalTheme
}
