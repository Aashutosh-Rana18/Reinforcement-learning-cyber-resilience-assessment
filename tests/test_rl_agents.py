"""Tests for RL Agents"""
import unittest, numpy as np, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rl_agents.dqn_agent import DQNAgent
from rl_agents.neural_network import DuelingDQN
from config import settings

class TestNeuralNetwork(unittest.TestCase):
    def test_forward(self):
        import torch
        net = DuelingDQN(32, 12)
        x = torch.randn(1, 32)
        out = net(x)
        self.assertEqual(out.shape, (1, 12))

if __name__ == "__main__": unittest.main()
