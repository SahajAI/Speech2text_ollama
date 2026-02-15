import json
import os
from typing import Optional

import requests
import streamlit as st

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:latest")


def query_ollama(prompt: str, model: Optional[str] = None) -> str:
    payload = {"model": model or OLLAMA_MODEL, "prompt": prompt}
    response = requests.post(OLLAMA_URL, json=payload, stream=True, timeout=120)
    response.raise_for_status()

    full_response = ""
    for line in response.iter_lines(decode_unicode=True):
        if not line:
            continue
        data = json.loads(line)
        full_response += data.get("response", "")
        if data.get("done", False):
            break

    return full_response.strip() or "(No response returned by Ollama)"


def check_ollama_status() -> tuple[bool, str]:
    base_url = OLLAMA_URL.replace("/api/generate", "")
    try:
        response = requests.get(f"{base_url}/api/tags", timeout=5)
        response.raise_for_status()
        return True, "Ollama is reachable"
    except Exception as exc:  # noqa: BLE001
        return False, f"Unable to connect to Ollama: {exc}"


st.set_page_config(page_title="Speech2Text + Ollama UI", page_icon="🎙️", layout="wide")

st.title("🎙️ Speech2Text + Ollama")
st.caption("Simple UI for testing your local Ollama model with typed input.")

with st.sidebar:
    st.header("Settings")
    selected_model = st.text_input("Ollama model", value=OLLAMA_MODEL)
    st.markdown("---")
    ok, status_message = check_ollama_status()
    if ok:
        st.success(status_message)
    else:
        st.error(status_message)
        st.info("Start Ollama first, then reload this page.")

if "history" not in st.session_state:
    st.session_state.history = []

for item in st.session_state.history:
    with st.chat_message(item["role"]):
        st.markdown(item["content"])

prompt = st.chat_input("Type your prompt and press Enter")
if prompt:
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                answer = query_ollama(prompt=prompt, model=selected_model)
                st.markdown(answer)
            except Exception as exc:  # noqa: BLE001
                answer = f"Error while calling Ollama: {exc}"
                st.error(answer)

    st.session_state.history.append({"role": "assistant", "content": answer})

col1, col2 = st.columns(2)
with col1:
    if st.button("Clear chat history"):
        st.session_state.history = []
        st.rerun()
with col2:
    st.link_button("Open Ollama docs", "https://github.com/ollama/ollama")
