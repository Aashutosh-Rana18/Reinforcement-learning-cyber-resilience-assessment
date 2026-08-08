#!/usr/bin/env python3
"""Engine Bridge - Connects Original Engine to Real Tools"""
import os, sys, logging
from typing import Dict, List, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class ToolResult:
    success: bool
    findings: List[Dict[str, Any]]
    raw_output: str
    execution_time: float
    tool_name: str

class RealToolBridge:
    def __init__(self):
        self.tool_registry = {}
        self._init_tools()

    def _init_tools(self):
        try:
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'real_tools'))
            from real_tools.tool_manager import ToolManager
            self.tool_manager = ToolManager()
            self.available = True
            logger.info("Real tool bridge initialized")
        except Exception as e:
            logger.warning(f"Real tools not available: {e}")
            self.available = False

    def execute_tool(self, action_id: int, target: str, opts: Dict = None) -> ToolResult:
        if not self.available:
            return ToolResult(False, [], "Tools not available", 0.0, "none")
        try:
            from real_tools.tool_registry import ACTION_MAP
            result = self.tool_manager.execute(action_id, target, opts or {})
            return ToolResult(result.success, result.findings, result.raw_output[:1000], result.execution_time, ACTION_MAP.get(action_id, "unknown"))
        except Exception as e:
            logger.error(f"Tool execution failed: {e}")
            return ToolResult(False, [], str(e), 0.0, "error")

_bridge = None
def get_bridge():
    global _bridge
    if _bridge is None: _bridge = RealToolBridge()
    return _bridge
