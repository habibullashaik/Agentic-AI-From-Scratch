"""

Project : My First Email AI Agent using LangGraph


Objective
---------
Build a ReAct AI Agent that can:

✔ Understand the user's request.
✔ Decide whether a tool is required.
✔ Execute the correct tool.
✔ Observe the tool result.
✔ Return the final response.

Current Tools
-------------
1. Send Email
2. Addition


Before Running This Project


STEP 1 : Create a Gmail App Password

Normal Gmail passwords DO NOT work with SMTP.

Google blocks login from less secure applications.

Instead, use an App Password.



STEP 2 : Enable 2-Step Verification

Google Account
    ↓
Security
    ↓
2-Step Verification
    ↓
Turn ON

Without enabling 2-Step Verification,
Google will NOT allow App Password creation.



STEP 3 : Create an App Password

Google Account
    ↓
Security
    ↓
App Passwords
    ↓
Select

App : Mail
Device : Windows (or Other)

Google generates something like:

abcd efgh ijkl mnop

This is NOT your Gmail password.

Use this password inside .env



STEP 4 : Create .env

EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_generated_app_password

Never hardcode credentials inside Python files.


Agent Architecture


                START
                  │
                  ▼
             Chatbot Node
                  │
       Does AI need a tool?
          │             │
         Yes            No
          │             │
          ▼             ▼
      ToolNode         END
          │
          ▼
     Execute Tool
          │
          ▼
     Tool Result
          │
          ▼
      Chatbot Node
          │
          ▼
         END


"""

# 
# Imports
# 

# Used to create custom tools
from langchain_core.tools import tool

# Groq LLM
from langchain_groq import ChatGroq

# Loads environment variables from .env
from dotenv import load_dotenv

# Gmail SMTP library
import smtplib

# Used to construct email
from email.message import EmailMessage

import os

# Reducer for storing conversation history
from langgraph.graph.message import add_messages

from typing import Annotated
from typing_extensions import TypedDict

# LangGraph Components
from langgraph.graph import START, END, StateGraph

# Prebuilt Tool Execution Node
from langgraph.prebuilt import ToolNode, tools_condition

# Human Message
from langchain_core.messages import HumanMessage

# 
# Load Environment Variables
# 

load_dotenv()

EMAIL = os.getenv("EMAIL_ADDRESS")
PASSWORD = os.getenv("EMAIL_PASSWORD")

# 
# State
# 
#
# State is shared memory of the graph.
#
# Here we only store conversation messages.
#
# add_messages automatically appends
# every new message into history.
#
# 

class State(TypedDict):
    messages: Annotated[list, add_messages]

# 
# Initialize LLM
# 

llm = ChatGroq(
    model="llama-3.3-70b-versatile"
)

# 
# Email Tool
# 
#
# This tool sends an email using Gmail SMTP.
#
# The LLM decides WHEN to call this tool.
#
# The tool itself only performs the action.
#
# 

@tool
def send_message(
    recipient: str,
    subject: str,
    body: str
) -> str:
    """
    Use this tool whenever the user
    asks for sending an email.
    """

    try:

        # Create Email
        message = EmailMessage()

        message["From"] = EMAIL
        message["To"] = recipient
        message["Subject"] = subject

        message.set_content(body)

        # Secure SMTP Connection
        with smtplib.SMTP_SSL(
            "smtp.gmail.com",
            465
        ) as sp:

            sp.login(
                EMAIL,
                PASSWORD
            )

            sp.send_message(message)

        return "Email Sent Successfully"

    except Exception as e:

        return f"Raises an error {e}"

# 
# Addition Tool
# 

@tool
def addition(a: int, b: int) -> int:
    """
    Use this tool whenever the user
    asks for addition.
    """

    return a + b

# 
# Register Tools
# 

tools = [
    send_message,
    addition
]

# ToolNode automatically executes tools
tool_node = ToolNode(tools)

# Tell the LLM which tools are available.
# bind_tools DOES NOT execute them.
llm_with_tools = llm.bind_tools(tools)

# 
# Chatbot Node
# 
#
# Responsibilities:
#
# 1. Read conversation
# 2. Ask LLM
# 3. Return AIMessage
#
# The chatbot DOES NOT execute tools.
#
# 

def chatbot(state: State):

    response = llm_with_tools.invoke(
        state["messages"]
    )

    return {
        "messages": [response]
    }

# 
# Build Graph
# 

graph = StateGraph(State)

# Register Nodes
graph.add_node("chatbot", chatbot)
graph.add_node("tools", tool_node)

# START → Chatbot
graph.add_edge(
    START,
    "chatbot"
)

# Chatbot
#      │
#      ▼
# tools_condition()
#
# If tool required
#      ▼
# ToolNode
#
# Otherwise
#      ▼
# END

graph.add_conditional_edges(
    "chatbot",
    tools_condition
)

# IMPORTANT
#
# In a complete ReAct loop, this edge should usually be:
#
# graph.add_edge("tools", "chatbot")
#
# so the LLM can observe the tool result and generate
# a final response.
#
# In this demo we directly finish after chatbot.

graph.add_edge(
    "chatbot",
    END
)

# 
# Compile Graph
# 

app = graph.compile()

# 
# User Input
# 

user = input("You: ")

# 
# Execute Graph
# 

response = app.invoke(
    {
        "messages": [
            HumanMessage(user)
        ]
    }
)

# 
# Final Response
# 

print(
    response["messages"][-1].content
)