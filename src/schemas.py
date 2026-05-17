from __future__ import annotations

from typing import List, Literal
from pydantic import BaseModel, Field


class AgentAnalysis(BaseModel):
    score: float = Field(description="Score from -10 very negative to +10 very positive")
    confidence: float = Field(description="Confidence from 0 to 100")
    evidence: List[str] = Field(description="Concrete evidence points")
    summary: str = Field(description="Short human-readable summary")


class TraderDecision(BaseModel):
    signal: Literal["BUY", "SELL", "HOLD"]
    confidence: float = Field(description="Confidence from 0 to 100")
    reasoning: str


class ManagerDecision(BaseModel):
    final_decision: Literal["BUY", "SELL", "HOLD"]
    position_size_pct: float = Field(description="Suggested position size percentage, 0 to 100")
    reasoning: str
