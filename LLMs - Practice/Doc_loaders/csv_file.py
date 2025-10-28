from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from langchain_core.vectorstores import InMemoryVectorStore

loader = CSVLoader(file_path = "industry.csv")

data = loader.load()

embeddings = GoogleGenerativeAIEmbeddings(
     model = "models/gemini-embedding-001",
     google_api_key = os.getenv("GEMINI_API_KEY")
)

#print the loaded data

for i, doc in enumerate(data):
    print(f"\nDocument {i+1}")
    print("Content: ",doc.page_content)
    print("Metadata: ", doc.metadata)




#Indexing and Retrieval
#------------------- indexing and retriving data usig as_retrive-------------
# Extract and flatten page_content to ensure it's a string
texts = []
metadatas = []

for doc in data:
    # If page_content is a list, join it into a single string
    if isinstance(doc.page_content, list):
        content = " ".join(str(item) for item in doc.page_content)
    else:
        content = str(doc.page_content)

    texts.append(content)
    metadatas.append(doc.metadata)



vectorstore = InMemoryVectorStore.from_texts(
    texts= texts,
    embedding= embeddings,
    metadatas=metadatas

)

# using vectorestore as retrieval
retrival= vectorstore.as_retriever()

# retrieve most similar text
retrieved_document = retrival.invoke("IT")

print(f"Retrieved document  {retrieved_document[0].page_content}")