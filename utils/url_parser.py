from urllib.parse import urlparse
from typing import Tuple
def parse_target(url: str) -> Tuple[str, str, int]:
    p = urlparse(url)
    return url, p.hostname or "localhost", p.port or (443 if p.scheme == "https" else 80)