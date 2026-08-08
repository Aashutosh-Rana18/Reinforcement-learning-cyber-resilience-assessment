from typing import List, Dict, Any
from real_tools.base_tool import BaseTool
class NmapTool(BaseTool):
    def __init__(self): super().__init__("nmap", "nmap")
    def build_command(self, target: str, opts=None):
        opts = opts or {}
        host = target.replace("http://","").replace("https://","").split(":")[0].split("/")[0]
        cmd = [self.binary_name, "-sV", "-sC", "--top-ports", "100", "-T4", "-Pn", host]
        if opts.get("full"): cmd = [self.binary_name, "-sV", "-sC", "-p-", "-T4", "-Pn", host]
        return cmd
    def parse_output(self, raw, rc):
        findings = []
        for line in raw.splitlines():
            if "/tcp" in line and "open" in line:
                parts = line.split()
                findings.append({"type": "open_port", "port": parts[0].split("/")[0], "service": " ".join(parts[2:])})
            if "OS details:" in line:
                findings.append({"type": "os_fingerprint", "os": line.split(":",1)[1].strip()})
        return findings