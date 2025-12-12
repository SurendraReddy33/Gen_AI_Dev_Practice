import os
import json
import shutil
from tqdm import tqdm
from utils.logger import get_logger
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

ARTICLE_STORE_BASE = os.getenv("ARTICLE_STORE_BASE", "article_store")
QUEUE_DIR = os.path.join(ARTICLE_STORE_BASE, "queue")
INPROGRESS_DIR = os.path.join(ARTICLE_STORE_BASE, "inprogress")
COMPLETED_DIR = os.path.join(ARTICLE_STORE_BASE, "completed")
FAILED_DIR = os.path.join(ARTICLE_STORE_BASE, "failed")

logger = get_logger("gpt2_reword_logger")

# Load GPT-2 model and tokenizer
model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)
model.eval()

def reword_with_gpt2(prompt, max_tokens=100):
    try:
        inputs = tokenizer.encode(prompt, return_tensors="pt")
        outputs = model.generate(
            inputs,
            max_length=len(inputs[0]) + max_tokens,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            temperature=0.7,
            num_return_sequences=1
        )
        result = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return result[len(prompt):].strip()
    except Exception as e:
        logger.error(f"GPT-2 error: {e}")
        return None

def process_article(article_id):
    source_path = os.path.join(QUEUE_DIR, article_id)
    working_folder = os.path.join(INPROGRESS_DIR, article_id)

    try:
        shutil.move(source_path, working_folder)
    except Exception as e:
        logger.error(f"Failed to move article {article_id} to inprogress: {e}")
        return

    article_path = os.path.join(working_folder, f"{article_id}.json")
    if not os.path.exists(article_path):
        logger.warning(f"Missing JSON file for {article_id}")
        shutil.move(working_folder, os.path.join(FAILED_DIR, article_id))
        return

    try:
        with open(article_path, "r", encoding="utf-8") as f:
            article_data = json.load(f)

        title = article_data.get("title", "").strip()
        description = article_data.get("description", "").strip()
        content = article_data.get("content", "").strip()

        if not any([title, description, content]):
            raise ValueError("Missing required fields.")

        article_data["reworded_title"] = reword_with_gpt2("Reword this title: " + title)
        article_data["reworded_description"] = reword_with_gpt2("Reword this description: " + description)
        article_data["reworded_content"] = reword_with_gpt2("Reword this content: " + content)

        dest_path = os.path.join(COMPLETED_DIR, article_id)
        os.makedirs(dest_path, exist_ok=True)

        shutil.copytree(working_folder, dest_path, dirs_exist_ok=True)

        with open(os.path.join(dest_path, f"{article_id}.json"), "w", encoding="utf-8") as f:
            json.dump(article_data, f, ensure_ascii=False, indent=2)

        shutil.rmtree(working_folder)
        logger.info(f"Completed: {article_id}")

    except Exception as e:
        logger.error(f"Failed to process article {article_id}: {e}")
        shutil.move(working_folder, os.path.join(FAILED_DIR, article_id))

def create_or_use_dirs():
    os.makedirs(INPROGRESS_DIR, exist_ok=True)
    os.makedirs(COMPLETED_DIR, exist_ok=True)
    os.makedirs(FAILED_DIR, exist_ok=True)

def main():
    create_or_use_dirs()
    article_folders = [name for name in os.listdir(QUEUE_DIR) if os.path.isdir(os.path.join(QUEUE_DIR, name))]
    print(f"{len(article_folders)} articles available to process.")

    for article_id in tqdm(article_folders, desc="Rewording with GPT-2"):
        process_article(article_id)

if __name__ == "__main__":
    main()