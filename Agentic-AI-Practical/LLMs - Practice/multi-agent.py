# --- Install dependencies ---
# pip install -U langchain langchain-core langchain-google-genai langgraph google-generativeai

from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
import os

# --- API Setup ---
api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError("⚠️ Please set your Gemini API key as 'API_KEY' environment variable")

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=api_key)

# --- Agent Functions ---
def research_agent(state):
    query = state.get("query")
    response = llm.invoke([HumanMessage(content=f"Find key information about: {query}")])
    state.set("research", response.content)  # save output
    return state

def summarize_agent(state):
    research = state.get("research")
    response = llm.invoke([HumanMessage(content=f"Summarize the following:\n{research}")])
    state.set("summary", response.content)
    return state

def supervisor(state):
    summary = state.get("summary")
    state.set("final_answer", f"✅ Final summarized answer:\n{summary}")
    return state

# --- Workflow Setup ---
workflow = StateGraph(state_schema=MessagesState)  # ✅ required in latest version

workflow.add_node("ResearchAgent", research_agent)
workflow.add_node("SummarizerAgent", summarize_agent)
workflow.add_node("Supervisor", supervisor)

workflow.add_edge(START, "ResearchAgent")
workflow.add_edge("ResearchAgent", "SummarizerAgent")
workflow.add_edge("SummarizerAgent", "Supervisor")
workflow.add_edge("Supervisor", END)

graph = workflow.compile()

# --- Run Multi-Agent Flow ---
inputs = MessagesState({"query": "Benefits of AI in Smart Parking Finder systems"})
result = graph.invoke(inputs)

# Print final output
print(result.get("final_answer"))
