"""
KRONOS Level 2 Controlled Autonomy Comprehensive Evaluation Suite
Validates:
1. Intent Classification Accuracy across 25+ English and Hinglish queries.
2. Hinglish Normalization & Multi-turn Pronoun Reference Resolution.
3. Structured Tool Execution Engine (26 tools, parameter typing, command compilation).
4. Safety Guardrail & Injection Rejection (Zero arbitrary script execution, prohibited blocks).
5. RAG Technical Knowledge Retrieval (Microsoft Learn / Windows reference coverage).
6. Persistent Memory Engine (Sanitization, hardware profiles, troubleshooting history).
7. End-to-End Diagnostic Pipeline (AIBrain Level 2 Controlled Autonomy).
8. FastAPI Endpoints (/health, /api/v1/skills, /api/v1/tools, /api/v1/memory).
"""

import sys
import os
import unittest
import json
import asyncio
from pathlib import Path

# Add server root to sys.path
SERVER_ROOT = Path(__file__).resolve().parents[1]
if str(SERVER_ROOT) not in sys.path:
    sys.path.insert(0, str(SERVER_ROOT))

from app.core.intent.classifier import IntentClassifier, IntentType
from app.core.intent.hinglish import HinglishProcessor
from app.core.tools.registry import ToolRegistry
from app.core.tools.executor import ToolExecutor
from app.core.guardrail import CommandGuardrail
from app.core.skills.registry import SkillsRegistry
from app.core.rag.knowledge_base import KnowledgeBase
from app.core.memory.store import MemoryStore
from app.core.ai_brain import AIBrain
from fastapi.testclient import TestClient
from app.main import app

class TestIntentClassification(unittest.TestCase):
    """Evaluates NLU intent classification accuracy."""

    def test_greetings_and_chitchat(self):
        queries = [
            "hi bhai",
            "hello kronos",
            "namaste",
            "good morning",
            "aur bhai kya haal",
            "hey there"
        ]
        for q in queries:
            res = IntentClassifier.classify(q)
            self.assertEqual(res.intent, IntentType.GREETING_CHITCHAT, f"Failed for query: {q}")

    def test_cancellation(self):
        queries = [
            "rehne do",
            "kuch mat karo",
            "cancel it",
            "chhod do yaar",
            "stop nothing to do"
        ]
        for q in queries:
            res = IntentClassifier.classify(q)
            self.assertEqual(res.intent, IntentType.CANCELLATION, f"Failed for query: {q}")

    def test_ambiguous_queries(self):
        queries = [
            "kuch to problem he",
            "laptop me kuch to garbar hai",
            "system issue",
            "something is wrong"
        ]
        for q in queries:
            res = IntentClassifier.classify(q)
            self.assertEqual(res.intent, IntentType.AMBIGUOUS_QUERY, f"Failed for query: {q}")

    def test_system_info_requests(self):
        queries = [
            "pc ke specs batao",
            "system details",
            "specs kya he",
            "mera ip address kya hai",
            "battery health check"
        ]
        for q in queries:
            res = IntentClassifier.classify(q)
            self.assertEqual(res.intent, IntentType.SYSTEM_INFO_REQUEST, f"Failed for query: {q}")

    def test_troubleshooting_requests(self):
        queries = [
            "mera internet slow chal raha hai",
            "audio nahi aa raha",
            "sound problem he",
            "cpu usage 100% ho gaya",
            "windows update error 0x80070002"
        ]
        for q in queries:
            res = IntentClassifier.classify(q)
            self.assertEqual(res.intent, IntentType.TROUBLESHOOTING_REQUEST, f"Failed for query: {q}")

    def test_technical_explanations(self):
        queries = [
            "dns kya hota hai",
            "what is sfc scannow",
            "difference between cmd and powershell"
        ]
        for q in queries:
            res = IntentClassifier.classify(q)
            self.assertEqual(res.intent, IntentType.TECHNICAL_EXPLANATION, f"Failed for query: {q}")


