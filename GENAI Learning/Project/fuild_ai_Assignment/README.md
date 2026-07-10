# Autonomous AI Agent for Document Generation

This project implements an autonomous AI agent capable of breaking down complex user requests into actionable tasks, executing them sequentially, and compiling the results into a fully formatted Word document (.docx). 

## Architecture & Workflow

The system is built on a **Plan-and-Execute** agent architecture:

1. **Request Validation**: User requests are validated through a FastAPI router using Pydantic schemas to ensure data integrity and enforce guardrails.
2. **Planner**: A primary LLM (Llama 3 70B via Groq) acts as the planner, taking the user request and generating a structured `ExecutionPlan` containing independent tasks.
3. **Executor**: The executor loops through each task in the plan. It invokes the LLM to generate the content for that specific section based on the task description.
4. **Tool Calling**: During execution, the LLM has access to tools (like `document_metadata`). If the LLM determines metadata is needed (which is enforced via prompt rules), it halts generation, invokes the tool, and then resumes generation using the retrieved metadata.
5. **Retry & Fallback**: Network requests to the LLM are inherently unstable. The system wraps LLM invocations in a retry loop (up to 3 attempts). If the primary LLM repeatedly fails, it autonomously degrades to a lighter fallback model (Llama 3.1 8B).
6. **Document Generation**: Generated sections are passed to a `document_service` which utilizes `python-docx` to format headings and text, saving the final output locally.

## Technologies Used
- **Framework**: FastAPI (for the asynchronous API server)
- **AI/LLM**: LangChain, Groq API (Llama 3 models)
- **Data Validation**: Pydantic & Pydantic Settings
- **Document Creation**: `python-docx`
- **Logging**: Loguru

## API Design
The API exposes a simple, RESTful interface:
- **`POST /agent`**: Accepts a JSON payload (`AgentRequest`) containing the objective. It runs the orchestrator asynchronously, returning the final document path, goal, and task breakdown upon completion.

---

## Debugging Insight (1–2 min)

**Issue:** During the implementation of the `document_metadata` tool, the generated document ended up containing only the task titles (headers) with completely empty body content.
**Root Cause:** We initially used LangChain's `tool_choice="any"` parameter to force the model to invoke the metadata tool. When modern LLMs (like Llama 3) decide to make a tool call, they typically stop generating textual content entirely. Because the script only requested one response from the LLM and grabbed `response.content`, it successfully retrieved the tool call but missed the actual markdown text.
**Resolution:** Removed the aggressive `tool_choice="any"` constraint and relied on strong prompt instructions. More importantly, we implemented a standard **tool-calling loop** in the executor: when a tool call is detected, the system executes the Python function, appends a `ToolMessage` containing the metadata back to the conversation history, and invokes the LLM a *second time*. This allows the model to "see" the metadata and proceed with generating the final text content.

## Tradeoff Discussion (1–2 min)

**Autonomous Planning vs Deterministic Workflows**
In this project, we opted for **Autonomous Planning**, where the LLM dynamically determines the steps needed to generate the document instead of using a hardcoded, deterministic template (e.g., *always* generate an Intro, Body, and Conclusion).

- **Pros**: It allows the system to be highly flexible and extensible. It can adapt to vastly different requests (e.g., writing a software proposal vs. a creative story) without needing codebase changes.
- **Cons**: It sacrifices strict predictability and speed. Because the LLM must first generate a plan before executing, latency is increased by an entire generation cycle. Additionally, there is a risk of the planner generating a suboptimal or nonsensical plan (hallucination), which requires heavy prompt engineering and output parsing to mitigate. 
If absolute accuracy and speed were the highest priority for a specific domain (like legal contracts), a deterministic workflow with rigid templates would have been a better engineering choice.
