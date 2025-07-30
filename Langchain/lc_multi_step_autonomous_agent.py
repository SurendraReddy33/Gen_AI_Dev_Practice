"""
Write an Agent which will accept the Goal
- Accept a Task 
- Chooose the Steps 
- Usage  of Tools to perform Sub Tasks
- Remebers the result and actions during conversation
"""

# Import Langchain Modules for Agent Creation
from langchain_openai import ChatOpenAI                 # Call Open A GPT LLM
from langchain.agents import initialize_agent, Tool     # Init and Create the Agent
from langchain.memory import ConversationBufferMemory   # Memory allocation for an Agent

# Create and Init LLM 
llm = ChatOpenAI(
    model = "gpt-4", 
    temperature = 0.3
)

# Goal -> Tool 1 -> Generate the Marketing Pitch
def generate_pitch(product_name: str) -> str: 
    prompt = f"Write a 2 sentence marketing  pitch for the product {product_name}"
    response = llm.invoke (prompt) # Call LLM and get the response
    return response.content # Extract the reply or content from the Model Response

# Goal -> Tool 2 -> Get the Tweet based on the pitch
def pitch_to_tweet(pitch: str) -> str: 
    prompt = f"Conver this pitch into a single twitter post (under 200 characters) : {pitch}"
    response = llm.invoke (prompt) # Call LLM and get the response
    return response.content # Extract the reply or content from the Model Response

# Goal -> Tool 3 -> Get the Hashtag based on the Tweet
def tweet_to_hashtags (tweet: str) ->str:
    prompt = f"Suggest 3 treding hashtags for this tweet : {tweet}"
    response = llm.invoke (prompt) # Call LLM and get the response
    return response.content # Extract the reply or content from the Model Response


# Register the the tools with Langchain 

tools = [
    Tool(
        name = "Generate Pitch",
        func = generate_pitch,
        description = "Creates a 2-sentence marketing pitch from a product name "
    ),
    Tool(
        name = "Pitch to Tweet",
        func = pitch_to_tweet,
        description = "Convert the marketing  pitch into tweet"
    ),
    Tool (
        name = "Tweet to Hashtags",
        func = tweet_to_hashtags,
        description = "Suggest trending hashtags for the given tweet"
    )
]

memory = ConversationBufferMemory(
    memory_key = "chat_history",
    return_messages = True
)

"""
Define Agent
Use tools, memory, to achive goals (one by one)
"""
agent = initialize_agent(
    tools  = tools,
    llm = llm,
    memory = memory, 
    verbose = True,
    agent = "zero-shot-react-description"
)

# Define the Goal for Agent.
goal = "Generate a pitch, then a tweet, then hashtags for 'Dell HP AI Powered Laptop'"

# Assign goal and run the agent
result = agent.run(goal)

print (result)