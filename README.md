# CyberResilience RL v14 - Complete Real Tool Integration

> **NO SIMULATION. REAL TOOLS ONLY.**
>
> Full pentesting framework with Flask API, Streamlit Dashboard, JWT+OTP Auth, and 9 real security tools.

---

## Features

| Component | Status |
|-----------|--------|
| Flask Backend API | JWT + OTP Authentication |
| Streamlit Dashboard | Real-time visualization |
| Real Tool Execution | Nmap, SQLMap, Gobuster, Nikto, Hydra, WPScan, SearchSploit, WhatWeb, Dalfox |
| RL Agent | Dueling DQN + PER + N-step |
| Docker Support | Kali Linux + all tools |
| Render Deployment | Ready (API + Dashboard) |

---

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start API Server
```bash
python backend_api.py
# API runs on http://localhost:5000
```

### 3. Start Dashboard
```bash
streamlit run dashboard.py
# Dashboard runs on http://localhost:8501
```

### 4. Train with Real Tools (Docker)
```bash
# Build image with all pentesting tools
docker build -t cyber-rl .

# Train against Juice Shop
docker run -it --network=host   -v $(pwd)/checkpoints_real:/app/checkpoints_real   cyber-rl python use_tool.py   --target http://host.docker.internal:3000   --train --episodes 2000 --explicit-auth
```

### 5. Assess with Trained Model
```bash
docker run -it --network=host   -v $(pwd)/checkpoints_real:/app/checkpoints_real   cyber-rl python use_tool.py   --target http://host.docker.internal:3000   --model checkpoints_real/best_model.pt --explicit-auth
```

---

## API Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/` | GET | No | Service info |
| `/health` | GET | No | Health check |
| `/api/auth/register` | POST | No | User registration |
| `/api/auth/login` | POST | No | Login (returns OTP) |
| `/api/auth/verify-otp` | POST | No | Verify OTP (returns JWT) |
| `/api/attacks` | POST | JWT | Create attack |
| `/api/attacks` | GET | JWT | List attacks |
| `/api/attacks/<id>` | GET | JWT | Get attack details |
| `/api/attacks/<id>` | DELETE | JWT | Stop attack |
| `/api/real/assess` | POST | JWT | Execute real tools |

---

## Authentication Flow

1. **Register**: `POST /api/auth/register` → `{email, password}`
2. **Login**: `POST /api/auth/login` → `{email, password}` → Returns OTP
3. **Verify OTP**: `POST /api/auth/verify-otp` → `{user_id, otp}` → Returns JWT Token
4. **Use JWT**: Add `Authorization: Bearer <token>` header

---

## Project Structure

```
CyberResilience_v14_COMPLETE/
├── backend_api.py              # Flask API + JWT + OTP
├── dashboard.py                # Streamlit Dashboard
├── engine_bridge.py            # Real Tool Bridge
├── use_tool.py                 # Main Entry Point
├── config/
│   └── settings.py             # Configuration
├── environment/
│   └── real_cyber_env.py     # Real Tool Environment
├── real_tools/                 # 9 Real Tool Wrappers
│   ├── base_tool.py
│   ├── tool_registry.py
│   ├── tool_manager.py
│   └── wrappers/
│       ├── nmap_tool.py
│       ├── sqlmap_tool.py
│       ├── gobuster_tool.py
│       ├── nikto_tool.py
│       ├── hydra_tool.py
│       ├── wpscan_tool.py
│       ├── searchsploit_tool.py
│       ├── whatweb_tool.py
│       └── dalfox_tool.py
├── rl_agents/                  # Dueling DQN + PER
│   ├── neural_network.py
│   ├── replay_buffer.py
│   └── dqn_agent.py
├── state_representation/
│   └── state_builder.py        # 32-dim state vector
├── training/
│   └── train.py                # Training loop
├── utils/
│   ├── url_parser.py
│   ├── auth_verifier.py
│   ├── wordlist_resolver.py
│   ├── data_loader.py
│   ├── logger.py
│   └── visualization.py
├── wordlists/                  # Bundled wordlists
│   ├── common.txt
│   ├── rockyou.txt
│   └── users.txt
├── tests/
│   ├── test_environment.py
│   └── test_rl_agents.py
├── Dockerfile                  # Kali + all tools
├── docker-compose.yml
├── render.yaml                 # Render Blueprint
├── requirements.txt
└── README.md
```

---

## Render Deployment

**Note**: Training is done LOCALLY. Render only serves API + Dashboard.

1. Train locally, save model to `checkpoints_real/best_model.pt`
2. Push to GitHub
3. Connect repo on [Render](https://render.com)
4. Auto-deploy via `render.yaml`

---

## Legal Warning

> **REAL TOOLS EXECUTE ACTUAL ATTACKS**
> 
> ONLY use on systems you own or have written authorization to test.
> Unauthorized testing is a CRIMINAL OFFENSE.

---

## Version

**v14.0.0** - Complete Real Tool Integration
