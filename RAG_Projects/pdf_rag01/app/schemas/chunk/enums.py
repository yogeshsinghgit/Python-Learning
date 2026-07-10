"""
Chunk related enums.
"""

from enum import StrEnum


class ChunkType(StrEnum):
    """
    Logical type of a chunk.
    """

    CONTENT = "content"

    SUMMARY = "summary"

    PARENT = "parent"

    CHILD = "child"

    QUESTION = "question"

    KEYWORD = "keyword"