"""Prioritized Experience Replay"""
import numpy as np, torch

class SumTree:
    def __init__(self, capacity):
        self.capacity, self.tree, self.data = capacity, np.zeros(2*capacity-1), np.zeros(capacity, dtype=object)
        self.write, self.n_entries = 0, 0
    def _propagate(self, idx, change):
        parent = (idx-1)//2
        self.tree[parent] += change
        if parent != 0: self._propagate(parent, change)
    def _retrieve(self, idx, s):
        left = 2*idx+1
        if left >= len(self.tree): return idx
        return self._retrieve(left, s) if s <= self.tree[left] else self._retrieve(left+1, s-self.tree[left])
    def total(self): return self.tree[0]
    def add(self, priority, data):
        idx = self.write + self.capacity - 1
        self.data[self.write] = data
        self.update(idx, priority)
        self.write = (self.write+1) % self.capacity
        self.n_entries = min(self.n_entries+1, self.capacity)
    def update(self, idx, priority):
        change = priority - self.tree[idx]
        self.tree[idx] = priority
        self._propagate(idx, change)
    def get(self, s):
        idx = self._retrieve(0, s)
        return idx, self.tree[idx], self.data[idx - self.capacity + 1]

class PrioritizedReplayBuffer:
    def __init__(self, capacity, alpha=0.6):
        self.tree, self.alpha, self.epsilon = SumTree(capacity), alpha, 1e-6
    def add(self, transition):
        max_prio = self.tree.tree[:self.tree.capacity-1].max() if self.tree.n_entries > 0 else 1.0
        self.tree.add(max_prio, transition)
    def sample(self, batch_size, beta=0.4):
        batch, indices, priorities = [], [], []
        segment = self.tree.total() / batch_size
        for i in range(batch_size):
            idx, prio, data = self.tree.get(np.random.uniform(segment*i, segment*(i+1)))
            priorities.append(prio); batch.append(data); indices.append(idx)
        is_weights = np.power(self.tree.n_entries * np.array(priorities)/self.tree.total(), -beta)
        return batch, indices, is_weights / is_weights.max()
    def update_priorities(self, indices, priorities):
        for idx, prio in zip(indices, priorities): self.tree.update(idx, prio + self.epsilon)
    def __len__(self): return self.tree.n_entries
