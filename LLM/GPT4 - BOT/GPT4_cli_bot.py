import os
import sys
import faiss
import openai
import fitz
import numpy as np
import logging
from dotenv import load_dotenv

CHUNK_SIZE = 500
EMBEDDING_MODEL = "text-embedding-3-small"


# step 1
load_dotenv() # Load the environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

pdf_file_path = "D:\Documents\WHAT IS AGENTIC AI.pdf"

# step 2 - Setup Logging
logging.basicConfig(
    filename = "cli_bot_log.log",
    level = logging.INFO,
    format = "%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

#step 3 - Read PDF File
def extract_text_from_pdf(pdf_file_path):
    try:
        pdf_pages = fitz.open(pdf_file_path)
        full_pdf_text = "\n".join([page.get_text() for page in pdf_pages])
        logger.info(f"Extracted text from Pdf File {pdf_file_path} with length og {len(full_pdf_text)}")
        return full_pdf_text
    except Exception as e:
        logger.exception(f"Failed to read text from {pdf_file_path}.Error is {e}")

#step 4 - Chunk the PDF Content based on Chunk size (500) - Words
def chunk_text(pdf_file_full_text, chunk_size):
    words = pdf_file_full_text.split()
    return [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

#step 5 - Use EMBEDDING_MODEL and get the Embeddings, Convert or cast to np Float 32
def get_embeddings_for_chunks(chunk_text):
    try:
        embeddings = openai.embeddings.create(model = EMBEDDING_MODEL, input = chunk_text)
        vectors = np.array([e.embedding for e in embeddings.data]).astype("float32")
        return vectors
    except Exception as e:
        logger.exception (f"Error while getting embeddings {e}")
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Tool Usage : Python gpt4-cli-bot.py <PDF Filepath>")
        sys.exit(1)

    pdf_file_path = sys.argv[1]

    # check if source PDF file exists
    print(pdf_file_path)
    if not os.path.exists(pdf_file_path):
        print("Source PDF file is not available.")
        sys.exit(1)

    pdf_text = extract_text_from_pdf(pdf_file_path)
    # print(f"\n PDF content are : {pdf_text}")

    chunked_text = chunk_text(pdf_text, CHUNK_SIZE)
    # print(f"\n PDF chunked content are : {chunked_text}")

    vectors = get_embeddings_for_chunks(chunked_text)
    # print(f"\n Vectors from chunked text are {vectors}")

    # declare a FAISS Index
    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors)
    logger.info(f"Faiss Index Created........{len(chunk_text)}")


if __name__ == "__main__":
    main()