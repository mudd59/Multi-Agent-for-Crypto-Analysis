from __future__ import annotations

import pandas as pd
import yfinance as yf


def download_market_data(symbol: str, period: str = "1y") -> pd.DataFrame:
    data = yf.download(
        symbol,
        period=period,
        interval="1d",
        auto_adjust=True,
        progress=False,
    )

    if data is None or data.empty:
        return pd.DataFrame()

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    needed_columns = [col for col in ["Open", "High", "Low", "Close", "Volume"] if col in data.columns]
    data = data[needed_columns].copy().dropna()
    return data
