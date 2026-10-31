"""
KRONOS Tool Execution & Validation Dispatcher
Validates structured tool requests, enforces permission tiers, and compiles deterministic PowerShell code.
"""

from typing import Dict, Any, List, Tuple
from .registry import ToolRegistry, ToolDefinition

class ToolExecutionResult:
    def __init__(self, is_valid: bool, actions: List[Dict[str, Any]], highest_risk: str, error_message: str = ""):
        self.is_valid = is_valid
        self.actions = actions
        self.highest_risk = highest_risk
        self.error_message = error_message

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_valid": self.is_valid,
            "actions": self.actions,
            "highest_risk": self.highest_risk,
            "error_message": self.error_message
        }

class ToolExecutor:
    """
    Validates and transforms structured tool calls into safe executable actions.
    """

    RISK_HIERARCHY = {
        "LOW": 1,
        "MODERATE": 2,
        "HIGH": 3,
        "PROHIBITED": 4
    }

    @classmethod
    def compile_tool_calls(cls, tool_calls: List[Dict[str, Any]]) -> ToolExecutionResult:
        """
        Validates a list of tool calls:
        [
          {"tool_id": "network.test_dns", "arguments": {"domain": "cloudflare.com"}}
        ]
        """
        compiled_actions = []
        highest_risk = "LOW"

        for call in tool_calls:
            tool_id = call.get("tool_id") or call.get("tool")
            if not tool_id:
                return ToolExecutionResult(
                    is_valid=False,
                    actions=[],
                    highest_risk="BLOCKED",
                    error_message="Tool call missing 'tool_id'."
                )

            tool = ToolRegistry.get(tool_id)
            if not tool:
                return ToolExecutionResult(
                    is_valid=False,
                    actions=[],
                    highest_risk="BLOCKED",
                    error_message=f"Unauthorized or unknown tool ID: '{tool_id}'."
                )

            args = call.get("arguments") or call.get("args") or {}

            # Strict parameter schema validation
            is_valid, err = tool.validate_args(args)
            if not is_valid:
                return ToolExecutionResult(
                    is_valid=False,
                    actions=[],
                    highest_risk="BLOCKED",
                    error_message=f"Validation failed for tool '{tool_id}': {err}"
                )

            # Build deterministic command & verification
            cmd = tool.build_command(args)
            verif = tool.build_verification(args)

            # Track risk level
            if cls.RISK_HIERARCHY.get(tool.risk, 1) > cls.RISK_HIERARCHY.get(highest_risk, 1):
                highest_risk = tool.risk

            action_item = {
                "tool_id": tool.tool_id,
                "description": tool.description,
                "command": cmd,
                "verification": verif,
                "risk": tool.risk,
                "requires_confirmation": tool.requires_confirmation,
                "recovery_info": tool.recovery_info
            }
            compiled_actions.append(action_item)

        return ToolExecutionResult(
            is_valid=True,
            actions=compiled_actions,
            highest_risk=highest_risk
        )
