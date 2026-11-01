"""
KRONOS Hinglish & English Semantic Normalizer
Handles bilingual terminology, colloquial phrasing, phonetic spelling variants, and pronoun resolution.
"""

from typing import Dict, Any, List, Optional, Tuple
import re

class HinglishProcessor:
    """
    Normalizes colloquial Hinglish terms into standardized semantic tokens.
    """

    # Common Hinglish phonetic spelling maps
    PHONETIC_MAP = {
        r"\bnahi\b": "nahi",
        r"\bnhi\b": "nahi",
        r"\bnh\b": "nahi",
        r"\bni\b": "nahi",
        r"\bhai\b": "hai",
        r"\bhe\b": "hai",
        r"\bh\b": "hai",
        r"\bkaro\b": "karo",
        r"\bkrdo\b": "karo",
        r"\bkar do\b": "karo",
        r"\bkr\b": "karo",
        r"\bkijiye\b": "karo",
        r"\bdekho\b": "dekho",
        r"\bdikhao\b": "dekho",
        r"\bbtayo\b": "batao",
        r"\bbatao\b": "batao",
        r"\bise\b": "ise",
        r"\bisko\b": "ise",
        r"\bisey\b": "ise",
        r"\busko\b": "use",
        r"\busey\b": "use",
        r"\bband\b": "band",
        r"\bchalu\b": "chalu",
        r"\bchal raha\b": "running",
        r"\bchalta\b": "running",
        r"\bkaam nahi kar raha\b": "not_working",
        r"\bchal nahi raha\b": "not_working"
    }

    # Intent domain keywords (bilingual)
    DOMAIN_KEYWORDS = {
        "network": [
            "internet", "wifi", "wi-fi", "net", "network", "ping", "dns", "adapter",
            "disconnect", "slow net", "packet loss", "ip", "gateway", "dhcp",
            "net slow hai", "net nahi chal raha", "wifi connect nahi ho raha", "router"
        ],
        "audio": [
            "audio", "sound", "speaker", "volume", "mic", "microphone", "headphone",
            "earphone", "aawaz", "awaaz", "sound nahi aa rahi", "aawaz nahi aa rahi",
            "speaker band hai", "sound crackle", "audio mute"
        ],
        "media": [
            "spotify", "youtube", "music", "song", "gaana", "gana", "play", "track",
            "album", "artist", "pause", "resume", "chalao", "bajaao", "bajana", "chala do",
            "song play", "gana play"
        ],
        "software": [
            "git", "github", "clone", "repo", "repository", "install", "pip", "npm",
            "cli", "tool", "zip", "extract", "setup", "download", "go build", "build",
            "compile", "package", "wheel", "tar", "tar.gz"
        ],
        "browser": [
            "chrome", "edge", "firefox", "browser", "open link", "website", "url",
            "tab", "pornhub", "reddit", "netflix", "google", "web"
        ],
        "performance": [
            "slow", "lag", "hang", "freeze", "cpu", "ram", "memory", "100%", "stuck",
            "laptop garam", "overheating", "fan", "speed up", "task manager", "heavy",
            "bohot slow chal raha", "hang ho raha hai"
        ],
        "storage": [
            "disk", "storage", "drive", "c drive", "space", "full", "cleanup", "temp",
            "junk", "delete", "free space", "space khali karo", "disk bhar gaya"
        ],
        "security": [
            "firewall", "defender", "virus", "antivirus", "malware", "scan", "port",
            "listening ports", "security", "blocked", "ports check karo"
        ],
        "service": [
            "service", "services", "daemon", "background", "audiocore", "wuauserv",
            "spooler", "print service", "service restart karo"
        ]
    }

    @classmethod
    def normalize_text(cls, text: str) -> str:
        """
        Cleans and standardizes punctuation, lowercase, and phonetic spellings.
        """
        t = text.lower().strip()
        t = re.sub(r'[\r\n\t]', ' ', t)
        t = re.sub(r'[!?,.:;"]', ' ', t)
        t = re.sub(r'\s+', ' ', t).strip()

        # Remove trailing imperative/request particles "na" (e.g. "karo na", "dikhao na", "batao na", "show karo na")
        t = re.sub(r'\b(karo|dikhao|batao|do|kijiye|show|print|bhejo|bolo|likho)\s+na\b', r'\1', t)
        # Normalize negative pre-verb "na" (e.g. "na ho", "na chal raha", "na karo") to "nahi"
        t = re.sub(r'\bna\s+(karo|hoga|hai|chal|de|le|kar|chalta|ho|chalra)\b', r'nahi \1', t)

        for pattern, replacement in cls.PHONETIC_MAP.items():
            t = re.sub(pattern, replacement, t)
        return t

    @classmethod
    def detect_domain(cls, text: str) -> Optional[str]:
        norm = cls.normalize_text(text)
        for domain, keywords in cls.DOMAIN_KEYWORDS.items():
            for kw in keywords:
                if kw in norm:
                    return domain
        return None

    @classmethod
    def extract_recent_entity(cls, history: Optional[List[Dict[str, Any]]]) -> Optional[str]:
        """
        Extracts recent specific named entities (GitHub repo name, software name, or URL)
        from recent conversation history turns.
        """
        if not history:
            return None

        for turn in reversed(history[-6:]):
            content = turn.get("content", "")
            # Check for GitHub repo URL: https://github.com/user/repo(.git)?
            gh_match = re.search(r'github\.com/[^/\s]+/([^/\s\.]+)(?:\.git)?', content, re.IGNORECASE)
            if gh_match:
                return gh_match.group(1).strip()

            # Check for explicit tool or software names
            tool_match = re.search(r'\b(spotify-cli|spotify_cli|spotify|chrome|vlc|discord|vscode|code)\b', content, re.IGNORECASE)
            if tool_match:
                return tool_match.group(1).strip()

            # Check for directory paths like C:\Temp\... or C:\Users\...
            path_match = re.search(r'([a-zA-Z]:\\[^\s"\'<>|]+)', content)
            if path_match:
                return path_match.group(1).strip()

        return None

    @classmethod
    def resolve_pronoun_reference(cls, text: str, history: Optional[List[Dict[str, Any]]] = None) -> Tuple[str, Optional[str]]:
        """
        Resolves pronouns like 'ise', 'isko', 'use', 'it', 'this' as well as follow-up queries
        like 'hogai kya', 'kaha he cmds', 'use kese kre' based on recent conversation history.
        """
        norm = cls.normalize_text(text)
        has_pronoun = bool(re.search(r'\b(ise|isko|isey|use|usko|it|this|that|problem|issue)\b', norm))
        is_follow_up = bool(re.search(r'\b(hogai\s+kya|ho\s+gaya\s+kya|ho\s+gya\s+kya|hua\s+kya|kya\s+hua|kaha\s+he|kaha\s+hai|cmds\s+batao|commands\s+batao|how\s+to\s+use|use\s+kese\s+kre|kaise\s+use\s+kare|run\s+it|show\s+nahi\s+ho\s+rahe)\b', norm))

        recent_entity = cls.extract_recent_entity(history) if history else None

        if not (has_pronoun or is_follow_up) or not history:
            detected = cls.detect_domain(text)
            return text, detected

        # Look back through recent history for previous domain
        last_domain = None
        for turn in reversed(history[-6:]):
            content = turn.get("content", "")
            found_domain = cls.detect_domain(content)
            if found_domain:
                last_domain = found_domain
                break

        # Context augmentation
        context_parts = []
        if recent_entity:
            context_parts.append(f"entity: {recent_entity}")
        if last_domain:
            context_parts.append(f"domain: {last_domain}")

        if context_parts:
            augmented_text = f"{text} (context: {', '.join(context_parts)})"
            return augmented_text, (last_domain or "software")

        return text, cls.detect_domain(text)
