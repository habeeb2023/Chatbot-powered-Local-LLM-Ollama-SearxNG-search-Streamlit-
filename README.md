## 🚀 Setup & Installation

This project runs a local LLM (via **Ollama**) and augments it with web search through **SearxNG**, wrapped in a **Streamlit** UI.

### 1) Prerequisites

Install these first:

- **Git**  
  - Windows: https://git-scm.com/downloads
- **Python** 3.9–3.12 (with `pip` and `venv`)  
  - Windows: https://www.python.org/downloads/ (check “Add Python to PATH” during install)
- **Ollama** (local LLM runtime)  
  - https://ollama.com/download
- **Docker Desktop** (to run SearxNG)  
  - https://www.docker.com/products/docker-desktop

> macOS/Linux: use your package manager for Git/Python and install Ollama/Docker from the links above.

---

### 2) Get the code

```powershell
# Windows PowerShell
git clone https://github.com/<your-username>/chat-streamlit.git
cd chat-streamlit
