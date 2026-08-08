#!/usr/bin/env python3
"""CyberResilience RL v14 - Main Entry Point (REAL ONLY)"""
import argparse, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import settings
from rl_agents.dqn_agent import DQNAgent
from training.train import train
from real_tools.tool_registry import NUM_ACTIONS

def get_env(target: str):
    from environment.real_cyber_env import RealCyberEnv
    return RealCyberEnv(target, {"max_steps": settings.MAX_STEPS})

def main():
    parser = argparse.ArgumentParser(description="CyberResilience RL v14 - Real Tools Only")
    parser.add_argument("--target", default=settings.TARGET_URL)
    parser.add_argument("--train", action="store_true")
    parser.add_argument("--episodes", type=int, default=None)
    parser.add_argument("--model", type=str, default=None, help="Load model for assessment")
    parser.add_argument("--explicit-auth", action="store_true")
    parser.add_argument("--max-steps", type=int, default=None)
    parser.add_argument("--api", action="store_true", help="Start API server")
    parser.add_argument("--dashboard", action="store_true", help="Start Streamlit dashboard")
    args = parser.parse_args()

    if args.api:
        print("Starting API Server...")
        os.system("python backend_api.py")
        return

    if args.dashboard:
        print("Starting Dashboard...")
        os.system("streamlit run dashboard.py")
        return

    if not args.explicit_auth:
        print("\n" + "="*60)
        print("ERROR: Real mode requires --explicit-auth flag")
        print("You MUST have written authorization to test the target.")
        print("="*60 + "\n")
        sys.exit(1)

    if args.max_steps: settings.MAX_STEPS = args.max_steps
    if args.episodes: settings.EPISODES = args.episodes

    env = get_env(args.target)

    if args.train:
        agent, rewards = train(env, episodes=args.episodes)
        try:
            from utils.visualization import plot_rewards
            plot_rewards(rewards, "training_rewards_real.png")
            print("Saved training_rewards_real.png")
        except: pass
    elif args.model:
        print(f"\nLoading model: {args.model}")
        agent = DQNAgent(settings.STATE_DIM, NUM_ACTIONS)
        agent.load(args.model); agent.epsilon = 0.0
        state = env.reset(); done = False; total_reward = 0.0; step = 0
        print(f"\n{'='*60}")
        print(f"ASSESSMENT | Target: {args.target} | Model: {args.model}")
        print(f"{'='*60}\n")
        while not done:
            action = agent.select_action(state, training=False)
            state, reward, done, info = env.step(action)
            total_reward += reward; step += 1
            print(f"Step {step:2d} | Action: {info['action']:15s} | Reward: {reward:8.1f} | Findings: {len(info['findings'])}")
            if info.get('findings'):
                for f in info['findings'][:3]: print(f"         -> {f}")
        print(f"\nComplete! Total Reward: {total_reward:.1f} | Steps: {step}")
    else:
        print("Usage:")
        print("  python use_tool.py --train --target URL --explicit-auth")
        print("  python use_tool.py --model checkpoints_real/best_model.pt --target URL --explicit-auth")
        print("  python use_tool.py --api")
        print("  python use_tool.py --dashboard")

if __name__ == "__main__":
    main()
