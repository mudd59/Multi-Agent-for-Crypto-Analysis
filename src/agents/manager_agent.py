from __future__ import annotations

from src.llm import get_llm
from src.prompts.templates import MANAGER_PROMPT
from src.schemas import ManagerDecision
from src.state import TradingState


def _fallback_manager(state: TradingState) -> tuple[str, float, str]:
    signal = state.get("signal", "HOLD")
    risk = state.get("risk_level", "UNKNOWN")
    confidence = float(state.get("confidence", 0))
    position = float(state.get("position_size_pct", 0))

    if confidence < 55:
        return "HOLD", 0.0, "Confidence ist zu niedrig, deshalb HOLD."

    if signal == "BUY" and risk == "HIGH":
        return "HOLD", 0.0, "BUY-Signal wurde wegen HIGH Risk blockiert."

    if signal == "HOLD":
        return "HOLD", 0.0, "Trader-Agent ist unsicher, deshalb HOLD."

    return signal, min(position, 30.0), "Signal wurde vom Manager akzeptiert."


def manager_agent(state: TradingState) -> dict:
    fallback_decision, fallback_position, fallback_reason = _fallback_manager(state)

    llm = get_llm()
    if llm is None:
        return {
            "final_decision": fallback_decision,
            "position_size_pct": fallback_position,
            "debate_summary": state.get("debate_summary", "") + " " + fallback_reason,
        }

    try:
        prompt = MANAGER_PROMPT.format(
            coin_name=state["coin_name"],
            signal=state.get("signal", "HOLD"),
            confidence=state.get("confidence", 0),
            risk_level=state.get("risk_level", "UNKNOWN"),
            volatility=state.get("technical_summary", {}).get("volatility", 0),
            bullish_score=state.get("bullish_score", 0),
            bearish_score=state.get("bearish_score", 0),
        )
        result: ManagerDecision = llm.with_structured_output(ManagerDecision).invoke(prompt)
        return {
            "final_decision": result.final_decision,
            "position_size_pct": max(0.0, min(float(result.position_size_pct), 30.0)),
            "debate_summary": state.get("debate_summary", "") + " " + result.reasoning,
        }
    except Exception:
        return {
            "final_decision": fallback_decision,
            "position_size_pct": fallback_position,
            "debate_summary": state.get("debate_summary", "") + " " + fallback_reason,
        }
