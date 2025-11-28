"""Runtime types for Grammar School."""

from dataclasses import dataclass
from typing import Any, Protocol


@dataclass
class Action:
    """A runtime action produced by the interpreter."""

    kind: str
    payload: dict[str, Any]


class Runtime(Protocol):
    """Protocol for runtime implementations that execute actions."""

    def execute(self, action: Action) -> None:
        """Execute a single action."""
        ...
