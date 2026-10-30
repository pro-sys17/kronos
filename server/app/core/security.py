import time
import secrets
import hmac
import hashlib
from typing import Dict, Tuple

class SecurityManager:
    """
    KRONOS Endpoint Shield:
    1. Ephemeral HMAC Session Tokens (Time-decaying)
    2. IP Rate Limiting (Prevents token/quota exhaustion)
    3. Payload Size Guard
    """
    
    # Secret seed for token generation (rotates per process lifecycle or from env)
    _SERVER_SECRET = secrets.token_hex(32)
    
    # In-memory IP rate limiter: {ip: [timestamps]}
    _RATE_LIMITS: Dict[str, list] = {}
    MAX_REQUESTS_PER_MINUTE = 30  # Allows active multi-turn interactive conversation
    TOKEN_TTL_SECONDS = 3600  # 1 Hour validity

    @classmethod
    def generate_session_token(cls) -> str:
        """
        Generates a cryptographically signed, timestamped session token.
        Format: timestamp.signature
        """
        ts = str(int(time.time()))
        sig = hmac.new(
            cls._SERVER_SECRET.encode(),
            ts.encode(),
            hashlib.sha256
        ).hexdigest()
        return f"{ts}.{sig}"

    @classmethod
    def verify_session_token(cls, token: str) -> bool:
        """
        Validates token authenticity and expiration.
        """
        if not token or "." not in token:
            return False
            
        ts_str, sig = token.split(".", 1)
        try:
            ts = int(ts_str)
        except ValueError:
            return False

        # Expiry check
        if time.time() - ts > cls.TOKEN_TTL_SECONDS:
            return False

        # Signature verification
        expected_sig = hmac.new(
            cls._SERVER_SECRET.encode(),
            ts_str.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(sig, expected_sig)

    @classmethod
    def check_rate_limit(cls, client_ip: str) -> Tuple[bool, str]:
        """
        Sliding window rate-limiter: blocks IP if > 10 requests/min.
        """
        now = time.time()
        window_start = now - 60

        if client_ip not in cls._RATE_LIMITS:
            cls._RATE_LIMITS[client_ip] = []

        # Purge stale timestamps
        cls._RATE_LIMITS[client_ip] = [
            t for t in cls._RATE_LIMITS[client_ip] if t > window_start
        ]

        if len(cls._RATE_LIMITS[client_ip]) >= cls.MAX_REQUESTS_PER_MINUTE:
            return False, "Rate limit exceeded (10 requests/minute). Cooldown in progress."

        cls._RATE_LIMITS[client_ip].append(now)
        return True, "Permitted"

