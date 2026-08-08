"""Base Tool - Real Subprocess Execution"""
import subprocess, logging, time
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

logging.basicConfig(level=logging.INFO, format="[%(name)s] %(message)s")

@dataclass
class ToolResult:
    success: bool
    findings: List[Dict[str, Any]]
    raw_output: str
    execution_time: float
    return_code: int
    error: Optional[str] = None

class BaseTool:
    def __init__(self, name: str, binary_name: str):
        self.name = name
        self.binary_name = binary_name
        self.logger = logging.getLogger(name)

    def build_command(self, target: str, opts: Dict[str, Any] = None) -> List[str]:
        raise NotImplementedError

    def parse_output(self, raw: str, rc: int) -> List[Dict[str, Any]]:
        raise NotImplementedError

    def run(self, target: str, opts: Dict[str, Any] = None, timeout: int = 300) -> ToolResult:
        opts = opts or {}
        try:
            cmd = self.build_command(target, opts)
            self.logger.info(f"EXECUTING: {' '.join(cmd)}")
            start = time.time()
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            elapsed = time.time() - start
            raw = proc.stdout + proc.stderr
            self.logger.info(f"DONE in {elapsed:.2f}s | RC={proc.returncode} | Output: {raw[:200]}...")
            if proc.returncode not in self.acceptable_return_codes():
                return ToolResult(False, [], raw, elapsed, proc.returncode, f"Exit code {proc.returncode}")
            findings = self.parse_output(raw, proc.returncode)
            return ToolResult(True, findings, raw, elapsed, proc.returncode)
        except subprocess.TimeoutExpired:
            self.logger.error(f"TIMEOUT after {timeout}s")
            return ToolResult(False, [], "", timeout, -1, "Timeout")
        except FileNotFoundError:
            self.logger.error(f"Binary '{self.binary_name}' not found")
            return ToolResult(False, [], "", 0.0, -1, f"{self.binary_name} not installed")
        except Exception as e:
            self.logger.error(f"Exception: {e}")
            return ToolResult(False, [], str(e), 0.0, -1, str(e))

    def acceptable_return_codes(self):
        return [0]
