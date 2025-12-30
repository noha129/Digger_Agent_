# Digger Agent — Agentic AI Research Assistant ✅

**Digger Agent** is a small, local agentic research assistant that uses a local LLM (via LlamaCpp) and LangChain components to research topics, fetch web content (DuckDuckGo / YouTube / URLs) and extract text from PDFs / DOCX files, then synthesize the findings into a concise JSON-formatted slide deck.

---

## 🔧 Features

- Research web and YouTube content using tools and wrappers
- Fetch and extract text from web pages, PDF, and DOCX files
- Generate exactly 5 presentation slides in JSON format using a local LLM
- Agent orchestration implemented with a simple workflow graph
- Local-first: runs with a local GGUF model via `llama_cpp`

---

## 🚀 Quickstart

1. Clone or open this repository.
2. Create and activate a Python virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # PowerShell
# or
.\.venv\Scripts\activate.bat   # cmd
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure the model path:

- Edit `Digger_Agent_/Agentswithtools.py` and set the `model_path` to your local GGUF model (Qwen/llama-style GGUF path) or set an env var and update the code to read it.

Example (Windows PowerShell):

```powershell
$env:MODEL_PATH = 'C:\path\to\model.gguf'
```

5. Run the agent:

```bash
python Digger_Agent_/main.py
```

Enter a topic or a document URL/path when prompted and the agent will run the workflow and print the final JSON slide output.

---

## 📁 Project structure

- `main.py` — Minimal entrypoint that runs the workflow
- `workflow.py` — Graph-based workflow and node definitions
- `Agentswithtools.py` — LLM setup, prompt template and agent construction
- `Tools.py` — Utility tools: DuckDuckGo, YouTube search wrapper, URL fetch, PDF/DOCX extractors
- `prompt.py` — Prompt template used by the agent
- `requirements.txt` — Python dependencies
- `LICENSE` — Apache 2.0

---

## 💡 Usage examples

- Run the program and enter a search query:

```
Enter the topic you want the agent to research: Explain reinforcement learning
```

- Or give a PDF/DOCX path or URL to get a summarized slide deck based on that document.

Example output (trimmed):

```json
{
  "slides": [
    {"slide_type": "Title slide", "slide_title": "Reinforcement Learning: An Intro", "slide_content": "..."},
    {"slide_type": "Bullet point slide", "slide_title": "Key Concepts", "slide_content": "..."}
  ],
  "summary": "Executive summary connecting slides"
}
```

---

## ⚠️ Notes & tips

- Ensure your local LLM model is compatible with `llama_cpp` (GGUF/compatible). Paths and model size will affect memory/VRAM requirements.
- `Agentswithtools.py` contains tuning parameters for `LlamaCpp` (temperature, n_ctx, threads). Tune them to your hardware.
- The project uses community wrappers (DuckDuckGo, YouTube) that may change; treat them as best-effort utilities.

---

## ✅ Contributing

Contributions are welcome — open an issue or a PR. Please include tests or a short description of changes.

---

## 📜 License

This project is licensed under the Apache License 2.0 — see the `LICENSE` file for details.

---

If you'd like, I can also add a usage example script, a CI test, or a short demo notebook to show a run with a sample query.