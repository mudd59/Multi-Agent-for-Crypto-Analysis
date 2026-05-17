from __future__ import annotations

from src.state import TradingState


def debate_agent(state: TradingState) -> dict:
    """Compare independent Bullish and Bearish researcher outputs.

    This node is the "Discussion" block from the architecture image.
    It receives evidence from both sides after LangGraph has executed
    bullish_agent and bearish_agent from the same sentiment/technical state.
    """
    bullish_score = float(state.get("bullish_score", 0))
    bearish_score = float(state.get("bearish_score", 0))
    bullish_evidence = state.get("bullish_evidence", [])
    bearish_evidence = state.get("bearish_evidence", [])

    diff = bullish_score - bearish_score

    if diff >= 2:
        winner = "Bullish"
        recommendation_bias = "BUY-Bias"
        summary = "Bullish-Seite ist deutlich stärker als Bearish-Seite."
    elif diff <= -2:
        winner = "Bearish"
        recommendation_bias = "SELL/HOLD-Bias"
        summary = "Bearish-Seite ist deutlich stärker als Bullish-Seite."
    else:
        winner = "Neutral"
        recommendation_bias = "HOLD-Bias"
        summary = "Bullish und Bearish liegen nah beieinander. Entscheidung eher vorsichtig."

    debate_summary = (
        f"Discussion Ergebnis: {summary} "
        f"Bullish Score: {bullish_score:.1f}, Bearish Score: {bearish_score:.1f}. "
        f"Stärkere Seite: {winner}. Bias: {recommendation_bias}. "
        f"Bullish Argumente: {len(bullish_evidence)}. "
        f"Bearish Argumente: {len(bearish_evidence)}."
    )

    return {"debate_summary": debate_summary}
