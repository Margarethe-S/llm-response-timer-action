import os
import requests
import json
import time
import threading
import sys
from logger import save_log


api_url = sys.argv[1] 

prompt_path = sys.argv[2]

user_input = sys.argv[3]

with open(prompt_path, "r") as f:
    prompt = f.read()

# Ensure the logs folder exists
os.makedirs("logs", exist_ok=True)

# Path to the system prompt file


# Event to stop the stopwatch thread
stop_event = threading.Event()

# Initialize elapsed time and status message
elapsed_time = 0
status_msg = "✅ Successful!"

# Load environment variables from .env file
def load_env(filepath=".env"):
    if not os.path.exists(filepath):
        print(f"⚠️  .env file not found at: {filepath}")
        return
    with open(filepath, "r") as f:
        for line in f:
            if line.strip() and not line.startswith("#"):
                key, value = line.strip().split("=", 1)
                os.environ[key] = value

load_env()

# Get API URL from environment variable
api_url = os.getenv("LMSTUDIO_API_URL")

# Load the system prompt
with open("prompts/action_prompt1.0.txt", "r", encoding="utf-8") as f:
    prompt = f.read()

print("Loading system prompt:", prompt[:300], "...")

# 🕒 Shared start time
start_time = time.time()
success = True  # Assume success unless an error occurs
response = None  # Placeholder for the model's response

# Start a live stopwatch in a separate thread
def live_stopwatch(start_time):
    while not stop_event.is_set():
        elapsed = time.time() - start_time
        mins, secs = divmod(int(elapsed), 60)
        millis = int((elapsed - int(elapsed)) * 1000)
        print(f"\r⏳ Elapsed Time: {mins:02d}:{secs:02d}.{millis:03d}", end="")
        time.sleep(0.1)
    print("\n✅ Stopwatch stopped.")

# 🟢 Start the stopwatch
t = threading.Thread(target=live_stopwatch, args=(start_time,))
t.start()



try:
    # Send request to LM Studio
    response = requests.post(
        api_url,
        headers={"Content-Type": "application/json"},
        json={
            "model": "em_german_mistral_v01",
            "messages": [
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_input}
            ],
            "temperature": 0.0
        },
        timeout=300  # 5-minute timeout
    )

    # Measure response time
    end_time = time.time()
    elapsed_time = end_time - start_time
    minutes, seconds = divmod(elapsed_time, 60)

    print(f"\n✅ Response time: {elapsed_time:.2f} seconds.")
    print(f"🕓 = {int(minutes)} minutes and {int(seconds)} seconds.")

    # Parse response content
    response = response.json()["choices"][0]["message"]["content"]
    print(f"\n📩 LM Studio Response:\n{response}")

except requests.exceptions.Timeout:
    error_msg = "⏱️ Request timed out after 5 minutes."
    status_msg = f"Response: {response}"
    print(error_msg)
    print(status_msg)
    response = f"{error_msg}"
    success = False

except requests.exceptions.RequestException as e:
    error_msg = f"❌ Request or connection error occurred: {e}"
    status_msg = f"Response: {response}"
    print(error_msg)
    print(status_msg)
    response = f"{error_msg}"
    success = False

except ValueError:
    error_msg = "❌❌ Could not parse response as valid JSON."
    status_msg = f"Response: {response}"
    print(error_msg)
    print(status_msg)
    response = f"{error_msg}"
    success = False

except KeyError as e:
    error_msg = f"❌ Incomplete or malformed response (KeyError: '{e.args[0]}')."
    status_msg = f"Response: {response}"
    print(error_msg)
    print(status_msg)
    response = f"{error_msg}"
    success = False

finally:
    try:
        save_log(prompt_path, user_input, str(response), elapsed_time, status_msg)
    except Exception as e:
        print(f"⚠️ Error while saving log file: {e}")

    stop_event.set()
    t.join()

    if success:
        os.system('powershell -c "[console]::beep(1000, 500)"')
        print(status_msg)
    else:
        os.system('powershell -c "[console]::beep(1000, 500); Start-Sleep -Milliseconds 200; [console]::beep(600, 500)"')
