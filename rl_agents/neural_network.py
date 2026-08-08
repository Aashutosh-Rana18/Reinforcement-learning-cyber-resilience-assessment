"""Dueling DQN with Noisy Nets"""
import torch, torch.nn as nn, torch.nn.functional as F, numpy as np

class NoisyLinear(nn.Module):
    def __init__(self, in_features, out_features, sigma_init=0.017):
        super().__init__()
        self.in_features, self.out_features = in_features, out_features
        self.weight_mu = nn.Parameter(torch.empty(out_features, in_features))
        self.weight_sigma = nn.Parameter(torch.empty(out_features, in_features))
        self.bias_mu = nn.Parameter(torch.empty(out_features))
        self.bias_sigma = nn.Parameter(torch.empty(out_features))
        self.sigma_init = sigma_init
        self.reset_parameters()
    def reset_parameters(self):
        mu_range = 1 / np.sqrt(self.in_features)
        self.weight_mu.data.uniform_(-mu_range, mu_range)
        self.weight_sigma.data.fill_(self.sigma_init / np.sqrt(self.in_features))
        self.bias_mu.data.uniform_(-mu_range, mu_range)
        self.bias_sigma.data.fill_(self.sigma_init / np.sqrt(self.out_features))
    def forward(self, x):
        weight = self.weight_mu + self.weight_sigma * torch.randn_like(self.weight_sigma)
        bias = self.bias_mu + self.bias_sigma * torch.randn_like(self.bias_sigma)
        return F.linear(x, weight, bias)

class DuelingDQN(nn.Module):
    def __init__(self, state_dim, action_dim):
        super().__init__()
        self.feature = nn.Sequential(nn.Linear(state_dim, 256), nn.ReLU(), nn.Linear(256, 256), nn.ReLU())
        self.value_stream = nn.Sequential(NoisyLinear(256, 128), nn.ReLU(), NoisyLinear(128, 1))
        self.advantage_stream = nn.Sequential(NoisyLinear(256, 128), nn.ReLU(), NoisyLinear(128, action_dim))
    def forward(self, x):
        features = self.feature(x)
        return self.value_stream(features) + (self.advantage_stream(features) - self.advantage_stream(features).mean(dim=1, keepdim=True))
