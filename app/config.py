"""RSS feed sources and app configuration."""

RSS_FEEDS = {
    "bbc": "http://feeds.bbci.co.uk/news/rss.xml",
    "reuters": "http://feeds.reuters.com/reuters/topNews",
    "cnn": "http://rss.cnn.com/rss/edition.rss",
    "aljazeera": "https://www.aljazeera.com/xml/rss/all.xml",
    "npr": "https://feeds.npr.org/1001/rss.xml",
}

DEFAULT_SENTENCE_COUNT = 4
MIN_SENTENCES = 3
MAX_SENTENCES = 5
