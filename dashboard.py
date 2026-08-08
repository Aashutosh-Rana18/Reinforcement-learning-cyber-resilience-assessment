#!/usr/bin/env python3
"""Interactive Pentesting Dashboard - Streamlit with Plotly"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import requests
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(page_title="CyberResilience RL v14", page_icon="🔐", layout="wide")

st.markdown("""
<style>
.main-header { font-size: 2.5rem; font-weight: bold; color: #667eea; }
.metric-card { background: #1e293b; padding: 20px; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

API_BASE = "http://localhost:5000"

if 'attack_id' not in st.session_state: st.session_state.attack_id = None

with st.sidebar:
    st.header("⚙️ Control Panel")
    target_url = st.text_input("Target URL", value="http://host.docker.internal:3000")
    mode = st.selectbox("Mode", ["real"], index=0)
    episodes = st.slider("Episodes", 100, 5000, 2000, 100)
    explicit_auth = st.checkbox("I have authorization", value=False)

    if st.button("Start Assessment", use_container_width=True):
        if not explicit_auth:
            st.error("Authorization required for real tools!")
        else:
            st.success(f"Assessment config ready!\nRun: python use_tool.py --mode real --target {target_url} --train --episodes {episodes} --explicit-auth")

    st.divider()
    st.subheader("System Status")
    try:
        r = requests.get(f"{API_BASE}/health", timeout=2)
        if r.status_code == 200: st.success("● API Online")
        else: st.error("● API Offline")
    except: st.error("● API Offline")

st.markdown('<div class="main-header">🔐 CyberResilience RL Dashboard</div>', unsafe_allow_html=True)
st.markdown("*Real Tool Execution - NO Simulation*")
st.divider()

col1, col2, col3, col4 = st.columns(4)
with col1: st.metric("Mode", "REAL", "Active")
with col2: st.metric("Tools", "9", "Nmap, SQLMap...")
with col3: st.metric("State Dim", "32", "Vector")
with col4: st.metric("Actions", "12", "Discrete")

st.divider()
st.subheader("📊 Training Progress")
fig = go.Figure(go.Indicator(
    mode="gauge+number", value=0,
    title={'text': "Training Progress (%)"},
    gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "#22c55e"}}
))
st.plotly_chart(fig, use_container_width=True)

st.divider()
st.subheader("🚀 Quick Commands")
st.code("""
# Start API Server
python backend_api.py

# Start Dashboard
streamlit run dashboard.py

# Train with Real Tools
docker build -t cyber-rl .
docker run -it --network=host cyber-rl \
  python use_tool.py --mode real \
  --target http://host.docker.internal:3000 \
  --train --episodes 2000 --explicit-auth

# Assess with Trained Model
docker run -it --network=host cyber-rl \
  python use_tool.py --mode real \
  --target http://host.docker.internal:3000 \
  --model checkpoints_real/best_model.pt --explicit-auth
""")

st.divider()
st.markdown("**CyberResilience RL v14.0** | Real Tool Integration\n⚠️ *For authorized security testing only*")
