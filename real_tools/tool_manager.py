"""Tool Manager - Deduplicated Findings"""
import hashlib, json
from typing import Dict, List, Any
from real_tools.base_tool import BaseTool, ToolResult
from real_tools.tool_registry import import_tools, ACTION_MAP

class ToolManager:
    def __init__(self):
        self.tools: Dict[str, BaseTool] = {}
        self.findings_history: set = set()
        for name, cls in import_tools().items():
            self.tools[name] = cls()

    def execute(self, action_id: int, target: str, opts: Dict[str, Any] = None) -> ToolResult:
        action_name = ACTION_MAP.get(action_id, "nmap")
        if action_name == "stop_assessment":
            return ToolResult(True, [{"type": "stop", "info": "Assessment stopped"}], "", 0.0, 0)
        if action_name in ("recon_combo", "web_combo"):
            return self._run_combo(action_name, target, opts)
        tool = self.tools.get(action_name)
        if not tool:
            return ToolResult(False, [], "", 0.0, -1, "Unknown tool")
        result = tool.run(target, opts)
        result.findings = self._dedup(result.findings)
        return result

    def _run_combo(self, combo_name: str, target: str, opts: Dict[str, Any] = None) -> ToolResult:
        tools_to_run = ["nmap", "whatweb"] if combo_name == "recon_combo" else ["gobuster", "nikto", "dalfox"]
        all_findings, all_raw, total_time = [], [], 0.0
        for tname in tools_to_run:
            r = self.tools[tname].run(target, opts)
            all_findings.extend(self._dedup(r.findings))
            all_raw.append(r.raw_output)
            total_time += r.execution_time
        return ToolResult(True, all_findings, "\n".join(all_raw), total_time, 0)

    def _dedup(self, findings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        unique = []
        for f in findings:
            key = hashlib.md5(json.dumps(f, sort_keys=True).encode()).hexdigest()
            if key not in self.findings_history:
                self.findings_history.add(key)
                unique.append(f)
        return unique

    def reset_history(self):
        self.findings_history.clear()
