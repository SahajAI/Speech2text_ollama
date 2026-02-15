# Speech2Text + Ollama

This project connects local speech recognition with a local Ollama model.

## What is included

- `voice_ollama.py`: original terminal voice loop (mic -> transcription -> Ollama -> spoken response).
- `app_ui.py`: new Streamlit UI so you can test prompts in a browser.

## Prerequisites

1. Install [Ollama](https://ollama.com/) and make sure it is running.
2. Pull a model (default in this repo is `llama3.2:latest`).
3. (Optional, for voice script) Download a Vosk model and place it in:
   - `models/vosk-model-en-in`

## Setup

```bash
conda create -p venv python=3.12 -y
conda activate venv/
pip install -r requirements.txt
```

## Run terminal voice app

```bash
python voice_ollama.py
```

## Run web UI

```bash
streamlit run app_ui.py
```

The UI defaults to `http://localhost:8501` and talks to Ollama at `http://localhost:11434`.

You can override defaults with environment variables:

- `OLLAMA_URL` (default: `http://localhost:11434/api/generate`)
- `OLLAMA_MODEL` (default: `llama3.2:latest`)
