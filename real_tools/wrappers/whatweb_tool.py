from typing import List, Dict, Any
from real_tools.base_tool import BaseTool
class WhatWebTool(BaseTool):
    def __init__(self): super().__init__("whatweb", "whatweb")
    def build_command(self, target: str, opts=None):
        return [self.binary_name, "--colour=never", target]
    def parse_output(self, raw, rc):
        findings = []
        for line in raw.splitlines():
            if "[" in line and "]" in line:
                findings.append({"type": "technology", "name": line.strip()})
        for tech in ["WordPress", "Apache", "nginx", "PHP", "React", "Node.js"]:
            if tech in raw: findings.append({"type": "technology", "name": tech})
        return findings