import os
import json
from tqdm import tqdm
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from utils.logger import get_logger
from config.settings import QUEUE_DIR

# Base Directories ================
ARTICLE_STORE_BASE = os.getenv("ARTICLE_STORE_BASE", "article_store")
#Base for folder exists
os.makedirs(ARTICLE_STORE_BASE,exist_ok=True)


INPROGRESS_DIR = os.path.join(ARTICLE_STORE_BASE, "inprogress")
COMPLETED_DIR = os.path.join(ARTICLE_STORE_BASE, "completed")
FAILED_DIR = os.path.join(ARTICLE_STORE_BASE, "failed")

for directory in [INPROGRESS_DIR,COMPLETED_DIR ,FAILED_DIR]:
    os.makedirs(directory,exist_ok=True)

#==== logger
logger = get_logger("Category_Logger")

# load tokenizer and model
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

#===list
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

# prompts
CATEGORY_PROMPT = (
    "Given the title, description, content of a news article, identify the most suitable category from the list "
    f"{','.join(CATEGORIES)}. If none matches then return 'Other'."
)

RAW_CATEGORY_PROMPT = (
    "Given the title, description, content of a news article, suggest a sytentic category name that best describes its subject. e.g. 'Crypto', 'Climate Newss"
)

def get_category_from_gpt2(prompt):
    inputs = tokenizer.encode(prompt,return_tensors = "pt")
    output = model.generate(
        inputs,
        max_length = inputs.shape[1]+20 , # response size
        num_return_sequences = 1,
        do_sample = True,
        top_p = 0.9,
        top_k= 50
    )

    result = tokenizer.decode(output[0],skip_special_tokens = True)

    result_lines = result.split("Category:") if "Category:" in result else result.split("Suggested Category:")

    if len(result_lines) >1 :
        return result_lines[1].strip().split("\n")[0]
    else :
        return result.strip()
    
def process_articles(article_id):
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
        
    title = article_json.get("title","")
    description = article_json.get("description","")
    content = article_json.get("content","")

    category_prompt = CATEGORY_PROMPT.format(
        title=title,
        description= description,
        content=content
    )

    raw_category_prompt = RAW_CATEGORY_PROMPT.format(
        title=title,
        content=content,
        description=description 
    )

    recommonded_cateogry = get_category_from_gpt2(category_prompt)
    gpt4_suggestion_category =get_category_from_gpt2(raw_category_prompt)

    article_json['recommended_category'] = recommonded_cateogry
    article_json['gpt4_suggestion_category'] = gpt4_suggestion_category

    completed_folder = os.path.join(COMPLETED_DIR,article_id)
    os.makedirs(completed_folder,exist_ok=True)
    completed_json_file = os.path.join(completed_folder,f"{article_id}.json")
    with open (completed_json_file, "w", encoding="utf-8") as f:
        json.dump(article_json, f, indent=2)
        
    logger.info (f"Categorized article {article_id}")


def main():
    article_folders = [name for name in os.listdir(QUEUE_DIR) if os.path.isdir(os.path.join(QUEUE_DIR, name))]
    print(f"{len(article_folders)} articles available to process.")

    for article_id in tqdm(article_folders, desc="Categorizing articles"):
        process_articles(article_id)

if __name__ == "__main__":
    main()