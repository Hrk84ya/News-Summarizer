"""Pydantic models for API request/response."""

from pydantic import BaseModel, Field

from app.config import MIN_SENTENCES, MAX_SENTENCES, DEFAULT_SENTENCE_COUNT


class SummarizeRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text to summarize")
    sentence_count: int = Field(
        DEFAULT_SENTENCE_COUNT, ge=MIN_SENTENCES, le=MAX_SENTENCES
    )


class SummaryResponse(BaseModel):
    title: str = ""
    source: str = ""
    link: str = ""
    summary: str = ""


class ArticleListResponse(BaseModel):
    articles: list[SummaryResponse]
    count: int
