
# 🔧 LangChain Tools & Tool Calling

This document explains:

- What tools are in LangChain
- Types of tools
- How tools work internally
- Tool calling flow
- Practical examples

---

# 1️⃣ What Are Tools in LangChain?

A **Tool** is a function that an LLM can use to perform actions outside of the model.

Normally, LLMs can only generate text. Tools allow them to interact with the **external world**, such as:

- APIs
- Databases
- Search engines
- Python functions
- File systems

### Basic Concept

Without tools:

```

User → LLM → Text Response

```

With tools:

```

User
↓
LLM decides to use tool
↓
Application executes tool
↓
Tool result returned
↓
LLM generates final answer


---

# 2️⃣ Why Tools Are Important

Tools transform an LLM from a **text generator** into a **capable AI system**.

Without tools:

```

LLM = Chatbot

```

With tools:

```

LLM = AI assistant capable of actions

````

Common use cases:

- Querying databases
- Searching the web
- Running calculations
- Automating workflows
- Calling APIs

---

# 3️⃣ Basic Tool Example

LangChain provides a simple way to convert Python functions into tools.

```python
from langchain.tools import tool

@tool
def multiply_numbers(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b
````

### What `@tool` Does

The decorator converts the function into a **LangChain tool** and automatically extracts:

* Tool name
* Description
* Input parameters

The LLM reads this metadata to understand how to use the tool.

---

# 4️⃣ Tool Metadata

Every tool contains metadata that the LLM uses for reasoning.

Example tool definition:

```
Tool Name: multiply_numbers

Description:
Multiply two numbers

Arguments:
{
  "a": integer
  "b": integer
}
```

This information is provided to the LLM so it can decide **when and how to use the tool**.

---

# 5️⃣ Types of Tools in LangChain

LangChain supports multiple types of tools.

---

## 1️⃣ Function Tools

The simplest type of tool created using the `@tool` decorator.

Example:

```python
@tool
def add_numbers(a: int, b: int) -> int:
    return a + b
```

Use case:

* simple utilities
* calculations
* small API wrappers

---

## 2️⃣ Structured Tools

Structured tools use **Pydantic schemas** to validate input arguments.

### Example Schema

```python
from pydantic import BaseModel, Field

class MultiplyInput(BaseModel):
    a: int = Field(description="First number")
    b: int = Field(description="Second number")
```

### Structured Tool

```python
from langchain.tools import StructuredTool

def multiply_numbers(a: int, b: int) -> int:
    return a * b

multiply_tool = StructuredTool.from_function(
    func=multiply_numbers,
    name="multiply_numbers",
    description="Multiply two numbers",
    args_schema=MultiplyInput
)
```

Advantages:

* strict validation
* clearer tool inputs
* better LLM understanding

---

## 3️⃣ Toolkits

A **Toolkit** is a collection of related tools.

Example:

```
SQLDatabaseToolkit
PythonREPLToolkit
```

Used when a system requires multiple tools for a domain.

Example:

```
Database toolkit:
 - run_sql
 - list_tables
 - describe_table
```

---

## 4️⃣ Built-in Tools

LangChain provides built-in integrations for common tasks.

Examples:

* Web search
* Python REPL
* SQL database tools
* File system tools

These allow LLMs to interact with real-world systems.

---

# 6️⃣ Binding Tools to an LLM

Tools must be explicitly provided to the LLM.

Example:

```python
llm_with_tools = llm.bind_tools([multiply_numbers])
```

This tells the model:

```
These tools are available for you to use.
```

The model will then decide **when to call them**.

---

# 7️⃣ Tool Calling Flow

Tool calling follows a multi-step process.

---

## Step 1 — User Request

```
User: What is 45 multiplied by 78?
```

---

## Step 2 — LLM Decides to Use Tool

The LLM generates a **tool call instruction** instead of answering.

Example:

```json
{
 "tool_calls": [
   {
     "name": "multiply_numbers",
     "args": {
       "a": 45,
       "b": 78
     }
   }
 ]
}
```

This is **not the final answer**.

It is an instruction for the application to execute the tool.

---

## Step 3 — Application Executes Tool

Your Python code executes the tool.

Example:

```
multiply_numbers(45, 78)
```

Result:

```
3510
```

---

## Step 4 — Tool Result Sent Back to LLM

The system sends the result back to the model.

```
Tool result: 3510
```

---

## Step 5 — LLM Generates Final Response

Now the model produces the final answer.

```
45 multiplied by 78 equals 3510.
```

---

# 8️⃣ Tool Calling Architecture

Full architecture:

```
User
 ↓
Prompt
 ↓
LLM
 ↓
Tool Call Decision
 ↓
Application Executes Tool
 ↓
Tool Result
 ↓
LLM Final Response
```

---

# 9️⃣ Message Flow During Tool Calling

Internally the conversation looks like this:

```
System: You are an assistant with access to tools.

User: What is 45 × 78?

Assistant:
{
 "tool_call": {
   "name": "multiply_numbers",
   "args": {"a": 45, "b": 78}
 }
}

Tool:
3510

Assistant:
45 multiplied by 78 equals 3510.
```

---

# 🔟 Important Concept

The **LLM does not execute tools itself**.

It only **suggests which tool to call and what arguments to use**.

The application is responsible for:

* executing the tool
* sending results back to the LLM
* managing the interaction loop

---

# 1️⃣1️⃣ Real Industry Use Cases

Tools enable powerful AI systems.

Examples:

### AI Data Analyst

```
User: Show total revenue for 2024
 ↓
LLM decides to run SQL
 ↓
SQL tool executes query
 ↓
Results returned
 ↓
LLM explains insights
```

---

### AI Research Assistant

```
User: Find latest AI research
 ↓
LLM calls web search tool
 ↓
Results retrieved
 ↓
LLM summarizes findings
```

---

### AI Automation Assistant

```
User: Send meeting reminder
 ↓
LLM calls email tool
 ↓
Email sent
 ↓
LLM confirms action
```

---

# 1️⃣2️⃣ Key Takeaways

* Tools allow LLMs to interact with external systems
* Tools are defined as Python functions
* LLMs only **suggest tool calls**, they do not execute them
* The application handles tool execution
* Tool calling enables AI systems like agents and copilots

---

# Next Topic

The next concept after tools is **Agents**.

Agents automate the **tool-calling loop**, allowing LLMs to:

* decide which tool to use
* execute tools
* process results
* continue reasoning until the task is complete

```

---

If you want, next I can explain **Agents in LangChain**, including:

- ReAct reasoning
- Agent loop
- `AgentExecutor`
- why **LangGraph is replacing classic agents**.
```
