"""Training Loop - Real Tools Only"""
import os, sys, numpy as np
from collections import deque
from config import settings
from rl_agents.dqn_agent import DQNAgent
from real_tools.tool_registry import NUM_ACTIONS

def train(env, episodes=None, checkpoint_dir=None, verbose=True):
    episodes = episodes or settings.EPISODES
    checkpoint_dir = checkpoint_dir or settings.CHECKPOINT_DIR
    os.makedirs(checkpoint_dir, exist_ok=True)

    agent = DQNAgent(settings.STATE_DIM, NUM_ACTIONS)
    best_reward = -float("inf")
    reward_window = deque(maxlen=50)
    all_rewards = []

    print(f"\n{'='*60}")
    print(f"Training REAL Mode | Episodes: {episodes} | Device: {agent.device}")
    print(f"Target: {env.target_url}")
    print(f"{'='*60}\n")

    for ep in range(1, episodes + 1):
        state = env.reset()
        ep_reward, ep_loss, step_count, done = 0.0, 0.0, 0, False

        while not done:
            action = agent.select_action(state, training=True)
            next_state, reward, done, info = env.step(action)
            agent.store_transition(state, action, reward, next_state, done)
            loss = agent.learn()
            if loss > 0: ep_loss += loss
            state = next_state; ep_reward += reward; step_count += 1

        reward_window.append(ep_reward)
        avg_reward = np.mean(reward_window)
        all_rewards.append(ep_reward)

        if ep_reward > best_reward:
            best_reward = ep_reward
            agent.save(os.path.join(checkpoint_dir, "best_model.pt"))

        if ep % 100 == 0:
            agent.save(os.path.join(checkpoint_dir, f"checkpoint_{ep}.pt"))

        if verbose and ep % 10 == 0:
            print(f"Ep {ep:5d} | Reward: {ep_reward:8.1f} | Avg50: {avg_reward:8.1f} | "
                  f"Steps: {step_count:2d} | Eps: {agent.epsilon:.3f} | Findings: {len(info.get('findings', []))}")

    agent.save(os.path.join(checkpoint_dir, "final_model.pt"))
    print(f"\n{'='*60}")
    print(f"Training Complete! Best Reward: {best_reward:.1f}")
    print(f"Models saved to: {checkpoint_dir}")
    print(f"{'='*60}")
    return agent, all_rewards
