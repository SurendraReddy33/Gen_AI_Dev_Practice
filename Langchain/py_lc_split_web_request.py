# Write an Program which will read the data from Web Site URL - https://www.virtualglobetechnology.com/testimonial 
# and convert into thee small chunks and summerize it. and save to the txt file
# Web URL - pip install requests beautifulsoup4 tiktoken

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from bs4 import BeautifulSoup
import requests


import os

url = "https://www.thezennialpro.com/policy"
output_file = "web_crawl_privacy_policy.txt"

# Step 1 : Load and Read the URL
response = requests.get(url=url)
soup = BeautifulSoup (response.text, "html.parser")
original_text = soup.get_text(separator="\n")

print (f"Original TEXT : {original_text} \n")

cleaned_text = "\n".join( line.strip() for line in original_text.splitlines() if line.strip() )

print (f"Cleaned TEXT : {cleaned_text} \n")

# Step 2 : Split the text and get small chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size = 300, 
    chunk_overlap = 50
)
chunks = splitter.split_text(cleaned_text)

# Step : Init LLM and Setup Prompt and Chain
llm = ChatOpenAI (model="gpt-4", temperature=0.3)

prompt = PromptTemplate (
     input_variables = ["text"],
    template = "Summerize this Chunk: \n {text}"
)

chain = LLMChain (llm=llm, prompt =prompt)

# Summerize and save to the File
with open (output_file, "w", encoding= "utf-8") as f:
    for i, chunk in enumerate (chunks):
        summary_text = chain.run({"text": chunk})
        f.write (f"\n--- Chunk {i+1} ---\n")
        f.write (f"Original : {chunk} \n")
        f.write (f"Summary: \n {summary_text} \n")

print (f"Web URL Crawling is done for {url}, ")
print (f"and Summary is saved to {output_file}.")