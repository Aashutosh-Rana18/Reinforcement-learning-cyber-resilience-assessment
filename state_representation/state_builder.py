"""32-Dimensional State Vector from Findings"""
import numpy as np
from typing import List, Dict, Any

class StateBuilder:
    def __init__(self, dim=32):
        self.dim = dim
        self.ports_found, self.tech_found, self.vulns_found = set(), set(), set()
        self.dirs_found, self.creds_found, self.tools_used = set(), [], []
        self.step_count = 0

    def reset(self):
        self.ports_found.clear(); self.tech_found.clear(); self.vulns_found.clear()
        self.dirs_found.clear(); self.creds_found.clear(); self.tools_used.clear(); self.step_count = 0

    def update(self, findings: List[Dict[str, Any]], tool_name: str):
        self.step_count += 1; self.tools_used.append(tool_name)
        for f in findings:
            t = f.get("type", "")
            if t == "open_port": self.ports_found.add(f.get("port", ""))
            elif t == "technology": self.tech_found.add(f.get("name", ""))
            elif t in ("sql_injection", "xss", "vulnerability", "wordpress_vuln"):
                import json; self.vulns_found.add(json.dumps(f, sort_keys=True))
            elif t == "directory": self.dirs_found.add(f.get("path", ""))
            elif t == "credentials": self.creds_found.append(f)

    def build(self) -> np.ndarray:
        state = np.zeros(self.dim, dtype=np.float32)
        state[0] = min(len(self.ports_found)/10.0, 1.0)
        state[1] = min(len(self.tech_found)/10.0, 1.0)
        state[2] = min(len(self.vulns_found)/5.0, 1.0)
        state[3] = min(len(self.dirs_found)/10.0, 1.0)
        state[4] = 1.0 if self.creds_found else 0.0
        state[5] = min(self.step_count/50.0, 1.0)
        if self.tools_used:
            from real_tools.tool_registry import ACTION_MAP
            aid = {v:k for k,v in ACTION_MAP.items()}.get(self.tools_used[-1], 0)
            if 6+aid < self.dim: state[6+aid] = 1.0
        state[18] = min(len(set(self.tools_used))/12.0, 1.0)
        state[19] = 1.0 if (self.ports_found or self.tech_found or self.vulns_found) else 0.0
        return state
