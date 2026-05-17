from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from src.config import COINS, get_api_status
from src.graph import build_graph


st.set_page_config(
    page_title="LangGraph Crypto Multi-Agent Analyzer",
    page_icon="📈",
    layout="wide",
)

st.title("📈 LangGraph Multi-Agent Crypto Analyzer")

st.write(
    """
Dieses Dashboard nutzt **LangGraph + LangChain + LLM Prompts**, um mehrere Agenten zu verbinden.
Der wichtige Researcher-Team-Teil läuft jetzt wie im Bild: **Bullish Agent und Bearish Agent analysieren parallel** und gehen danach gemeinsam in den **Discussion/Debate Agent**.

Flow: Data → Indicator → News → Sentiment → Bullish/Bearish parallel → Debate → Trader → Risk → Manager → Backtest → Report.
"""
)


@st.cache_resource
def get_graph():
    return build_graph()


graph = get_graph()


# =========================
# SIDEBAR
# =========================
st.sidebar.header("⚙️ Einstellungen")

api_status = get_api_status()
st.sidebar.write("### API Status")
st.sidebar.write("OpenAI LLM:", "✅ aktiv" if api_status["openai_llm"] else "⚠️ nicht aktiv")
st.sidebar.write("Model:", api_status["openai_model"])
st.sidebar.write("Tavily News:", "✅ aktiv" if api_status["tavily_news"] else "⚠️ RSS Fallback")
st.sidebar.write("yfinance:", "✅ ohne API Key")

selected_coin_names = st.sidebar.multiselect(
    "Wähle 3 bis 5 Coins:",
    options=list(COINS.keys()),
    default=["Bitcoin", "Ethereum", "Solana"],
    max_selections=5,
)

period = st.sidebar.selectbox(
    "Zeitraum:",
    ["3mo", "6mo", "1y", "2y"],
    index=2,
)

initial_cash = st.sidebar.number_input(
    "Startkapital in USD:",
    min_value=1000,
    max_value=1000000,
    value=10000,
    step=1000,
)

if len(selected_coin_names) < 3:
    st.warning("Bitte wähle mindestens 3 Coins aus.")
    st.stop()


# =========================
# GRAPH VISUALIZATION
# =========================
st.subheader("🧠 LangGraph Agent Workflow")

st.graphviz_chart(
    """
digraph {
    rankdir=LR;
    node [shape=box, style="rounded"];

    START -> DataAgent;
    DataAgent -> IndicatorAgent;
    IndicatorAgent -> NewsAgent;
    NewsAgent -> SentimentAgent;

    subgraph cluster_researcher_team {
        label="Researcher Team";
        style="rounded";
        color="orange";
        BullishAgent [label="Bullish Agent"];
        BearishAgent [label="Bearish Agent"];
        DebateAgent [label="Discussion / Debate"];
    }

    SentimentAgent -> BullishAgent;
    SentimentAgent -> BearishAgent;
    BullishAgent -> DebateAgent;
    BearishAgent -> DebateAgent;

    DebateAgent -> TraderAgent;
    TraderAgent -> RiskAgent;
    RiskAgent -> ManagerAgent;
    ManagerAgent -> BacktestAgent;
    BacktestAgent -> ReportAgent;
    ReportAgent -> END;
}
"""
)


# =========================
# RUN GRAPH
# =========================
results = []
price_comparison = pd.DataFrame()

with st.spinner("Agenten analysieren Coins..."):
    for coin_name in selected_coin_names:
        symbol = COINS[coin_name]

        initial_state = {
            "coin_name": coin_name,
            "symbol": symbol,
            "period": period,
            "initial_cash": float(initial_cash),
            "data": None,
            "technical_summary": {},
            "news_items": [],
            "sentiment_score": 0.0,
            "sentiment_summary": "",
            "bullish_evidence": [],
            "bearish_evidence": [],
            "bullish_score": 0.0,
            "bearish_score": 0.0,
            "debate_summary": "",
            "signal": "HOLD",
            "confidence": 0.0,
            "risk_level": "UNKNOWN",
            "position_size_pct": 0.0,
            "final_decision": "HOLD",
            "final_value": 0.0,
            "profit": 0.0,
            "strategy_return": 0.0,
            "buy_hold_return": 0.0,
            "report": "",
        }

        result = graph.invoke(initial_state)
        data = result["data"]

        if data is None or data.empty:
            st.error(f"Keine Daten für {coin_name} gefunden.")
            continue

        latest = data.iloc[-1]

        results.append(
            {
                "Coin": coin_name,
                "Symbol": symbol,
                "Price": round(float(latest["Close"]), 2),
                "RSI": round(float(latest["RSI"]), 2),
                "Volatility": round(float(latest["Volatility"]), 4),
                "Sentiment": round(float(result["sentiment_score"]), 2),
                "Bullish Score": round(float(result["bullish_score"]), 2),
                "Bearish Score": round(float(result["bearish_score"]), 2),
                "Signal": result["signal"],
                "Confidence": round(float(result["confidence"]), 1),
                "Risk": result["risk_level"],
                "Final Decision": result["final_decision"],
                "Position %": round(float(result["position_size_pct"]), 1),
                "Strategy Return %": round(float(result["strategy_return"]), 2),
                "Buy & Hold Return %": round(float(result["buy_hold_return"]), 2),
                "Result Object": result,
            }
        )

        normalized_price = data["Close"] / data["Close"].iloc[0] * 100
        price_comparison[coin_name] = normalized_price


