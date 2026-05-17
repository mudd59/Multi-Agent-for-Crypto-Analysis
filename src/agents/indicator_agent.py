from __future__ import annotations

import pandas as pd

from src.state import TradingState
from src.tools.indicators import add_indicators, build_technical_summary


def indicator_agent(state: TradingState) -> dict:
    data = state["data"]

    if data is None or data.empty:
        return {"data": pd.DataFrame(), "technical_summary": {}}

    data = add_indicators(data)
    summary = build_technical_summary(data)

    return {"data": data, "technical_summary": summary}
