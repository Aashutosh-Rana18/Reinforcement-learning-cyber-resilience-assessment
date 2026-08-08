import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
def plot_rewards(rewards: list, path: str = "rewards.png"):
    plt.figure(figsize=(10,5)); plt.plot(rewards); plt.title("Episode Rewards"); plt.xlabel("Episode"); plt.ylabel("Reward"); plt.savefig(path); plt.close()