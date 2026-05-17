from __future__ import annotations

from src.llm import get_llm
from src.prompts.templates import BULLISH_PROMPT
from src.schemas import AgentAnalysis
from src.state import TradingState


def _fallback_bullish(state: TradingState) -> tuple[list[str], float]:
    tech = state.get("technical_summary", {})
    evidence = []
    score = 0.0

    if tech.get("trend") == "bullish":
        evidence.append("SMA20 > SMA50: kurzfristiger Trend ist stärker als langfristiger Trend.")
        score += 3

    if tech.get("rsi_status") == "oversold":
        evidence.append("RSI < 30: Coin wirkt überverkauft, mögliche Erholung.")
        score += 2
    elif tech.get("rsi_status") == "neutral":
        evidence.append("RSI ist neutral: kein starker Überkauft-Druck.")
        score += 1

    if float(tech.get("volatility", 0)) < 0.04:
        evidence.append("Volatilität ist relativ niedrig.")
        score += 1

    if float(state.get("sentiment_score", 0)) > 1:
        evidence.append("News-/Social-Sentiment ist positiv.")
        score += 2

    return evidence, min(score, 10)


def bullish_agent(state: TradingState) -> dict:
    fallback_evidence, fallback_score = _fallback_bullish(state)

    llm = get_llm()
    if llm is None:
        return {"bullish_evidence": fallback_evidence, "bullish_score": fallback_score}

    try:
        prompt = BULLISH_PROMPT.format(
            coin_name=state["coin_name"],
            symbol=state["symbol"],
            technical_summary=state.get("technical_summary", {}),
            sentiment_score=state.get("sentiment_score", 0),
            sentiment_summary=state.get("sentiment_summary", ""),
        )
        result: AgentAnalysis = llm.with_structured_output(AgentAnalysis).invoke(prompt)
        score = max(0.0, min(float(result.score), 10.0))
        return {"bullish_evidence": result.evidence, "bullish_score": score}
    except Exception:
        return {"bullish_evidence": fallback_evidence, "bullish_score": fallback_score}
