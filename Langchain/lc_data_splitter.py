# Problem Statement: Write a CLI Application which will Ask user to Process the Documents. On Local or on Web
#  1. Text Document - .txt
#  2. PDF Document - .pdf
#  3. Word Document - .docx
#  4. Markdown file - .md
#  5. HTML File     - .html
#  6. JSON Files    - JSON
#  7. Web Page or Local Page     - HTML

from io import StringIO
import os
import requests
import sys

from bs4 import BeautifulSoup

from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    HTMLHeaderTextSplitter,
    TokenTextSplitter
)

from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    UnstructuredHTMLLoader,
    UnstructuredMarkdownLoader,
    UnstructuredWordDocumentLoader
)

# Init GPT 4, LLM and Prompt Enviroment

llm = ChatOpenAI (model="gpt-4", temperature = 0.3)

prompt = PromptTemplate(
    input_variables =["text"],
    template = "Summarize: \n {text}"
)

chain = LLMChain(llm=llm, prompt=prompt)


def load_file (file_path):
    ext = os.path.splitext(file_path)[1].lower()  # Get the File Extension
    
    if ext == ".txt": # Load the Files with .txt extension
        loader = TextLoader(file_path)
    elif ext == ".pdf": # Load the PDF using PyPDFLoader
        loader = PyPDFLoader (file_path)
    elif ext == ".docx":
        loader = UnstructuredWordDocumentLoader (file_path)
    elif ext == ".md":
        loader = UnstructuredMarkdownLoader (file_path)
    elif ext == ".html":
        loader = UnstructuredHTMLLoader (file_path)
    elif ext == ".json":
        with open(file_path, "r", encoding="utf-8") as f:
            from langchain.schema import Document
            loader =  [Document (page_content = f.read())]
            return loader
    else:
        print ("Unsupported file type.")
        sys.exit (1)
    return loader.load()


def load_url(url):
    response = requests.get (url=url)
    soup = BeautifulSoup(response.text, "html.parser")
    content = soup.get_text(separator= "\n")
    from langchain.schema import Document
    loader =  [Document(page_content = content)]
    return loader

def choose_splitter(source_type = "text"):
    if source_type =="html":
        return HTMLHeaderTextSplitter(headers_to_split_on=[("h1", "Header 1"), ("h2", "Header 2")])
    elif source_type =="token":
        return TokenTextSplitter (chunk_size=200, chunk_overlap=50)
    else:
        return RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)
    
def summarize_chunks(docs, splitter, output_file):
    if isinstance(splitter, HTMLHeaderTextSplitter): # Raw Data, JSON, Non Formatted HTML
        html_text = docs[0].page_content
        chunks = splitter.split_text_from_file(StringIO(html_text))
    else:
        chunks = splitter.split_documents(docs)

    with open(output_file, "w", encoding="utf-8") as f:
        for i, chunk in enumerate(chunks):
            result = chain.run({"text": chunk.page_content})
            f.write(f"\n--- Chunk {i+1} ---\n")
            f.write(f"Original:\n{chunk.page_content}\n")
            f.write(f"Summary:\n{result}\n")

    print(f"✅ Summary saved to {output_file}")

if __name__ == "__main__":
    print ("Langchain Document Summarizer: ")
    print ("Choose a Input Type")
    print ("1. Summarize the Local File")
    print ("2. Summarize the Web URL")
    choice = input ("Select and Option: ")

    if choice == "1":        
        file_path = input ("Enter the full path of the file : ").strip()
        docs = load_file (file_path)
        ext = os.path.splitext(file_path)[1].lower() # File name extenstion. .pdf, .md, .docx, .txt
        s_type = "html" if ext == ".html" else "token" if ext == ".json" else "text"
        splitter = choose_splitter(s_type)
        summarize_chunks (docs, splitter, "summary_for local file")

    elif choice == "2":
        url = input ("Enter Web URL to Crawl and Summarize: ")
        docs = load_url(url)
        splitter = choose_splitter("html")
        summarize_chunks(docs,splitter, "summary_from_web.txt" )

    else:
        print ("Invalid Input. Please Select option 1 or 2")
