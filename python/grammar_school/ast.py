"""AST types for Grammar School."""

from dataclasses import dataclass
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
    """A chain of calls connected by dots (method chaining)."""

    calls: list[Call]

