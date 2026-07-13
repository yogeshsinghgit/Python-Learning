from enum import StrEnum


class MessageRole(StrEnum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


class PromptType(StrEnum):
    RAG = "rag"
    CITATION = "citation"
    JSON = "json"
    EVALUATION = "evaluation"
    AGENT = "agent"


class PromptStatus(StrEnum):
    ACTIVE = "active"
    DEPRECATED = "deprecated"