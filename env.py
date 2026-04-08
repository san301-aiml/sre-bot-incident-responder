from models import SREAction, SREObservation, SREState

class SREBotEnv:
    def __init__(self):
        self.step_count = 0
        self.task_id = "easy"
        self.done = False

    def reset(self, task_id="easy"):
        self.step_count = 0
        self.task_id = task_id
        self.done = False
        prompts = {
            "easy": "Identify the error code in 'logs.txt'.",
            "medium": "Process 405 is at 99% CPU. Stop it.",
            "hard": "Disk full! Find and delete the large log file."
        }
        return SREObservation(terminal_output=prompts.get(task_id, ""), system_status="ALARM", current_step=0, reward=0.0, done=False)

    def step(self, action: SREAction):
        self.step_count += 1
        cmd = action.command.lower().replace("`", "").strip()
        reward = -0.01 
        output = f"System: Command '{cmd}' executed. No critical change, but system is still under ALARM."

        # ================= EASY TASK =================
        if self.task_id == "easy":
            if any(x in cmd for x in ["ls", "dir"]):
                output, reward = "Files: logs.txt, config.yaml, app.py", 0.2
            elif any(x in cmd for x in ["grep", "cat", "read"]):
                output, reward, self.done = "SUCCESS: Found CRITICAL_ERROR_505: DB Connection Failed", 1.0, True

        # ================= MEDIUM TASK =================
        elif self.task_id == "medium":
            if any(x in cmd for x in ["ps", "top", "htop"]):
                output, reward = "USER PID %CPU COMMAND\nroot 405 99.2 python3\nroot 102 0.1 systemd", 0.4
            elif "kill" in cmd and "405" in cmd:
                output, reward, self.done = "SUCCESS: Process 405 killed. CPU load back to normal.", 1.0, True
            elif "kill" in cmd:
                output = "Error: You must specify the correct PID to kill (use ps to find it)."

        # ================= HARD TASK =================
        elif self.task_id == "hard":
            # If they check disk usage OR search for logs
            if any(x in cmd for x in ["df", "du", "ls", "find"]):
                output, reward = "Storage: /var/log/server_backup.log is 40GB (99% full).", 0.5
            # If they try to investigate the log itself
            elif "grep" in cmd or "cat" in cmd:
                output, reward = "System: This file is too large to read (40GB). You should probably delete it.", 0.3
            # Success Condition
            elif any(x in cmd for x in ["rm", "truncate", "del", "unlink"]):
                if "log" in cmd or "server_backup" in cmd:
                    output, reward, self.done = "SUCCESS: /var/log/server_backup.log deleted. 40GB freed.", 1.0, True
                else:
                    output = "Error: Specify the log file to remove."

        if self.step_count >= 10: self.done = True
        
        obs = SREObservation(
            terminal_output=output, 
            system_status="OK" if self.done and reward >= 0.9 else "ALARM", 
            current_step=self.step_count, 
            reward=reward, 
            done=self.done
        )
        return obs, reward, self.done, {}

    def get_state(self):
        return SREState(status="completed" if self.done else "running", task_id=self.task_id, step_count=self.step_count)
