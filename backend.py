import os
import json
from datetime import datetime
from langchain_ollama import OllamaLLM
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool
from langchain.prompts import PromptTemplate


# Configure Ollama with your llama3 model
# llm = OllamaLLM(
#     model="llama3",
#     temperature=0.1,
#     num_ctx=4096,
#     # top_p=0.9,  # Adjust for creativity. Lower values make the model more focused and less creative.
# )


# Define tool functions with single string input
def save_task(input_str: str) -> str:
    """Save a task with priority. Format: 'task_description|priority' where priority is low/medium/high"""
    try:
        # Parse input
        parts = input_str.split('|')
        task = parts[0].strip()
        priority = parts[1].strip().lower() if len(parts) > 1 else "medium"
        
        # Validate priority
        if priority not in ["low", "medium", "high"]:
            priority = "medium"
        
        # Load existing tasks
        tasks = []
        if os.path.exists("tasks.json"):
            with open("tasks.json", "r") as f:
                tasks = json.load(f)
        
        # Create new task
        new_task = {
            "id": len(tasks) + 1,
            "task": task,
            "priority": priority,
            "created": datetime.now().isoformat(),
            "completed": False
        }
        tasks.append(new_task)
        
        # Save tasks
        with open("tasks.json", "w") as f:
            json.dump(tasks, f, indent=2)
        
        return f"✅ Task saved: '{task}' with priority {priority}"
    except Exception as e:
        return f"❌ Error saving task: {str(e)}"


def list_tasks(filter_priority: str = "") -> str:
    """List pending tasks. Optionally filter by priority: low, medium, high"""
    if not os.path.exists("tasks.json"):
        return "📋 No tasks saved yet"
    
    with open("tasks.json", "r") as f:
        tasks = json.load(f)
    
    pending = [t for t in tasks if not t["completed"]]
    
    # Apply filter if provided
    if filter_priority and filter_priority.lower() in ["low", "medium", "high"]:
        pending = [t for t in pending if t["priority"] == filter_priority.lower()]
    
    if not pending:
        return "✨ No pending tasks"
    
    # Sort by priority
    priority_order = {'high': 0, 'medium': 1, 'low': 2}
    pending.sort(key=lambda x: priority_order.get(x['priority'], 3))
    
    result = "📋 Pending tasks:\n"
    for t in pending:
        emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(t['priority'], "⚪")
        result += f"{emoji} [{t['id']}] {t['task']}\n"
    
    return result.rstrip()


def complete_task(task_id_str: str) -> str:
    """Mark a task as completed by its ID"""
    try:
        task_id = int(task_id_str.strip())
    except ValueError:
        return "❌ Please provide a valid task ID number"
    
    if not os.path.exists("tasks.json"):
        return "❌ No tasks saved"
    
    with open("tasks.json", "r") as f:
        tasks = json.load(f)
    
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            task["completed_at"] = datetime.now().isoformat()
            with open("tasks.json", "w") as f:
                json.dump(tasks, f, indent=2)
            return f"✅ Task {task_id} completed: {task['task']}"
    
    return f"❌ Task with ID {task_id} not found"


def delete_task(task_id_str: str) -> str:
    """Delete a task permanently by its ID"""
    try:
        task_id = int(task_id_str.strip())
    except ValueError:
        return "❌ Please provide a valid task ID number"
    
    if not os.path.exists("tasks.json"):
        return "❌ No tasks saved"
    
    with open("tasks.json", "r") as f:
        tasks = json.load(f)
    
    original_length = len(tasks)
    tasks = [t for t in tasks if t["id"] != task_id]
    
    if len(tasks) < original_length:
        with open("tasks.json", "w") as f:
            json.dump(tasks, f, indent=2)
        return f"🗑️ Task {task_id} deleted"
    
    return f"❌ Task with ID {task_id} not found"


def task_stats(_: str = "") -> str:
    """Show task statistics"""
    if not os.path.exists("tasks.json"):
        return "📊 No statistics available"
    
    with open("tasks.json", "r") as f:
        tasks = json.load(f)
    
    total = len(tasks)
    completed = len([t for t in tasks if t.get("completed", False)])
    pending = total - completed
    
    by_priority = {}
    for t in tasks:
        if not t.get("completed", False):
            priority = t.get("priority", "medium")
            by_priority[priority] = by_priority.get(priority, 0) + 1
    
    stats = f"""📊 Task Statistics:

Total: {total}
✅ Completed: {completed}
⏳ Pending: {pending}

\n\nBy priority:
🔴 High: {by_priority.get('high', 0)}
🟡 Medium: {by_priority.get('medium', 0)}
🟢 Low: {by_priority.get('low', 0)}
"""
    return stats
