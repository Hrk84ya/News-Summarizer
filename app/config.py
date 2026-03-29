"""RSS feed sources and app configuration."""

RSS_FEEDS = {
    "bbc": "http://feeds.bbci.co.uk/news/rss.xml",
    "cnn": "http://rss.cnn.com/rss/edition.rss",
    "aljazeera": "https://www.aljazeera.com/xml/rss/all.xml",
    "npr": "https://feeds.npr.org/1001/rss.xml",
    "guardian": "https://www.theguardian.com/world/rss",
    "nytimes": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
    "ndtv": "https://feeds.feedburner.com/ndtvnews-top-stories",
    "toi": "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
}

DEFAULT_SENTENCE_COUNT = 4
MIN_SENTENCES = 3
MAX_SENTENCES = 5
