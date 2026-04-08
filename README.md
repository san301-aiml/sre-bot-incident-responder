# SRE-Bot: An OpenEnv Agentic Debugging Environment

SRE-Bot is a specialized reinforcement learning environment built on the **OpenEnv** specification. It simulates the high-stakes world of Site Reliability Engineering (SRE), providing a playground for LLM-based agents to practice autonomous infrastructure troubleshooting.

## 🏗 Why SRE-Bot?
Most RL environments focus on games (like Chess or Atari). While fun, they don't help us build agents that can manage real cloud infrastructure. SRE-Bot bridges this gap by forcing agents to interact with a simulated Linux terminal to resolve critical system failures.

## 🛠 Action & Observation Specs
- **Action**: The agent sends `SREAction` objects containing a shell command and a "thought" string (Chain of Thought). This encourages the agent to explain its reasoning before execution.
- **Observation**: The environment returns `SREObservation`, which includes raw terminal output, current system health status, and step counts.

## 🚀 Scenario-Based Tasks
I have designed three progressive scenarios that mirror actual on-call incidents:

1. **Log Investigation (Easy)**:
   - **Scenario**: A "Latency High" alert is triggered.
   - **Goal**: Use `grep` to parse a massive log file and find the specific failure code.
   
2. **Process Management (Medium)**:
   - **Scenario**: A service is unresponsive due to a "zombie" process.
   - **Goal**: Identify the problematic PID (405) and use `kill` signals to restore stability.

3. **Disk Recovery (Hard)**:
   - **Scenario**: A database has locked up because the disk is 100% full.
   - **Goal**: Safely identify non-critical `.log` files and clear them to regain capacity.

## 📈 Grader & Rewards
This environment uses a **dense reward function**. Instead of a binary success/failure at the end, the agent receives partial signals for:
- Executing valid Linux syntax.
- Narrowing down the problem area.
- Final resolution (1.0 score).

## 💻 Local Quickstart
```bash
# Install the OpenEnv core
pip install openenv-core fastapi uvicorn pydantic

# Launch the environment server
python -m uvicorn app:app --port 7860
