# 📜 llm-response-timer-action
> ➡️ [Click here for the German version](README_de.md)

This GitHub Action tests a locally running Language Model via LM Studio by sending a prompt-based request, measuring the response time, and playing acoustic feedback upon completion.

## 🔗 Used in: Dr. Nature

This GitHub Action was originally developed as part of the [Dr. Nature](https://github.com/Margarethe-Techstarter/dr-nature) project – a local AI assistant for natural health questions.

➡️ View the main project: **[Dr. Nature – A holistic AI-powered health assistant](https://github.com/Margarethe-Techstarter/dr-nature)**

## 📊 This project is currently in active development.

Even though the Action is not yet published on the GitHub Marketplace, it is already being tested and explored by other developers.  
This shows that the concept resonates and has practical relevance.

The development is intentionally transparent and learning-focused – including all tests, errors, and improvements.  
The goal is stability, clarity, and real progress – not perfection.

🛠️ A Marketplace release is planned as soon as the core functionality is reliably established.


## ✅ Features

- Loads `.env` file to retrieve the LM Studio API URL
- Loads a system prompt from a local `.txt` file
- Sends a prompt to a local LLM via HTTP POST (JSON)
- Measures exact response time in seconds and minutes
- Plays a **success tone** when a response is received
- Plays a **warning tone** when timeout or error occurs
- Differentiates between:
  - ⏰ Timeout (after 300 seconds)
  - ❌ Connection or request error
  - ❌ JSON or key parsing error

## 📁 Logs

All results are stored in:
`/logs`
After each run, the script creates a log file inside the logs/.txt folder.
Each log entry includes:
- The used prompt path
- The input question
- The full response or error
- The elapsed time
- Status message (“✅ Successful” or error details)

## 🧪 Ideal for

- Testing response time of local LLMs
- Debugging system prompt behavior
- Automating your AI development workflow

---

## 📂 Example Prompt File

Store your prompt in:
`prompts/action_promt1.0.txt`

You can replace the path in `main.py` by editing the `prompt_path` variable.


## ⚙️ Requirements

Create a `.env` file in your root directory with the following content:

```env
LMSTUDIO_API_URL=http://localhost:1234/v1/chat/completions
```

## 🛠️ Installation

```bash
pip install -r requirements.txt
```

## ▶️ Run the Action Locally

```bash
python main.py
```
The script will:
- Load environment variables and system prompt
- Send a sample user question
- Measure response time
- Print the model’s answer
- Play system sound
- Log all results in the /logs folder


## 🖼️ Screenshots 
Screenshot: Log folder structure

![alt text](images/image-1.png)

Screenshot: Example log file content

![alt text](images/image-3.png)


Screenshot: Terminal response 

![alt text](images/image-4.png)
---
## 🔓 Use Freely

This repository is shared in the spirit of learning and development.  
Feel free to fork or adapt it if it’s useful for your own projects.

Good luck with your builds!
---

> ⚠️ **Note**  
> This GitHub Action has been successfully tested with a locally running model via **LM Studio** (e.g. *Mistral 7B*).  
> Other models may also work, but have **not been tested yet**.


