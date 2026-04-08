from pydantic import BaseModel
from typing import Optional

class SREAction(BaseModel):
    """Action space for the SRE agent."""
    command: str
    thought: str

class SREObservation(BaseModel):
    """Observation space returned by the environment."""
    terminal_output: str
    system_status: str
    current_step: int
    echoed_message: Optional[str] = None
    # Mandatory for OpenEnv Step/Reset validation
    reward: float = 0.0
    done: bool = False

class SREState(BaseModel):
    """State metadata for the current session."""
    status: str
    task_id: str
    step_count: int
