# 🤖 Task Planner AI Agent (Llama3 + LangChain)

This project is a CLI-based AI agent that helps you **manage your tasks using natural language**.  
It is built in Python using `LangChain` and a local LLM model powered by **Ollama (LLaMA 3)**.

You can:
- 📝 Add tasks with priorities
- 📋 List tasks or filter them
- ✅ Mark tasks as completed
- ❌ Delete tasks
- 📊 Show task statistics

## 🚀 How it works

This agent implements the **ReAct** pattern (Reasoning + Acting), using internal tools (Python functions) to take actions.

General flow:
1. You type a command in natural language.
2. The agent interprets it with Llama3.
3. It calls the appropriate function (`save_task`, `list_tasks`, `complete_task`, etc.).
4. You get a clear response.

## 🛠️ Tech Stack

- Python 3.10+
- [LangChain](https://www.langchain.com/)
- [Ollama](https://ollama.com/) + LLaMA 3 (local model)
- `json`, `datetime`, `rich`
- Local CLI app (no frontend needed)

## 📦 Installation

```bash
git clone https://github.com/herchila/ai-agent-task-planner.git
cd ai-agent-task-planner
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

Make sure you have Ollama installed and the `llama3` model available:

```bash
ollama run llama3
```

## ▶️ Usage

```bash
python main.py
```

🧠 Example commands:

- `"Add a task: review code with high priority"`
- `"What tasks do I have?"`
- `"Mark task 2 as completed"`
- `"Delete task 1"`
- `"Show me statistics"`
- `"bye, exit"` to quit

## 📁 Project Structure

```
AI_AGENT_TASKS/
├── agent.py        # LangChain agent + tools
├── backend.py      # Core task logic: add, list, complete, delete
├── main.py         # CLI interface
├── tasks.json      # Local storage
├── requirements.txt
```

## ✍️ Author

Built by Hernan Chilabert.

X: [@herchila](https://x.com/herchila)
