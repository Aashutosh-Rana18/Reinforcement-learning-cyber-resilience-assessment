from typing import List, Dict, Any
from real_tools.base_tool import BaseTool
class DalfoxTool(BaseTool):
    def __init__(self): super().__init__("dalfox", "dalfox")
    def build_command(self, target: str, opts=None):
        opts = opts or {}
        endpoint = opts.get("endpoint", "")
        url = target.rstrip("/") + "/" + endpoint.lstrip("/") if endpoint else target
        return [self.binary_name, "url", url, "--silence"]
    def parse_output(self, raw, rc):
        findings = []
        if "xss" in raw.lower() or "vulnerable" in raw.lower():
            findings.append({"type": "xss", "severity": "high", "details": raw[:300]})
        return findings