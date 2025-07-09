import os
import json
from tqdm import tqdm
from transformers import GPT2LMHeadModel, GPT2Tokenizer , logging
from utils.logger import get_logger
from config.settings import QUEUE_DIR
import shutil

#Silence unnecessary transformers waring : The attention mask .... (it comes from transformers)
logging.set_verbosity_error()  # this will supress transformers info  and warning messages.


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
    try:
        inputs = tokenizer.encode(prompt,return_tensors = "pt")
        output = model.generate(
            inputs,
            max_length = inputs.shape[1]+50 , # response size
            num_return_sequences = 1,
            do_sample = True,
            top_p = 0.9,
            top_k= 50
        )

        result = tokenizer.decode(output[0],skip_special_tokens = True)
        return  result[len(prompt):].strip()
    except Exception as e:
        logger.error(f"GPT-2 error: {e}")
        return None

    
def process_articles(article_id):
    folder_path = os.path.join (QUEUE_DIR, article_id)
    working_folder = os.path.join(INPROGRESS_DIR,folder_path)

    try:
        shutil.move(folder_path,working_folder)
    except Exception as e:
        logger.error(f"Failed to move article {article_id} to inprogress: {e}")
        return
    
    article_json_file = os.path.join (working_folder, f"{article_id}.json")


    if not os.path.exists(article_json_file):
        logger.error (f"{article_json_file} Article files does not exists")
        shutil.move(os.path.join(FAILED_DIR,article_json_file))
        return
    
    try:
        with open (article_json_file, "r", encoding="utf-8") as f:
            try:
                article_json = json.load(f)
            except Exception as e:
                logger.info ("Failed.......")
                return
            
        title = article_json.get("title","")
        description = article_json.get("description","")
        content = article_json.get("content","")

        if not any([title, description, content]):
                raise ValueError("Missing required fields.")

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
        shutil.copytree(working_folder,completed_folder,dirs_exist_ok=True)
        completed_json_file = os.path.join(completed_folder,f"{article_id}.json")
        with open (completed_json_file, "w", encoding="utf-8") as f:
            json.dump(article_json, f, indent=2)
        shutil.rmtree(working_folder)
            
        logger.info (f"Categorized article {article_id}")

    except Exception as e:
        logger.error(f"Failed to process article {article_id}: {e}")
        shutil.move(working_folder, os.path.join(FAILED_DIR, article_id))


def main():
    article_folders = [name for name in os.listdir(QUEUE_DIR) if os.path.isdir(os.path.join(QUEUE_DIR, name))]
    print(f"{len(article_folders)} articles available to process.")

    for article_id in tqdm(article_folders, desc="Categorizing articles"):
        process_articles(article_id)

if __name__ == "__main__":
    main()