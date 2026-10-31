"""
KRONOS Cryptographic Server-Side Operation Authorization Engine
Generates and enforces single-use, cryptographically signed, argument-bound approval tickets.
Prevents:
1. Client-side risk level spoofing
2. Argument tampering after approval
3. Ticket replay attacks (single-use nonces)
4. Expired ticket exploitation
"""

from __future__ import annotations
import hmac
import hashlib
import time
import secrets
import json
from typing import Dict, Any, Tuple, Optional
from .security import SecurityManager


class OperationAuthorizer:
    """
    Cryptographic authorization authority for privileged and modifying system operations.
    """

    TICKET_TTL_SECONDS: int = 300  # 5 minutes validity
    _CONSUMED_NONCES: Dict[str, float] = {}
    _LAST_PURGE: float = 0.0

    @classmethod
    def _get_server_secret(cls) -> str:
        return SecurityManager._SERVER_SECRET

    @classmethod
    def canonical_args_hash(cls, args: Dict[str, Any]) -> str:
        """
        Computes a deterministic, canonical SHA-256 digest of tool arguments.
        """
        if not isinstance(args, dict):
            args = {}
        # Normalize nested primitives and produce strict sorted key JSON
        norm_json = json.dumps(args, sort_keys=True, separators=(',', ':'))
        return hashlib.sha256(norm_json.encode('utf-8')).hexdigest()[:32]

    @classmethod
    def create_ticket(cls, tool_id: str, args: Dict[str, Any], risk: str) -> str:
        """
        Generates a cryptographically signed approval ticket bound to:
        - tool_id
        - exact canonical arguments hash
        - tool risk classification
        - expiration timestamp
        - single-use cryptographically random nonce
        Format: {tool_id}|{args_hash}|{risk}|{expires_at}|{nonce}|{signature}
        """
        tool_id_clean = tool_id.strip()
        args_hash = cls.canonical_args_hash(args)
        risk_clean = risk.strip().upper()
        expires_at = int(time.time()) + cls.TICKET_TTL_SECONDS
        nonce = secrets.token_hex(8)

        payload = f"{tool_id_clean}|{args_hash}|{risk_clean}|{expires_at}|{nonce}"
        sig = hmac.new(
            cls._get_server_secret().encode('utf-8'),
            payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()[:32]

        return f"{payload}|{sig}"

    @classmethod
    def verify_and_consume_ticket(
        cls,
        ticket: Optional[str],
        tool_id: str,
        args: Dict[str, Any]
    ) -> Tuple[bool, str]:
        """
        Verifies ticket authenticity, argument integrity, non-expiration, and single-use status.
        If valid, marks the ticket's nonce as consumed so it cannot be reused.
        """
        if not ticket or not isinstance(ticket, str):
            return False, "Missing or invalid approval ticket."

        parts = ticket.strip().split("|")
        if len(parts) != 6:
            return False, "Malformed approval ticket structure."

        t_tool_id, t_args_hash, t_risk, t_expires_str, t_nonce, t_sig = parts

        # 1. Signature Verification
        expected_payload = f"{t_tool_id}|{t_args_hash}|{t_risk}|{t_expires_str}|{t_nonce}"
        expected_sig = hmac.new(
            cls._get_server_secret().encode('utf-8'),
            expected_payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()[:32]

        if not hmac.compare_digest(t_sig, expected_sig):
            return False, "Cryptographic signature verification failed: ticket signature is invalid."

        # 2. Expiration Verification
        try:
            expires_at = float(t_expires_str)
        except ValueError:
            return False, "Invalid timestamp in approval ticket."

        now = time.time()
        if now > expires_at:
            return False, f"Approval ticket has expired (expired at {expires_at:.0f}, current {now:.0f})."

        # 3. Tool ID Binding Verification
        if t_tool_id != tool_id.strip():
            return False, f"Approval ticket was authorized for tool '{t_tool_id}', not '{tool_id}'."

        # 4. Argument Integrity Verification (Prevents parameter tampering after approval)
        current_args_hash = cls.canonical_args_hash(args)
        if not hmac.compare_digest(t_args_hash, current_args_hash):
            return False, "Approval ticket argument hash mismatch: arguments were modified after authorization."

        # 5. Single-Use Nonce & Replay Protection
        cls._purge_stale_nonces(now)
        if t_nonce in cls._CONSUMED_NONCES:
            return False, "Approval ticket has already been used (replay detected)."

        # Consume nonce
        cls._CONSUMED_NONCES[t_nonce] = expires_at
        return True, "Operation successfully authorized."

    @classmethod
    def _purge_stale_nonces(cls, now: float):
        """Purges expired nonces from memory periodically."""
        if now - cls._LAST_PURGE < 60.0:
            return
        cls._LAST_PURGE = now
        stale_keys = [nonce for nonce, exp in cls._CONSUMED_NONCES.items() if exp < now]
        for k in stale_keys:
            del cls._CONSUMED_NONCES[k]

