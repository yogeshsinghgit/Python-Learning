# LangGraph Revision Notes

> These notes are meant for **quick revision** of every LangGraph
> concept learned so far. They focus on **what the concept is, why it
> exists, when to use it, and the important production takeaways.**

------------------------------------------------------------------------

# 1. What is LangGraph?

LangGraph is a framework for building **stateful, controllable AI
workflows** using graphs.

Instead of writing one long function, you break the workflow into
**nodes** connected by **edges**. Every node reads from a shared state,
performs work, and returns updates to that state.

------------------------------------------------------------------------

# 2. StateGraph

## Definition

`StateGraph` is the graph builder used to define your workflow.

It knows:

-   what the shared state looks like
-   which nodes exist
-   how nodes are connected

After defining the graph, it is compiled into an executable graph.

**Use when:** Building deterministic workflows with shared state.

------------------------------------------------------------------------

# 3. State

## Definition

State is the shared data that flows through the graph.

Each node:

-   receives the current state
-   reads required values
-   returns only the fields it wants to update

LangGraph merges those updates into the existing state.

**Production Tip:** Treat state as the single source of truth.

------------------------------------------------------------------------

# 4. Nodes

## Definition

A node is simply a Python function.

Responsibilities:

-   Read state
-   Perform logic
-   Return updated state

A node should ideally have **one responsibility**.

------------------------------------------------------------------------

# 5. START and END

`START` marks where graph execution begins.

`END` marks successful completion.

Every graph begins at START and eventually reaches END unless routed
elsewhere.

------------------------------------------------------------------------

# 6. Edges

Edges connect nodes.

Types learned:

-   Static edges (always go to the same node)
-   Conditional edges (next node depends on runtime state)

------------------------------------------------------------------------

# 7. Conditional Routing

Instead of always following the same path, a routing function decides
the next node.

Useful when execution depends on:

-   LLM output
-   User choice
-   State values
-   Tool results

------------------------------------------------------------------------

# 8. Command

We learned two completely different uses.

## A. Routing Command

Purpose:

-   Update state
-   Dynamically choose the next node

Conceptually:

-   update state
-   goto another node

Use when node itself decides where execution should continue.

------------------------------------------------------------------------

## B. Resume Command

Used together with interrupts.

Purpose:

Resume a paused graph by providing the value requested by `interrupt()`.

Conceptually:

-   resume paused execution
-   inject external input

------------------------------------------------------------------------

# 9. Parallel Execution

A graph can execute multiple independent nodes simultaneously.

Benefits:

-   Better performance
-   Independent processing
-   Cleaner architecture

Eventually execution joins back together.

------------------------------------------------------------------------

# 10. Reducers

## Problem

Multiple parallel nodes updating the same state key create conflicts.

## Solution

Reducers define **how those values should be merged**.

We learned reducers using `typing.Annotated`.

Production use:

-   collecting retrieved documents
-   accumulating messages
-   merging search results

------------------------------------------------------------------------

# 11. MessagesState

A built-in state designed for conversational applications.

Contains conversation history.

Typical message types:

-   HumanMessage
-   AIMessage
-   ToolMessage

Production systems usually extend it with application-specific fields
such as retrieved documents, citations, namespaces, etc.

------------------------------------------------------------------------

# 12. Tool Calling

The LLM can decide that it needs external information.

Flow:

User

↓

LLM

↓

Tool Call

↓

Tool Executes

↓

Tool Result

↓

LLM

↓

Final Answer

We learned:

-   bind_tools()
-   ToolNode
-   tools_condition

------------------------------------------------------------------------

# 13. ReAct Pattern

ReAct stands for:

Reason + Act

The LLM repeatedly decides:

-   Should I answer?
-   Should I call another tool?

until it has enough information.

------------------------------------------------------------------------

# 14. Checkpointing

Checkpointing stores graph progress.

It saves:

-   graph state
-   current execution position

It does **not** save:

-   Python call stack
-   local variables
-   interpreter state

We learned:

-   InMemorySaver
-   thread_id
-   compile(checkpointer=...)

Purpose:

Resume long-running workflows safely.

------------------------------------------------------------------------

# 15. Interrupts

Interrupts pause graph execution and return control to the application.

Instead of continuing automatically, the graph waits for external input.

Typical use cases:

-   Human approval
-   User confirmation
-   Manual review
-   Authentication

Resume is done using `Command(resume=...)`.

------------------------------------------------------------------------

# 16. Replay-safe Nodes

Important production concept.

Interrupted nodes are replayed from the beginning.

Because of that:

Everything before `interrupt()` executes again.

Safe before interrupt:

-   calculations
-   searches
-   read-only API calls

Avoid before interrupt:

-   payments
-   emails
-   database writes
-   notifications
-   deleting resources

These should happen **after** the interrupt or in a separate node.

------------------------------------------------------------------------

# 17. Production Best Practices

-   Keep nodes small.
-   Give each node one responsibility.
-   Keep state clean.
-   Avoid unnecessary mutations.
-   Prefer deterministic nodes.
-   Make interrupt nodes replay-safe.
-   Separate side effects into dedicated nodes.
-   Use conditional routing only when needed.

------------------------------------------------------------------------

# 18. Projects Built

## Travel Agent

Learned:

-   MessagesState
-   ToolNode
-   Tool Calling
-   ReAct workflow

## Booking Approval Workflow

Learned:

-   Checkpointing
-   Interrupts
-   Resume Command
-   Replay-safe execution

------------------------------------------------------------------------

# Revision Checklist

-   [x] StateGraph
-   [x] State
-   [x] Nodes
-   [x] START / END
-   [x] Static Edges
-   [x] Conditional Routing
-   [x] Command (Routing)
-   [x] Parallel Execution
-   [x] Reducers
-   [x] MessagesState
-   [x] Tool Calling
-   [x] ReAct Pattern
-   [x] Checkpointing
-   [x] Interrupts
-   [x] Command (Resume)
-   [x] Replay-safe Nodes

------------------------------------------------------------------------

# Next Topics

-   Memory
-   Persistent Checkpointers
-   Subgraphs
-   Multi-Agent Systems
-   Streaming
-   Long-running Agents
-   Production Deployment
-   Observability
