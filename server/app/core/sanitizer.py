"""
KRONOS Robust Sanitization & Safe JSON Parsing Pipeline
Enforces:
1. Reusable output-normalization for safe Windows console rendering (CP1252 & UTF-8).
2. Robust JSON parsing for multiline Markdown, unescaped control chars, and code blocks.
3. Preservation of Hindi/Devanagari scripts, Markdown tables, and PowerShell syntax.
4. Security metadata tracking for repaired and truncated JSON payloads to prevent unauthorized execution.
5. Fail-safe defaults: requires_confirmation defaults to TRUE and risk_level defaults to HIGH if actions exist.
"""

from __future__ import annotations
import json
import re
from typing import Dict, Any, Optional, List


def sanitize_output_text(text: Optional[str]) -> str:
    """
    Normalizes Unicode characters in model outputs and user-visible strings
    to ensure 100% safe rendering on Windows consoles without corrupting
    Hindi/Devanagari scripts, Markdown tables, code blocks, or PowerShell syntax.
    """
    if not text:
        return ""

    s = str(text)

    # 1. Spaces & Zero-Width characters
    s = s.replace('\u202f', ' ')
    s = s.replace('\u00a0', ' ')
    s = s.replace('\u200b', '')
    s = s.replace('\u200e', '').replace('\u200f', '')

    # 2. Smart Quotes -> ASCII standard quotes
    s = re.sub(r'[\u2018\u2019\u201a\u201b\u02bc\u2032]', "'", s)
    s = re.sub(r'[\u201c\u201d\u201e\u201f\u2033]', '"', s)

    # 3. Dashes & Hyphens -> ASCII hyphen '-'
    s = re.sub(r'[\u2010\u2011\u2012\u2013\u2014\u2015\u2212\ufe58\ufe63\uff0d]', '-', s)

    # 4. Unicode Ellipsis -> ASCII '...'
    s = s.replace('\u2026', '...')

    # 5. Unicode List Bullets -> ASCII '-'
    s = re.sub(r'[\u2022\u25aa\u25cf]', '-', s)

    # 6. Unicode Arrows -> ASCII equivalents
    s = s.replace('\u2192', '->').replace('\u2190', '<-')

    # 7. Common UTF-8 Mojibake artifacts seen on Windows CP1252
    s = s.replace('â¯', ' ').replace('â', '-')

    # 8. Checkmarks & Crosses -> Safe ASCII representation
    s = re.sub(r'[\u2713\u2714]', '[OK]', s)
    s = re.sub(r'[\u2717\u2718]', '[X]', s)

    return s


def safe_parse_json(raw_text: str) -> Dict[str, Any]:
    """
    Robust JSON parser for LLM outputs.
    Handles:
    - Markdown code fences (```json ... ``` or ``` ... ```)
    - Unescaped control characters inside multiline Markdown string literals (strict=False)
    - Preamble / postscript text outside the main JSON object
    - Validates schema, tracks repair/truncation metadata, and ensures safe fail-closed defaults.
    """
    if not raw_text or not raw_text.strip():
        raise ValueError("Empty response string received from model.")

    clean_text = raw_text.strip()

    # 1. Strip markdown code fences if wrapped
    if clean_text.startswith("```"):
        clean_text = re.sub(r"^```(?:json)?\s*", "", clean_text, flags=re.IGNORECASE)
        clean_text = re.sub(r"\s*```$", "", clean_text)
        clean_text = clean_text.strip()

    # 2. Extract outermost JSON object if there is text before or after
    if not clean_text.startswith("{"):
        match = re.search(r"(\{.*\})", clean_text, flags=re.DOTALL)
        if match:
            clean_text = match.group(1).strip()

    # 3. First attempt: standard strict JSON parse
    try:
        data = json.loads(clean_text)
        if isinstance(data, dict):
            return _ensure_schema(data, is_repaired=False, is_truncated=False)
    except json.JSONDecodeError:
        pass

    # 4. Second attempt: non-strict parse (allows literal unescaped newlines/tabs inside strings)
    try:
        data = json.loads(clean_text, strict=False)
        if isinstance(data, dict):
            return _ensure_schema(data, is_repaired=False, is_truncated=False)
    except json.JSONDecodeError:
        pass

    # 5. Third attempt: repair unescaped newlines inside string values using token scanner
    repaired = _repair_json_control_chars(clean_text)
    try:
        data = json.loads(repaired, strict=False)
        if isinstance(data, dict):
            return _ensure_schema(data, is_repaired=True, is_truncated=False)
    except json.JSONDecodeError:
        pass

    # 6. Fourth attempt: auto-close unclosed brackets or strings if truncated near end
    for base_text in [clean_text, repaired]:
        closed_text = _try_close_json(base_text)
        if closed_text != base_text:
            try:
                data = json.loads(closed_text, strict=False)
                if isinstance(data, dict):
                    return _ensure_schema(data, is_repaired=True, is_truncated=True)
            except json.JSONDecodeError:
                pass

    # If all parsing attempts failed, raise descriptive ValueError
    raise ValueError(f"Failed to parse LLM response into valid JSON object: {clean_text[:200]}")


