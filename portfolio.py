import matplotlib.pyplot as plt

from config import (
    INITIAL_CAPITAL,
    TRADING_FEE,
    SYMBOL,
    START_DATE,
    END_DATE,
    SMA_FAST,
    SMA_SLOW,
    RSI_PERIOD
)

from data_loader import load_crypto_data
from indicators import add_indicators
from backtesting import generate_signals, run_backtest
from metrics import calculate_buy_and_hold_return


def main():
    df = load_crypto_data(SYMBOL, START_DATE, END_DATE)
    df = add_indicators(df, SMA_FAST, SMA_SLOW, RSI_PERIOD)
    df = generate_signals(df)

    result_df, summary, trades = run_backtest(
        df,
        INITIAL_CAPITAL,
        TRADING_FEE
    )

    buy_hold_value, buy_hold_return = calculate_buy_and_hold_return(
        result_df,
        INITIAL_CAPITAL
    )

    print("\n========== BACKTEST SUMMARY ==========\n")
    print(f"Symbol: {SYMBOL}")
    print(f"Period: {START_DATE} to {END_DATE}")
    print(f"Initial Capital: ${INITIAL_CAPITAL}")
    print()

    for key, value in summary.items():
        print(f"{key}: {value}")

    print("\n========== BENCHMARK ==========\n")
    print(f"Buy & Hold Final Value: {buy_hold_value}")
    print(f"Buy & Hold Return %: {buy_hold_return}")

    difference = summary["strategy_return_pct"] - buy_hold_return
    print(f"Strategy vs Benchmark Difference: {round(difference, 2)}%")

    print("\n========== RECENT DATA ==========\n")
    print(result_df.tail())

    result_df["Buy_Hold_Value"] = (
        INITIAL_CAPITAL / float(result_df["Close"].iloc[0])
    ) * result_df["Close"]

    # Chart 1: Portfolio comparison with executed trades only
    plt.figure(figsize=(14, 7))

    plt.plot(
        result_df["Date"],
        result_df["Portfolio_Value"],
        label="Strategy Portfolio",
        linewidth=2
    )

    plt.plot(
        result_df["Date"],
        result_df["Buy_Hold_Value"],
        label="Buy and Hold",
        linewidth=2
    )

    trade_df = result_df[result_df["Trade"].notna()]

    buy_points = trade_df[trade_df["Trade"] == "BUY"]
    sell_points = trade_df[trade_df["Trade"] == "SELL"]

    plt.scatter(
        buy_points["Date"],
        buy_points["Portfolio_Value"],
        marker="^",
        s=120,
        label="Executed BUY"
    )

    plt.scatter(
        sell_points["Date"],
        sell_points["Portfolio_Value"],
        marker="v",
        s=120,
        label="Executed SELL"
    )

    plt.title("Multi-Agent Portfolio Backtest")
    plt.xlabel("Date")
    plt.ylabel("Portfolio Value")
    plt.legend()
    plt.grid(True)
    plt.savefig("portfolio_dashboard.png")
    plt.show()

    # Chart 2: Drawdown
    plt.figure(figsize=(14, 4))

    plt.plot(
        result_df["Date"],
        result_df["Drawdown_Pct"],
        linewidth=2
    )

    plt.title("Portfolio Drawdown Over Time")
    plt.xlabel("Date")
    plt.ylabel("Drawdown %")
    plt.grid(True)
    plt.savefig("drawdown_dashboard.png")
    plt.show()


if __name__ == "__main__":
    main()