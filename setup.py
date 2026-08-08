from setuptools import setup, find_packages
setup(
    name="cyberresilience-rl",
    version="14.0.0",
    packages=find_packages(),
    install_requires=[
        "torch>=2.0.0", "numpy>=1.24.0", "flask>=2.3.0", "flask-cors>=4.0.0",
        "flask-socketio>=5.3.0", "flask-limiter>=3.5.0", "matplotlib>=3.7.0",
        "requests>=2.31.0", "streamlit>=1.28.0", "plotly>=5.18.0", "pandas>=2.0.0",
    ],
    python_requires=">=3.9",
)
