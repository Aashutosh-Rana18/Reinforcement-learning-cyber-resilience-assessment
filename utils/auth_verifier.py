import socket, urllib.request
def verify_target(url: str, timeout=10) -> bool:
    try:
        req = urllib.request.Request(url, method="HEAD")
        req.add_header("User-Agent", "CyberResilience-RL/1.0")
        with urllib.request.urlopen(req, timeout=timeout) as resp: return resp.status < 500
    except: pass
    try:
        from urllib.parse import urlparse
        p = urlparse(url)
        with socket.create_connection((p.hostname or "localhost", p.port or 80), timeout=timeout): return True
    except: return False
def require_auth(url: str):
    if not verify_target(url): raise ConnectionError(f"Target {url} unreachable. Start target first.")