from __future__ import annotations

from src.llm import get_llm
from src.prompts.templates import BEARISH_PROMPT
from src.schemas import AgentAnalysis
from src.state import TradingState


def _fallback_bearish(state: TradingState) -> tuple[list[str], float]:
    tech = state.get("technical_summary", {})
    evidence = []
    score = 0.0

    if tech.get("trend") == "bearish":
        evidence.append("SMA20 < SMA50: kurzfristiger Trend ist schwächer als langfristiger Trend.")
        score += 3

    if tech.get("rsi_status") == "overbought":
        evidence.append("RSI > 70: Coin wirkt überkauft, Rücksetzer möglich.")
        score += 2

    if float(tech.get("volatility", 0)) > 0.06:
        evidence.append("Volatilität ist hoch: Risiko ist erhöht.")
        score += 2

    if float(state.get("sentiment_score", 0)) < -1:
        evidence.append("News-/Social-Sentiment ist negativ.")
        score += 2

    return evidence, min(score, 10)


def bearish_agent(state: TradingState) -> dict:
    fallback_evidence, fallback_score = _fallback_bearish(state)

    llm = get_llm()
    if llm is None:
        return {"bearish_evidence": fallback_evidence, "bearish_score": fallback_score}

    try:
        prompt = BEARISH_PROMPT.format(
            coin_name=state["coin_name"],
            symbol=state["symbol"],
            technical_summary=state.get("technical_summary", {}),
            sentiment_score=state.get("sentiment_score", 0),
            sentiment_summary=state.get("sentiment_summary", ""),
        )
        result: AgentAnalysis = llm.with_structured_output(AgentAnalysis).invoke(prompt)
        score = max(0.0, min(float(result.score), 10.0))
        return {"bearish_evidence": result.evidence, "bearish_score": score}
    except Exception:
        return {"bearish_evidence": fallback_evidence, "bearish_score": fallback_score}
