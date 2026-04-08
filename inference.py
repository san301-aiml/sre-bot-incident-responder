import os, requests, time
from huggingface_hub import InferenceClient

HF_TOKEN = os.getenv("HF_TOKEN")

client = InferenceClient(
    model="meta-llama/Meta-Llama-3-70B-Instruct", 
    token=HF_TOKEN
)
BASE_URL = "http://localhost:7860"

def safe_post(url, payload=None):
    try:
        res = requests.post(url, json=payload, timeout=15)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print(f"⚠️ Request failed: {e}")
        return None

def solve_with_llm(task_id):
    print(f"\n" + "="*40)
    print(f"🚀 STARTING SRE TASK: {task_id.upper()}")
    print("="*40)

    res = safe_post(f"{BASE_URL}/reset?task_id={task_id}")
    if not res: return
    
    terminal_output = res.get("terminal_output", "")
    done = False
    total_reward = 0
    step_count = 0

    while not done and step_count < 10:
        step_count += 1
        prompt = f"You are an SRE. Task: {task_id}\nSystem Output: {terminal_output}\nRespond exactly as:\nThought: <reasoning>\nCommand: <cmd>"
        
        try:
            response = client.chat_completion(messages=[{"role": "user", "content": prompt}], max_tokens=150)
            llm_text = response.choices[0].message.content
            
            # --- IMPROVED NATURAL PARSING ---
            thought = "Thinking..."
            command = "ls" # fallback
            
            if "Thought:" in llm_text:
                thought = llm_text.split("Thought:")[1].split("Command:")[0].strip()
            if "Command:" in llm_text:
                command = llm_text.split("Command:")[1].strip().replace("`", "").split("\n")[0]

            # Step environment
            step_res = safe_post(f"{BASE_URL}/step", {"command": command, "thought": thought})
            if not step_res: break
            
            obs = step_res["observation"]
            terminal_output = obs["terminal_output"]
            reward = step_res["reward"]
            done = step_res["done"]
            total_reward += reward

            # --- NATURAL LOGS ---
            print(f"\n[STEP {step_count}]")
            print(f"🤖 AI THOUGHT: {thought}")
            print(f"⌨️  AI COMMAND: {command}")
            print(f"🖥️  SYSTEM OUTPUT: {terminal_output}")
            print(f"📊 REWARD: {reward} | TOTAL: {total_reward:.2f}")
            print("-" * 30)

        except Exception as e:
            print(f"⚠️ Error: {e}")
            break

    print(f"✅ TASK {task_id.upper()} FINISHED. TOTAL SCORE: {total_reward:.2f}")

if __name__ == "__main__":
    for task in ["easy", "medium", "hard"]: solve_with_llm(task)