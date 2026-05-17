from __future__ import annotations

import re
from typing import Iterable

from src.config import NEGATIVE_WORDS, POSITIVE_WORDS


def simple_sentiment_score(texts: Iterable[str]) -> tuple[float, str]:
    combined = " ".join(texts).lower()
    words = re.findall(r"[a-zA-ZäöüÄÖÜß]+", combined)

    if not words:
        return 0.0, "Keine News-Texte für Sentiment gefunden."

    positive = sum(1 for w in words if w in POSITIVE_WORDS)
    negative = sum(1 for w in words if w in NEGATIVE_WORDS)
    total_hits = positive + negative

    if total_hits == 0:
        return 0.0, "Sentiment neutral: keine starken positiven oder negativen Wörter gefunden."

    score = ((positive - negative) / total_hits) * 10
    summary = f"Positive Treffer: {positive}, Negative Treffer: {negative}, Score: {score:.2f}"
    return round(score, 2), summary
