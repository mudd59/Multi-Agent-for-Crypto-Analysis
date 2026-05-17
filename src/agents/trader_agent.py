from __future__ import annotations

from src.llm import get_llm
from src.prompts.templates import TRADER_PROMPT
from src.schemas import TraderDecision
from src.state import TradingState


def _fallback_trader(state: TradingState) -> tuple[str, float]:
    bullish = float(state.get("bullish_score", 0))
    bearish = float(state.get("bearish_score", 0))
    diff = bullish - bearish

    if diff >= 2:
        return "BUY", min(90.0, 55.0 + diff * 8)
    if diff <= -2:
        return "SELL", min(90.0, 55.0 + abs(diff) * 8)
    return "HOLD", 55.0


def trader_agent(state: TradingState) -> dict:
    fallback_signal, fallback_confidence = _fallback_trader(state)

    llm = get_llm()
    if llm is None:
        return {"signal": fallback_signal, "confidence": fallback_confidence}

    try:
        prompt = TRADER_PROMPT.format(
            coin_name=state["coin_name"],
            symbol=state["symbol"],
            bullish_score=state.get("bullish_score", 0),
            bearish_score=state.get("bearish_score", 0),
            bullish_evidence=state.get("bullish_evidence", []),
            bearish_evidence=state.get("bearish_evidence", []),
            debate_summary=state.get("debate_summary", ""),
        )
        result: TraderDecision = llm.with_structured_output(TraderDecision).invoke(prompt)
        return {"signal": result.signal, "confidence": float(result.confidence)}
    except Exception:
        return {"signal": fallback_signal, "confidence": fallback_confidence}
