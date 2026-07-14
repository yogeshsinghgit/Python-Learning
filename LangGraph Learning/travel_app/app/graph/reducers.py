from typing import Any


# def append_lists(current: list[Any], new: list[Any]) -> list[Any]:
#     """
#     Merge two lists returned by parallel nodes.
#     """

#     if current is None:
#         current = []

#     if new is None:
#         new = []

#     return current + new

# prod one
from collections.abc import Sequence
from typing import TypeVar

T = TypeVar("T")


def append_lists(
    current: Sequence[T] | None,
    new: Sequence[T] | None,
) -> list[T]:
    current = list(current or [])
    new = list(new or [])
    return current + new