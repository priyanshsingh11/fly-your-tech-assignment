import os
from typing import Annotated, TypedDict, List
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from tools import tools
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage

load_dotenv()

# Define the state for the graph
class State(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]

# Initialize the LLM with tool-calling capabilities using Groq
# Using llama-3.3-70b-versatile for high performance on the free tier
llm = ChatGroq(model="llama-3.3-70b-versatile")
llm_with_tools = llm.bind_tools(tools)

from langchain_core.messages import SystemMessage

# Professional system prompt for better output formatting
SYSTEM_PROMPT = SystemMessage(content=(
    "You are the professional AI assistant for 'Fly Your Tech'. "
    "Your goal is to help users with company information and lead management. "
    "When providing lead information, always format it clearly in a professional list or table. "
    "Do not just dump raw data JSON. Be concise and polite."
))

# Define the nodes
def chatbot(state: State):
    messages = state["messages"]

    exit_words = ["bye", "thanks", "thank you", "end", "exit", "quit"]

    last_message = messages[-1]
    if isinstance(last_message, HumanMessage):
        user_text = last_message.content.lower()

        if any(word in user_text for word in exit_words):
            return {
                "messages": [
                    SystemMessage(
                        content="Thanks for chatting with Fly Your Tech! 👋 Have a great day."
                    )
                ],
                "__end__": True,   
            }

    messages = [SYSTEM_PROMPT] + messages
    return {"messages": [llm_with_tools.invoke(messages)]}

# Create the graph
workflow = StateGraph(State)

# Add nodes
workflow.add_node("chatbot", chatbot)
workflow.add_node("tools", ToolNode(tools))

# Add edges
workflow.add_edge(START, "chatbot")
workflow.add_conditional_edges("chatbot", tools_condition)
workflow.add_edge("tools", "chatbot")

# Compile the graph
app = workflow.compile()
