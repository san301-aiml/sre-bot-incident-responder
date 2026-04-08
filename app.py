from fastapi import FastAPI
from models import SREAction, SREObservation, SREState
from env import SREBotEnv

app = FastAPI(title="sre-bot-incident-responder")
env = SREBotEnv()

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/reset", response_model=SREObservation)
async def reset(task_id: str = "easy"):
    return env.reset(task_id)

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
