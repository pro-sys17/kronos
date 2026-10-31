from contextlib import contextmanager
"""
KRONOS Controlled Persistent Memory Engine (SQLite)
Securely persists user preferences, hardware profiles, and verified troubleshooting history.
Never stores passwords, API keys, credentials, or sensitive command output.
Memory is strictly advisory context and NEVER acts as an execution authorization.
"""

import sqlite3
import json
import re
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

DB_PATH = Path(__file__).resolve().parents[2] / "kronos_memory.db"

class MemoryStore:
    """
    Thread-safe SQLite persistent memory for KRONOS AI.
    """

    @classmethod
    @contextmanager
    def _get_connection(cls):
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    @classmethod
    def initialize(cls):
        """
        Initializes schema tables if not present.
        """
        with cls._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_profiles (
                machine_id TEXT PRIMARY KEY,
                hostname TEXT,
                os_caption TEXT,
                os_version TEXT,
                total_ram_gb REAL,
                drives TEXT,
                last_seen TEXT
            )
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_preferences (
                username TEXT PRIMARY KEY,
                preferred_language TEXT DEFAULT 'hinglish',
                voice_enabled INTEGER DEFAULT 1,
                last_updated TEXT
            )
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS troubleshooting_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                issue_summary TEXT,
                root_cause TEXT,
                tools_executed TEXT,
                outcome TEXT
            )
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS session_summaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                session_token TEXT,
                summary TEXT
            )
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                session_token TEXT,
                user_message TEXT,
                ai_summary TEXT,
                intent TEXT,
                actions_count INTEGER DEFAULT 0
            )
            """)
            conn.commit()

    @classmethod
    def sanitize_text(cls, text: str) -> str:
        """
        Strips potential credentials, tokens, or passwords before persisting.
        """
        t = re.sub(r'(?i)(password|passcode|token|key|secret)\s*[:=]\s*[^\s]+', r'\1: [REDACTED]', str(text))
        return t.strip()

    @classmethod
    def update_system_profile(cls, telemetry: Dict[str, Any]):
        if not telemetry:
            return
        hostname = telemetry.get("ComputerName") or telemetry.get("hostname") or "UNKNOWN"
        os_caption = telemetry.get("OSName") or telemetry.get("os_name") or "Microsoft Windows"
        os_ver = telemetry.get("OSVersion") or telemetry.get("os_version") or ""
        ram_val = telemetry.get("TotalMemoryGB") or telemetry.get("ram_total_gb") or 16.0
        try:
            ram = float(ram_val)
        except (ValueError, TypeError):
            ram = 16.0
        drives = str(telemetry.get("Drives") or telemetry.get("drives") or "C:")
        now_iso = datetime.now(timezone.utc).isoformat()

        cls.initialize()
        with cls._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO system_profiles (machine_id, hostname, os_caption, os_version, total_ram_gb, drives, last_seen)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(machine_id) DO UPDATE SET
                hostname=excluded.hostname,
                os_caption=excluded.os_caption,
                os_version=excluded.os_version,
                total_ram_gb=excluded.total_ram_gb,
                drives=excluded.drives,
                last_seen=excluded.last_seen
            """, (hostname, hostname, os_caption, os_ver, ram, drives, now_iso))
            conn.commit()

    @classmethod
    def get_latest_profile(cls) -> Optional[Dict[str, Any]]:
        cls.initialize()
        with cls._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM system_profiles ORDER BY last_seen DESC LIMIT 1")
            row = cursor.fetchone()
            return dict(row) if row else None

    @classmethod
    def record_troubleshooting(cls, issue: str, root_cause: str, tools_used: List[str], outcome: str = "completed"):
        cls.initialize()
        clean_issue = cls.sanitize_text(issue)
        clean_cause = cls.sanitize_text(root_cause)
        tools_str = json.dumps(tools_used)
        now_iso = datetime.now(timezone.utc).isoformat()

        with cls._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO troubleshooting_history (timestamp, issue_summary, root_cause, tools_executed, outcome)
            VALUES (?, ?, ?, ?, ?)
            """, (now_iso, clean_issue, clean_cause, tools_str, outcome))
            conn.commit()

    @classmethod
    def save_chat_turn(cls, session_token: str, user_message: str, ai_summary: str,
                       intent: str = "unknown", actions_count: int = 0):
        """
        Saves each chat turn (user question + AI response summary) to persistent history.
        Only stores sanitized, non-sensitive content.
        """
        cls.initialize()
        clean_msg = cls.sanitize_text(user_message)[:500]
        clean_summary = cls.sanitize_text(ai_summary)[:1000]
        now_iso = datetime.now(timezone.utc).isoformat()

        with cls._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO chat_sessions (timestamp, session_token, user_message, ai_summary, intent, actions_count)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (now_iso, session_token or "default", clean_msg, clean_summary, intent, actions_count))
            conn.commit()

    @classmethod
    def get_chat_history(cls, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Returns recent chat turns across all sessions for TUI memory dashboard.
        """
        cls.initialize()
        with cls._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT id, timestamp, session_token, user_message, ai_summary, intent, actions_count
            FROM chat_sessions
            ORDER BY id DESC LIMIT ?
            """, (limit,))
            rows = cursor.fetchall()
            return [dict(r) for r in rows]

    @classmethod
    def get_recent_history(cls, limit: int = 3) -> List[Dict[str, Any]]:
        cls.initialize()
        with cls._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT timestamp, issue_summary, root_cause, tools_executed, outcome
            FROM troubleshooting_history
            ORDER BY id DESC LIMIT ?
            """, (limit,))
            rows = cursor.fetchall()
            return [dict(r) for r in rows]

    @classmethod
    def clear_memory(cls):
        cls.initialize()
        with cls._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM troubleshooting_history")
            cursor.execute("DELETE FROM session_summaries")
            cursor.execute("DELETE FROM chat_sessions")
            cursor.execute("DELETE FROM system_profiles")
            conn.commit()

    @classmethod
    def build_memory_context(cls) -> str:
        """
        Formats safe memory context for LLM grounding.
        """
        cls.initialize()
        profile = cls.get_latest_profile()
        history = cls.get_recent_history(limit=3)
        if not profile and not history:
            return ""

        lines = ["\n[KRONOS PERSISTENT MEMORY CONTEXT]"]
        if profile:
            lines.append(f"Host Profile: {profile.get('os_caption', 'Windows')} | RAM: {profile.get('total_ram_gb', 0)}GB | Drives: {profile.get('drives', 'C:')}")
        for h in history:
            lines.append(f"Past Issue: {h['issue_summary']} | Diagnosed Cause: {h['root_cause']} | Outcome: {h['outcome']}")
        lines.append("Note: Memory is reference history only. Always verify live system state before acting.")
        return "\n".join(lines)
