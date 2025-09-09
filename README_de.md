> ➡️ [Hier geht’s zur englischen Version](README.md)
# 📜 llm-response-timer-action
![MIT License](https://img.shields.io/badge/license-MIT-green)
![Tested on LM Studio](https://img.shields.io/badge/tested-LM%20Studio-blue)


Diese GitHub Action testet ein lokal laufendes Sprachmodell über LM Studio, indem sie eine promptbasierte Anfrage sendet, die Antwortzeit misst, bei Abschluss ein akustisches Feedback ausgibt und die Ergebnisse in einer Log-Datei speichert.


## 🔗 Einsatz in Dr. Nature

Diese GitHub Action wurde ursprünglich im Rahmen des Projekts [Dr. Nature](https://github.com/Margarethe-S/dr-nature) entwickelt – einer lokalen KI-Anwendung zur Beantwortung naturheilkundlicher Gesundheitsfragen.

➡️ Zum Hauptprojekt: **[Dr. Nature – A holistic AI-powered health assistant](https://github.com/Margarethe-S/dr-nature)**

## ✅ Dieses Projekt hat einen stabilen Funktionsstand erreicht.


Die Action wurde erfolgreich in lokalen und Docker-basierten Umgebungen getestet. Sie ist jetzt bereit zur öffentlichen Nutzung und wird auf Basis von Nutzerfeedback weiterentwickelt.


Die Entwicklung bleibt offen, nachvollziehbar und lernorientiert – inklusive aller Tests, Logs und Optimierungen.

✅ Die Grundfunktionalität wurde erfolgreich getestet. Eine Veröffentlichung im GitHub Marketplace ist erfolgt.


## 🛠️ Funktionen

- Lädt den System-Prompt aus einer `.txt`-Datei ℹ️ Der Pfad zur Datei muss je nach Setup (lokal vs. Docker) korrekt angegeben werden.
- Sendet eine promptbasierte Anfrage an ein lokal laufendes Sprachmodell (z. B. LM Studio)
- Misst die genaue Antwortzeit in Sekunden und Minuten
- Spielt einen **Erfolgston**, wenn eine Antwort empfangen wurde
- Spielt einen **Warnton**, wenn ein Timeout oder Fehler auftritt
- Speichert die Antwort und Zeitmessung in einer Log-Datei
- Unterscheidet zwischen:
  - ⏰ Zeitüberschreitung (nach 300 Sekunden)
  - ❌ Verbindungs- oder Anfragefehler
  - ❌ JSON- oder Schlüsselverarbeitungsfehler

## 📁 Logs

Alle Ergebnisse werden gespeichert unter:  
`/logs`

Nach jedem Durchlauf erstellt das Skript eine Log-Datei im Ordner `logs/.txt`.  
Jeder Eintrag enthält:

- Den verwendeten Prompt-Pfad
- Die gestellte Nutzerfrage
- Die vollständige Antwort oder eine Fehlermeldung
- Die benötigte Zeit
- Eine Statusmeldung („✅ Erfolgreich“ oder Details zum Fehler)


## 🧪 Ideal geeignet für

- Testen der Antwortzeit lokal laufender Sprachmodelle (z. B. LM Studio)
- Debugging und Feintuning von Systemprompts
- Automatisierung deines lokalen KI-Entwicklungsworkflows
- Schnelle Funktionstests bei Promptänderungen
- Fehlersuche mit akustischem Feedback und Logdateien
- Vergleich von Reaktionszeiten bei unterschiedlichen Modellen oder Konfigurationen

## 📂 Beispiel-Prompt-Datei


In diesem Repository findest du eine Beispiel-Datei unter:

`prompts/action_prompt1.0.txt`

Du kannst entweder:
- diese Datei bearbeiten,
- oder eine eigene Prompt-Datei anlegen und im Aufrufpfad angeben.

🛠️ Der Pfad zur Datei wird beim Aufruf übergeben – du musst dafür **nichts im Code ändern.**


## 🛠️ Installation

```bash
pip install -r requirements.txt
```

## ▶️ Aktion lokal ausführen (ohne Docker)

✅ Beispiel:
```bash
python actions/timer/main.py http://localhost:1234/v1/chat/completions prompts/action_prompt1.0.txt "Was kann ich gegen Kopfschmerzen auf natürliche Weise tun?" 
```
> ⚠️ **Achte auf die genaue Schreibweise und die Leerzeichen im Befehl!**
> 
> - Der `localhost`-Pfad (`http://localhost:1234/v1/chat/completions`) muss exakt mit der API-URL deines lokal laufenden LM Studios übereinstimmen.
> - Die drei Argumente müssen mit Leerzeichen getrennt sein:
>   1. Die API-URL
>   2. Der Pfad zur Prompt-Datei (.txt)
>   3. Die Nutzerfrage in Anführungszeichen
>
> 📂 Du kannst:
> - Die vorhandene Beispiel-Promptdatei verwenden (`prompts/action_prompt1.0.txt`)
> - Oder den Pfad zu deiner eigenen Prompt-Datei angeben (z. B. `meine_prompts/prompt2.txt`)
>
> 👉 Falls du nicht sicher bist, unter welcher Adresse dein LM Studio erreichbar ist, öffne die Einstellungen in LM Studio. Dort findest du die genaue API-URL unter dem Menüpunkt „API“ oder „OpenRouter“.

Das Skript führt dann folgende Schritte aus:
- Lädt Umgebungsvariablen und den Systemprompt
- Sendet eine Beispiel-Nutzerfrage
- Misst die Antwortzeit
- Gibt die Antwort des Modells im Terminal aus
- Spielt einen Systemton ab
- Speichert das Ergebnis im /logs-Ordner

## 🐳 Aktion via Docker ausführen

```bash
docker run --rm -e TZ=Europe/Berlin -v "C:\Pfad\zu\deinem\Projekt\prompts:/app/prompts" -v "C:\Pfad\zu\deinem\Projekt\logs:/app/logs" llm-response-timer-action http://<DEINE-LOKALE-IP>:1234/v1/chat/completions /app/prompts/action_prompt1.0.txt "Was kann ich gegen Kopfschmerzen auf natürliche Weise tun?"
```
>⚠️ Wichtige Hinweise:
>- Ersetze "C:\path\to\your\project" durch den tatsächlichen Pfad zu deinem lokalen Projektverzeichnis.
>- Ersetze http://1234/v1/chat/completions durch die korrekte IP-Adresse deines lokal laufenden LM Studio Modells.
>- Achte unbedingt auf die genaue Syntax und Leerzeichen (besonders unter Windows vs. Linux/Mac).

💡 Achte darauf:

>- Der -e TZ=Europe/Berlin Parameter sorgt dafür, dass deine Log-Zeiten in der richtigen Zeitzone erscheinen.
>- Die -v Parameter verbinden deine lokalen Ordner mit dem Container:
-prompts → für deine .txt-Promptdateien
-logs → um die Log-Dateien dauerhaft auf deinem PC zu speichern

> Der letzte Teil enthält:
>- die API-URL (z. B. http://<DEINE-LOKALE-IP>:1234/v1/chat/completions)
>- den Pfad zur Prompt-Datei innerhalb des Containers (/app/prompts/...)
>- und deine Nutzerfrage in Anführungszeichen

Im Container führt das Skript folgende Schritte aus:
- Lädt Umgebungsvariablen und den Systemprompt
- Sendet eine Beispiel-Nutzerfrage an LM Studio
- Misst die Antwortzeit 

⚠️ Die Stoppuhr funktioniert in Docker möglicherweise nicht zuverlässig

- Gibt die Antwort des Modells im Terminal aus
- Speichert das Ergebnis im /logs-Ordner (gemappt von deinem lokalen Projekt)

⚠️ Hinweis: Akustisches Feedback (Systemton) ist innerhalb von Docker nicht verfügbar.

---



## 🖼️ Screenshots 
Screenshot: Log-Ordnerstrucktur

![alt text](images/image-1.png)

Screenshot: Beispiel-Inhalt einer Log-Datei

![alt text](images/image.png)

Screenshot: Terminalausgabe der Antwortzeit

![alt text](images/image-2.png)

---
## 🔓 Frei verwendbar

Dieses Repository wird im Sinne von Lernen und Weiterentwicklung bereitgestellt.  
Gerne darfst du es forken oder anpassen, wenn es dir bei eigenen Projekten hilft.

Viel Erfolg bei deinen Entwicklungen!

📝 Lizenz: Dieses Projekt steht unter der MIT-Lizenz.  
Details findest du in der Datei [LICENSE](./LICENSE).

---
 
> ⚠️ **Hinweis**  
> Diese GitHub Action wurde bisher erfolgreich mit einem lokal laufenden Modell über **LM Studio** getestet (z. B. *Mistral 7B*).  
> Andere Modelle könnten ebenfalls funktionieren, wurden jedoch **noch nicht getestet**.
