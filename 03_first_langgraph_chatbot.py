"""
===

Project : My First LangGraph Chatbot
Author  : Habibulla Shaik

Objective
---------
This is the simplest possible LangGraph application.

In this project we learn:

✔ What is State?
✔ What is StateGraph?
✔ What is a Node?
✔ What are START and END?
✔ What does compile() do?
✔ What does invoke() do?
✔ How LangGraph executes a graph.

Architecture
------------

                START
                   │
                   ▼
              Chatbot Node
                   │
                   ▼
                  END

Execution Flow
--------------

User Input
      │
      ▼
HumanMessage
      │
      ▼
START
      │
      ▼
Chatbot Node
      │
      ▼
LLM generates response
      │
      ▼
END
      │
      ▼
Final Answer

Important Note
--------------
This project does NOT use any tools.

It is simply a chatbot implemented using LangGraph.

The purpose of this project is to understand
how LangGraph works before building AI Agents.

===
"""

# Used for adding extra information (Reducer) to a datatype.
from typing import Annotated

# TypedDict allows us to define the structure of our State.
from typing_extensions import TypedDict

# LangGraph Components
#
# START  -> Entry point of the graph.
# END    -> Exit point of the graph.
# StateGraph -> Used to build our graph.
#
from langgraph.graph import START, END, StateGraph

# add_messages is a Reducer.
#
# Reducers tell LangGraph HOW to update state.
#
# Here it automatically appends new messages instead
# of replacing the old conversation.
#
from langgraph.graph.message import add_messages

# Groq LLM
from langchain_groq import ChatGroq

# Used to send user input to the LLM.
from langchain_core.messages import HumanMessage

from dotenv import load_dotenv

load_dotenv()


# 
# State
# 
#
# Think of State as the "Memory" of our graph.
#
# Every node receives the current state.
#
# Every node returns an updated state.
#
# In this chatbot our state contains only one variable:
#
# messages
#
# Example:
#
# {
#     "messages":[
#          HumanMessage(...),
#          AIMessage(...)
#     ]
# }
#
class State(TypedDict):

    # Annotated tells Python that this field has
    # an additional behaviour.
    #
    # add_messages automatically appends new messages
    # into the conversation history.
    #
    # Without add_messages,
    # every new response would replace
    # the previous messages.
    #
    messages: Annotated[list, add_messages]


# 
# Initialize LLM
# 
#
# This is the brain of our chatbot.
#
# LangGraph does NOT replace the LLM.
#
# It only manages the workflow around the LLM.
#
llm = ChatGroq(
    model="llama-3.3-70b-versatile"
)


# 
# Chatbot Node
# 
#
# Every LangGraph Node is simply a Python function.
#
# Responsibilities:
#
# 1. Receive the current State.
# 2. Perform some work.
# 3. Return an updated State.
#
# Here our node performs only one task:
#
# Send conversation history to the LLM.
#
def chatbot(state: State):

    # Read the conversation from State
    response = llm.invoke(state["messages"])

    # Return the new AI response.
    #
    # We DO NOT append messages manually.
    #
    # add_messages reducer automatically updates
    # the conversation history.
    #
    return {
        "messages": [response]
    }


# 
# Create Graph
# 
#
# StateGraph is the blueprint of our application.
#
# It tells LangGraph:
#
# "My graph will use this State."
#
graph = StateGraph(State)


# 
# Register Nodes
# 
#
# Here we tell LangGraph:
#
# There is one node called "chatbot".
#
# Whenever the graph reaches this node,
# execute chatbot().
#
graph.add_node(
    "chatbot",
    chatbot
)


# 
# Connect START -> Chatbot
# 
#
# Every graph must have one starting point.
#
# Execution begins here.
#
graph.add_edge(
    START,
    "chatbot"
)


# 
# Connect Chatbot -> END
# 
#
# After chatbot finishes,
# stop the graph.
#
graph.add_edge(
    "chatbot",
    END
)


# 
# Compile Graph
# 
#
# compile() converts the graph blueprint
# into a runnable application.
#
# Think like this:
#
# Design
#    │
# compile()
#    │
# Runnable Application
#
app = graph.compile()


# 
# Get User Input
# 
#
user = input("You: ")


# 
# Execute Graph
# 
#
# invoke() starts graph execution.
#
# The graph follows this path:
#
# START
#   │
#   ▼
# Chatbot
#   │
#   ▼
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
# Print Final AI Response
# 
#
# response contains the COMPLETE State.
#
# Example:
#
# {
#     "messages":[
#         HumanMessage(...),
#         AIMessage(...)
#     ]
# }
#
# The last message is always
# the latest AI response.
#
print(response["messages"][-1].content)