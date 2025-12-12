import os


BASE_URL = "https://newsapi.org/v2/everything"
NEWS_API_KEY = "5b502fb9f6d94a9c977ae3e9e49e03c8"
DEFAULT_QUERY = "bitcoin"
MAX_PAGES = 2
PAGE_SIZE = 10
LOG_DIR = "logs"
ARTICLE_STORE_BASE = "article_store"
QUEUE_DIR = os.path.join(ARTICLE_STORE_BASE, "queue")


