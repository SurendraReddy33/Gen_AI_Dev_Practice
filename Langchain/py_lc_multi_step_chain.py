# Product - Dell Laptop 
# Step 1 - Task - Write a Marketing Pitch for the Product {product_name}
# Step 2 - Task - Convert the Pitch into single twitter post (under 200 characters)
# Step 3 - Task - Build 3 hashtags for this Tweet 
# General 
# What is RunnableLambda -> Which wraps any Lambda, function
# What is RunnableSequence => Runs multiple Runnables in a Order 

# Runnable -> Invoke() -> Step
# Each Step is going to have a Prompt

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import  RunnableLambda, RunnableSequence

llm = ChatOpenAI (model="gpt-4", temperature=0.3)

pitch_prompt = ChatPromptTemplate.from_template(
    "Write a 2 sentenence marketing pitch for the product {product_name}"
)

tweet_prompt = ChatPromptTemplate.from_template(
    "Convert the following pitch into a single Twitter post (under 200 characters ) : \n {pitch}"
)

hashtag_prompt = ChatPromptTemplate.from_template(
    "Suggest 3 trending hashtags for this tweet \n {tweet}"
)


# Step 1 
# A Chain Step is Created
# 1. Use pitch_prompt to format the user input into a complete prompt statement 
# 1. Example : Write a 2 sentenence marketing pitch for the product "Dell HP AI Powered Laptop"
# 2. Send the Prompt to the LLM
# 3. Capture the LLM Output with lambda so that we have a {dict of product_name and pitch}
# 4. now step1 = {dict of product_name and pitch}
# pitch_prompt -> llm --> Response 
step1 = (
    pitch_prompt | llm | RunnableLambda (
        lambda msg : {
            "product_name" : input_data["product_name"],
            "pitch" : msg.content if hasattr(msg, "content")  else str(msg)
        }
    )
)

# Step 2 (Get the Tweet from Pitch - Step -1)
# 1. Pass the Pitch Text (Step1)
# 2. Format it with Tweet Prompt
# 2. Example : Convert the following pitch into a single Twitter post (under 200 characters ) : \n bla bla bla"
# 3. Send this to LLM
# 4. Store Pitch, Tweet (Response from LLM)
step2 = (
    RunnableLambda (
        lambda x: {"pitch" : x["pitch"]}) # Extract the Pitch from Step 1
        | tweet_prompt # Formatting or getting vlaue from step 1 
        | llm
        | RunnableLambda (
            lambda msg : {
                "pitch" : input_data["pitch"], # Get from Step 1
                "tweet" : msg.content if hasattr(msg, "content") else str (msg)
            })
    )

# Step 3 (Get the Hash Tags - From the Tweet)
# 1. Pass the Tweet
# 2. Format the Tweet Prompt  
# 3. Example : Suggest 3 trending hashtags for this tweet {Bla Bla Bla}
# 4. Send to LLM
# 5. Store pitch, tweet text, hashtag. From the LLM Output
step3 = (
    RunnableLambda( lambda x: {"tweet" : x["tweet"]})
    | hashtag_prompt
    | llm
    | RunnableLambda (
        lambda msg : {
            "pitch" : input_data["pitch"],
            "tweet" : input_data ["tweet"],
            "hashtags" : msg.content if hasattr (msg, "content") else str(msg)
        }
    )
)

# step1_wrapped = RunnableLambda (lambda x : x) | step1
# step2_wrapped = RunnableLambda (lambda x : x) | step2
# step3_wrapped = RunnableLambda (lambda x : x) | step3

chain  = RunnableSequence(
    first = step1,
    middle = [step2],
    last = step3
)

input_data = {"product_name" : "Dell HP AI Powered Laptop"}

step1_output = step1.invoke(input_data)
input_data["pitch"] = step1_output["pitch"]

step2_output = step2.invoke(input_data)
input_data["tweet"] = step2_output["tweet"]

step3_output = step3.invoke(input_data)

print ("Pitch:", input_data["pitch"])
print ("Tweet:", step2_output["tweet"])
print ("Hashtags:", step3_output.get("hashtags"))

