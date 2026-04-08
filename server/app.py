from fastapi import FastAPI, Body
from typing import Optional
from .models import SREAction, SREObservation, SREState
from .env import SREBotEnv
import uvicorn

app = FastAPI(title="sre-bot-incident-responder")
env = SREBotEnv()

@app.get("/")
async def root():
    return {"message": "SRE-Bot Environment is Live", "docs": "/docs"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

# ✅ FIXED: Added default task_id and Optional type to handle empty JSON bodies {}
@app.post("/reset", response_model=SREObservation)
async def reset(task_id: Optional[str] = Body("easy")):
    return env.reset(task_id if task_id else "easy")

# ✅ FIXED: Explicitly return a dictionary containing 'observation' 
# This ensures your inference.py can find res["observation"]
@app.post("/step")
async def step(action: SREAction):
    obs, reward, done, info = env.step(action)
    return {
        "observation": obs,
        "reward": reward,
        "done": done,
        "info": info
    }

@app.get("/state", response_model=SREState)
async def state():
    return env.get_state()

@app.get("/metadata")
async def metadata():
    return {
        "name": "sre-bot-incident-responder",
        "version": "1.0.0",
        "tasks": ["easy", "medium", "hard"]
    }
def main():
    """Main entry point for multi-mode deployment."""
    # Ensure this matches your actual file name (server.app or just app)
    uvicorn.run("server.app:app", host="0.0.0.0", port=8000)
if __name__ == "__main__":
    main()
