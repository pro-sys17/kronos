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
    Enforces that registered ToolDefinition implementations are the only source of executable operations.
    """

    RISK_HIERARCHY = {
        "LOW": 1,
        "MODERATE": 2,
        "HIGH": 3,
        "PROHIBITED": 4
    }

    @classmethod
    def compile_tool_calls(cls, tool_calls: Any) -> ToolExecutionResult:
        """
        Validates a list of tool calls:
        [
          {"tool_id": "network.test_dns", "arguments": {"domain": "cloudflare.com"}}
        ]
        """
        if not isinstance(tool_calls, list):
            return ToolExecutionResult(
                is_valid=False,
                actions=[],
                highest_risk="BLOCKED",
                error_message="Tool calls must be provided as a list."
            )

        compiled_actions = []
        highest_risk = "LOW"

        for call in tool_calls:
            if not isinstance(call, dict):
                return ToolExecutionResult(
                    is_valid=False,
                    actions=[],
                    highest_risk="BLOCKED",
                    error_message="Each tool call entry must be a dictionary."
                )

            tool_id = call.get("tool_id") or call.get("tool")
            if not tool_id or not isinstance(tool_id, str) or not tool_id.strip():
                return ToolExecutionResult(
                    is_valid=False,
                    actions=[],
                    highest_risk="BLOCKED",
                    error_message="Tool call missing valid 'tool_id' string."
                )

            tool_id_clean = tool_id.strip()
            tool = ToolRegistry.get(tool_id_clean)
            if not tool:
                return ToolExecutionResult(
                    is_valid=False,
                    actions=[],
                    highest_risk="BLOCKED",
                    error_message=f"Unauthorized or unknown tool ID: '{tool_id_clean}'."
                )

            args = call.get("arguments") if "arguments" in call else call.get("args", {})
            if not isinstance(args, dict):
                return ToolExecutionResult(
                    is_valid=False,
                    actions=[],
                    highest_risk="BLOCKED",
                    error_message=f"Arguments for tool '{tool_id_clean}' must be a dictionary."
                )

            # Strict parameter schema validation (types, bounds, and unexpected argument rejection)
            is_valid, err = tool.validate_args(args)
            if not is_valid:
                return ToolExecutionResult(
                    is_valid=False,
                    actions=[],
                    highest_risk="BLOCKED",
                    error_message=f"Validation failed for tool '{tool_id_clean}': {err}"
                )

            # Build deterministic command & verification
            cmd = tool.build_command(args)
            verif = tool.build_verification(args)

            # Track risk level strictly from registered ToolDefinition
            tool_risk = tool.risk.upper()
            if cls.RISK_HIERARCHY.get(tool_risk, 1) > cls.RISK_HIERARCHY.get(highest_risk, 1):
                highest_risk = tool_risk

            # Clean resolved arguments with defaults
            resolved_args = {p_name: args.get(p_name, param.default) for p_name, param in tool.parameters.items()}

            action_item = {
                "tool_id": tool.tool_id,
                "tool_name": tool.name,
                "arguments": resolved_args,
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
