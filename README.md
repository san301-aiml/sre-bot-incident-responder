---
Title: SRE Bot Incident Responder
emoji: 🏢
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
license: apache-2.0
---

# SRE-Bot: An OpenEnv Agentic Debugging Environment

SRE-Bot is a specialized agentic environment built on the **OpenEnv** specification for the Meta AI Hackathon. It simulates real-world Site Reliability Engineering (SRE) scenarios, providing a playground for LLM-based agents to solve infrastructure incidents autonomously.

## 🏗 Why SRE-Bot?
Most RL environments focus on toy problems. SRE-Bot bridges the gap by forcing agents to interact with a simulated Linux terminal to resolve critical system failures using "Natural Reasoning" and Chain-of-Thought (CoT).

## 🚀 Scenario-Based Tasks (Tiered Difficulty)
Designed with progressive difficulty to test agent persistence and logic:

1. **Log Analysis (Easy)**:
   - **Objective**: Use shell commands to identify the specific error code `CRITICAL_ERROR_505` from system logs.
   
2. **Process Management (Medium)**:
   - **Objective**: Identify a resource-hogging process (PID 405) using `ps` or `top` and terminate it to restore system stability.

3. **Disk Recovery (Hard)**:
   - **Objective**: Troubleshoot a 100% disk exhaustion event by locating a massive hidden log file and removing it safely.

## 🛠 Action & Observation Specs
- **Action (`SREAction`)**: The agent provides a shell command and a "thought" string.
- **Observation (`SREObservation`)**: The environment returns terminal output, system health status, rewards, and task completion flags.

## 📈 Grader & Rewards
This environment implements a **dense reward function** to guide agent learning:
- **Progressive Rewards**: Rewards (0.2 - 0.5) for investigative commands that narrow down the root cause.
- **Success Reward**: A terminal 1.0 score upon successful resolution of the incident.
- **Efficiency Penalty**: Small step penalties (-0.01) to encourage the agent to find the shortest path to recovery.

## 💻 Setup & Local Usage

### 1. Installation
```bash
pip install fastapi uvicorn pydantic requests huggingface_hub
# Set your Hugging Face API Token
export HF_TOKEN="your_token_here"

# Start the Environment Server in the background
uvicorn app:app --host 0.0.0.0 --port 7860 &

# Wait 3 seconds and run the baseline agent
sleep 3
python inference.py
docker build -t sre-bot .
docker run -p 7860:7860 sre-bot
