import pandas as pd


def calculate_sma(
    df: pd.DataFrame,
    column: str = "Close",
    window: int = 20
) -> pd.Series:
    return df[column].rolling(window=window).mean()


def calculate_rsi(
    df: pd.DataFrame,
    column: str = "Close",
    period: int = 14
) -> pd.Series:
    delta = df[column].diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi


def add_indicators(
    df: pd.DataFrame,
    sma_fast: int,
    sma_slow: int,
    rsi_period: int
) -> pd.DataFrame:
    df = df.copy()

    df["SMA_FAST"] = calculate_sma(df, window=sma_fast)
    df["SMA_SLOW"] = calculate_sma(df, window=sma_slow)
    df["RSI"] = calculate_rsi(df, period=rsi_period)

    # Used by risk_agent.py
    df["Daily_Price_Return"] = df["Close"].pct_change().fillna(0)

    df = df.dropna()

    return df