class TestHinglishAndPronounResolution(unittest.TestCase):
    """Evaluates Hinglish normalization, domain detection, and pronoun tracking."""

    def test_hinglish_normalization(self):
        norm = HinglishProcessor.normalize_text("chalu kr do")
        self.assertIn("karo", norm)
        self.assertIn("network", HinglishProcessor.detect_domain("net slow chalra hai"))
        self.assertIn("audio", HinglishProcessor.detect_domain("speaker me sound nahi he"))
        self.assertIn("storage", HinglishProcessor.detect_domain("c drive full ho gaya"))

    def test_pronoun_reference_resolution(self):
        history = [
            {"role": "user", "content": "Mera internet slow hai aur ping drop ho raha hai"},
            {"role": "assistant", "content": "Maine network adapter check kiya"}
        ]
        resolved, domain = HinglishProcessor.resolve_pronoun_reference("Ab ise fix karo", history)
        self.assertEqual(domain, "network")
        self.assertIn("context: network", resolved)

        history_audio = [
            {"role": "user", "content": "Speaker se awaz nahi aa rahi"},
            {"role": "assistant", "content": "AudioSrv service check kar raha hoon"}
        ]
        resolved_aud, domain_aud = HinglishProcessor.resolve_pronoun_reference("isko theek kar do", history_audio)
        self.assertEqual(domain_aud, "audio")
        self.assertIn("context: audio", resolved_aud)


class TestToolRegistryAndExecutor(unittest.TestCase):
    """Evaluates the 26 registered system tools and validation compiler."""

    def test_registered_tools_count(self):
        tools = ToolRegistry.list_all()
        self.assertGreaterEqual(len(tools), 26)

    def test_tool_schema_export(self):
        schemas = ToolRegistry.get_schemas()
        self.assertGreaterEqual(len(schemas), 26)
        for s in schemas:
            self.assertIn("tool_id", s)
            self.assertIn("risk", s)
            self.assertIn("parameters", s)
            self.assertIn(s["risk"], ["LOW", "MODERATE", "HIGH", "PROHIBITED"])

    def test_compile_valid_tool_call(self):
        calls = [
            {"tool_id": "network.test_dns", "arguments": {"domain": "cloudflare.com"}},
            {"tool_id": "network.ping", "arguments": {"target": "1.1.1.1", "count": 2}}
        ]
        res = ToolExecutor.compile_tool_calls(calls)
        self.assertTrue(res.is_valid)
        self.assertEqual(res.highest_risk, "LOW")
        self.assertEqual(len(res.actions), 2)
        self.assertIn("Resolve-DnsName", res.actions[0]["command"])
        self.assertIn("Test-NetConnection", res.actions[1]["command"])

    def test_compile_moderate_risk_tool(self):
        calls = [{"tool_id": "network.flush_dns", "arguments": {}}]
        res = ToolExecutor.compile_tool_calls(calls)
        self.assertTrue(res.is_valid)
        self.assertEqual(res.highest_risk, "MODERATE")
        self.assertTrue(res.actions[0]["requires_confirmation"])

    def test_compile_high_risk_tool(self):
        calls = [{"tool_id": "file.delete_item", "arguments": {"path": "C:\\temp\\junk.tmp"}}]
        res = ToolExecutor.compile_tool_calls(calls)
        self.assertTrue(res.is_valid)
        self.assertEqual(res.highest_risk, "HIGH")
        self.assertTrue(res.actions[0]["requires_confirmation"])

    def test_reject_unregistered_tool(self):
        calls = [{"tool_id": "malicious.tool", "arguments": {}}]
        res = ToolExecutor.compile_tool_calls(calls)
        self.assertFalse(res.is_valid)
        self.assertEqual(res.highest_risk, "BLOCKED")
        self.assertIn("Unauthorized or unknown tool ID", res.error_message)

    def test_reject_parameter_injection(self):
        calls = [{"tool_id": "network.test_dns", "arguments": {"domain": "google.com; Remove-Item C:\\"}}]
        res = ToolExecutor.compile_tool_calls(calls)
        self.assertFalse(res.is_valid)
        self.assertEqual(res.highest_risk, "BLOCKED")
        self.assertIn("Illegal characters detected", res.error_message)


class TestSafetyGuardrail(unittest.TestCase):
    """Evaluates AST security guardrails against dangerous commands."""

    def test_reject_destructive_commands(self):
        dangerous_commands = [
            "format c: /fs:ntfs",
            "diskpart /s script.txt",
            "Remove-Item -Path C:\\Windows\\System32 -Recurse -Force",
            "rmdir /s /q C:\\",
            "cipher /w:C:\\",
            "Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled False"
        ]
        for cmd in dangerous_commands:
            actions = [{"description": "Dangerous action", "command": cmd}]
            safe_actions, highest_risk = CommandGuardrail.sanitize_plan(actions)
            self.assertEqual(len(safe_actions), 0, f"Dangerous command was not rejected: {cmd}")
            self.assertEqual(highest_risk, "BLOCKED")


