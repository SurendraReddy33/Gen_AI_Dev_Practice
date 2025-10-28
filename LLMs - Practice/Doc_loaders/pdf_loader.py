from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage,SystemMessage
import os

#specify the path
loader = PyPDFLoader("Surendra.pdf")



#load document
documents = loader.load()

llm= ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash",
    api_key = os.getenv("GEMINI_API_KEY")

)


text = [doc.page_content for i,doc in enumerate(documents)]

query = input("Data fetching done. Please enter your Query : ").strip()
messages = [
    SystemMessage(content="You are a helpful assistant.Please answer the query from the given text"),
    HumanMessage(content=f"{text}  \n Query : {query}")
]
response = llm.invoke(messages)
print(response.content)
# content

# for i,doc in enumerate(documents):
#     print(f"\n Document {i+1}")
#     print("Content: ",doc.page_content)
#     print("Metadata: ",doc.metadata)