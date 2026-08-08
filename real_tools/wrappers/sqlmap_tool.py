from typing import List, Dict, Any
from real_tools.base_tool import BaseTool
class SQLMapTool(BaseTool):
    def __init__(self): super().__init__("sqlmap", "sqlmap")
    def build_command(self, target: str, opts=None):
        opts = opts or {}
        endpoint = opts.get("endpoint", "")
        url = target.rstrip("/") + "/" + endpoint.lstrip("/") if endpoint else target
        cmd = [self.binary_name, "-u", url, "--batch", "--level=1", "--risk=1", "--random-agent", "-v", "0"]
        if opts.get("forms"): cmd.extend(["--forms"])
        if opts.get("crawl"): cmd.extend(["--crawl=2"])
        return cmd
    def parse_output(self, raw, rc):
        findings = []
        if "is vulnerable" in raw.lower() or "sqlmap identified" in raw.lower():
            findings.append({"type": "sql_injection", "severity": "critical", "details": raw[:500]})
        return findings
    def acceptable_return_codes(self): return [0, 1]