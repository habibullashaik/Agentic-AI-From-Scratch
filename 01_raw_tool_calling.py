"""

Project : Raw Tool Calling using Groq API
Author  : Habibulla Shaik

Objective
---------
Learn how Tool Calling works internally without using LangChain or LangGraph.

In this project we will understand:

1. How an LLM decides to call a tool.
2. How tools are defined using JSON Schema.
3. How the LLM returns a tool request instead of a final answer.
4. How Python executes the requested tool.
5. How the application controls the complete workflow.

Architecture
------------

                    User Question
                        │
                        ▼
                    Groq LLM (Llama 3.3)
                        │
            Does it need an external tool?
                    │                 │
                Yes                No
                    │                 │
                    ▼                 ▼
            Return Tool Call      Return Answer
                    │
                    ▼
        Python Application executes tool
                    │
                    ▼
            Tool Result Returned

NOTE:
-----
This project DOES NOT automatically send the tool result back to the LLM.
That is the next step (Manual ReAct Loop).


"""

from groq import Groq
import json

# 
# Create Groq Client
# 
# This client is responsible for communicating with Groq's API.
#
# Every request to the LLM will go through this client.
#
client = Groq(api_key="YOUR_API_KEY")


# 
# Tool Definitions
# 
# Here we describe every tool available to the LLM.
#
# IMPORTANT:
#
# These are NOT Python functions.
#
# These are JSON Schemas that explain:
#
# • Tool Name
# • Tool Description
# • Input Parameters
# • Required Fields
#
# The LLM only reads these descriptions.
#
# It DOES NOT execute them.
#
tools = [
    {
        "type": "function",
        "function": {
            "name": "Multiply",

            # Description helps the LLM decide
            # when this tool should be used.
            "description": "Multiply two numbers",

            "parameters": {
                "type": "object",

                "properties": {

                    "a": {
                        "type": "number"
                    },

                    "b": {
                        "type": "number"
                    }

                },

                "required": ["a", "b"]
            }
        }
    },

    {
        "type": "function",

        "function": {

            "name": "weather",

            "description":
            "Use this function whenever the user asks about weather.",

            "parameters": {

                "type": "object",

                "properties": {

                    "city": {

                        "type": "string"

                    }

                },

                "required": ["city"]

            }

        }
    }
]


# 
# Actual Python Tool
# 
# This is the REAL implementation.
#
# Unlike the JSON schema above,
# this function actually performs the calculation.
#
def calculator(a, b):
    return int(a) * int(b)


# 
# Weather Tool
# 
# Here we are using a fake database instead of a real API.
#
# Later this can be replaced with:
#
# - OpenWeather API
# - WeatherAPI
# - Any external REST API
#
def weather(city):

    fake_db = {

        "Hyderabad": "Weather is currently 28°C",

        "Ongole": "Weather is currently 35°C",

        "Ammanabrolu": "Weather is currently 30°C"

    }

    return fake_db.get(
        city,
        "Weather data not available."
    )


# 
# Conversation History
# 
# Every Chat Completion API expects messages.
#
# Each message contains:
#
# role
# content
#
messages = [

    {

        "role": "user",

        "content": "What is the weather condition in Hyderabad?"

    }

]


# 
# Send Request to Groq
# 
#
# We send:
#
# 1. User messages
# 2. Tool definitions
#
# The model now has two choices:
#
# A) Answer directly.
#
# B) Ask us to execute a tool.
#
response = client.chat.completions.create(

    model="llama-3.3-70b-versatile",

    messages=messages,

    tools=tools,

    tool_choice="auto"

)


# 
# Extract LLM Response
# 
#
# The first choice contains the assistant's reply.
#
msg = response.choices[0].message

print(msg)


# 
# Did the LLM request a tool?
# 
#
# If tool_calls exists:
#
# The model is NOT answering yet.
#
# Instead it is saying:
#
# "Please execute this tool for me."
#
if msg.tool_calls:

    tool_call = msg.tool_calls[0]

    # Tool Name
    tool_name = tool_call.function.name

    # Tool Arguments
    #
    # Arguments are returned as JSON string.
    #
    # Convert them into Python dictionary.
    #
    tool_args = json.loads(
        tool_call.function.arguments
    )

    # Unique ID of tool call
    tool_id = tool_call.id

    print("=" * 60)

    print("Tool Selected :", tool_name)

    print("Arguments :", tool_args)

    print("=" * 60)


    # ---------------------------------------------------------------
    # Execute Weather Tool
    # ---------------------------------------------------------------
    #
    if tool_name == "weather":

        result = weather(**tool_args)

        print("Weather Result")

        print(result)

    # ---------------------------------------------------------------
    # Execute Calculator Tool
    # ---------------------------------------------------------------
    #
    else:

        result = calculator(**tool_args)

        print("Calculation Result")

        print(result)

# No Tool Needed
#
# If tool_calls is empty,
# the LLM already knows the answer.
#
else:

    print("No Tool Required")

    print(msg.content)