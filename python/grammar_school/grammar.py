"""Grammar definition system for Grammar School."""

from collections.abc import Callable
from typing import Any, TypeVar

from grammar_school.ast import CallChain
from grammar_school.backend_lark import DEFAULT_GRAMMAR, LarkBackend
from grammar_school.interpreter import Interpreter
from grammar_school.runtime import Action, Runtime

T = TypeVar("T")


def rule(
    grammar: str | None = None,
    **kwargs: str | Any,
) -> Callable[[type[T]], type[T]]:
    """
    Decorator to define grammar rules.

    Supports three forms:
    1. @rule("call_chain: call ('.' call)*")
    2. @rule(call_chain="call ('.' call)*")
    3. @rule(call_chain = sym("call") + many(lit(".") + sym("call")))
    """
    if grammar is not None:

        def decorator_with_grammar(cls: type[T]) -> type[T]:
            if not hasattr(cls, "_grammar_rules"):
                cls._grammar_rules = {}  # type: ignore[attr-defined]
            cls._grammar_rules["_default"] = grammar  # type: ignore[attr-defined]
            return cls

        return decorator_with_grammar

    def decorator_with_kwargs(cls: type[T]) -> type[T]:
        if not hasattr(cls, "_grammar_rules"):
            cls._grammar_rules = {}  # type: ignore[attr-defined]
        for key, value in kwargs.items():
            cls._grammar_rules[key] = value  # type: ignore[attr-defined]
        return cls

    return decorator_with_kwargs


def verb(func: Callable) -> Callable:
    """
    Decorator to mark a method as a semantic handler for a verb.

    Example:
        @verb
        def track(self, name, color=None, _context=None):
            return Action(kind="create_track", payload={...})
    """
    func._is_verb = True  # type: ignore[attr-defined]
    return func


class Grammar:
    """Grammar implementation using Lark backend."""

    def __init__(self, dsl_instance: Any, grammar: str = DEFAULT_GRAMMAR):
        """Initialize grammar with DSL instance and optional grammar string."""
        self.dsl = dsl_instance
        self.backend = LarkBackend(grammar)
        self.interpreter = Interpreter(dsl_instance)

    def parse(self, code: str) -> CallChain:
        """Parse DSL code into a CallChain AST."""
        return self.backend.parse(code)

    def compile(self, code: str) -> list[Action]:
        """Compile DSL code into a list of Actions."""
        call_chain = self.parse(code)
        return self.interpreter.interpret(call_chain)

    def execute(self, code_or_plan: str | list[Action], runtime: Runtime) -> None:
        """Execute DSL code or a plan of actions using the given runtime."""
        plan = self.compile(code_or_plan) if isinstance(code_or_plan, str) else code_or_plan

        for action in plan:
            runtime.execute(action)


def sym(name: str) -> Any:
    """Create a nonterminal symbol."""
    return {"type": "sym", "name": name}


def lit(text: str) -> Any:
    """Create a literal terminal."""
    return {"type": "lit", "text": text}


def many(expr: Any) -> Any:
    """Create a many (zero or more) combinator."""
    return {"type": "many", "expr": expr}


class _Optional:
    """Helper for optional combinators."""

    def __init__(self, expr: Any):
        self.expr = expr

    def optional(self) -> Any:
        """Make an expression optional."""
        return {"type": "optional", "expr": self.expr}


def optional(expr: Any) -> Any:
    """Create an optional combinator."""
    return _Optional(expr).optional()
