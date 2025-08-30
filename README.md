# 🔎 Local LLM + SearxNG Chat Assistant

A powerful **AI chat assistant** that combines the best of both worlds: **privacy-focused local inference** using [Ollama](https://ollama.com) with **real-time web search** capabilities through [SearxNG](https://docs.searxng.org/). 

The assistant intelligently routes your queries - using local knowledge for general questions and web search for current events, facts, and time-sensitive information.

![Python](https://img.shields.io/badge/python-v3.9+-blue.svg)
![Ollama](https://img.shields.io/badge/ollama-compatible-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

---

## ✨ Features

- 🤖 **Local LLM Chat** - Private, offline conversations using Ollama models
- 🧠 **Smart Routing** - Automatically detects when web search is needed
- 🔍 **Real-time Search** - Fetches current news, prices, events, and facts via SearxNG
- 🎯 **Manual Overrides** - Force local-only or web-search modes with simple commands
- 💬 **Clean Interface** - User-friendly chat UI with conversation history
- 🔒 **Privacy First** - All processing happens locally, no data sent to external APIs
- ⚡ **Fast Response** - Optimized for quick local inference and efficient search

---

## 🚀 Quick Start Guide

### Prerequisites

Before you begin, ensure you have:
- **Python 3.9-3.12** installed
- **Docker** installed (for SearxNG)
- **Git** installed

### Step 1: Install Ollama

#### Windows/macOS:
1. Download Ollama from [ollama.com](https://ollama.com/download)
2. Run the installer
3. Open terminal/command prompt and verify installation:
   ```bash
   ollama --version
