from __future__ import annotations

from src.llm import get_llm
from src.prompts.templates import REPORT_PROMPT
from src.state import TradingState


def _fallback_report(state: TradingState) -> str:
    return f"""
Coin: {state['coin_name']}
Symbol: {state['symbol']}

Signal: {state.get('signal', 'HOLD')}
Risk Level: {state.get('risk_level', 'UNKNOWN')}
Final Decision: {state.get('final_decision', 'HOLD')}
Position Size: {state.get('position_size_pct', 0):.1f}%

Strategy Return: {state.get('strategy_return', 0):.2f}%
Buy & Hold Return: {state.get('buy_hold_return', 0):.2f}%

Sentiment:
{state.get('sentiment_summary', '')}

Bullish Evidence:
{state.get('bullish_evidence', [])}

Bearish Evidence:
{state.get('bearish_evidence', [])}

Hinweis: Das ist nur eine Lern- und Paper-Trading-Analyse, keine Finanzberatung.
"""


def report_agent(state: TradingState) -> dict:
    fallback = _fallback_report(state)

    llm = get_llm()
    if llm is None:
        return {"report": fallback}

    try:
        prompt = REPORT_PROMPT.format(**state)
        report = llm.invoke(prompt).content
        return {"report": report}
    except Exception:
        return {"report": fallback}
