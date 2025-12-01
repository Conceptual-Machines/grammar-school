"""AST types for Grammar School."""

from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Value:
    """A value in the AST (number, string, identifier, etc.)."""

    kind: str
    value: Any


@dataclass
class Arg:
    """A named argument to a call."""

    name: str
    value: Value


@dataclass
class Call:
    """A single function call with named arguments."""

    name: str
    args: dict[str, Value]


@dataclass
class CallChain:
    """
    A chain of calls connected by dots (method chaining).

    Can be initialized with a list, iterator, or any iterable of Call objects.
    """

    calls: list[Call] = field(default_factory=list)

    def __init__(self, calls: list[Call] | Iterator[Call] | Iterable[Call] | None = None):
        """
        Initialize CallChain with calls.

        Args:
            calls: List, iterator, or iterable of Call objects. If None, creates empty chain.
        """
        if calls is None:
            object.__setattr__(self, "calls", [])
        elif isinstance(calls, list):
            object.__setattr__(self, "calls", calls)
        else:
            # Convert iterator/iterable to list
            object.__setattr__(self, "calls", list(calls))

    def __iter__(self) -> Iterator[Call]:
        """Make CallChain iterable."""
        return iter(self.calls)
