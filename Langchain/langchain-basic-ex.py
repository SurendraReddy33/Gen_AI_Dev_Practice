# LangChain is an open-source Python framework designed to build applications with Large Language Models (LLMs).
#  It allows developers to create powerful, context-aware, and data-connected AI apps using components like prompts, chains, agents, memory, and retrievers. 

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
 
prompt = PromptTemplate.from_template("What is a good name for a company that makes {product}?")
llm = OpenAI()
chain = LLMChain(prompt=prompt, llm=llm)

 
print(chain.run("sports shoes"))