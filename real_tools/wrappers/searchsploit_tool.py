from typing import List, Dict, Any
from real_tools.base_tool import BaseTool
class SearchSploitTool(BaseTool):
    def __init__(self): super().__init__("searchsploit", "searchsploit")
    def build_command(self, target: str, opts=None):
        opts = opts or {}
        return [self.binary_name, opts.get("keyword", "apache"), "--json"]
    def parse_output(self, raw, rc):
        findings = []
        try:
            import json
            data = json.loads(raw)
            for item in data.get("RESULTS_EXPLOIT", [])[:5]:
                findings.append({"type": "exploit", "title": item.get("Title"), "path": item.get("Path"), "severity": "high"})
        except: pass
        return findings