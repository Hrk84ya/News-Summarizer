"""Extractive text summarization using sumy (TextRank)."""

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer

from app.config import DEFAULT_SENTENCE_COUNT


def summarize(text: str, sentence_count: int = DEFAULT_SENTENCE_COUNT) -> str:
    """
    Summarize text using TextRank extractive summarization.

    Args:
        text: The article text to summarize.
        sentence_count: Number of sentences in the summary (3-5).

    Returns:
        The extractive summary as a string.
    """
    if not text or not text.strip():
        return ""

    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = TextRankSummarizer()
    sentences = summarizer(parser.document, sentence_count)

    return " ".join(str(s) for s in sentences)
