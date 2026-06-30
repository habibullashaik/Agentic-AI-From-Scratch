# 🚀 Agentic AI From Scratch

> A complete hands-on journey to mastering Agentic AI by building everything from scratch using Python, LangChain, LangGraph, and modern LLMs.


## 📖 About This Repository

This repository documents my journey of learning **Agentic AI** from the ground up.

Instead of relying on pre-built frameworks, I focus on understanding **how AI agents actually work internally** by implementing every concept step by step.

Every project in this repository is heavily documented with beginner-friendly explanations, architecture diagrams, and production-oriented code.

The goal is not only to build AI agents but also to understand the reasoning behind every component.

---

# 🎯 Goals

- Learn Agentic AI from first principles
- Master LangChain and LangGraph
- Understand ReAct architecture deeply
- Build production-ready AI agents
- Learn memory, workflows, and multi-agent systems
- Document everything for teaching and revision
- Build a strong AI Engineering portfolio

---

# 🛣️ Learning Roadmap

## ✅ Completed

- [x] Raw Tool Calling using Groq API
- [x] Manual Tool Calling using LangChain
- [x] First LangGraph Chatbot
- [x] First ReAct Agent using LangGraph

## 🚧 Coming Soon

- [ ] Memory
- [ ] Checkpointers
- [ ] Conversation Memory
- [ ] Human In The Loop
- [ ] Interrupts
- [ ] Multi-Agent Systems
- [ ] MCP (Model Context Protocol)
- [ ] RAG Agent
- [ ] SQL Agent
- [ ] Code Agent
- [ ] AI Email Assistant
- [ ] AI Research Agent
- [ ] Production Agent Architecture

---

# 📂 Projects

## 01. Raw Tool Calling

Learn how LLMs call tools without using LangChain.

Topics Covered

- JSON Tool Schema
- Function Calling
- Tool Execution
- Tool Response
- Groq API

---

## 02. Manual ReAct Agent

Build the complete ReAct Loop manually.

Topics Covered

- Tool Registry
- Tool Execution
- ToolMessage
- AIMessage
- Manual ReAct Loop
- Conversation History

---

## 03. First LangGraph Chatbot

Build the simplest chatbot using LangGraph.

Topics Covered

- State
- TypedDict
- Annotated
- add_messages
- Nodes
- Edges
- START
- END
- Graph Compilation

---

## 04. LangGraph ReAct Agent

Build a complete AI Agent using LangGraph.

Topics Covered

- ToolNode
- bind_tools()
- tools_condition()
- Conditional Edges
- ReAct Workflow
- Graph Execution
- Tool Calling

---

# 🧠 Skills Covered

- Python
- Prompt Engineering
- Tool Calling
- ReAct Architecture
- LangChain
- LangGraph
- AI Agents
- LLM Workflows
- State Management
- Graph-based Execution

---

# 🏗️ Architecture

```text
                User
                  │
                  ▼
              LangGraph
                  │
        ┌─────────┴─────────┐
        │                   │
        ▼                   ▼
   Chatbot Node         Tool Node
        │                   │
        └─────────┬─────────┘
                  ▼
             Final Response
```

---

# 💻 Technologies

- Python
- LangChain
- LangGraph
- Groq
- Python Dotenv

---

# 🚀 Getting Started

Clone the repository

```bash
git clone https://github.com/habibullashaik/Agentic-AI-From-Scratch.git
```

Move into the project

```bash
cd Agentic-AI-From-Scratch
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```env
GROQ_API_KEY=your_api_key
```

Run any project

```bash
python 01_raw_tool_calling.py
```

---

# 📚 Why This Repository?

Many tutorials show **how** to build AI agents.

This repository focuses on explaining **why** each concept exists and **how it works internally**.

Every project is written with detailed comments so that it can be used for:

- Revision
- Teaching
- Interview preparation
- Portfolio showcase

---

# 📈 Progress

| Day | Topic | Status |
|------|-------|--------|
| Day 1 | Raw Tool Calling | ✅ |
| Day 2 | Manual ReAct Agent | ✅ |
| Day 3 | First LangGraph Chatbot | ✅ |
| Day 4 | LangGraph ReAct Agent | ✅ |
| Next | Memory & Checkpointers | 🚀 |

---

# 🎯 Future Projects

- AI Research Agent
- Browser Agent
- Coding Agent
- Email Agent
- SQL Agent
- PDF Chat Agent
- Multi-Agent Systems
- Human-in-the-Loop Workflows
- Long-Term Memory
- MCP
- Production AI Agents

---

# 🤝 Contributions

Suggestions, improvements, and discussions are always welcome.

If you find this repository useful, consider giving it a ⭐.

---

# 📬 Connect With Me

💼 LinkedIn

I regularly share my learning journey, projects, and insights about Generative AI, Agentic AI, and AI Engineering.

---

⭐ If you found this repository helpful, don't forget to Star it!
