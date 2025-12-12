# Write an Program which will read the data from Word Document File 
# and convert into thee small chunks and summerize it. and save to the txt file
# Word Document - pip python-docx unstructured[all]

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
import os

# os.environ["OPENAI_API_KEY"] = "sk-xxxxxxxxxxxxxxx-xxxxxxxxxxxxxxxx-xxxxxxxxx"

word_file = "DD_VAPT_Draft.docx"
output_file = "word_doc_summary.txt"

# Load the Document and Get text for each document
loader = UnstructuredWordDocumentLoader(word_file)
docs = loader.load() # 100 Pages
document_text = "\n".join(  [ doc.page_content for doc in docs]) # Text for all 1000 Pages

# Chunk the Document
splitter = RecursiveCharacterTextSplitter(
    chunk_size = 300, 
    chunk_overlap = 50
)

# Split the Text and Get the Chunks
chunks = splitter.split_text(document_text)

# Init LLM
llm = ChatOpenAI(model="gpt-4", temperature=0.3)

# Define the Prompt 
prompt = PromptTemplate(
    input_variables = ["text"],
    template = "Summerize this Chunk: \n {text}"
)

# Setup LLM Chain
chain = LLMChain (llm= llm, prompt = prompt)

# Save the Output file
with open(output_file, "w", encoding="utf-8") as f:
    for i, chunk in enumerate (chunks):
        result  = chain.run({"text": chunk})
        f.write(f"\n Chunk {i+1} ---\n")
        f.write (f"\nOriginal: \n {chunk}")
        f.write (f"\nSummary: \n {result}")

print (f"The Document {word_file} summary is saved to {output_file}")
