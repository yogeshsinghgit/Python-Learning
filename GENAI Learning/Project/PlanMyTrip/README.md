# PlanMyTrip -- Architecture Handover

> This document summarizes the architecture, project structure, and
> implementation completed so far so another LLM can continue
> development without losing context.

------------------------------------------------------------------------

# Project Goal

Build a **production-ready AI Travel Agent** using:

-   Python 3.12+
-   FastAPI
-   LangGraph
-   LangChain
-   Pydantic
-   Async-first architecture
-   Clean Architecture
-   Dependency Injection
-   Loguru

The project is **not** a demo chatbot.

The goal is an enterprise-quality AI agent that can:

-   Understand user intent
-   Plan before acting
-   Call domain tools
-   Interact with external APIs
-   Maintain conversation history
-   Scale to multiple travel capabilities

------------------------------------------------------------------------

# High-Level Architecture

``` text
                 User
                   │
                   ▼
              FastAPI Router
                   │
                   ▼
             ChatService
                   │
                   ▼
             TravelAgent
                   │
                   ▼
            Compiled LangGraph
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
   Planner Node         Chatbot Node
                              │
                              ▼
                        ToolNode (planned)
                              │
                              ▼
                     Domain Tools (planned)
                              │
                              ▼
                   Hotel / Weather / etc.
```

------------------------------------------------------------------------

# Current Folder Structure

``` text
app/
├── ai/
│   ├── agents/
│   │   ├── base.py
│   │   └── travel_agent.py
│   │
│   ├── planner/
│   │   ├── models.py
│   │   ├── prompts.py
│   │   ├── exceptions.py
│   │   └── service.py
│   │
│   └── runtime_dependencies/
│       └── runtime.py
│
├── graph/
│   ├── builder.py
│   ├── graph_context.py
│   ├── state.py
│   └── nodes/
│       ├── planner_node.py
│       └── chatbot_node.py
│
├── services/
│   └── chat_service.py
│
├── core/
│   └── lifespan.py
│
└── tools/
    (planned)
```

------------------------------------------------------------------------

# Components

## PlannerService

Purpose:

-   Runs before every LLM response.
-   Produces a structured `PlannerDecision`.

Input:

-   User query
-   Chat history

Output:

-   intent
-   confidence
-   should_use_tools
-   tool_names

PlannerService accepts only a `BaseChatModel` to avoid circular
dependencies.

------------------------------------------------------------------------

## GraphContext

Carries runtime dependencies into graph nodes.

Current fields:

-   llm
-   planner
-   redis

------------------------------------------------------------------------

## GraphState

Extends `MessagesState`.

Current custom field:

-   planner_decision

Nodes currently access runtime state using dictionary syntax:

``` python
state["messages"]
state["planner_decision"]
```

------------------------------------------------------------------------

## planner_node.py

Responsibilities:

-   Read latest user message
-   Build PlannerRequest
-   Call PlannerService
-   Store PlannerDecision

Returns:

``` python
{
    "planner_decision": decision
}
```

------------------------------------------------------------------------

## chatbot_node.py

Responsibilities:

-   Read conversation messages
-   Read planner decision
-   Invoke tool-aware LLM
-   Return AIMessage

Current implementation does **not** execute tools yet.

------------------------------------------------------------------------

## Builder

Current flow:

``` text
START
   │
   ▼
Planner
   │
   ▼
Chatbot
   │
   ▼
END
```

ToolNode integration is planned.

------------------------------------------------------------------------

# Important Bug Fixes Already Made

1.  Fixed circular dependency between PlannerService and GraphContext.
2.  PlannerService now accepts BaseChatModel instead of GraphContext.
3.  Runtime creates PlannerService.
4.  Lifespan passes wrapper clients instead of raw SDK clients.
5.  BaseAgent now correctly calls `_build_graph()`.
6.  Graph compilation happens only once.
7.  Node state uses dictionary access instead of attribute access.

------------------------------------------------------------------------

# Planned Architecture (Do NOT Simplify)

The project should follow:

``` text
TravelAgent
│
├── Planner
│
├── Chatbot
│
├── ToolNode (LangGraph)
│
└── Domain Tools
      │
      ├── HotelTool
      │       │
      │       ▼
      │   HotelAgent
      │       │
      │       ▼
      │   HotelService
      │
      ├── WeatherTool
      │       │
      │       ▼
      │   WeatherAgent
      │
      └── AttractionTool
              │
              ▼
          AttractionAgent
```

Important:

-   Use LangGraph's ToolNode.
-   Do NOT implement a custom tool executor.
-   Domain logic belongs in domain agents/services, not inside tools.

------------------------------------------------------------------------

# Tool Design Requirements

Every tool should be class-based.

No simple `@tool` decorators.

Each tool should contain:

-   Pydantic Input model
-   Pydantic Output model
-   Async execution
-   Validation
-   Dependency Injection
-   Thin adapter over domain agent

------------------------------------------------------------------------

# Coding Standards

-   Python 3.12+
-   Async only
-   Type hints everywhere
-   Loguru logging
-   Pydantic models
-   Clean Architecture
-   Service Layer
-   Repository Layer
-   Dependency Injection
-   No giant files
-   No unnecessary abstractions
-   No duplicated business logic

------------------------------------------------------------------------

# Current Status

Completed:

-   Runtime
-   Planner
-   Planner Node
-   Chatbot Node
-   GraphContext
-   GraphState
-   Builder
-   TravelAgent
-   ChatService
-   Structured planner pipeline

Next:

1.  Build class-based domain tools.
2.  Implement HotelAgent / WeatherAgent / AttractionAgent.
3.  Integrate LangGraph ToolNode.
4.  Connect ToolNode back to Chatbot.
5.  Replace mock services with real APIs.
