from __future__ import annotations

import pandas as pd

from src.state import TradingState


def backtest_agent(state: TradingState) -> dict:
    data = state["data"]

    if data is None or data.empty:
        return {
            "final_value": 0.0,
            "profit": 0.0,
            "strategy_return": 0.0,
            "buy_hold_return": 0.0,
            "data": pd.DataFrame(),
        }

    initial_cash = float(state["initial_cash"])
    cash = initial_cash
    crypto = 0.0
    portfolio_values = []

    for _, row in data.iterrows():
        price = float(row["Close"])

        # Simple strategy for backtest only:
        # Buy 50% when trend is bullish and RSI is not overbought.
        if float(row["SMA20"]) > float(row["SMA50"]) and float(row["RSI"]) < 70 and cash > 0:
            amount_to_invest = cash * 0.5
            crypto += amount_to_invest / price
            cash -= amount_to_invest

        # Sell everything when trend turns bearish.
        elif float(row["SMA20"]) < float(row["SMA50"]) and crypto > 0:
            cash += crypto * price
            crypto = 0.0

        total_value = cash + crypto * price
        portfolio_values.append(total_value)

    data = data.copy()
    data["Portfolio_Value"] = portfolio_values

    final_value = float(portfolio_values[-1])
    profit = final_value - initial_cash
    strategy_return = (profit / initial_cash) * 100

    buy_hold_return = (
        (float(data["Close"].iloc[-1]) - float(data["Close"].iloc[0]))
        / float(data["Close"].iloc[0])
    ) * 100

    return {
        "data": data,
        "final_value": final_value,
        "profit": profit,
        "strategy_return": strategy_return,
        "buy_hold_return": buy_hold_return,
    }
