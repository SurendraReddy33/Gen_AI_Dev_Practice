from openai import OpenAI # pip install openai
import numpy as np # Used to vector math and array conversation
import pickle # Save and Load Dictionary (label to Index) - Heatmap
import faiss # pip install faiss
import os


# Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
FAISS_INDEX = "text_index.faiss" # faiss database
LABEL_MAP_FILE = "text_label.pk1" # pickle
VECTOR_DIM = 1536 # - Embeddings - Mean, Full -> Mean -> 768 -d (GPT2) : GPT4 : 1536



# Init Open AI GPT4 - Client 
client = OpenAI (api_key = os.getenv("OPENAI_API_KEY")) # always read from Enviroments

# Create or use existing Index
if os.path.exists(FAISS_INDEX):
    index = faiss.read_index(FAISS_INDEX) # Use Existing Index
else:
    index = faiss.IndexFlatL2 (VECTOR_DIM) # Create Index

# Create or Init Pickle file 
if os.path.exists(LABEL_MAP_FILE):
    with open (LABEL_MAP_FILE, "rb") as f:
        label_map = pickle.load(f)
else:
    label_map = {} # {index, label}

def get_embeddings(text:str) -> list:
    # Model is text-embedding-3-small used to get embeddings for text
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    return response.data[0].embedding # Return final embeddings

def add_to_index():
    text  = input ("Enter text to add to faiss db (index): ") # text = How are you Manish
    label  = input ("Enter lable for text {text} : ") # label = Manish

    text_embeddings = get_embeddings(text) # Get the embeddings for text
    print (f"text_embeddings : {text_embeddings}")

    vector = np.array([text_embeddings]).astype("float32")
    print (f"vector : {vector}")  

    index_id = index.ntotal # Current size of total vectors
    print (f"index_id : {index_id}")  

    index.add(vector) # Add to Index (Faiss DB) -> Float 32 - Embedings -> Vector
    label_map[index_id] = label
    save_index()


def save_index(): # Save Index to local db {faiss db}
    faiss.write_index(index,FAISS_INDEX) # Save Index
    with open (LABEL_MAP_FILE, "wb") as f: # Save Pickle -> heatmap
        pickle.dump (label_map, f)

def list_labels():
    for idx, label in label_map.items():
        print (f"{idx} : {label}")

def compare_labels():
    first_label = input("Enter the name of first lable : ") # "AmeetParse"
    second_lable = input("Enter the name of second lable : ") # "AllenJoe"
    v1 = v2 = None

    for idx, label in label_map.items(): # Iterate for every row in the collection
       if  label == first_label:           
           v1 = index.reconstruct(idx)
        #    print (f"V1:::::{v1}") 
       
       if label == second_lable:
           v2 = index.reconstruct(idx)
        #    print (f"V2:::::{v2}")
    
    if v1 is None or v2 is None:
        print ("first or second label was not found.....")
        return
    
    v1, v2 = np.array(v1) ,np.array(v2)

    # np.dot(v1,v2) = Measure how aligned these vectors are. v1, v2
    # (np.linalg.nom(Vx) = Length of each Vector
    # similarity : Score : 1.0 : Same :::: 0.8 + - Very Similar :::: 0.0 ::: NR ::: < 0 :: 
    similarity = float (np.dot(v1,v2) / (np.linalg.norm(v1)  * (np.linalg.norm(v2) )))
    print (f"similarity Score for {first_label} and {second_lable} is : {similarity}")





def main():
    while True:
        print  ("\n ===== FAISS CLI Tools {Add, List, Compare} =====")
        print  ("1. Add new text")
        print  ("2. List Lables")
        print  ("3. Compare Lables")
        print  ("4. Exit CLI")
        choice = input("Select an FAISS CLI Operation : ")

        if choice == "1":
            add_to_index() # Save Text to FAISS and Entry in Pickle
        elif choice == "2":
            list_labels()
        elif choice == "3":
            compare_labels()
        elif choice == "4":
            break
        else:
            print("Invalid CLI input. Use from 1 to 4 and try again")
            
            


        
        


if __name__ == "__main__":
    main()