import os
import requests
import json
import time
import threading
import sys
from logger import save_log
import platform
from playsound import playsound

def beep_success():
    system_type = platform.system()
    try:
        if system_type == "Windows":
            import winsound
            winsound.Beep(1000, 200)
        elif system_type == "Darwin":  # macOS
            os.system('say "done"')
        elif system_type == "Linux":
            os.system('paplay /usr/share/sounds/freedesktop/stereo/complete.oga')
        else:
            docker_beep()
    except Exception as e:
        docker_beep(error=True, error_msg=e)

def beep_failure(error=None):
    system_type = platform.system()
    try:
        if system_type == "Windows":
            import winsound
            winsound.Beep(500, 200)
            time.sleep(0.1)
            winsound.Beep(500, 200)
        elif system_type == "Darwin":
            os.system('say "error"')
        elif system_type == "Linux":
            os.system('paplay /usr/share/sounds/freedesktop/stereo/dialog-warning.oga && paplay /usr/share/sounds/freedesktop/stereo/dialog-warning.oga')
        else:
            docker_beep(error=True, error_msg=error)
    except Exception as e:
        docker_beep(error=True, error_msg=e)

def docker_beep(success=True, error_msg=None):
    if success:
        print("✅ SUCCESS (Docker Fallback)")
        try:
            playsound("sounds/success.mp3")
        except Exception as e:
            print(f"⚠️ Audio-Fallback failed: {e}")
            print("\a")  # Notfallbeep als Zeichen
    else:
        print("❌ ERROR (Docker Fallback)")
        if error_msg:
            print(f"Details: {str(error_msg)}")
        try:
            playsound("sounds/error.mp3")
        except Exception as e:
            print(f"⚠️ Audio-Fallback failed: {e}")
            print("\a\a")

# Check arguments
if len(sys.argv) < 4:
    print("❌ Usage: python main.py <API-URL> <PROMPT-PATH> <QUESTION>")
    sys.exit(1)

api_url = sys.argv[1]
prompt_path = sys.argv[2]
user_input = sys.argv[3]

# Print the inputs (for transparency/logging)
print(f"📡 API-URL: {api_url}")
print(f"📄 Prompt file: {prompt_path}")
print(f"💬 Question: {user_input}")

with open(prompt_path, "r", encoding="utf-8") as f:
    prompt = f.read()
print("Loading system prompt:", prompt[:300], "...")

# Ensure the logs folder exists
os.makedirs("logs", exist_ok=True)

# Event to stop the stopwatch thread
stop_event = threading.Event()

# Initialize elapsed time and status message
elapsed_time = 0
status_msg = "✅ Successful!"

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
        
        if success:
            beep_success()
        else:
            beep_failure(error=response)

    except Exception as e:
        print(f"⚠️ Error while saving log file: {e}")
        beep_failure(error=e)

    stop_event.set()
    t.join()
    print(status_msg)


