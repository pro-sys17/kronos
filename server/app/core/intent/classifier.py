"""
KRONOS Intent Classification Engine
Classifies user queries into semantic operational intents across English & Hinglish.
"""

from typing import Dict, Any, List, Optional
from enum import Enum
import re
from .hinglish import HinglishProcessor

class IntentType(str, Enum):
    GREETING_CHITCHAT = "GREETING_CHITCHAT"
    TECHNICAL_EXPLANATION = "TECHNICAL_EXPLANATION"
    SYSTEM_INFO_REQUEST = "SYSTEM_INFO_REQUEST"
    TROUBLESHOOTING_REQUEST = "TROUBLESHOOTING_REQUEST"
    ACTION_REQUEST = "ACTION_REQUEST"
    FOLLOW_UP_REQUEST = "FOLLOW_UP_REQUEST"
    AMBIGUOUS_QUERY = "AMBIGUOUS_QUERY"
    CONFIRMATION = "CONFIRMATION"
    CANCELLATION = "CANCELLATION"

class IntentResult:
    def __init__(self, intent: IntentType, confidence: float, domain: Optional[str] = None, normalized_query: str = "", context_inferred: Optional[str] = None):
        self.intent = intent
        self.confidence = confidence
        self.domain = domain
        self.normalized_query = normalized_query
        self.context_inferred = context_inferred

    def to_dict(self) -> Dict[str, Any]:
        return {
            "intent": self.intent.value,
            "confidence": self.confidence,
            "domain": self.domain,
            "normalized_query": self.normalized_query,
            "context_inferred": self.context_inferred
        }

