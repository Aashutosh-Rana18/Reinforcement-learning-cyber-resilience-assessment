"""Tool Registry - 12 Actions to 9 Real Tools"""
from typing import Dict, Type
from real_tools.base_tool import BaseTool

def import_tools():
    from real_tools.wrappers.nmap_tool import NmapTool
    from real_tools.wrappers.sqlmap_tool import SQLMapTool
    from real_tools.wrappers.gobuster_tool import GobusterTool
    from real_tools.wrappers.nikto_tool import NiktoTool
    from real_tools.wrappers.hydra_tool import HydraTool
    from real_tools.wrappers.wpscan_tool import WPScanTool
    from real_tools.wrappers.searchsploit_tool import SearchSploitTool
    from real_tools.wrappers.whatweb_tool import WhatWebTool
    from real_tools.wrappers.dalfox_tool import DalfoxTool
    return {
        "nmap": NmapTool, "sqlmap": SQLMapTool, "gobuster": GobusterTool,
        "nikto": NiktoTool, "hydra": HydraTool, "wpscan": WPScanTool,
        "searchsploit": SearchSploitTool, "whatweb": WhatWebTool, "dalfox": DalfoxTool,
    }

ACTION_MAP = {
    0: "nmap", 1: "sqlmap", 2: "gobuster", 3: "nikto",
    4: "hydra", 5: "wpscan", 6: "searchsploit", 7: "whatweb",
    8: "dalfox", 9: "recon_combo", 10: "web_combo", 11: "stop_assessment",
}

NUM_ACTIONS = len(ACTION_MAP)
