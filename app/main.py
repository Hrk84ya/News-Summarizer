"""FastAPI news summarizer application."""

import nltk
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from app.config import RSS_FEEDS, MIN_SENTENCES, MAX_SENTENCES, DEFAULT_SENTENCE_COUNT
from app.fetcher import fetch_feed, fetch_article_text, fetch_all_feeds
from app.summarizer import summarize
from app.models import SummarizeRequest, SummaryResponse, ArticleListResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    nltk.download("punkt_tab", quiet=True)
    yield


app = FastAPI(
    title="News Summarizer API",
    description="Extractive news summarization using TextRank with automatic RSS fetching",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "app": "News Summarizer API",
        "version": "2.0.0",
        "docs": "/docs",
        "endpoints": ["/health", "/sources", "/news", "/news/{source}", "/summarize"],
    }


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/sources")
async def list_sources():
    """List available RSS news sources."""
    return {"sources": list(RSS_FEEDS.keys())}


@app.get("/news/{source}", response_model=ArticleListResponse)
async def get_summarized_news(
    source: str,
    sentence_count: int = Query(
        DEFAULT_SENTENCE_COUNT, ge=MIN_SENTENCES, le=MAX_SENTENCES
    ),
):
    """Fetch and summarize news from a specific RSS source."""
    if source not in RSS_FEEDS:
        raise HTTPException(
            status_code=404,
            detail=f"Source '{source}' not found. Available: {list(RSS_FEEDS.keys())}",
        )

    articles = await fetch_feed(source)
    results = []

    for article in articles:
        text = await fetch_article_text(article["link"])
        if not text:
            text = article.get("description", "")
        if not text:
            continue
        summary = summarize(text, sentence_count)
        if summary:
            results.append(SummaryResponse(
                title=article["title"],
                source=source,
                link=article["link"],
                summary=summary,
            ))

    return ArticleListResponse(articles=results, count=len(results))


@app.get("/news", response_model=ArticleListResponse)
async def get_all_news(
    sentence_count: int = Query(
        DEFAULT_SENTENCE_COUNT, ge=MIN_SENTENCES, le=MAX_SENTENCES
    ),
):
    """Fetch and summarize news from all RSS sources."""
    articles = await fetch_all_feeds()
    results = []

    for article in articles:
        text = await fetch_article_text(article["link"])
        if not text:
            text = article.get("description", "")
        if not text:
            continue
        summary = summarize(text, sentence_count)
        if summary:
            results.append(SummaryResponse(
                title=article["title"],
                source=article["source"],
                link=article["link"],
                summary=summary,
            ))

    return ArticleListResponse(articles=results, count=len(results))


@app.post("/summarize", response_model=SummaryResponse)
async def summarize_text(request: SummarizeRequest):
    """Summarize custom text (paste your own article)."""
    summary = summarize(request.text, request.sentence_count)
    if not summary:
        raise HTTPException(status_code=400, detail="Could not generate summary.")
    return SummaryResponse(summary=summary)
