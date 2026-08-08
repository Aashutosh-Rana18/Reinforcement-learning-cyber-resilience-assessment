"""Real Tool Execution Environment - NO SIMULATION"""
import numpy as np
from typing import Dict, List, Tuple, Any
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import settings
from real_tools.tool_manager import ToolManager
from real_tools.tool_registry import ACTION_MAP
from state_representation.state_builder import StateBuilder
from utils.auth_verifier import require_auth

class RealCyberEnv:
    def __init__(self, target_url: str, config: Dict[str, Any] = None):
        self.target_url = target_url
        self.config = config or {}
        self.max_steps = self.config.get("max_steps", settings.MAX_STEPS)
        self.tool_manager = ToolManager()
        self.state_builder = StateBuilder(settings.STATE_DIM)
        self.action_map = ACTION_MAP
        self.reset()

    def reset(self) -> np.ndarray:
        self.step_count = 0; self.episode_reward = 0.0
        self.state_builder.reset(); self.tool_manager.reset_history()
        require_auth(self.target_url)
        return self.state_builder.build()

    def step(self, action: int) -> Tuple[np.ndarray, float, bool, Dict]:
        self.step_count += 1
        action_name = self.action_map.get(action, "nmap")
        reward = settings.BASE_REWARD
        done = False
        info = {"action": action_name, "findings": [], "raw": ""}

        result = self.tool_manager.execute(action, self.target_url)
        info["findings"] = result.findings
        info["raw"] = result.raw_output[:500]
        info["exec_time"] = result.execution_time
        info["success"] = result.success

        if result.success and action_name != "stop_assessment":
            reward += settings.EXPLORATION_BONUS
            for f in result.findings:
                sev = f.get("severity", "info")
                if sev == "critical": reward += settings.CRITICAL_REWARD
                elif sev == "high": reward += settings.FINDING_REWARD * 2
                else: reward += settings.FINDING_REWARD

        self.state_builder.update(result.findings, action_name)
        self.episode_reward += reward

        if action_name == "stop_assessment" or self.step_count >= self.max_steps:
            done = True
            if self.step_count >= self.max_steps: reward += settings.MAX_STEPS_PENALTY

        return self.state_builder.build(), reward, done, info
