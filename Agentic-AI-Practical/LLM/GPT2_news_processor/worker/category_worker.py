import os
import json
from tqdm import tqdm
from utils.logger import get_logger
from openai import OpenAI

ARTICLE_STORE_BASE = os.getenv("ARTICLE_STORE_BASE", "article_store")
QUEUE_DIR = os.path.join(ARTICLE_STORE_BASE, "queue")
INPROGRESS_DIR = os.path.join(ARTICLE_STORE_BASE, "inprogress")
COMPLETED_DIR = os.path.join(ARTICLE_STORE_BASE, "completed")
FAILED_DIR = os.path.join(ARTICLE_STORE_BASE, "failed")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

logger = get_logger("category_logger")
client = OpenAI(api_key=OPENAI_API_KEY)

CATEGORIES = [
   "Politics",
   "Finance",
   "Health",
   "Science", 
   "Technology", 
   "Sports", 
   "Crypto Currency",
   "Other",
   "Entertainment"
]

CATEGORY_PROMPT = (
    "Given the title, description, content of a news article, identify the most suitable category from the list "
    f"{','.join(CATEGORIES)}. If none matches then return 'Other'."
)

RAW_CATEGORY_PROMPT = (
    "Given the title, description, content of a news article, suggest a sytentic category name that best describes its subject. e.g. 'Crypto', 'Climate Newss"
)

def  get_cateogry_from_gpt4 (categories, context):
    try:
        response = client.chat.completions.create(
            model = "gpt-4",
            messages = [
                {"role" : "user" , "content" : categories},
                {"role" : "system", "content" :context}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error (f"GPT4 Category Classification failed {str(e)}")
        return None


def process_article (article_id):
    folder_path = os.path.join (QUEUE_DIR, article_id)
    article_json_file = os.path.join (folder_path, f"{article_id}.json")

    if not os.path.exists(article_json_file):
        logger.error (f"{article_json_file} Article files does not exists")
        return
    
    with open (article_json_file, "r", encoding="utf-8") as f:
        try:
            article_json = json.load(f)
        except Exception as e:
            logger.info ("Failed.......")
            return
        
    context = f"Title: {article_json.get('title','')} \n\nDescription: {article_json.get('description','')} \n\nContent: {article_json.get('content','')}"

    recommonded_cateogry = get_cateogry_from_gpt4(CATEGORY_PROMPT, context)
    gpt4_suggestion_category = get_cateogry_from_gpt4(RAW_CATEGORY_PROMPT, context)

    article_json['recommended_category'] = recommonded_cateogry
    article_json['gpt4_suggestion_category'] = gpt4_suggestion_category

    with open (article_json_file, "w", encoding="utf-8") as f:
        json.dump(article_json, f, indent=2)
    logger.info (f"Categorized article {article_id}")
    
def main():
    article_folders = [name for name in os.listdir(QUEUE_DIR) if os.path.isdir(os.path.join(QUEUE_DIR, name))]
    print(f"{len(article_folders)} articles available to process.")

    for article_id in tqdm(article_folders, desc="Categorizing articles"):
        process_article(article_id)

if __name__ == "__main__":
    main()