from langchain.prompts import PromptTemplate

template = """
You are a mathematical reasoning agent.

You have access to the following tools:

{tools}

Use the following format:

Question: the question to solve
Thought: think step by step
Action: the tool to use, should be one of [{tool_names}]
Action Input: JSON input for the tool
Observation: result of the tool

Repeat Thought/Action/Observation as needed.

When finished respond with:

Final Answer: the answer

Begin!

Question: {input}

{agent_scratchpad}
"""

prompt = PromptTemplate(
    input_variables=["tools", "tool_names", "input", "agent_scratchpad"],
    template=template
)