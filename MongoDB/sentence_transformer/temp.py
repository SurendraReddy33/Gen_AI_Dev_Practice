import os
import faiss
import numpy as np
import fitz
from openai import OpenAI
from pymongo import MongoClient
from transformers import GPT2Tokenizer,GPT2LMHeadModel,GPT2Model,pipeline
import torch
from sentence_transformers import SentenceTransformer
import pickle
 
 
# -------------------- Configuration --------------------
PDF_FOLDER = "resumes"
#FAISS_INDEX_FILE = "resume_index.faiss"
FAISS_INDEX_FILE = "faiss.index"
#INDEX_DATA_FILE = "resume_chunks.npy"
INDEX_DATA_FILE = "faiss_ids.pkl"

MONGO_URI = "mongodb+srv://surendrareddygandra3:onTwB6qFMES4HF24@genai-cluster.cb98ycb.mongodb.net/"
DB_NAME = "resume_db"
COLLECTION_NAME = "resume_gpt2"
#OPENAI_API_KEY = os.getenv ("OPENAI_API_KEY")
#TEXT_EMBEDDINGS_MODEL = "text-embedding-ada-002"
 
# -------------------- Initalisation --------------------
#openai_client = OpenAI  (api_key=OPENAI_API_KEY )
DB_NAME = "Resume_db"
sample_data = "sample_data"
 
client = MongoClient(MONGO_URI)
database = client[DB_NAME]
collection = database[sample_data]
embedding_dim = 384
index = faiss.IndexFlatL2(embedding_dim) # faiss
index_data = []
 
 
# ---------------------------------- define tokenizer and model --------------------------
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")
model = GPT2Model.from_pretrained("gpt2")
 
 
# use local embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')
 
qa_pipeline = pipeline("question-answering",model = "deepset/roberta-base-squad2")
 
#by default GPT2 model is not having pad_tokens
tokenizer.pad_token = tokenizer.eos_token
 
model.pad_token_id = model.config.eos_token_id
 
def load_index():
    global index,index_data
    if os.path.exists (FAISS_INDEX_FILE) and os.path.exists(INDEX_DATA_FILE):
         
        index = faiss.read_index(FAISS_INDEX_FILE)
        with open(INDEX_DATA_FILE,"rb") as f:
            index_data = pickle.load(f)
    else:
        print("NO Existing index found.A new one will be created")
 
def load_pdf_text(pdf_path):
    pdf_document = fitz.open(pdf_path)
    return "\n".join([page.get_text() for page in pdf_document])
 
def chunk_text (text, chunk_size=500):
    words = text.split()
    return [ " ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
 
def get_openai_embeddings(text):
    response = openai_client.embeddings.create(
        model = TEXT_EMBEDDINGS_MODEL,
        input =  text
    )
    return response.data[0].embedding
 
def get_embeddings(chunked_text):
    """
    Gets the mean embedding from the input_text
 
    Args:
        input_text : Text to get the mean embedding
    """
 
    tokens = tokenizer(chunked_text,return_tensors="pt")  # Gets the result in PY Tensor format
 
    with torch.no_grad():  # Load the model for basic operations and not for training
        model_output = model(**tokens)   # In the PY- TF format
        full_embeddings = model_output.last_hidden_state
        return full_embeddings.squeeze(0).numpy().astype('float32').reshape(1,-1)
     
   
def save_index():
    faiss.write_index(index, FAISS_INDEX_FILE)
    with open(INDEX_DATA_FILE,"wb") as f:
        pickle.dump(index_data,f)
    print("Index Saved")
    #np.save(INDEX_DATA_FILE, index_data) # Mapping
 
def index_resumes():
    global index_data
    for filename in os.listdir (PDF_FOLDER):
        if filename.endswith(".pdf"):
            if collection.find_one({"_id": filename }):
                print (f"Skipping : {filename} - already indexed")
                continue
 
            text = load_pdf_text (os.path.join(PDF_FOLDER, filename))
            chunks = chunk_text (text)
            #collection.insert_one({"_id":filename,"text":text})
            #return chunks
            for chunk in chunks:
                embedding = model.encode(chunk).astype('float32').reshape(1,-1)
                #index.add(np.array([embedding], dtype="float32"))
                index.add(embedding)
                index_data.append({"_id" : filename, "chunk" : chunk})
            save_index()
            collection.insert_one({"_id" : filename, "text" : text})
            print (f"Indexed the resume {filename}")
   
 
def query_resume (query):
   
    # if index.ntotal ==0 or len (index_data) ==0:
    #     print ("No resumes are indexed. Please Use Option 1 ")
    #     return
    # query_vector = get_openai_embeddings (query)
    # X, I = index.search (np.array([query_vector], dype ="float32"),3) # Extract Chunk
   
    # context = []
    # for i in I [0]:
 
    #
   
    query_embedding = model.encode(query).astype('float32').reshape(1,-1)
    D,I = index.search(query_embedding,1)
    results =[]
    for id in I[0]:
        if id<len(index_data):
            results.append(index_data[id])
    if not results:
        print("No matching chunks found")
        return
   
    top_chunk = results[0]["chunk"]
 
    # use local QA pipline
 
    # answer = qa_pipeline({
    #     "question":query,
    #     "context":top_chunk
    # })
 
    print(f"Response :{results}")
 
   
 
 
# Main - Implementation
 
def main():
    load_index()
    print (index_data)
    while True:
        print ("\n GPT4 Based Resume QNA")
        print ("1. Process the Resumes in Resume Folder")
        print ("2. Ask Questions")
        print ("3. Exit")
        choice = input ("Select an Option : ")
 
        if choice == "1":
            print(index_resumes())
        elif choice == "2":
            query = input ("Ask you question : ")
            query_resume (query)
            # for idx,res in enumerate(results,1):
            #     print(f"\n Result {idx}:")
            #     print(f"Chunk Preview : {res['chunk'][:200]}")
            #     print("\n"+"-"*50)
        elif choice == "3":
            print ("Goodbye..... See you again.")
            break
        else:
            print ("Invalid user input. Please try again")
 
 
if __name__ == "__main__":
    main()