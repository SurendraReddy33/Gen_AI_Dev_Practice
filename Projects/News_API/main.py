from app.data.user_data import save_to_json
from app.services.news_service import (
    mean_embedding,
    fetch_news_articles,
    generate_headlines,
    process_news_articles
)

file_path = "app\\data\\news_articles.json"  # Using double backslashes


NEWS_API_URL = "https://newsapi.org/v2/everything?q=bitcoin&apiKey=5b502fb9f6d94a9c977ae3e9e49e03c8"
API_KEY = "5b502fb9f6d94a9c977ae3e9e49e03c8"
HEADLINE_COUNT = 5
ARTICLE_COUNT = 5


def main():
    articles = fetch_news_articles(API_KEY, ARTICLE_COUNT)
    processed_data=process_news_articles(articles)
    save_to_json(processed_data,file_path)


if __name__ == "__main__":
    main()
    







