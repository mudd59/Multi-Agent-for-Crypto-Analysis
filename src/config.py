from __future__ import annotations

import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4-mini").strip()
USE_LLM = os.getenv("USE_LLM", "true").lower().strip() in {"1", "true", "yes", "y"}

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "").strip()

COINS = {
    "Bitcoin": "BTC-USD",
    "Ethereum": "ETH-USD",
    "Solana": "SOL-USD",
    "Binance Coin": "BNB-USD",
    "Cardano": "ADA-USD",
    "XRP": "XRP-USD",
    "Dogecoin": "DOGE-USD",
    "Avalanche": "AVAX-USD",
    "Polkadot": "DOT-USD",
    "Chainlink": "LINK-USD",
}

NEWS_RSS_FEEDS = [
    "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "https://cointelegraph.com/rss",
    "https://bitcoinmagazine.com/.rss/full/",
]

POSITIVE_WORDS = {
    "surge", "rally", "gain", "bullish", "adoption", "approve", "approval", "inflow",
    "partnership", "growth", "breakout", "record", "upgrade", "support", "buy", "positive",
    "steigen", "anstieg", "gewinn", "wachstum", "positiv", "akzeptanz"
}

NEGATIVE_WORDS = {
    "crash", "fall", "drop", "bearish", "ban", "lawsuit", "hack", "exploit", "outflow",
    "liquidation", "risk", "warning", "decline", "sell", "negative", "fear", "regulation",
    "fallen", "verlust", "risiko", "warnung", "negativ", "verkaufen"
}


def get_api_status() -> dict:
    return {
        "openai_llm": bool(OPENAI_API_KEY and USE_LLM),
        "openai_model": OPENAI_MODEL,
        "tavily_news": bool(TAVILY_API_KEY),
        "rss_news_fallback": True,
        "yfinance": True,
    }
