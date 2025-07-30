# Write an Program which will accept the long text and chunk into 
# small parts. Send each chunk to GPT4 and ask to Summerize it

# pip install langchain openai tiktoken langchain_community --upgrade

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os

# os.environ["OPENAI_API_KEY"] = "sk-xxxxxxxxxxxxxxx-xxxxxxxxxxxxxxxx-xxxxxxxxx"

# Step 1 : Get the Long Text
long_text = """
LangChain is a powerful framework for building applications using language models. 
It offers tools to manage prompts, chains, memory, agents, and external tools.
This makes it easier to build complex LLM applications that interact with real-world data.
You can process documents, create chatbots, query databases, or even automate workflows.
"""

# chunk_overlap : Ensures context is preserved between chunks by overlapping 
# 10 characters from the end of one chunk into the next.

# Step 2 : Split the Text and Get the Chunks
splitter = RecursiveCharacterTextSplitter (
    chunk_size=50, 
    chunk_overlap = 10,
    separators = ["\n\n", ".", " ", "", "\n"]
)

chunks = splitter.split_text(long_text)

print (f" Total Length {len(chunks)} \n")

# Chunks
# ['LangChain is a powerful framework for building', 
# 'building applications using language models', 
# '. \nIt offers tools to manage prompts, chains,
# ', 'chains, memory, agents, and external tools', 
# '.\nThis makes it easier to build complex LLM', 
# 'LLM applications that interact with real-world', 
# 'data', '.\nYou can process documents, create chatbots,', 
# 'chatbots, query databases, or even automate', 
# 'automate workflows', '.']

# Step 3 : Send Each Chunk to GPT4 - Summerize it.

llm = ChatOpenAI(model="gpt-4", temperature=0.3)

prompt = PromptTemplate (
    input_variables = ["text"],
    template = "Summarize this chunk: \n{text}"
)

chain = LLMChain (llm=llm, prompt= prompt)

for i, chunk in enumerate(chunks):
    chunk_summary = chain.run({"text": chunk})    
    print (f"\n ---Chunk {i+1} : {chunk} \n Summary is : {chunk_summary}")