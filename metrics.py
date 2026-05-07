import numpy as np
import pandas as pd


def calculate_total_return(initial_value: float, final_value: float) -> float:
    return ((final_value - initial_value) / initial_value) * 100


def calculate_max_drawdown(equity_curve: pd.Series) -> float:
    running_max = equity_curve.cummax()
    drawdown = (equity_curve - running_max) / running_max
    return drawdown.min() * 100


def calculate_sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0.0) -> float:
    if returns.std() == 0:
        return 0.0

    excess_returns = returns - risk_free_rate / 252
    return np.sqrt(252) * excess_returns.mean() / excess_returns.std()


def calculate_buy_and_hold_return(df: pd.DataFrame, initial_capital: float):
    first_price = float(df["Close"].iloc[0])
    last_price = float(df["Close"].iloc[-1])

    crypto_units = initial_capital / first_price
    final_value = crypto_units * last_price

    return_pct = calculate_total_return(initial_capital, final_value)

    return round(final_value, 2), round(return_pct, 2)