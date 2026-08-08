from typing import List, Dict, Any
from real_tools.base_tool import BaseTool
from utils.wordlist_resolver import resolve_wordlist
class GobusterTool(BaseTool):
    def __init__(self): super().__init__("gobuster", "gobuster")
    def build_command(self, target: str, opts=None):
        wordlist = resolve_wordlist("common.txt")
        cmd = [self.binary_name, "dir", "-u", target, "-w", wordlist, "-t", "50", "-q", "--no-error", "--exclude-length", "9903"]
        if opts and opts.get("extensions"): cmd.extend(["-x", opts["extensions"]])
        return cmd
    def parse_output(self, raw, rc):
        findings = []
        for line in raw.splitlines():
            if "Status:" in line:
                parts = line.split()
                findings.append({"type": "directory", "path": parts[0], "status": line.split("Status:")[1].split()[0]})
        return findings