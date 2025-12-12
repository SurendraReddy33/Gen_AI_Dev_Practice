"""
Autonomous News Processing Agent using LangChain
- Downloads latest news articles
- Rewords each article
- Detects category
- Suggests hashtags
- Saves everything to JSON for download
"""

#=======================
# Config / Setting 
#=======================
NEWS_API_URL = "https://newsapi.org/v2/top-headlines"
API_KEY = "fd5dd9059e6c423ab6d91ea447f2e72d"  # <-- Replace if needed
COUNTRY = "us"
ARTICLE_COUNT = 5
OUTPUT_FILE = "processed_news.json"

#=======================
# Import Langchain Modules for Agent Creation
#=======================

import requests
import json  

from langchain_openai import ChatOpenAI                 # Call Open A GPT LLM
from langchain.agents import initialize_agent, Tool     # Init and Create the Agent
from langchain.memory import ConversationBufferMemory   # Memory allocation for an Agent

# Dynamic / Runtime Article Collection - Store
processed_result = []

#=======================
# LLM - Setup Create and Init LLM
#=======================
 
llm = ChatOpenAI(
    model = "gpt-4", 
    temperature = 0.3
)



#=======================
# Tools - Define Tools {Steps}
#=======================

# Tool - 1 - Download the news articles from the news api.
def download_news(_: str) -> str:
    params = {"apikey" : API_KEY, "country" : COUNTRY, "pageSize" : ARTICLE_COUNT }
    response = requests.get(NEWS_API_URL, params= params)
    response.raise_for_status()
    articles = response.json().get("articles", [])

    for article in articles: # 5 Articles will be processed {As per PageSize)
        processed_result.append(
            {
                "original" : article,
                "reworded" : "",
                "category" : "",
                "hashtags" : ""
            }
        )
    return f"Downloaded {len(processed_result)} news articles from the {NEWS_API_URL} "


# Tool 2 - Reowrd the new article in 2 - 3 sentences.
def reword_news (article_index: str) -> str:
    idx = int(article_index)
    article_text = processed_result[idx]["original"].get("content") or processed_result[idx]["original"].get("description") or processed_result[idx]["original"].get("title")    
    prompt = f"Reword this news article in 2 - 3 sentences for clarify: \n\n {article_text}"
    reworded = llm.invoke(prompt).content.strip()
    processed_result[idx]["reworded"] = reworded
    return reworded

# Tool 3 - Detect the Category for Article
def detect_category(article_index: str) -> str:
    idx = int(article_index)
    article_text = article_text = processed_result[idx]["original"].get("content") or processed_result[idx]["original"].get("description") or processed_result[idx]["original"].get("title")
    prompt = f"Classify this news article into one category like Politics, Sports, Tech, Science, Health, Entertainment : \n\n {article_text}"
    category = llm.invoke (prompt).content.strip()
    processed_result[idx]["category"] = category
    return category

# Tool 4 - Generate the Hashtags for article
def generate_hashtags (article_index: str) -> str:
    idx = int(article_index)
    article_text = article_text = processed_result[idx]["original"].get("content") or processed_result[idx]["original"].get("description") or processed_result[idx]["original"].get("title")
    prompt = f"Generate 3 trending hashtags for this news article: \n\n {article_text}"
    hashtags = llm.invoke (prompt).content.strip()
    processed_result[idx]["hashtags"] = hashtags
    return hashtags


# Tool 5 - Save the updated article as JSON 
def save_to_json(_: str) -> str:
    with open (OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(processed_result,f, ensure_ascii=False, indent=4)
    return f"Saved {len (processed_result)} records to the {OUTPUT_FILE}" 


#=======================
# Register the Tools with Langchain
#=======================

tools = [
    Tool(
        name = "Download News",
        func = download_news,
        description = "Fetch  the latest news articles from the News API"
    ),
    Tool(
        name = "Reword News",
        func = reword_news,
        description = "Reword the news at given numeric index (string of an integer, '0'.) "
    ),
    Tool(
        name = "Detect Category",
        func = detect_category,
        description = "Detect the category of news article at given numeric index"
    ),
    Tool(
        name = "Generate Hashtags",
        func = generate_hashtags,
        description = "Generate the hashtags for the news at given numeric index"
    ),
    Tool(
        name = "Save to JSON",
        func = save_to_json,
        description = "Save the processed articles to JSON File"
    )
]

#=======================
# Memory for Agent (Conversation)
#=======================

memory = ConversationBufferMemory(
    memory_key = "chat_history", 
    return_messages = True
)

#=======================
# Create the Agent / Init Agent
#=======================

agent = initialize_agent(
    tools = tools,
    llm = llm,
    agent = "zero-shot-react-description",
    memory = memory,
    verbose = True,
    max_iterations = 100
)

goal = f"""
Download the latest {ARTICLE_COUNT} news articles from the US. 
For each article index (0 to {ARTICLE_COUNT -1}):
    1. Call 'Reword News' with the index number as a string.
    2. Call 'Detect Category' with the same index.
    3. Call 'Generate Hashtags' with the same index.
After all the articles are processed call 'Save to JSON'
"""

result = agent.run(goal)

print (f"\n News agent execution completed \n {result}")