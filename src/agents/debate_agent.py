from __future__ import annotations

from src.llm import get_llm
from src.state import TradingState


def debate_agent(state: TradingState) -> dict:
    llm = get_llm()

    bullish_score = float(state.get("bullish_score", 0))
    bearish_score = float(state.get("bearish_score", 0))

    bullish_evidence = state.get("bullish_evidence", [])
    bearish_evidence = state.get("bearish_evidence", [])

    if llm is None:
        return {
            "debate_summary": (
                "LLM wurde nicht geladen. "
                f"Bullish Score: {bullish_score}, "
                f"Bearish Score: {bearish_score}."
            )
        }

    prompt = f"""
Du bist der Debate Agent eines Krypto-Analyse-Systems.

Analysierter Coin:
{state.get("coin_name")} ({state.get("symbol")})

Bullish Score:
{bullish_score}

Bullish Argumente:
{bullish_evidence}

Bearish Score:
{bearish_score}

Bearish Argumente:
{bearish_evidence}

Sentiment:
{state.get("sentiment_summary", "")}

Vergleiche die bullishe und bearishe Seite.

Schreibe auf Deutsch:
- 4 bis 6 vollständige Sätze
- stärkstes bullishes Argument
- stärkstes bearishes Argument
- neutrale Bewertung
- am Ende BUY-Bias, SELL-Bias oder HOLD-Bias

Gib keinen Python-Code aus.
Gib kein JSON aus.
Gib keine Markdown-Codeblöcke aus.
"""

    try:
        response = llm.invoke(prompt)

        content = response.content

        if isinstance(content, str):
            text = content.strip()
        else:
            text = str(content).strip()

        if not text:
            raise ValueError("Die LLM-Antwort ist leer.")

        return {
            "debate_summary": text
        }

    except Exception as e:
        print(
            f"DEBATE LLM ERROR: "
            f"{type(e).__name__}: {e}"
        )

        return {
            "debate_summary": (
                f"⚠️ Debate-LLM-Fehler: "
                f"{type(e).__name__}: {e}"
            )
        }