def _repair_json_control_chars(text: str) -> str:
    """
    Replaces literal control newlines and tabs inside JSON string literals with \\n and \\t.
    """
    result = []
    in_string = False
    escape = False

    for char in text:
        if escape:
            result.append(char)
            escape = False
            continue

        if char == '\\':
            result.append(char)
            escape = True
            continue

        if char == '"':
            in_string = not in_string
            result.append(char)
            continue

        if in_string:
            if char == '\n':
                result.append('\\n')
            elif char == '\r':
                result.append('\\r')
            elif char == '\t':
                result.append('\\t')
            elif ord(char) < 32:
                result.append(f'\\u{ord(char):04x}')
            else:
                result.append(char)
        else:
            result.append(char)

    return ''.join(result)


def _try_close_json(text: str) -> str:
    """
    Attempts to close an open string, array, or object in strict LIFO nesting order
    if truncated by token limits.
    """
    t = text.rstrip()
    stack = []
    in_string = False
    escape = False

    for char in t:
        if escape:
            escape = False
            continue
        if char == '\\':
            escape = True
            continue
        if char == '"':
            in_string = not in_string
            continue
        if in_string:
            continue

        if char in ('{', '['):
            stack.append(char)
        elif char == '}':
            if stack and stack[-1] == '{':
                stack.pop()
        elif char == ']':
            if stack and stack[-1] == '[':
                stack.pop()

    suffix = ""
    if in_string:
        suffix += '"'

    # Close open brackets in strict LIFO reverse nesting order
    for bracket in reversed(stack):
        if bracket == '{':
            suffix += '}'
        elif bracket == '[':
            suffix += ']'

    return t + suffix


def _ensure_schema(data: Dict[str, Any], is_repaired: bool = False, is_truncated: bool = False) -> Dict[str, Any]:
    """
    Ensures all required KRONOS schema fields are present with correct types.
    Enforces secure fail-closed defaults:
    - If actions or selected_tools are present and confirmation/risk fields are missing:
      defaults to requires_confirmation = True and risk_level = 'HIGH'.
    - Never infers 'LOW' risk from absent fields when executable actions exist.
    """
    if not isinstance(data, dict):
        raise ValueError("Model output is not a JSON object dictionary.")

    # Record structural integrity metadata
    data["_metadata"] = {
        "repaired": is_repaired,
        "truncated": is_truncated
    }

    # Validate types of list fields first so has_actions is accurate
    if not isinstance(data.get("selected_tools"), list):
        data["selected_tools"] = []
    if not isinstance(data.get("actions"), list):
        data["actions"] = []

    has_actions = bool(data.get("actions")) or bool(data.get("selected_tools"))

    data.setdefault("issue_id", "SYS-DIAG-001")
    data.setdefault("root_cause", "Diagnostic evaluation")
    data.setdefault("intent", "TECHNICAL_EXPLANATION")
    data.setdefault("summary", "")
    data.setdefault("verification_command", "$true")

    # Safe defaults:
    # Missing requires_confirmation must default to TRUE if actions exist.
    # Missing risk_level must default to HIGH if actions exist. Never infer LOW risk from absent fields!
    if "requires_confirmation" not in data or data["requires_confirmation"] is None:
        data["requires_confirmation"] = True if has_actions else False

    if "risk_level" not in data or not data["risk_level"]:
        data["risk_level"] = "HIGH" if has_actions else "LOW"
    else:
        data["risk_level"] = str(data["risk_level"]).upper()

    return data
