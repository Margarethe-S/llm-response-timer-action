import os
import sys
import requests
import json
import time
import threading
import platform
from datetime import datetime
from logger import save_log
from playsound import playsound  # Optional, falls du mp3s nutzen willst

# 🎵 Sound- und Popup-Handling
def beep_success():
    try:
        if platform.system() == "Windows":
            import winsound
            winsound.Beep(1000, 200)
        elif platform.system() == "Darwin":
            os.system('say "done"')
        elif platform.system() == "Linux":
            os.system('paplay /usr/share/sounds/freedesktop/stereo/complete.oga')
        else:
            docker_fallback(success=True)
    except Exception as e:
        docker_fallback(success=True, error_msg=str(e))


def beep_failure(error_msg=None):
    try:
        if platform.system() == "Windows":
            import winsound
            winsound.Beep(500, 200)
            time.sleep(0.1)
            winsound.Beep(500, 200)
        elif platform.system() == "Darwin":
            os.system('say "error"')
        elif platform.system() == "Linux":
            os.system('paplay /usr/share/sounds/freedesktop/stereo/dialog-warning.oga')
            os.system('paplay /usr/share/sounds/freedesktop/stereo/dialog-warning.oga')
        else:
            docker_fallback(success=False, error_msg=error_msg)
    except Exception as e:
        docker_fallback(success=False, error_msg=str(e))


def docker_fallback(success=True, error_msg=None):
    print("\a" if success else "\a\a")
    if success:
        print("✅ SUCCESS (Docker fallback)")
    else:
        print("❌ ERROR (Docker fallback)")
        if error_msg:
            print(f"🔎 Details: {error_msg}")

# ✅ CLI-Argumente prüfen
if len(sys.argv) < 4:
    print("❌ Usage: python main.py <API-URL> <PROMPT-PATH> <QUESTION>")
    sys.exit(1)

api_url = sys.argv[1]
prompt_path = sys.argv[2]
user_input = sys.argv[3]

# 📂 Logs-Verzeichnis sicherstellen
os.makedirs("logs", exist_ok=True)

# 📄 Prompt-Datei lesen
with open(prompt_path, "r", encoding="utf-8") as f:
    prompt = f.read()

print(f"📡 API-URL: {api_url}")
print(f"📄 Prompt file: {prompt_path}")
print(f"💬 Question: {user_input}")
print("📤 Sende Anfrage an LM Studio...")

# 🕒 Stoppuhr starten
stop_event = threading.Event()
start_time = time.time()


def live_stopwatch(start):
    while not stop_event.is_set():
        elapsed = time.time() - start
        mins, secs = divmod(int(elapsed), 60)
        millis = int((elapsed - int(elapsed)) * 1000)
        print(f"\r⏳ {mins:02d}:{secs:02d}.{millis:03d}", end="")
        time.sleep(0.1)
    print("\n✅ Stopwatch stopped.")


threading.Thread(target=live_stopwatch, args=(start_time,)).start()

success = True
response_text = ""
status_msg = "✅ Successful!"
elapsed_time = 0

try:
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
        timeout=300
    )

    elapsed_time = time.time() - start_time
    print(f"\n✅ Response in {elapsed_time:.2f} seconds.")
    response_text = response.json()["choices"][0]["message"]["content"]
    print(f"\n📩 Antwort:\n{response_text}")

except requests.exceptions.Timeout:
    success = False
    response_text = "⏱️ Timeout: Keine Antwort innerhalb von 5 Minuten."

except requests.exceptions.RequestException as e:
    success = False
    response_text = f"❌ Request/Connection error: {e}"

except (ValueError, KeyError) as e:
    success = False
    response_text = f"❌ Parsing/Key error: {e}"

finally:
    # 🧠 Log speichern
    try:
        save_log(prompt_path, user_input, response_text, elapsed_time, status_msg)
        if success:
            beep_success()
        else:
            beep_failure(error_msg=response_text)
    except Exception as e:
        print(f"⚠️ Fehler beim Log-Speichern: {e}")
        beep_failure(error_msg=str(e))

    stop_event.set()

