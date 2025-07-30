# Problem Statement : Write an Pyhon Program which will demo the Langchain - Single Step Chain.

# Sample Text - Input
# Patient complains of frequent headaches over the past two weeks, especially in the mornings. 
# No history of trauma. Blood pressure normal. Advised to reduce screen time and stay hydrated.


# Expected Response - Output
# You've been experiencing headaches frequently for the past two weeks, 
# particularly in the mornings. There's no evidence that these headaches are 
# due to any injury. Your blood pressure is normal. 
# To help manage your headaches, it's recommended that you decrease the 
# amount of time you spend looking at screens and make sure you're drinking enough water.

from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

# Init LLM
llm = ChatOpenAI(model ="gpt-4", temperature=0.3)

# Basic transcript 
transcript =  """Patient complains of frequent headaches over the past two weeks, especially in the mornings. 
No history of trauma. Blood pressure normal. Advised to reduce screen time and stay hydrated."""

# System Prompt
system_prompt = SystemMessagePromptTemplate.from_template(
    "You are an clinical AI assistent. Generate a patient-friendly summary from the provided transcript."
)

# Human Prompt
human_prompt = HumanMessagePromptTemplate.from_template(
    "Transcript : {transcript_text}"
)

# Build the Chat Prompt
chat_prompt = ChatPromptTemplate.from_messages([system_prompt, human_prompt])

# Build the Chain
chain = LLMChain (llm= llm, prompt =chat_prompt)

response = chain.run({"transcript_text": transcript})

print (f"Patient Summary : {response} ")