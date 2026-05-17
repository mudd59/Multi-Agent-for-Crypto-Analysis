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
        lines.append(f"- {item.get('title', '')}: {item.get('summary', '')}")
    return "\n".join(lines)


def sentiment_agent(state: TradingState) -> dict:
    news_items = state.get("news_items", [])
    texts = [f"{item.get('title', '')} {item.get('summary', '')}" for item in news_items]

    fallback_score, fallback_summary = simple_sentiment_score(texts)

    llm = get_llm()
    if llm is None:
        return {
            "sentiment_score": fallback_score,
            "sentiment_summary": fallback_summary,
        }

    try:
        prompt = SENTIMENT_PROMPT.format(
            coin_name=state["coin_name"],
            symbol=state["symbol"],
            news_text=_news_text(news_items),
        )
        result: AgentAnalysis = llm.with_structured_output(AgentAnalysis).invoke(prompt)
        return {
            "sentiment_score": float(result.score),
            "sentiment_summary": result.summary,
        }
    except Exception:
        return {
            "sentiment_score": fallback_score,
            "sentiment_summary": fallback_summary,
        }