class TestRAGKnowledgeRetrieval(unittest.TestCase):
    """Evaluates RAG knowledge base retrieval."""

    def test_retrieve_dns_docs(self):
        docs = KnowledgeBase.search("dns cache flush latency", limit=2)
        self.assertGreaterEqual(len(docs), 1)
        self.assertEqual(docs[0].doc_id, "KB-NET-001")

    def test_retrieve_service_docs(self):
        docs = KnowledgeBase.search("AudioSrv audio service restart", limit=2)
        self.assertGreaterEqual(len(docs), 1)
        self.assertEqual(docs[0].doc_id, "KB-AUD-001")

    def test_retrieve_eventlog_docs(self):
        docs = KnowledgeBase.search("event viewer event id error 41 kernel", limit=2)
        self.assertGreaterEqual(len(docs), 1)
        self.assertEqual(docs[0].doc_id, "KB-SYS-001")

    def test_build_rag_context(self):
        ctx = KnowledgeBase.build_rag_context("mera internet slow hai")
        self.assertIn("TECHNICAL KNOWLEDGE", ctx)


class TestPersistentMemory(unittest.TestCase):
    """Evaluates persistent SQLite memory and security sanitization."""

    def setUp(self):
        MemoryStore.initialize()
        MemoryStore.clear_memory()

    def test_system_profile_and_sanitization(self):
        telemetry = {
            "OSName": "Windows 11 Pro",
            "ComputerName": "DESKTOP-PROFESSOR",
            "TotalMemoryGB": 16.0,
            "secret_token": "sk-live-1234567890abcdef"
        }
        MemoryStore.update_system_profile(telemetry)
        ctx = MemoryStore.build_memory_context()
        self.assertIn("Windows 11 Pro", ctx)
        self.assertNotIn("sk-live-1234567890abcdef", ctx)

    def test_record_troubleshooting(self):
        MemoryStore.record_troubleshooting(
            issue="TEST-001",
            root_cause="Stale DNS cache",
            tools_used=["dns_flush", "network_ping"],
            outcome="completed"
        )
        history = MemoryStore.get_recent_history(limit=5)
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["root_cause"], "Stale DNS cache")


class TestAIBrainDiagnose(unittest.TestCase):
    """Evaluates end-to-end Level 2 Controlled Autonomy diagnostic execution."""

    def setUp(self):
        self.brain = AIBrain()

    def test_chitchat_diagnosis(self):
        async def run():
            plan = await self.brain.diagnose("hi bhai", {})
            self.assertEqual(plan["issue_id"], "SYS-CHITCHAT")
            self.assertEqual(len(plan["actions"]), 0)
            self.assertEqual(plan["risk_level"], "LOW")
        asyncio.run(run())

    def test_ambiguous_diagnosis(self):
        async def run():
            plan = await self.brain.diagnose("kuch problem he", {})
            self.assertEqual(plan["issue_id"], "SYS-AMBIGUOUS")
            self.assertEqual(len(plan["actions"]), 0)
        asyncio.run(run())

    def test_offline_fallback_sound(self):
        plan = self.brain._local_expert_engine("sound nahi aa raha", {})
        self.assertEqual(plan["issue_id"], "SKILL-AUDIO-REPAIR")
        self.assertGreater(len(plan["actions"]), 0)
        self.assertTrue(plan["requires_confirmation"])


class TestFastAPIRoutes(unittest.TestCase):
    """Evaluates FastAPI HTTP endpoints."""

    def setUp(self):
        self.client = TestClient(app)

    def test_health(self):
        resp = self.client.get("/health")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["status"], "HEALTHY")

    def test_skills_list(self):
        resp = self.client.get("/api/v1/skills")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertGreaterEqual(len(data), 10)

    def test_tools_list(self):
        resp = self.client.get("/api/v1/tools")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "SUCCESS")
        self.assertGreaterEqual(data["total_tools"], 26)

    def test_memory_routes(self):
        from app.core.memory.store import MemoryStore
        MemoryStore.save_chat_turn("session-123", "kya haal hai", "Sab badhiya bhai", "GREETING_CHITCHAT", 0)

        resp = self.client.get("/api/v1/memory")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "SUCCESS")
        self.assertIn("recent_chats", data)
        self.assertGreaterEqual(data["recent_chats_count"], 1)

        clear_resp = self.client.post("/api/v1/memory/clear")
        self.assertEqual(clear_resp.status_code, 200)
        self.assertEqual(clear_resp.json()["status"], "SUCCESS")


if __name__ == "__main__":
    unittest.main()
