import fitz
import os
from transformers import GPT2Tokenizer, GPT2LMHeadModel, logging
import torch

logging.set_verbosity_error()

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
head_model = GPT2LMHeadModel.from_pretrained("gpt2")

# Add Padding Tokens {Becuase this is not default in GPT2}
tokenizer.pad_token = tokenizer.eos_token
head_model.pad_token_id = head_model.config.eos_token_id

PDF_FOLDER = "resumes"

context = []



def load_pdf_text(pdf_path):
    pdf_document = fitz.open(pdf_path)
    return "\n".join([page.get_text() for page in pdf_document])
 
def chunk_text (text, chunk_size=500):
    words = text.split()
    return [ " ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

def index_resumes():
    global context
    for filename in os.listdir (PDF_FOLDER):
        if filename.endswith(".pdf"):
            # if resume_collection.find_one({"_id": filename }):
            #     print (f"Skipping : {filename} - already indexed")
            #     continue

            text = load_pdf_text (os.path.join(PDF_FOLDER, filename))
            chunks = chunk_text (text)
            context = chunks
            return chunks

def query_resume(context, query):
    prompt = f"\nContext: {context} \n \n Query {query} \n Answer"

    input_ids = tokenizer.encode (prompt, return_tensors ="pt")

    output_ids = head_model.generate(input_ids, max_length=2000, do_sample=True, num_return_sequences=1, temperature=0.7)

    # Use a Loop here
    answer_text_0 = tokenizer.decode(output_ids[0], skip_special_tokens = True)
    print  (f"\n answer_text_0 - Generated Text : {answer_text_0}")
    return True


def main():
    print("You are in Main Block..............")
    while True:
        print ("\n GPT4 Based Resume QNA")
        print ("1. Process the Resumes in Resume Folder")
        print ("2. Ask Questions")
        print ("3. Exit")
        choice = input ("Select an Option : ")

        if choice == "1":
            print(index_resumes())
        elif choice == "2":
            global context
            query = input("Ask you question : ")
            query_resume(context, query)
        elif choice == "3":
            print ("Goodbye..... See you again.")
            break
        else:
            print ("Invalid user input. Please try again")


if __name__ == "__main__":
    main()