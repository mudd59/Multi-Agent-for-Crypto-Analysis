from __future__ import annotations

from typing import Dict, List

import feedparser

from src.config import NEWS_RSS_FEEDS, TAVILY_API_KEY


def _clean_text(value: str | None) -> str:
    if not value:
        return ""
    return " ".join(str(value).replace("\n", " ").split())


def _search_with_tavily(coin_name: str, symbol: str, max_items: int) -> List[Dict[str, str]]:
    if not TAVILY_API_KEY:
        return []

    try:
        from tavily import TavilyClient

        client = TavilyClient(api_key=TAVILY_API_KEY)
        query = f"latest crypto news {coin_name} {symbol.replace('-USD', '')}"
        response = client.search(query=query, max_results=max_items, topic="news")
        results = response.get("results", [])

        return [
            {
                "title": _clean_text(item.get("title")),
                "summary": _clean_text(item.get("content")),
                "link": item.get("url", ""),
                "source": "Tavily",
                "published": "",
            }
            for item in results
            if item.get("title")
        ]
    except Exception:
        return []


def _search_with_rss(coin_name: str, symbol: str, max_items: int) -> List[Dict[str, str]]:
    symbol_short = symbol.replace("-USD", "").lower()
    keywords = {coin_name.lower(), symbol_short, "crypto", "bitcoin", "ethereum"}
    collected: List[Dict[str, str]] = []

    for feed_url in NEWS_RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
        except Exception:
            continue

        for entry in feed.entries[:30]:
            title = _clean_text(getattr(entry, "title", ""))
            summary = _clean_text(getattr(entry, "summary", ""))
            text = f"{title} {summary}".lower()

            if coin_name.lower() in text or symbol_short in text or len(collected) < 3:
                collected.append(
                    {
                        "title": title,
                        "summary": summary[:500],
                        "link": getattr(entry, "link", ""),
                        "source": getattr(feed.feed, "title", "RSS"),
                        "published": getattr(entry, "published", ""),
                    }
                )

            if len(collected) >= max_items:
                return collected

    return collected[:max_items]


def fetch_crypto_news(coin_name: str, symbol: str, max_items: int = 8) -> List[Dict[str, str]]:
    tavily_results = _search_with_tavily(coin_name, symbol, max_items)
    if tavily_results:
        return tavily_results[:max_items]

    return _search_with_rss(coin_name, symbol, max_items)
