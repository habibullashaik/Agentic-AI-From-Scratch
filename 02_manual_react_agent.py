"""
Manual ReAct Agent using LangChain

Objective
---------
This project demonstrates how a ReAct (Reason + Act) agent works manually.

Workflow
--------
1. Receive the user's question.
2. Send the conversation to the LLM.
3. Let the LLM decide whether a tool is required.
4. Execute the requested tool.
5. Send the tool result back to the LLM.
6. Repeat until the LLM produces the final answer.

This helps us understand what happens internally before learning LangGraph.
"""

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool
from langchain_groq import ChatGroq

load_dotenv()

# Initialize the LLM
llm = ChatGroq(model="llama-3.3-70b-versatile")


# Tool Definitions
# ----------------
# These tools can be selected by the LLM whenever required.


@tool
def add(a: int, b: int) -> int:
    """Use this tool when adding two numbers."""
    return a + b


@tool
def sub(a: int, b: int) -> int:
    """Use this tool when subtracting two numbers."""
    return a - b


@tool
def division(a: int, b: int) -> float:
    """Use this tool when dividing two numbers."""
    return a / b


@tool
def multiplication(a: int, b: int) -> int:
    """Use this tool when multiplying two numbers."""
    return a * b


@tool
def weather(city: str) -> str:
    """Use this tool whenever the user asks for weather information."""

    fake_db = {
        "hyderabad": "Currently the weather is 20°C.",
        "ongole": "Currently the weather is 35°C.",
        "ammanabrolu": "Currently the weather is 25°C.",
        "vetapalem": "Currently the weather is 29°C."
    }

    return fake_db.get(city.lower(), "Weather information not found.")


# Register all available tools.
# The LLM will only be able to use tools listed here.

tool_registry = {
    "add": add,
    "sub": sub,
    "division": division,
    "multiplication": multiplication,
    "weather": weather
}


# Bind the registered tools with the LLM.
# This allows the model to generate tool calls whenever needed.

llm_with_tools = llm.bind_tools(
    list(tool_registry.values())
)


# Get the user's question.

prompt = input("User: ")

messages = [
    HumanMessage(prompt)
]


# Manual ReAct Loop
#
# Reason  -> LLM decides what to do.
# Act     -> Execute the selected tool.
# Observe -> Read tool output.
# Repeat  -> Continue until a final answer is generated.

while True:

    # Send the complete conversation to the LLM.
    res = llm_with_tools.invoke(messages)

    # Store the AI response in conversation history.
    messages.append(res)

    # If there are no tool calls,
    # the LLM has generated the final answer.

    if not res.tool_calls:
        print("\nAI Answer:\n")
        print(res.content)
        break

    # Execute every tool requested by the LLM.

    for tool_call in res.tool_calls:

        tool_name = tool_call["name"]
        tool_args = tool_call["args"]

        print(f"\nTool Selected : {tool_name}")
        print(f"Arguments     : {tool_args}")

        # Find the requested tool.

        selected_tool = tool_registry.get(tool_name)

        # Execute the tool using the generated arguments.

        tool_result = selected_tool.invoke(tool_args)

        print(f"Tool Result   : {tool_result}")

        # Return the tool result back to the LLM.
        # This allows the model to observe the output
        # and continue its reasoning process.

        messages.append(
            ToolMessage(
                content=str(tool_result),
                tool_call_id=tool_call["id"]
            )
        )