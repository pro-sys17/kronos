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
        r"\bna\b": "nahi",
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
    def resolve_pronoun_reference(cls, text: str, history: Optional[List[Dict[str, Any]]] = None) -> Tuple[str, Optional[str]]:
        """
        Resolves pronouns like 'ise', 'isko', 'use', 'it', 'this' based on recent conversation history.
        Example:
          User: 'Mera audio band ho gaya'
          Next: 'Ab ise fix karo' -> returns ('Ab audio fix karo', 'audio')
        """
        norm = cls.normalize_text(text)
        has_pronoun = bool(re.search(r'\b(ise|isko|isey|use|usko|it|this|that|problem|issue)\b', norm))

        if not has_pronoun or not history:
            return text, cls.detect_domain(text)

        # Look back through recent history for previous domain
        last_domain = None
        for turn in reversed(history[-6:]):
            content = turn.get("content", "")
            found_domain = cls.detect_domain(content)
            if found_domain:
                last_domain = found_domain
                break

        if last_domain:
            # Augment text with the inferred domain context
            augmented_text = f"{text} (context: {last_domain})"
            return augmented_text, last_domain

        return text, cls.detect_domain(text)
