from __future__ import annotations

from src.state import TradingState


def risk_agent(state: TradingState) -> dict:
    """Risk Management Team.

    It receives the Trader Agent's transaction proposal and checks whether the
    market volatility allows a realistic paper-trading position size.
    """
    tech = state.get("technical_summary", {})
    volatility = float(tech.get("volatility", 0))
    signal = state.get("signal", "HOLD")

    if volatility > 0.06:
        risk_level = "HIGH"
        position_size_pct = 5.0
    elif volatility > 0.035:
        risk_level = "MEDIUM"
        position_size_pct = 15.0
    else:
        risk_level = "LOW"
        position_size_pct = 25.0

    # No position when the trader does not propose a trade.
    if signal == "HOLD":
        position_size_pct = 0.0

    return {
        "risk_level": risk_level,
        "position_size_pct": position_size_pct,
    }
