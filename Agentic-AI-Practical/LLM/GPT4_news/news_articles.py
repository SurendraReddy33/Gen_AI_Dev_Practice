import os
import requests
import json
from fastapi import FastAPI, HTTPException,Query
from dotenv import load_dotenv

load_dotenv()
NEWS_API_KEY = "5b502fb9f6d94a9c977ae3e9e49e03c8"

app = FastAPI()

def save_news_articles(article : dict , query : str):

    if not os.path.exists("GPT4_news/articles"):
        os.makedirs("GPT4_news/articles")

    query_clean = query.replace(" ", "_")
    filename = f"GPT4_news/articles/{query_clean}_articles.json"

    with open(filename,"w",encoding="utf-8") as f:
        json.dump(article,f,indent=4,ensure_ascii=False)
    
    print(f"Saved : {filename}")

def download_news_articles(query:str,page_size:int):

    url = "https://newsapi.org/v2/everything"

    params= {
        "q":query,
        "pageSize":page_size,
        "apiKey":NEWS_API_KEY
    }

    response = requests.get(url,params=params)

    if response.status_code == 200:
        data = response.json()

        articles = data.get("articles",[])

        
        save_news_articles(articles,query)
        
        return {"Message":f"Downloaded and saved {len(articles)} articles."}
    
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch news articles.")
    

@app.get("/fetch-news")
def fetch_news(
    query: str = Query(..., description="Search query for news articles."),
    page_size: int = Query(5, description="Number of articles to fetch.")
):
    """
    FastAPI GET endpoint to trigger download_news_article.
    Example: /fetch-news?query=AI&page_size=5
    """
    return download_news_articles(query, page_size)

if __name__ == "__main__":
    app()