class IntentClassifier:
    """
    Rule-guided and semantic intent classifier.
    """

    CANCELLATION_PATTERNS = [
        r"^(nahi|no|nope|cancel|abort|mat karo|don't|dont|stop)(\s+(karo|mat karo|bhai|it))?$",
        r"\b(rehne do|rehne de|kuch mat karo|kuch mat kr|chhod do|chhod de|cancel it|stop nothing to do)\b"
    ]

    CONFIRMATION_PATTERNS = [
        r"^(haan|haanji|yes|yep|sure|proceed|do it|karo|kar do|bilkul|approve)(\s+(kar do|karo|please|bhai))?$"
    ]

    AMBIGUOUS_PATTERNS = [
        r"^(problem|dikkat|issue|error|help|kharab hai)$",
        r"\b(kuch\s+(to\s+)?(problem|dikkat|garbar|issue|kharabi)|something is wrong|system issue|help me|kuch karo|dekho na|please help)\b"
    ]

    CHITCHAT_PATTERNS = [
        r"\b(hi|hello|hey|namaste|pranam|halo|hola)\b",
        r"\b(good\s+(morning|evening|afternoon|night))\b",
        r"\b(kya haal|kaise ho|kaisa hai|how are you|wassup|sup)\b",
        r"\b(ok|okay|theek hai|thik hai|theek he|thik he|sahi hai|badhiya|cool|nice)\b",
        r"\b(mene kab bola|maine kab bola|mene to kuch nahi kaha|chill karo|chill marte|chill)\b",
        r"\b(thanks|thank you|dhanyawad|shukriya|arigato)\b"
    ]

    EXPLANATION_PATTERNS = [
        r"\b(kya hai|kya hota hai|kya hoti hai|explain karo|batao kya hai|what is|how does|why does|difference between)\b",
        r"\b(kaise kaam karta hai|ka matlab kya hai|meaning of|kise kehte hai)\b",
        r"^(what is|how does|why is|explain)\b"
    ]

    SYSTEM_INFO_PATTERNS = [
        r"\b(specs|specifications|pc details|laptop details|system details|system info|hardware details|device details)\b",
        r"\b(ram kitni|processor kaunsa|os version|build number|cpu details|ip address|my ip|battery health|battery report)\b",
        r"\b(kitna space hai|storage kitni bachi|free space|battery percentage)\b",
        r"^(systeminfo|fastfetch|specs|battery report)\b"
    ]

    ACTION_PATTERNS = [
        r"\b(flush karo|restart karo|clean karo|clear karo|delete karo|kill karo|close karo|stop karo)\b",
        r"\b(turn on|turn off|enable karo|disable karo|chalu karo|band karo|reset karo)\b",
        r"^(flush|restart|kill|stop|start|clean|clear|enable|disable)\s+"
    ]

    FOLLOW_UP_PATTERNS = [
        r"\b(ab |aur |fir |then |now |next )?\b(ise|isko|isey|use|usko|it|this)\b\s*(fix karo|solve karo|theek karo|restart karo|check karo)",
        r"\b(ab ise fix karo|ab isko theek karo|fix it|repair it|do it now|solve this)\b",
        r"\b(kya ye theek hua|kya solve hua|check again|fir se check karo)\b"
    ]

    @classmethod
    def classify(cls, query: str, history: Optional[List[Dict[str, Any]]] = None) -> IntentResult:
        norm = HinglishProcessor.normalize_text(query)
        augmented_query, resolved_domain = HinglishProcessor.resolve_pronoun_reference(query, history)

        # 1. Cancellation check
        for pat in cls.CANCELLATION_PATTERNS:
            if re.search(pat, norm) or re.search(pat, query.lower()):
                return IntentResult(IntentType.CANCELLATION, 0.98, domain=resolved_domain, normalized_query=norm)

        # 2. Confirmation check
        for pat in cls.CONFIRMATION_PATTERNS:
            if re.match(pat, norm):
                return IntentResult(IntentType.CONFIRMATION, 0.98, domain=resolved_domain, normalized_query=norm)

        # 3. Ambiguity check
        for pat in cls.AMBIGUOUS_PATTERNS:
            if re.search(pat, norm) or re.search(pat, query.lower()):
                return IntentResult(IntentType.AMBIGUOUS_QUERY, 0.90, domain=None, normalized_query=norm)

        # 4. Chit-chat / Greetings / Idle check
        for pat in cls.CHITCHAT_PATTERNS:
            if re.search(pat, norm) or re.search(pat, query.lower()):
                return IntentResult(IntentType.GREETING_CHITCHAT, 0.95, domain=None, normalized_query=norm)

        # 5. Follow-up intent check
        for pat in cls.FOLLOW_UP_PATTERNS:
            if re.search(pat, norm):
                return IntentResult(
                    IntentType.FOLLOW_UP_REQUEST,
                    0.92,
                    domain=resolved_domain,
                    normalized_query=norm,
                    context_inferred=resolved_domain
                )

        # 6. System Information Request (Checked before general explanation)
        for pat in cls.SYSTEM_INFO_PATTERNS:
            if re.search(pat, norm) or re.search(pat, query.lower()):
                return IntentResult(IntentType.SYSTEM_INFO_REQUEST, 0.92, domain=resolved_domain, normalized_query=norm)

        # 7. Technical explanation (Educational - Zero commands)
        for pat in cls.EXPLANATION_PATTERNS:
            if re.search(pat, norm):
                return IntentResult(IntentType.TECHNICAL_EXPLANATION, 0.90, domain=resolved_domain, normalized_query=norm)

        # 8. Explicit Action Request
        for pat in cls.ACTION_PATTERNS:
            if re.search(pat, norm):
                return IntentResult(IntentType.ACTION_REQUEST, 0.92, domain=resolved_domain, normalized_query=norm)

        # 9. Troubleshooting Request (Problem symptoms)
        domain = resolved_domain or HinglishProcessor.detect_domain(norm) or HinglishProcessor.detect_domain(query)
        trouble_indicators = ["slow", "lag", "hang", "freeze", "crash", "bsod", "band", "nahi chal", "not working", "fail", "error", "disconnect", "drop"]
        if domain or any(w in norm for w in trouble_indicators):
            return IntentResult(IntentType.TROUBLESHOOTING_REQUEST, 0.85, domain=domain, normalized_query=norm)

        # Default fallback
        return IntentResult(IntentType.TECHNICAL_EXPLANATION, 0.70, domain=domain, normalized_query=norm)
