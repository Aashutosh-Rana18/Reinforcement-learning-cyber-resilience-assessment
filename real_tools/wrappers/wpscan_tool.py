from typing import List, Dict, Any
from real_tools.base_tool import BaseTool
class WPScanTool(BaseTool):
    def __init__(self): super().__init__("wpscan", "wpscan")
    def build_command(self, target: str, opts=None):
        return [self.binary_name, "--url", target, "--no-update", "--format", "json"]
    def parse_output(self, raw, rc):
        findings = []
        if rc == 4 or "database file is missing" in raw.lower():
            findings.append({"type": "wordpress", "detected": False})
            return findings
        if "WordPress" in raw: findings.append({"type": "wordpress", "detected": True})
        for line in raw.splitlines():
            if "CVE-" in line: findings.append({"type": "wordpress_vuln", "details": line.strip()})
        return findings
    def acceptable_return_codes(self): return [0, 4]