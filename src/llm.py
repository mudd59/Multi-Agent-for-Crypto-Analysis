from __future__ import annotations

import os
from functools import lru_cache

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()


def _get_secret(name: str, default: str = "") -> str:
    """
    Liest zuerst aus Environment/.env.
    Falls die App auf Streamlit Cloud läuft, versucht sie zusätzlich st.secrets.
    """
    value = os.getenv(name)
    if value:
        return value.strip()

    try:
        import streamlit as st

        value = st.secrets.get(name, default)
        if value:
            return str(value).strip()
    except Exception:
        pass

    return default


@lru_cache(maxsize=1)
def get_llm():
    """
    Gibt ein LLM zurück:
    - huggingface: nutzt Hugging Face Router
    - local: nutzt LocalAI/Ollama/LM Studio über OpenAI-compatible API
    - none/false: gibt None zurück
    """

    use_llm = _get_secret("USE_LLM", "false").lower() == "true"

    if not use_llm:
        return None

    provider = _get_secret("LLM_PROVIDER", "huggingface").lower()

    if provider == "huggingface":
        hf_token = _get_secret("HF_TOKEN")
        hf_model = _get_secret("HF_MODEL", "meta-llama/Llama-3.1-8B-Instruct:cerebras")

        if not hf_token:
            return None

        return ChatOpenAI(
            api_key=hf_token,
            base_url="https://router.huggingface.co/v1",
            model=hf_model,
            temperature=0.2,
        )

    if provider == "local":
        base_url = _get_secret("OPENAI_BASE_URL", "http://localhost:8080/v1")
        model = _get_secret("OPENAI_MODEL", "")
        api_key = _get_secret("OPENAI_API_KEY", "local")

        if not model:
            return None

        return ChatOpenAI(
            api_key=api_key,
            base_url=base_url,
            model=model,
            temperature=0.2,
        )

    return None


def is_llm_available() -> bool:
    use_llm = _get_secret("USE_LLM", "false").lower() == "true"

    if not use_llm:
        return False

    provider = _get_secret("LLM_PROVIDER", "huggingface").lower()

    if provider == "huggingface":
        return bool(_get_secret("HF_TOKEN"))

    if provider == "local":
        return bool(_get_secret("OPENAI_MODEL"))

    return False
