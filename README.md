# 🔎 Local LLM + SearxNG Chat (Streamlit)

A simple **chat interface** that runs a local LLM (via [Ollama](https://ollama.com)) and augments it with **web search** through [SearxNG](https://docs.searxng.org/).  

The app uses [Streamlit](https://streamlit.io) for the UI and routes user queries either to the **local model** or to a **search-enabled agent** depending on whether the question requires up-to-date information.

---

## ✨ Features
- **Local-only chat** with an Ollama model (`llama3.1` by default).
- **Automatic routing**: decides when a web search is needed using a lightweight router agent.
- **SearxNG integration**: fetches recent news, facts, stats, or events when local knowledge is insufficient.
- **Streamlit UI**: clean chat interface with history, reset, and sidebar settings.
- **Overrides**:  
  - `/search your message` → force web search  
  - `/local your message` → force local-only response  

---

## 📦 Requirements

- **Python** 3.9–3.12  
- **Ollama** installed & running  
  - [Download Ollama](https://ollama.com/download)  
  - Pull your preferred model (default: `llama3.1`)  
    ```bash
    ollama pull llama3.1
    ollama serve
    ```
- **SearxNG** running locally at `http://localhost:8080`  
  - Quick Docker setup:  
    ```bash
    docker run -d --name searxng -p 8080:8080 searxng/searxng:latest
    ```
  - If using **Caddy** or another reverse proxy, make sure the base URL points correctly (no `/search` at the end).  

---

## ⚙️ Setup Instructions

Clone the repo:

```bash
git clone https://github.com/your-username/chat-streamlit.git
cd chat-streamlit
