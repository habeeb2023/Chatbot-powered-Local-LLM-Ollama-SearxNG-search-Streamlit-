# app.py
import json
import os
import re
import streamlit as st
from dotenv import load_dotenv

from agents import make_chat_agent, make_search_agent, make_router

load_dotenv()  # loads .env if present

st.set_page_config(page_title="LLM + SearxNG Chat", page_icon="🔎", layout="wide")

# --- Sidebar controls ---------------------------------------------------------
with st.sidebar:
    st.header("Settings")
    model_id = st.text_input("Ollama model", os.getenv("MODEL_ID", "llama3.1"))
    model_cutoff = st.text_input("Model cutoff", os.getenv("MODEL_CUTOFF", "2021-12-31"))
    searx_url = st.text_input("SearxNG URL", os.getenv("SEARXNG_PUBLIC_URL", "http://localhost:8080"))
    st.caption("Make sure `ollama serve` is running and the model is pulled.")

    force_mode = st.radio("Routing", ["Auto (router decides)", "Force Local (/local)", "Force Web (/search)"], index=0)

    if st.button("Reset conversation"):
        st.session_state.clear()
        st.experimental_rerun()

# --- Session state ------------------------------------------------------------
if "chat" not in st.session_state:
    st.session_state.chat = []
if "agents" not in st.session_state:
    st.session_state.agents = {
        "chat": make_chat_agent(model_id),
        "search": make_search_agent(model_id, searx_url),
        "router": make_router(model_id, model_cutoff),
    }

# helper: (re)build agents if settings changed
def refresh_agents():
    st.session_state.agents = {
        "chat": make_chat_agent(model_id),
        "search": make_search_agent(model_id, searx_url),
        "router": make_router(model_id, model_cutoff),
    }

# Detect changes
if st.session_state.get("last_settings") != (model_id, model_cutoff, searx_url):
    refresh_agents()
    st.session_state.last_settings = (model_id, model_cutoff, searx_url)

chat_agent = st.session_state.agents["chat"]
search_agent = st.session_state.agents["search"]
router = st.session_state.agents["router"]

st.title("🔎 Chat: Local or Search-Routed")

st.markdown(
    """
- **Auto** mode lets the router choose when to search.
- Use commands in your message:
  - `/search your message` → force web
  - `/local your message`  → force local
"""
)

# Render history
for msg in st.session_state.chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Chat input ---------------------------------------------------------------
user_text = st.chat_input("Type a message…")
if user_text:
    st.session_state.chat.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    # Routing decision
    lower = user_text.lower()
    manual_force = None
    if lower.startswith("/search "):
        manual_force = "web"
        query = user_text[len("/search "):].strip()
    elif lower.startswith("/local "):
        manual_force = "local"
        query = user_text[len("/local "):].strip()
    else:
        query = user_text

    # Apply sidebar override if used
    if force_mode == "Force Local (/local)" and manual_force is None:
        manual_force = "local"
    elif force_mode == "Force Web (/search)" and manual_force is None:
        manual_force = "web"

    # Decide and respond
    if manual_force == "local":
        with st.chat_message("assistant"):
            resp = chat_agent.run(query).content
            st.markdown(resp)
        st.session_state.chat.append({"role": "assistant", "content": resp})

    elif manual_force == "web":
        with st.chat_message("assistant"):
            enriched = f"{query}\n\nIf needed, use SearxNG to gather recent or factual sources first, then answer succinctly."
            resp = search_agent.run(enriched).content
            st.markdown(resp)
        st.session_state.chat.append({"role": "assistant", "content": resp})

    else:
        # Auto route: ask router first
        router_prompt = (
            f"User asked: {query}\n"
            "Decide search necessity per the rules and respond with the JSON line."
        )
        route_raw = router.run(router_prompt).content
        m = re.search(r"\{.*\}", route_raw.strip(), re.DOTALL)
        decision = {"search": False, "reason": "fallback:no-json", "queries": []}
        if m:
            try:
                data = json.loads(m.group(0))
                decision.update({
                    "search": bool(data.get("search", False)),
                    "reason": data.get("reason", ""),
                    "queries": data.get("queries", []) or []
                })
            except Exception:
                decision["reason"] = "fallback:json-parse-failed"

        # Route accordingly
        if decision["search"]:
            seed = f" Seed queries to try: {', '.join(decision['queries'])}" if decision["queries"] else ""
            enriched = f"{query}\n\nIf needed, use SearxNG to gather recent or factual sources first, then answer succinctly.{seed}"
            with st.chat_message("assistant"):
                resp = search_agent.run(enriched).content
                st.markdown(resp)
            st.session_state.chat.append({"role": "assistant", "content": resp})
        else:
            with st.chat_message("assistant"):
                resp = chat_agent.run(query).content
                st.markdown(resp)
            st.session_state.chat.append({"role": "assistant", "content": resp})
