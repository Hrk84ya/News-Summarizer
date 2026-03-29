# News Summarizer API

Extractive news summarizer that automatically fetches articles from RSS feeds and generates 3-5 sentence summaries using TextRank.

## Features

- Automatic news fetching from BBC, Reuters, CNN, Al Jazeera, NPR
- Fast extractive summarization (TextRank via sumy) — no GPU needed
- REST API built with FastAPI
- Paste your own text for summarization

## Quick Start

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/sources` | List available news sources |
| GET | `/news/{source}` | Summarized news from a source (e.g. `/news/bbc`) |
| GET | `/news` | Summarized news from all sources |
| POST | `/summarize` | Summarize custom text |

### Examples

```bash
# Get summarized BBC news
curl http://localhost:8000/news/bbc

# Get 5-sentence summaries from Reuters
curl "http://localhost:8000/news/reuters?sentence_count=5"

# Summarize your own text
curl -X POST http://localhost:8000/summarize \
  -H "Content-Type: application/json" \
  -d '{"text": "Your article text here...", "sentence_count": 4}'
```

## Docker

```bash
docker build -t news-summarizer .
docker run -p 8000:8000 news-summarizer
```

API docs available at `http://localhost:8000/docs`
