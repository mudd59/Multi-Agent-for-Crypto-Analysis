from __future__ import annotations

from src.state import TradingState
from src.tools.news_fetcher import fetch_crypto_news


def news_agent(state: TradingState) -> dict:
    news_items = fetch_crypto_news(
        coin_name=state["coin_name"],
        symbol=state["symbol"],
        max_items=8,
    )
    return {"news_items": news_items}
