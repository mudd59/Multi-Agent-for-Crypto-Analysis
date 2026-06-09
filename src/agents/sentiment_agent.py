from __future__ import annotations

from src.llm import get_llm
from src.prompts.templates import SENTIMENT_PROMPT
from src.schemas import AgentAnalysis
from src.state import TradingState
from src.tools.sentiment import simple_sentiment_score


def _news_text(news_items: list[dict]) -> str:
    if not news_items:
        return "No news found."

    lines = []

    for item in news_items:
        title = item.get("title", "")
        summary = item.get("summary", "")
        lines.append(f"- {title}: {summary}")

    return "\n".join(lines)


def sentiment_agent(state: TradingState) -> dict:
    news_items = state.get("news_items", [])

    texts = [
        f"{item.get('title', '')} {item.get('summary', '')}"
        for item in news_items
    ]

    fallback_score, fallback_summary = simple_sentiment_score(texts)

    llm = get_llm()

    if llm is None:
        return {
            "sentiment_score": fallback_score,
            "sentiment_summary": (
                "⚠️ LLM wurde nicht geladen. Fallback: "
                + fallback_summary
            ),
        }

    try:
        prompt = SENTIMENT_PROMPT.format(
            coin_name=state["coin_name"],
            symbol=state["symbol"],
            news_text=_news_text(news_items),
        )

        structured_llm = llm.with_structured_output(
            AgentAnalysis,
            method="json_schema",
            include_raw=True,
        )

        response = structured_llm.invoke(prompt)

        if response.get("parsing_error") is not None:
            raise response["parsing_error"]

        result = response.get("parsed")

        if result is None:
            raise ValueError("Keine gültige LLM-Antwort erhalten.")

        score = max(-10.0, min(float(result.score), 10.0))

        return {
            "sentiment_score": score,
            "sentiment_summary": result.summary,
        }

    except Exception as e:
        print(
            f"SENTIMENT LLM ERROR: "
            f"{type(e).__name__}: {e}"
        )

        return {
            "sentiment_score": fallback_score,
            "sentiment_summary": (
                f"⚠️ LLM-Fehler: {type(e).__name__}: {e}. "
                f"Fallback: {fallback_summary}"
            ),
        }
