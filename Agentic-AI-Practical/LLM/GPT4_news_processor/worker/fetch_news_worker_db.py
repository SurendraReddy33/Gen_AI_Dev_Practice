import os
import requests
import json
import uuid
from fastapi import Query
from typing import Optional,List
from config.settings import (
    Base_url,
    NEWS_API_KEY,
    DEFAULT_QUERY,
    QUEUE_DIR,
    LOG_DIR,
    PAGE_SIZE,
    MAX_PAGES
)
from utils.image_handler import handle_article_image
from utils.logger import get_logger
from datetime import datetime,timezone
from tqdm import tqdm
from fastapi import APIRouter,HTTPException
from pymongo import MongoClient

logger = get_logger(__name__)

router = APIRouter()

def ensure_directores():
    os.makedirs(LOG_DIR,exist_ok=True)
    os.makedirs(QUEUE_DIR,exist_ok=True)



def fetch_articles(query):
    all_articles = []

    for page in range(1,MAX_PAGES+1):
        params = {
            "q":query,
            "pageSize":PAGE_SIZE,
            "page":page,
            "apikey":NEWS_API_KEY
        }

        response = requests.get(Base_url,params=params)
        response.raise_for_status()
        data = response.json()
        if "articles" in data:
            all_articles.extend(data["articles"])
            logger.info(f"Fetching the page : {page} -> {response.status_code} -> {response.url}")
        else:
            logger.info (f"Page {page} : Dose not have articles ")
        
        return all_articles
    
# =================== Mongo ==========================================

Mongo_Url = "mongodb+srv://surendrareddygandra3:onTwB6qFMES4HF24@genai-cluster.cb98ycb.mongodb.net/"
DB_NAME = "Resume_db"
COLLECTION_NAME = "news_articles"
def save_mongo(article_json):
    article_id = str(uuid.uuid4())
    try:
        client = MongoClient(Mongo_Url)
        db=client[DB_NAME]
        collection = db[COLLECTION_NAME]

        document = {
           "article_id":article_id,
           "title": article_json.get('title',""),
           "url":article_json.get("url",""),
           "fetched_at":article_json.get("fetched_at",""),
           "recommended_category": article_json.get('recommended_category'),
           "gpt4_suggestion_category":article_json.get('gpt4_suggestion_category'),
           "inserted_at":datetime.utcnow()
        }

        # skip if already exists

        if not collection.find_one({"article_id":article_id}):
            collection.insert_one(document)
            logger.info(f"Data Stored Sucessfully {article_id} in MongoDB.")
        else:
            logger.info(f"Article {article_id} already exists.")
    except Exception as e:
        logger.error(f"Mongo Insert error for the article {article_id} : {e}")
        


def save_articles(article):
    article_id = str(uuid.uuid4())
    article["fetched_at"]=datetime.now(timezone.utc).isoformat()
    # file_path = os.path.join(QUEUE_DIR,f"{article_id}.json")

    folder_path = os.path.join(QUEUE_DIR,article_id)
    os.makedirs(folder_path,exist_ok=True)

    image_path = handle_article_image(article.get('urlToImage'),folder_path,article_id)
    article["article_image_original"] = image_path.replace("\\","/")

    json_path = os.path.join(folder_path,f"{article_id}.json")

    try:      # for only articles pass file_path 
        with open(json_path,"w",encoding="utf-8") as f:
            json.dump(article,f,indent=4)
        logger.info (f"Saved article to {json_path}")
    except Exception as e:
        logger.error(f"Error saving article {article_id}: {e}")


@router.post("/create_news_article")
def create_news_article(query : Optional[str] = Query(None,description="Query")):
    
    ensure_directores()
    logger.info ("Starting fetch for api....")
    # Fetch Articles
    articles = fetch_articles(query)
    logger.info (f"Total Fetched Articles are {len(articles)}")
   
    # Save Articles in Folder

    for idx, article in enumerate (tqdm(articles,desc="Saving Articles")):
        if article.get("title") and article.get("url"):
            save_articles(article)
            save_mongo(article)

    return {"Message":"Success "}

