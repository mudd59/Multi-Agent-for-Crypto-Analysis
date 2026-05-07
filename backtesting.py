import pandas as pd

from metrics import (
    calculate_total_return,
    calculate_max_drawdown,
    calculate_sharpe_ratio,
)


from agents.voting_agent import final_agent_signal


def generate_signals(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["Signal"] = df.apply(final_agent_signal, axis=1)
    return df


def run_backtest(df: pd.DataFrame, initial_capital: float, trading_fee: float):
    cash = initial_capital
    crypto_units = 0
    position_open = False

    equity_curve = []
    trades = []
    trade_events = []

    for _, row in df.iterrows():
        price = float(row["Close"])
        signal = row["Signal"]
        trade_event = None

        if signal == "BUY" and not position_open:
            crypto_units = (cash * (1 - trading_fee)) / price
            cash = 0
            position_open = True
            trade_event = "BUY"

            trades.append({
                "type": "BUY",
                "price": price,
                "date": row["Date"]
            })

        elif signal == "SELL" and position_open:
            cash = crypto_units * price * (1 - trading_fee)
            crypto_units = 0
            position_open = False
            trade_event = "SELL"

            trades.append({
                "type": "SELL",
                "price": price,
                "date": row["Date"]
            })

        portfolio_value = cash + crypto_units * price

        equity_curve.append(portfolio_value)
        trade_events.append(trade_event)

    df["Portfolio_Value"] = equity_curve
    df["Daily_Return"] = df["Portfolio_Value"].pct_change().fillna(0)
    df["Trade"] = trade_events

    running_max = df["Portfolio_Value"].cummax()

    df["Drawdown_Pct"] = (
        (df["Portfolio_Value"] - running_max)
        / running_max
    ) * 100

    summary = {
        "initial_capital": initial_capital,
        "final_value": round(df["Portfolio_Value"].iloc[-1], 2),
        "strategy_return_pct": round(
            calculate_total_return(
                initial_capital,
                df["Portfolio_Value"].iloc[-1]
            ),
            2
        ),
        "max_drawdown_pct": round(
            calculate_max_drawdown(df["Portfolio_Value"]),
            2
        ),
        "sharpe_ratio": round(
            calculate_sharpe_ratio(df["Daily_Return"]),
            2
        ),
        "number_of_trades": len(trades),
    }

    return df, summary, trades