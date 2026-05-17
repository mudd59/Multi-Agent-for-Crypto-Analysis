from __future__ import annotations

from functools import lru_cache

from src.config import OPENAI_API_KEY, OPENAI_MODEL, USE_LLM


@lru_cache(maxsize=1)
def get_llm():
    """Return ChatOpenAI model if an API key is available, otherwise None."""
    if not OPENAI_API_KEY or not USE_LLM:
        return None

    try:
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model=OPENAI_MODEL, temperature=0)
    except Exception:
        return None


def is_llm_available() -> bool:
    return get_llm() is not None
