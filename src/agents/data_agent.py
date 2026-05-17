from __future__ import annotations

import pandas as pd

from src.state import TradingState
from src.tools.market_data import download_market_data


def data_agent(state: TradingState) -> dict:
    data = download_market_data(state["symbol"], state["period"])

    if data is None or data.empty:
        return {"data": pd.DataFrame()}

    return {
        "data": data,
        "bullish_evidence": [],
        "bearish_evidence": [],
        "bullish_score": 0.0,
        "bearish_score": 0.0,
    }
