from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from src.agents.backtest_agent import backtest_agent
from src.agents.bearish_agent import bearish_agent
from src.agents.bullish_agent import bullish_agent
from src.agents.data_agent import data_agent
from src.agents.debate_agent import debate_agent
from src.agents.indicator_agent import indicator_agent
from src.agents.manager_agent import manager_agent
from src.agents.news_agent import news_agent
from src.agents.report_agent import report_agent
from src.agents.risk_agent import risk_agent
from src.agents.sentiment_agent import sentiment_agent
from src.agents.trader_agent import trader_agent
from src.state import TradingState


def build_graph():
    builder = StateGraph(TradingState)

    builder.add_node("data_agent", data_agent)
    builder.add_node("indicator_agent", indicator_agent)
    builder.add_node("news_agent", news_agent)
    builder.add_node("sentiment_agent", sentiment_agent)
    builder.add_node("bullish_agent", bullish_agent)
    builder.add_node("bearish_agent", bearish_agent)
    builder.add_node("debate_agent", debate_agent)
    builder.add_node("risk_agent", risk_agent)
    builder.add_node("trader_agent", trader_agent)
    builder.add_node("manager_agent", manager_agent)
    builder.add_node("backtest_agent", backtest_agent)
    builder.add_node("report_agent", report_agent)

    builder.add_edge(START, "data_agent")
    builder.add_edge("data_agent", "indicator_agent")
    builder.add_edge("indicator_agent", "news_agent")
    builder.add_edge("news_agent", "sentiment_agent")

    # Researcher Team split:
    # Bullish Agent and Bearish Agent receive the same prepared state
    # and analyze the market independently.
    builder.add_edge("sentiment_agent", "bullish_agent")
    builder.add_edge("sentiment_agent", "bearish_agent")

    # Discussion/Debate waits for BOTH researcher outputs.
    # Important: use a list here, not two separate edges, so the debate node
    # starts after Bullish and Bearish have both finished.
    builder.add_edge(["bullish_agent", "bearish_agent"], "debate_agent")

    # Architecture from the image: Researcher Team -> Trader -> Risk Team -> Manager.
    builder.add_edge("debate_agent", "trader_agent")
    builder.add_edge("trader_agent", "risk_agent")
    builder.add_edge("risk_agent", "manager_agent")
    builder.add_edge("manager_agent", "backtest_agent")
    builder.add_edge("backtest_agent", "report_agent")
    builder.add_edge("report_agent", END)

    return builder.compile()
