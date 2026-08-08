"""Double DQN Agent with PER and N-step Returns"""
import torch, torch.nn as nn, torch.optim as optim, numpy as np
from collections import deque
from rl_agents.neural_network import DuelingDQN
from rl_agents.replay_buffer import PrioritizedReplayBuffer
from config import settings

class DQNAgent:
    def __init__(self, state_dim, action_dim, lr=None, gamma=None, epsilon=None):
        self.state_dim, self.action_dim = state_dim, action_dim
        self.lr, self.gamma = lr or settings.LEARNING_RATE, gamma or settings.GAMMA
        self.epsilon, self.epsilon_min, self.epsilon_decay = epsilon or settings.EPSILON_START, settings.EPSILON_MIN, settings.EPSILON_DECAY
        self.batch_size, self.n_step = settings.BATCH_SIZE, settings.N_STEP
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.policy_net = DuelingDQN(state_dim, action_dim).to(self.device)
        self.target_net = DuelingDQN(state_dim, action_dim).to(self.device)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.eval()
        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=self.lr)
        self.memory = PrioritizedReplayBuffer(settings.BUFFER_SIZE)
        self.n_step_buffer = deque(maxlen=self.n_step)
        self.steps_done = 0

    def select_action(self, state, training=True):
        if training and np.random.random() < self.epsilon:
            return np.random.randint(self.action_dim)
        with torch.no_grad():
            return self.policy_net(torch.FloatTensor(state).unsqueeze(0).to(self.device)).argmax().item()

    def store_transition(self, state, action, reward, next_state, done):
        self.n_step_buffer.append((state, action, reward, next_state, done))
        if len(self.n_step_buffer) < self.n_step: return
        R = sum([self.n_step_buffer[i][2] * (self.gamma ** i) for i in range(self.n_step)])
        s0, a0, _, _, _ = self.n_step_buffer[0]
        _, _, _, sN, dN = self.n_step_buffer[-1]
        self.memory.add((s0, a0, R, sN, dN))

    def learn(self):
        if len(self.memory) < settings.LEARNING_STARTS: return 0.0
        batch, indices, is_weights = self.memory.sample(self.batch_size)
        states = torch.FloatTensor([t[0] for t in batch]).to(self.device)
        actions = torch.LongTensor([t[1] for t in batch]).to(self.device)
        rewards = torch.FloatTensor([t[2] for t in batch]).to(self.device)
        next_states = torch.FloatTensor([t[3] for t in batch]).to(self.device)
        dones = torch.FloatTensor([t[4] for t in batch]).to(self.device)
        is_weights_t = torch.FloatTensor(is_weights).to(self.device)
        q_values = self.policy_net(states).gather(1, actions.unsqueeze(1)).squeeze(1)
        with torch.no_grad():
            next_actions = self.policy_net(next_states).argmax(1)
            next_q = self.target_net(next_states).gather(1, next_actions.unsqueeze(1)).squeeze(1)
            target_q = rewards + (self.gamma ** self.n_step) * next_q * (1 - dones)
        td_errors = torch.abs(q_values - target_q).detach().cpu().numpy()
        loss = (is_weights_t * nn.functional.mse_loss(q_values, target_q, reduction='none')).mean()
        self.optimizer.zero_grad(); loss.backward(); torch.nn.utils.clip_grad_norm_(self.policy_net.parameters(), 10); self.optimizer.step()
        self.memory.update_priorities(indices, td_errors)
        self.epsilon = max(self.epsilon_min, self.epsilon - (1.0 - self.epsilon_min) / self.epsilon_decay)
        self.steps_done += 1
        if self.steps_done % settings.TARGET_UPDATE_FREQ == 0:
            self.target_net.load_state_dict(self.policy_net.state_dict())
        return loss.item()

    def save(self, path):
        torch.save({"policy": self.policy_net.state_dict(), "target": self.target_net.state_dict(),
                    "optimizer": self.optimizer.state_dict(), "epsilon": self.epsilon, "steps": self.steps_done}, path)

    def load(self, path):
        ckpt = torch.load(path, map_location=self.device)
        self.policy_net.load_state_dict(ckpt["policy"])
        self.target_net.load_state_dict(ckpt["target"])
        self.optimizer.load_state_dict(ckpt["optimizer"])
        self.epsilon = ckpt.get("epsilon", self.epsilon)
        self.steps_done = ckpt.get("steps", 0)
