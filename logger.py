import datetime
from datetime import datetime

def save_log(prompt_path, user_input, response, elapsed_time, status_msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_path = f"logs/log_{datetime.now().strftime('%Y-%m-%d')}.txt"  # or e.g. f"logs/{promptname}_log.txt"

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"📝 Status: {status_msg}\n")
        f.write(f"⏰ Timestamp: {timestamp}\n")
        f.write(f"🕓 Duration: {elapsed_time:.2f} seconds\n")
        f.write(f"📤 Prompt file: {prompt_path}\n")
        f.write(f"🧠 Response: {response}\n")
        f.write("-" * 40 + "\n")
    
    print(f"✅ Log saved in: {log_path}")
