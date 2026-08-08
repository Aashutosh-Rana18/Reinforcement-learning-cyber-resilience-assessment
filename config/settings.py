"""Configuration - REAL ONLY Mode"""
import os

MODE = os.getenv("CYBER_RL_MODE", "real")
TARGET_URL = os.getenv("TARGET_URL", "http://localhost:3000")

EPISODES = int(os.getenv("EPISODES", "2000"))
MAX_STEPS = int(os.getenv("MAX_STEPS", "50"))
LEARNING_RATE = float(os.getenv("LR", "3e-4"))
GAMMA = float(os.getenv("GAMMA", "0.99"))
EPSILON_START = float(os.getenv("EPS_START", "1.0"))
EPSILON_MIN = float(os.getenv("EPS_MIN", "0.05"))
EPSILON_DECAY = int(os.getenv("EPS_DECAY", "10000"))
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "64"))
BUFFER_SIZE = int(os.getenv("BUFFER_SIZE", "100000"))
LEARNING_STARTS = int(os.getenv("LEARNING_STARTS", "500"))
TARGET_UPDATE_FREQ = int(os.getenv("TARGET_UPDATE", "1000"))
N_STEP = int(os.getenv("N_STEP", "3"))

BASE_REWARD = float(os.getenv("BASE_REWARD", "-0.1"))
FINDING_REWARD = float(os.getenv("FINDING_REWARD", "10.0"))
CRITICAL_REWARD = float(os.getenv("CRITICAL_REWARD", "50.0"))
DUPLICATE_PENALTY = float(os.getenv("DUP_PENALTY", "-0.5"))
MAX_STEPS_PENALTY = float(os.getenv("MAX_STEPS_PEN", "-5.0"))
EXPLORATION_BONUS = float(os.getenv("EXP_BONUS", "1.0"))

STATE_DIM = 32
NUM_ACTIONS = 12

CHECKPOINT_DIR = os.getenv("CHECKPOINT_DIR", "checkpoints_real")
os.makedirs(CHECKPOINT_DIR, exist_ok=True)

WORDLIST_DIR = os.path.join(os.path.dirname(__file__), "..", "wordlists")

API_PORT = int(os.getenv("API_PORT", "5000"))
API_HOST = os.getenv("API_HOST", "0.0.0.0")
SECRET_KEY = os.getenv("SECRET_KEY", "cyber-resilience-secret-key-2024")
JWT_SECRET = os.getenv("JWT_SECRET", "jwt-secret-key-2024")
