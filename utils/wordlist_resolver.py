import os
from pathlib import Path
PROJECT_DIR = Path(__file__).parent.parent
WORDLIST_DIR = PROJECT_DIR / "wordlists"
SYSTEM_PATHS = {
    "common.txt": ["/usr/share/wordlists/dirb/common.txt", "/usr/share/seclists/Discovery/Web-Content/common.txt"],
    "rockyou.txt": ["/usr/share/wordlists/rockyou.txt"],
    "users.txt": ["/usr/share/wordlists/metasploit/default_users.txt"],
}
def resolve_wordlist(name: str) -> str:
    bundled = WORDLIST_DIR / name
    if bundled.exists(): return str(bundled)
    for path in SYSTEM_PATHS.get(name, []):
        if os.path.exists(path): return path
    fallback = WORDLIST_DIR / name
    fallback.parent.mkdir(parents=True, exist_ok=True)
    lines = {"common.txt": ["admin","login","api","test","dev","config","backup",".env","robots.txt","wp-admin"],
             "rockyou.txt": ["password","123456","admin","qwerty","letmein","password123","admin123","welcome","monkey","dragon"],
             "users.txt": ["admin","root","user","test","guest","administrator","demo","support","service","manager"]}.get(name, ["test"])
    with open(fallback, "w") as f: f.write("\n".join(lines) + "\n")
    return str(fallback)