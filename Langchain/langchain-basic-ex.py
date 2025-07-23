from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
 
prompt = PromptTemplate.from_template("What is a good name for a company that makes {product}?")
llm = OpenAI()
chain = LLMChain(prompt=prompt, llm=llm)
 
print(chain.run("sports shoes"))