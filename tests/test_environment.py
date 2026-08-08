"""Tests for Real Environment"""
import unittest, numpy as np, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from real_tools.tool_registry import NUM_ACTIONS, ACTION_MAP
from config import settings

class TestToolRegistry(unittest.TestCase):
    def test_actions(self):
        self.assertEqual(NUM_ACTIONS, 12)
        self.assertIn(0, ACTION_MAP)
        self.assertEqual(ACTION_MAP[0], "nmap")

class TestConfig(unittest.TestCase):
    def test_settings(self):
        self.assertEqual(settings.STATE_DIM, 32)
        self.assertEqual(settings.NUM_ACTIONS, 12)

class TestDQNAgent(unittest.TestCase):
    def test_creation(self):
        from rl_agents.dqn_agent import DQNAgent
        agent = DQNAgent(settings.STATE_DIM, 12)
        self.assertIsNotNone(agent.policy_net)
    def test_action(self):
        from rl_agents.dqn_agent import DQNAgent
        agent = DQNAgent(settings.STATE_DIM, 12)
        state = np.random.random(settings.STATE_DIM).astype(np.float32)
        action = agent.select_action(state, training=False)
        self.assertIn(action, range(12))

if __name__ == "__main__": unittest.main()
