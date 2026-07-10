"""
Utility functions for text normalization.

These functions are intentionally stateless so they can be reused by:
- Document preprocessing
- Chunkers
- Query preprocessing
"""

from __future__ import annotations

import re


class TextNormalizer:
    """Utility class for common text normalization operations."""

    _MULTIPLE_SPACES = re.compile(r"[ \t]+")
    _MULTIPLE_NEWLINES = re.compile(r"\n{3,}")

    @classmethod
    def normalize(cls, text: str) -> str:
        """
        Normalize whitespace while preserving paragraph boundaries.
        """

        if not text:
            return ""

        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")

        # Collapse repeated spaces/tabs.
        text = cls._MULTIPLE_SPACES.sub(" ", text)

        # Allow at most two consecutive newlines.
        text = cls._MULTIPLE_NEWLINES.sub("\n\n", text)

        return text.strip()