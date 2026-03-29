"""Fetch news articles from RSS feeds."""

import logging
import feedparser
import httpx
from bs4 import BeautifulSoup

from app.config import RSS_FEEDS

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


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
            "source": source,
            "description": entry.get("summary", ""),
        })
    return articles


async def fetch_article_text(url: str) -> str:
    """Fetch full article text from a URL."""
    try:
        async with httpx.AsyncClient(
            timeout=15, follow_redirects=True, headers=HEADERS
        ) as client:
            resp = await client.get(url)
            resp.raise_for_status()
    except httpx.HTTPError as e:
        logger.warning(f"Failed to fetch {url}: {e}")
        return ""

    soup = BeautifulSoup(resp.text, "html.parser")

    # Remove non-content elements
    for tag in soup(["script", "style", "nav", "header", "footer", "aside", "figure", "figcaption"]):
        tag.decompose()

    # Try article tag first, then fall back to all paragraphs
    article = soup.find("article")
    container = article if article else soup

    paragraphs = container.find_all("p")
    text = " ".join(p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 40)

    if len(text) < 100:
        logger.warning(f"Insufficient text extracted from {url} ({len(text)} chars)")

    return text


async def fetch_all_feeds() -> list[dict]:
    """Fetch articles from all configured RSS sources."""
    all_articles = []
    for source in RSS_FEEDS:
        articles = await fetch_feed(source)
        all_articles.extend(articles)
    return all_articles
