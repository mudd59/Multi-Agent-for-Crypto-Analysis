from __future__ import annotations

from typing import Any, Dict, List, TypedDict


class TradingState(TypedDict):
    coin_name: str
    symbol: str
    period: str
    initial_cash: float

    data: Any
    technical_summary: Dict[str, Any]
    news_items: List[Dict[str, str]]
    sentiment_score: float
    sentiment_summary: str

    bullish_evidence: List[str]
    bearish_evidence: List[str]
    bullish_score: float
    bearish_score: float
    debate_summary: str

    signal: str
    confidence: float
    risk_level: str
    position_size_pct: float
    final_decision: str

    final_value: float
    profit: float
    strategy_return: float
    buy_hold_return: float

    report: str
