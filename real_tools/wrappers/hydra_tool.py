from typing import List, Dict, Any
from real_tools.base_tool import BaseTool
from utils.wordlist_resolver import resolve_wordlist
class HydraTool(BaseTool):
    def __init__(self): super().__init__("hydra", "hydra")
    def build_command(self, target: str, opts=None):
        opts = opts or {}
        host = target.replace("http://","").replace("https://","").split("/")[0]
        if ":" in host: hostname, port = host.split(":")
        else: hostname, port = host, "80"
        userlist = resolve_wordlist("users.txt")
        passlist = resolve_wordlist("rockyou.txt")
        login_path = opts.get("login_path", "/login")
        form = opts.get("form_params", "username=^USER^&password=^PASS^:F=Invalid")
        return [self.binary_name, "-L", userlist, "-P", passlist, "-s", port, "-t", "16", "-f", hostname, "http-post-form", f"{login_path}:{form}"]
    def parse_output(self, raw, rc):
        findings = []
        for line in raw.splitlines():
            if "login:" in line.lower() and "password:" in line.lower():
                findings.append({"type": "credentials", "severity": "critical", "details": line.strip()})
        return findings
    def acceptable_return_codes(self): return [0, 255]