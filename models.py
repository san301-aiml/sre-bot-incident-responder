from pydantic import BaseModel
from typing import Optional

class SREAction(BaseModel):
    command: str
    thought: str

class SREObservation(BaseModel):
    terminal_output: str
    system_status: str
    current_step: int
    echoed_message: Optional[str] = None
    reward: float = 0.0
    done: bool = False

class SREState(BaseModel):
    status: str
    task_id: str
    step_count: int
