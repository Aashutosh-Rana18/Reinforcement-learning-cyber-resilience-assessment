from typing import List, Dict, Any
from real_tools.base_tool import BaseTool
class NiktoTool(BaseTool):
    def __init__(self): super().__init__("nikto", "nikto")
    def build_command(self, target: str, opts=None):
        return [self.binary_name, "-h", target, "-maxtime", "120s"]
    def parse_output(self, raw, rc):
        findings = []
        for line in raw.splitlines():
            if "OSVDB" in line or "CVE-" in line or "vulnerable" in line.lower():
                findings.append({"type": "vulnerability", "source": "nikto", "details": line.strip()})
        return findings