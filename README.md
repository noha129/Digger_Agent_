# Digger Agent — Agentic AI Research Assistant: ✅

**Digger Agent** is a small, local agentic research assistant that uses LangChain components and local model backends to research topics, fetch web content (DuckDuckGo / YouTube / URLs) and extract text from PDFs / DOCX files, then synthesize the findings into a concise JSON-formatted slide deck.

---

## 🔧 Features

- Research web and YouTube content using simple tool wrappers
- Fetch and extract text from web pages, PDF, and DOCX files
- Generate a JSON slide deck (default: 5 slides) using a local model backend
- Agent orchestration implemented with a lightweight workflow graph
- Supports Ollama (`langchain-ollama`) and local model backends (see `workflow.py`)

---

## 🚀 Quickstart

1. Clone or open this repository.
2. Create and activate a Python virtual environment (recommended Python 3.10+):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # PowerShell
# or
.\.venv\Scripts\activate.bat   # cmd
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

4. Configure the model (edit `workflow.py`):

- By default the project uses `ChatOllama` in `workflow.py` (example: `model = ChatOllama(model="qwen3:4b", ...)`).
- To use a different model or backend, edit `workflow.py` and change the `model = ...` line to the model of your choice (e.g., Ollama model name or a local Llama backend). If you prefer an env var, set it and update `workflow.py` to read it.

> Note: If you use Ollama, ensure the `ollama` binary/server is installed and the requested model (e.g., `qwen3:4b`) is available.

5. Run the agent:

```powershell
python main.py
```

Follow the prompts and provide either a search query or a document path/URL. The script will save a JSON file (default `output.json`) with the slide deck.

---

## 📁 Project structure

- `main.py` — Minimal entrypoint that runs the workflow
- `workflow.py` — Graph-based workflow and model setup (edit here to swap models)
- `tools.py` — Utility tools: DuckDuckGo/YouTube search, URL fetch, PDF/DOCX extractors
- `prompt.py` — Prompt templates used by the agent
- `requirements.txt` — Python dependencies
- `LICENSE` — Apache 2.0

---

## 💡 Usage examples

- Run the program and enter a search query when prompted:

```
Enter PDF/DOCX path, URL, or search query: Explain reinforcement learning
Number of slides (default 5): 5
JSON filename (e.g., slides.json): slides.json
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

## ⚠️ Troubleshooting & tips

- If the code prints a JSON parse error, the model returned non-JSON text; try adjusting the prompt in `prompt.py` or tuning model temperature.
- If using Ollama, ensure the Ollama daemon is running and the model name in `workflow.py` exists.
- For local LLM backends (e.g., `llama_cpp_python`), check memory/VRAM requirements for large models.

---

## ✅ Contributing

Contributions are welcome — open an issue or a PR. Please include tests or a short description of changes. If you change the model backend, add short docs about how to configure and run it.

---

## 📜 License

This project is licensed under the Apache License 2.0 — see the `LICENSE` file for details.

---

If you'd like, I can add a short demo notebook or an automated example script (e.g., `examples/run_demo.py`) and a simple CI check that runs the workflow with a fixed input and verifies JSON output. Would you like me to add that?