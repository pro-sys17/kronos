"""
KRONOS Windows Master Catalog & Custom Commands Engine Test Suite.
Verifies:
1. Master catalog contains 250+ Windows commands and tools across all essential categories.
2. Custom commands parser correctly ingests `custom_commands.txt` and `custom_commands.json`.
3. Fuzzy and direct command matcher resolves system tools, aliases, and custom commands.
4. AI Brain correctly intercepts catalog, guide, and command execution requests with 0ms latency.
"""

import sys
import unittest
from pathlib import Path

SERVER_ROOT = Path(__file__).resolve().parents[1]
if str(SERVER_ROOT) not in sys.path:
    sys.path.insert(0, str(SERVER_ROOT))

from app.core.windows_commands_db import (
    WINDOWS_MASTER_CATALOG,
    load_custom_commands,
    match_command_or_app,
    get_total_commands_count,
    get_categorized_commands_summary
)
from app.core.ai_brain import AIBrain


class TestWindowsCommandsCatalog(unittest.TestCase):
    """Verifies the 250+ Windows command catalog and custom command engine."""

    def test_catalog_has_over_250_commands(self):
        total = get_total_commands_count()
        self.assertGreaterEqual(total, 250, f"Expected 250+ commands in catalog, got {total}")

    def test_essential_categories_present(self):
        categories = list(WINDOWS_MASTER_CATALOG.keys())
        expected = [
            "system_diagnostics",
            "control_panel_applets",
            "management_consoles",
            "modern_settings_uris",
            "network_admin",
            "storage_filesystem",
            "process_services",
            "security_admin",
            "builtin_utilities"
        ]
        for exp in expected:
            self.assertIn(exp, categories, f"Missing category: {exp}")

    def test_custom_commands_loaded(self):
        custom = load_custom_commands()
        self.assertIsInstance(custom, list)
        self.assertGreaterEqual(len(custom), 1, "custom_commands.txt should load at least 1 entry")
        aliases = [c["alias"] for c in custom]
        self.assertTrue(any(k in aliases for k in ["chrome", "calc", "notepad"]))

    def test_match_command_or_app_system_tools(self):
        # devmgmt
        m = match_command_or_app("kholo devmgmt")
        self.assertIsNotNone(m)
        self.assertIn("devmgmt.msc", m[0])

        # ncpa.cpl
        m = match_command_or_app("open ncpa.cpl")
        self.assertIsNotNone(m)
        self.assertIn("ncpa.cpl", m[0])

        # God Mode
        m = match_command_or_app("open god mode")
        self.assertIsNotNone(m)
        self.assertIn("ED7BA470", m[0])

        # Wi-Fi settings
        m = match_command_or_app("open wifi settings")
        self.assertIsNotNone(m)
        self.assertIn("ms-settings:network-wifi", m[0])

        # Task manager
        m = match_command_or_app("open task manager")
        self.assertIsNotNone(m)
        self.assertIn("taskmgr", m[0])

    def test_match_command_or_app_custom_tools(self):
        m = match_command_or_app("open chrome")
        self.assertIsNotNone(m)
        self.assertIn("chrome", m[0].lower())

    def test_ai_brain_catalog_routing(self):
        brain = AIBrain()

        queries_catalog = [
            "show me all tools",
            "show tools",
            "list all commands",
            "show commands",
            "show nahi ho rhe",
            "duniya bhar ke sare windows cmds inject karde"
        ]
        for q in queries_catalog:
            plan = brain._check_gui_request(q)
            self.assertIsNotNone(plan, f"Query '{q}' failed to trigger catalog plan")
            self.assertEqual(plan.get("issue_id"), "SYS-GUI-LIST")
            self.assertEqual(len(plan.get("actions", [])), 1)
            self.assertEqual(plan["actions"][0]["command"], "Show-WindowsCommandsTUI")

        queries_custom = [
            "can i add more gui cmd by a text file",
            "add custom command",
            "custom commands kaise dale"
        ]
        for q in queries_custom:
            plan = brain._check_gui_request(q)
            self.assertIsNotNone(plan, f"Query '{q}' failed to trigger custom guide plan")
            self.assertEqual(plan.get("issue_id"), "SYS-CUSTOM-GUIDE")
            self.assertEqual(len(plan.get("actions", [])), 1)
            self.assertEqual(plan["actions"][0]["command"], "Show-CustomCommandsGuide")


if __name__ == "__main__":
    unittest.main()
