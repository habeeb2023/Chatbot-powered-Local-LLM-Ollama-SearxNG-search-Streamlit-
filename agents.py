# agents.py
# pip install "agno[tools]"

import os
from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.tools.searxng import SearxngTools

MODEL_ID = os.getenv("MODEL_ID", "llama3.1")
MODEL_CUTOFF = os.getenv("MODEL_CUTOFF", "2021-12-31")
PUBLIC_SEARX_URL = os.getenv("SEARXNG_PUBLIC_URL", "http://localhost:8080")

def make_chat_agent(model_id: str | None = None):
    return Agent(
        model=Ollama(id=model_id or MODEL_ID),
        markdown=True,
        instructions=(
            "You are a friendly, helpful chat assistant. "
            "Answer from your own knowledge and reasoning. Do NOT browse."
        ),
    )

def make_search_agent(model_id: str | None = None, searx_url: str | None = None):
    searxng = SearxngTools(
        host=(searx_url or PUBLIC_SEARX_URL),  # base URL only
        engines=[],
        fixed_max_results=5,
        news=True,
        science=True,
    )
    return Agent(
        model=Ollama(id=model_id or MODEL_ID),
        tools=[searxng],
        markdown=True,
        instructions=(
            "You are a research assistant. Use the SearxNG tool to gather sources "
            "for current events, time-sensitive data (news, prices, schedules), "
            "or whenever accuracy depends on external facts. Then synthesize clearly "
            "and, when possible, mention site names or domains for attribution."
        ),
    )

def make_router(model_id: str | None = None, cutoff: str | None = None):
    cutoff = cutoff or MODEL_CUTOFF
    return Agent(
        model=Ollama(id=model_id or MODEL_ID),
        markdown=False,
        instructions=(
            "You decide if web search is needed BEFORE answering.\n"
            f"Knowledge cutoff: {cutoff}.\n"
            "Return a single line as JSON with fields:\n"
            '{"search": true|false, "reason": "...", "queries": ["optional", "queries"]}\n'
            "Use search=true if ANY of these are true:\n"
            "- The user asks for news, prices, schedules, events, releases, rankings, sports, weather.\n"
            "- The topic likely changed after the cutoff or is time-sensitive.\n"
            "- The request needs exact, verifiable facts, or citations.\n"
            "- You are not confident you can answer from model knowledge alone.\n"
            "Otherwise, set search=false.\n"
            "Keep the JSON compact. No extra text."
        ),
    )
