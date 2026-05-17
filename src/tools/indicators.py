from __future__ import annotations

import numpy as np
import pandas as pd


def calculate_rsi(close: pd.Series, period: int = 14) -> pd.Series:
    delta = close.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


def add_indicators(data: pd.DataFrame) -> pd.DataFrame:
    if data is None or data.empty:
        return pd.DataFrame()

    data = data.copy()
    close = data["Close"].astype(float)

    data["SMA20"] = close.rolling(20).mean()
    data["SMA50"] = close.rolling(50).mean()
    data["RSI"] = calculate_rsi(close)
    data["Return"] = close.pct_change()
    data["Volatility"] = data["Return"].rolling(20).std()
    data["Volume_SMA20"] = data["Volume"].rolling(20).mean() if "Volume" in data.columns else np.nan

    return data.dropna()


def build_technical_summary(data: pd.DataFrame) -> dict:
    if data is None or data.empty:
        return {}

    latest = data.iloc[-1]
    summary = {
        "close": round(float(latest["Close"]), 4),
        "sma20": round(float(latest["SMA20"]), 4),
        "sma50": round(float(latest["SMA50"]), 4),
        "rsi": round(float(latest["RSI"]), 2),
        "volatility": round(float(latest["Volatility"]), 4),
    }

    summary["trend"] = "bullish" if summary["sma20"] > summary["sma50"] else "bearish"

    if summary["rsi"] < 30:
        summary["rsi_status"] = "oversold"
    elif summary["rsi"] > 70:
        summary["rsi_status"] = "overbought"
    else:
        summary["rsi_status"] = "neutral"

    return summary
