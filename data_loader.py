import yfinance as yf
import pandas as pd


def load_crypto_data(symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
    df = yf.download(symbol, start=start_date, end=end_date, auto_adjust=True)

    if df.empty:
        raise ValueError(f"No data found for {symbol}")

    df = df.reset_index()

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    return df