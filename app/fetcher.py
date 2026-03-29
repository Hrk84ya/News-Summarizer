"""Fetch news articles from RSS feeds."""

import feedparser
import httpx
from bs4 import BeautifulSoup

from app.config import RSS_FEEDS


async def fetch_feed(source: str) -> list[dict]:
    """Parse an RSS feed and return article metadata."""
    url = RSS_FEEDS.get(source)
    if not url:
        return []

    feed = feedparser.parse(url)
    articles = []
    for entry in feed.entries[:10]:
        articles.append({
            "title": entry.get("title", ""),
            "link": entry.get("link", ""),
            "published": entry.get("published", ""),
            "source": source,
        })
    return articles


async def fetch_article_text(url: str) -> str:
    """Fetch full article text from a URL."""
    try:
        async with httpx.AsyncClient(
            timeout=15, follow_redirects=True
        ) as client:
            resp = await client.get(url)
            resp.raise_for_status()
    except httpx.HTTPError:
        return ""

    soup = BeautifulSoup(resp.text, "html.parser")

    # Remove script/style elements
    for tag in soup(["script", "style", "nav", "header", "footer"]):
        tag.decompose()

    paragraphs = soup.find_all("p")
    text = " ".join(p.get_text(strip=True) for p in paragraphs)
    return text


async def fetch_all_feeds() -> list[dict]:
    """Fetch articles from all configured RSS sources."""
    all_articles = []
    for source in RSS_FEEDS:
        articles = await fetch_feed(source)
        all_articles.extend(articles)
    return all_articles