# =========================
# SUMMARY TABLE
# =========================
st.subheader("📊 Coin Übersicht")

summary_df = pd.DataFrame(results)

if summary_df.empty:
    st.error("Keine Ergebnisse verfügbar.")
    st.stop()

display_df = summary_df.drop(columns=["Result Object"])
st.dataframe(display_df, use_container_width=True)


# =========================
# BEST COIN
# =========================
st.subheader("🏆 Beste Strategie-Performance")

best_coin = summary_df.sort_values("Strategy Return %", ascending=False).iloc[0]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Bester Coin", best_coin["Coin"])
col2.metric("Strategy Return", f'{best_coin["Strategy Return %"]}%')
col3.metric("Final Decision", best_coin["Final Decision"])
col4.metric("Risk", best_coin["Risk"])


# =========================
# PRICE COMPARISON
# =========================
st.subheader("📈 Normalisierter Preisvergleich")
st.line_chart(price_comparison)


# =========================
# DETAIL ANALYSIS
# =========================
st.subheader("🔍 Detailanalyse pro Coin")

for _, row in summary_df.iterrows():
    coin_name = row["Coin"]
    result = row["Result Object"]
    data = result["data"]

    with st.expander(f"Analyse für {coin_name}"):
        latest = data.iloc[-1]

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Preis", f'{float(latest["Close"]):.2f} USD')
        col2.metric("RSI", f'{float(latest["RSI"]):.2f}')
        col3.metric("Risiko", result["risk_level"])
        col4.metric("Entscheidung", result["final_decision"])

        st.write("### Technical Summary")
        st.json(result["technical_summary"])

        st.write("### News")
        if result["news_items"]:
            for item in result["news_items"][:5]:
                st.write(f"- **{item.get('title', '')}**")
                if item.get("link"):
                    st.caption(item.get("link"))
        else:
            st.write("Keine News gefunden.")

        st.write("### Sentiment")
        st.write(result["sentiment_summary"])

        st.write("### Bullish Evidence")
        if result["bullish_evidence"]:
            for item in result["bullish_evidence"]:
                st.write("✅", item)
        else:
            st.write("Keine bullishen Signale.")

        st.write("### Bearish Evidence")
        if result["bearish_evidence"]:
            for item in result["bearish_evidence"]:
                st.write("❌", item)
        else:
            st.write("Keine bearishen Signale.")

        st.write("### Preis mit SMA20 und SMA50")
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(data.index, data["Close"], label="Close")
        ax.plot(data.index, data["SMA20"], label="SMA20")
        ax.plot(data.index, data["SMA50"], label="SMA50")
        ax.set_title(f"{coin_name} Price with SMA20 and SMA50")
        ax.set_xlabel("Date")
        ax.set_ylabel("Price")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

        st.write("### Backtest Portfolio Value")
        fig2, ax2 = plt.subplots(figsize=(10, 4))
        ax2.plot(data.index, data["Portfolio_Value"], label="Portfolio Value")
        ax2.set_title(f"{coin_name} Backtest Portfolio Value")
        ax2.set_xlabel("Date")
        ax2.set_ylabel("Portfolio Value in USD")
        ax2.legend()
        ax2.grid(True)
        st.pyplot(fig2)

        st.write("### Agent Report")
        st.text(result["report"])


# =========================
# EXPLANATION
# =========================
st.subheader("📌 Projekt-Erklärung")

st.markdown(
    """
Dieses Projekt ist jetzt sauber aufgeteilt:

- **Data Agent:** lädt historische Coin-Daten mit `yfinance`.
- **Indicator Agent:** berechnet SMA20, SMA50, RSI, Return und Volatility.
- **News Agent:** sammelt aktuelle News über RSS oder Tavily.
- **Sentiment Agent:** bewertet die News-Stimmung mit Regeln oder LLM.
- **Bullish Agent:** sucht Kaufargumente.
- **Bearish Agent:** sucht Risiko- und Verkaufsargumente.
- **Debate Agent:** bekommt beide Ergebnisse und vergleicht Bullish vs. Bearish wie eine Discussion.
- **Trader Agent:** erzeugt aus der Discussion einen BUY / SELL / HOLD Vorschlag.
- **Risk Agent:** prüft danach den Vorschlag anhand der Volatilität.
- **Manager Agent:** trifft finale Entscheidung und Positionsgröße.
- **Backtest Agent:** testet einfache Strategie auf historischen Daten.
- **Report Agent:** schreibt den Bericht.
"""
)
