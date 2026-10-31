"""
Unit tests for KRONOS Sanitization and Safe JSON Parsing Pipeline (Phase 2).
"""

import sys
import unittest
from pathlib import Path

SERVER_ROOT = Path(__file__).resolve().parents[1]
if str(SERVER_ROOT) not in sys.path:
    sys.path.insert(0, str(SERVER_ROOT))

from app.core.sanitizer import sanitize_output_text, safe_parse_json


class TestUnicodeSanitization(unittest.TestCase):
    """Validates output normalization and character sanitization."""

    def test_spaces_and_zero_width(self):
        # U+202F, U+00A0, U+200B
        raw = "RAM:\u202f16\u00a0GB\u200b available"
        clean = sanitize_output_text(raw)
        self.assertEqual(clean, "RAM: 16 GB available")
        self.assertNotIn("\u202f", clean)
        self.assertNotIn("\u00a0", clean)
        self.assertNotIn("\u200b", clean)

    def test_smart_quotes(self):
        raw = "“Windows 11” ‘Pro’ ‚edition‛ ʼupdate′"
        clean = sanitize_output_text(raw)
        self.assertEqual(clean, '"Windows 11" \'Pro\' \'edition\' \'update\'')

    def test_dashes_and_hyphens(self):
        # ‐ ‑ ‒ – — ― −
        raw = "NTFS\u2010exFAT\u2013FAT32\u2014ReFS\u2212EXT4"
        clean = sanitize_output_text(raw)
        self.assertEqual(clean, "NTFS-exFAT-FAT32-ReFS-EXT4")

    def test_ellipsis_and_bullets(self):
        raw = "Scanning\u2026\n\u2022 CPU\n\u25aa RAM\n\u25cf Disk"
        clean = sanitize_output_text(raw)
        self.assertIn("Scanning...", clean)
        self.assertIn("- CPU", clean)
        self.assertIn("- RAM", clean)
        self.assertIn("- Disk", clean)

    def test_arrows_and_checkmarks(self):
        raw = "Step 1 \u2192 Step 2 \u2190 Back\nDNS: \u2713 | Ping: \u2717"
        clean = sanitize_output_text(raw)
        self.assertEqual(clean, "Step 1 -> Step 2 <- Back\nDNS: [OK] | Ping: [X]")

    def test_hindi_devanagari_preservation(self):
        raw = "नमस्ते भाई, आपका स्वागत है! DNS क्या होता है aur ise kaise theek karein?"
        clean = sanitize_output_text(raw)
        self.assertEqual(clean, raw, "Devanagari Hindi text was modified!")
        self.assertIn("नमस्ते", clean)
        self.assertIn("क्या होता है", clean)

    def test_markdown_formatting_preservation(self):
        table = (
            "| Feature | NTFS | exFAT |\n"
            "|---|---|---|\n"
            "| Max File Size | 16 TB | 128 PB |\n"
            "| Security | Permissions | None |\n"
        )
        clean = sanitize_output_text(table)
        self.assertEqual(clean, table)

    def test_powershell_syntax_preservation(self):
        cmd = "Get-Process | Where-Object { $_.CPU -gt 50 } | Select-Object -First 5"
        clean = sanitize_output_text(cmd)
        self.assertEqual(clean, cmd)


class TestSafeJSONParser(unittest.TestCase):
    """Validates robust JSON extraction, repairs, and schema validation."""

    def test_standard_valid_json(self):
        raw = '{"issue_id": "SYS-001", "summary": "All good", "actions": []}'
        data = safe_parse_json(raw)
        self.assertEqual(data["issue_id"], "SYS-001")
        self.assertEqual(data["summary"], "All good")
        self.assertEqual(data["actions"], [])

    def test_markdown_code_fence_stripping(self):
        raw = "```json\n{\n  \"issue_id\": \"SYS-002\",\n  \"summary\": \"Fenced JSON\"\n}\n```"
        data = safe_parse_json(raw)
        self.assertEqual(data["issue_id"], "SYS-002")
        self.assertEqual(data["summary"], "Fenced JSON")

    def test_unescaped_newlines_in_multiline_string(self):
        # A JSON string that contains literal unescaped newlines inside the summary string (common with LLM markdown tables)
        raw = '{\n  "issue_id": "SYS-003",\n  "summary": "| Col1 | Col2 |\n|---|---|\n| A | B |\n",\n  "actions": []\n}'
        data = safe_parse_json(raw)
        self.assertEqual(data["issue_id"], "SYS-003")
        self.assertIn("| Col1 | Col2 |", data["summary"])

    def test_preamble_and_postscript_extraction(self):
        raw = 'Here is the diagnosis you requested:\n{"issue_id": "SYS-004", "summary": "Extracted"}\nHope this helps!'
        data = safe_parse_json(raw)
        self.assertEqual(data["issue_id"], "SYS-004")
        self.assertEqual(data["summary"], "Extracted")

    def test_truncated_json_recovery(self):
        # Truncated before closing brace
        raw = '{"issue_id": "SYS-005", "summary": "Truncated", "actions": ['
        data = safe_parse_json(raw)
        self.assertEqual(data["issue_id"], "SYS-005")
        self.assertEqual(data["summary"], "Truncated")

    def test_default_schema_completion(self):
        raw = '{"summary": "Minimal input"}'
        data = safe_parse_json(raw)
        self.assertEqual(data["summary"], "Minimal input")
        self.assertIn("issue_id", data)
        self.assertIn("root_cause", data)
        self.assertIn("risk_level", data)
        self.assertIn("selected_tools", data)
        self.assertIn("verification_command", data)

    def test_invalid_json_rejection(self):
        with self.assertRaises(ValueError):
            safe_parse_json("This is purely conversational with no JSON at all.")


if __name__ == "__main__":
    unittest.main()

