from backend import save_task, list_tasks, complete_task, delete_task, task_stats
from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from langchain.agents import create_react_agent, AgentExecutor
from langchain_ollama import OllamaLLM


# Configure Ollama with your llama3 model
llm = OllamaLLM(
    model="llama3",
    temperature=0.1,
    num_ctx=4096,
    # top_p=0.9,  # Adjust for creativity. Lower values make the model more focused and less creative.
)


# Create tools with proper descriptions
tools = [
    Tool(
        name="save_task",
        func=save_task,
        description="Save a new task. Input format: 'task description|priority'. Example: 'Buy milk|low' or just 'Buy milk' for medium priority"
    ),
    Tool(
        name="list_tasks",
        func=list_tasks,
        description="List all pending tasks. Optionally filter by priority (low/medium/high). Input: empty string for all tasks or priority level"
    ),
    Tool(
        name="complete_task",
        func=complete_task,
        description="Mark a task as completed. Input: task ID number"
    ),
    Tool(
        name="delete_task",
        func=delete_task,
        description="Delete a task permanently. Input: task ID number"
    ),
    Tool(
        name="task_stats",
        func=task_stats,
        description="Show task statistics. Input: empty string"
    )
]

# Create a prompt template for the agent
prompt_template = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
Thought: I now know the final answer
Final Answer: the final answer to the original input question

IMPORTANT RULES:
- After getting a result from list_tasks, IMMEDIATELY provide the Final Answer
- Do NOT repeat the same action multiple times
- If you get task information, that IS your answer
- 🆕 When showing task lists, ALWAYS preserve the exact format with emojis and IDs
- 🆕 Your Final Answer should be EXACTLY what the tool returned, do not summarize

Begin!

Question: {input}
Thought:{agent_scratchpad}"""

prompt = PromptTemplate(
    template=prompt_template,
    input_variables=["input", "tools", "tool_names", "agent_scratchpad"]
)

# Create the agent
agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

# Create agent executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,  # Set to True for debugging
    max_iterations=5,
    handle_parsing_errors=True,
    return_intermediate_steps=True,
)
