"""

Project : My First ReAct AI Agent using LangGraph

Objective
---------
Build a simple AI Agent using LangGraph that can:

✔ Understand the user's question.
✔ Decide whether a tool is required.
✔ Execute the appropriate tool.
✔ Observe the tool result.
✔ Generate the final answer.

Unlike the previous project (Simple Chatbot),
this project introduces Tool Calling and the
complete ReAct (Reason + Act) workflow.

Concepts Covered
----------------
✔ State
✔ MessagesState
✔ Reducers (add_messages)
✔ Tool Calling
✔ bind_tools()
✔ ToolNode
✔ Conditional Edges
✔ ReAct Architecture
✔ Graph Execution

Architecture
------------

                    START
                        │
                        ▼
                    Chatbot Node
                        │
            Does the AI need a tool?
                │            │
                Yes           No
                │            │
                ▼            ▼
            ToolNode        END
                │
                ▼
            Chatbot Node

    Execution Flow
    --------------

    User Question
        │
        ▼
    HumanMessage
        │
        ▼
    Chatbot Node
        │
        ▼
    LLM decides:
    "Do I need a tool?"
        │
        ▼
    tools_condition()
        │
    ┌────┴────┐
    │         │
    ▼         ▼
    ToolNode   END
    │
    ▼
    Execute Tool
    │
    ▼
    ToolMessage
    │
    ▼
    Chatbot Node
    │
    ▼
    Final Answer
    """

# Used to create custom tools that the LLM can execute.
from langchain_core.tools import tool

# Groq LLM
from langchain_groq import ChatGroq

# LangGraph Components
#
# START -> Beginning of graph execution.
# END   -> End of graph execution.
# StateGraph -> Used to build the graph.
#
from langgraph.graph import START, END, StateGraph

# Reducer used for automatically appending messages.
from langgraph.graph.message import add_messages

# Prebuilt LangGraph Components
#
# ToolNode:
# Executes tools automatically.
#
# tools_condition:
# Decides whether the graph should
# execute a tool or stop.
#
from langgraph.prebuilt import ToolNode, tools_condition

# Used to create Human Messages.
from langchain_core.messages import HumanMessage

from typing import Annotated
from typing_extensions import TypedDict

from dotenv import load_dotenv

load_dotenv()


# 
# State
# 
#
# State is the shared data that moves
# from one node to another.
#
# In this project our State stores
# only conversation messages.
#
# add_messages automatically appends
# new messages into conversation history.
#
class State(TypedDict):

    messages: Annotated[list, add_messages]


# 
# Initialize LLM
# 
#
# This is our reasoning engine.
#
llm = ChatGroq(
    model="llama-3.3-70b-versatile"
)


# 
# Multiplication Tool
# 
#
# Whenever the model decides that accurate
# multiplication is required,
# it will call this tool.
#
@tool
def multiplication(a: int, b: int) -> int:
    """
    Use this tool whenever multiplication
    of two numbers is required.
    """

    print("🔥 TOOL EXECUTED")

    return a * b


# 
# Weather Tool
# 
#
# This tool returns weather information
# from our local fake database.
#
# In real-world projects this would call:
#
# - OpenWeather API
# - Weather API
# - Any external REST API
#
@tool
def weather(city: str):

    """
    Returns weather information
    for the requested city.
    """

    print(f"Tool received city -> {city}")

    city = city.lower().strip()

    fake_db = {

        "hyderabad": "Currently Hyderabad is 28°C.",

        "ongole": "Currently Ongole is 30°C.",

        "ammanabrolu": "Currently Ammanabrolu is 32°C."

    }

    return fake_db.get(
        city,
        "Weather not found."
    )


# 
# Register Tools
# 
#
# Every tool that the LLM is allowed
# to use must be registered here.
#
tools = [

    multiplication,

    weather

]


# 
# Bind Tools with LLM
# 
#
# bind_tools() does NOT execute tools.
#
# It simply tells the LLM:
#
# "These are the tools available."
#
# The LLM can now decide whether
# it needs one of them.
#
llm_with_tool = llm.bind_tools(tools)


# 
# Chatbot Node
# 
#
# Responsibilities:
#
# 1. Read conversation history.
# 2. Send messages to the LLM.
# 3. Return the AI response.
#
# The chatbot DOES NOT execute tools.
#
# It only decides WHETHER a tool
# should be executed.
#
def chatbot(state: State):

    response = llm_with_tool.invoke(
        state["messages"]
    )

    return {

        "messages": [response]

    }


# 
# ToolNode
# 
#
# ToolNode is one of LangGraph's
# prebuilt nodes.
#
# Responsibilities:
#
# ✔ Read tool_calls from AIMessage.
# ✔ Find the correct tool.
# ✔ Execute the tool.
# ✔ Create ToolMessage.
# ✔ Return updated State.
#
# Without ToolNode we would have to:
#
# - Find the tool manually
# - Execute it
# - Create ToolMessage
# - Append ToolMessage
#
tool_node = ToolNode(tools)


# 
# Build Graph
# 
#
# StateGraph creates the workflow
# of our AI Agent.
#
graph = StateGraph(State)


# 
# Register Nodes
# 
#
# chatbot -> LLM reasoning
#
# tools -> Tool execution
#
graph.add_node("chatbot", chatbot)

graph.add_node("tools", tool_node)


# 
# START -> Chatbot
# 
#
# Every graph starts here.
#
graph.add_edge(

    START,

    "chatbot"

)


# 
# Conditional Edge
# 
#
# After chatbot finishes,
# LangGraph automatically checks:
#
# Does the AI want to call a tool?
#
# YES
#  │
#  ▼
# ToolNode
#
# NO
#  │
#  ▼
# END
#
# This replaces our old Manual ReAct code:
#
# if response.tool_calls:
#     execute_tool()
#
graph.add_conditional_edges(

    "chatbot",

    tools_condition

)


# 
# ToolNode -> Chatbot
# 
#
# After tool execution,
# the AI must observe the tool result.
#
# Therefore the graph returns
# back to the Chatbot.
#
# This creates the ReAct loop.
#
graph.add_edge(

    "tools",

    "chatbot"

)


# 
# Compile Graph
# 
#
# Converts the graph blueprint
# into a runnable application.
#
app = graph.compile()


# 
# User Input
# 
#
user = input("You: ")


# 
# Execute Graph
# 
#
# invoke() starts graph execution.
#
# The graph follows:
#
# START
#   │
# Chatbot
#   │
# Tool?
#   │
# ToolNode
#   │
# Chatbot
#   │
# END
#
response = app.invoke(

    {

        "messages": [

            HumanMessage(user)

        ]

    }

)


# 
# Print Final Answer
# 
#
# The graph returns the complete State.
#
# The latest AI response
# is always the last message.
#
print("\nUser:", user)

print("\nAI:", response["messages"][-1].content)