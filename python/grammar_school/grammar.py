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
    """
    Main Grammar class for Grammar School.

    Subclass this and define @verb methods to create your DSL handlers.
    Then use parse(), compile(), or execute() to process DSL scripts.

    **The Two-Layer Architecture:**

    1. **@verb methods** (in Grammar subclass):
       - Transform DSL syntax into Action data structures
       - Pure functions - no side effects, just return Actions
       - Example: `track(name="Drums")` → `Action(kind="create_track", payload={...})`

    2. **Runtime** (separate class):
       - Takes Actions and performs actual side effects
       - Handles state management, I/O, database operations, etc.
       - Example: Receives `Action(kind="create_track", ...)` → creates actual track in system

    This separation allows:
    - Same Grammar to work with different Runtimes (testing vs production)
    - @verb methods to be testable without side effects
    - Runtime to manage state independently of Grammar logic

    Example:
        ```python
        from grammar_school import Grammar, verb, Action

        class MyGrammar(Grammar):
            @verb
            def greet(self, name, _context=None):
                # Pure function - just returns Action, no side effects
                return Action(kind="greet", payload={"name": name})

        # Default runtime prints actions - no need to import Runtime!
        grammar = MyGrammar()
        grammar.execute('greet(name="World")')

        # Or provide a custom runtime for actual behavior
        from grammar_school import Runtime

        class MyRuntime(Runtime):
            def __init__(self):
                self.greetings = []  # Runtime manages state

            def execute(self, action: Action) -> None:
                # This is where side effects happen
                if action.kind == "greet":
                    name = action.payload["name"]
                    self.greetings.append(name)
                    print(f"Hello, {name}!")

        grammar = MyGrammar(runtime=MyRuntime())
        grammar.execute('greet(name="World")')
        ```
    """

    def __init__(self, runtime: Runtime | None = None, grammar: str = DEFAULT_GRAMMAR):
        """
        Initialize grammar with runtime and optional custom grammar string.

        Args:
            runtime: Runtime instance that executes actions (optional, defaults to printing actions)
            grammar: Optional custom grammar string (defaults to Grammar School's default)
        """
        self.runtime = runtime if runtime is not None else _DefaultRuntime()
        self.backend = LarkBackend(grammar)
        self.interpreter = Interpreter(self)

    def parse(self, code: str) -> CallChain:
        """Parse DSL code into a CallChain AST."""
        return self.backend.parse(code)

    def compile(self, code: str) -> list[Action]:
        """Compile DSL code into a list of Actions."""
        call_chain = self.parse(code)
        return self.interpreter.interpret(call_chain)

    def stream(self, code: str):
        """
        Stream Actions as they're generated from DSL code.

        This is a generator that yields actions one at a time, allowing
        for memory-efficient processing and real-time execution of large DSL programs.

        Args:
            code: DSL code string to compile and stream

        Yields:
            Action: Actions as they're generated from verb handlers

        Example:
            ```python
            grammar = MyGrammar()
            for action in grammar.stream('track(name="A").track(name="B").track(name="C")'):
                print(f"Got action: {action.kind}")
                # Process action immediately, don't wait for all actions
            ```
        """
        call_chain = self.parse(code)
        yield from self.interpreter.interpret_stream(call_chain)

    def execute(self, code_or_plan: str | list[Action], runtime: Runtime | None = None) -> None:
        """
        Execute DSL code or a plan of actions using the runtime.

        Args:
            code_or_plan: DSL code string or list of Actions to execute
            runtime: Optional runtime instance (uses instance runtime if not provided)

        Raises:
            ValueError: If no runtime is available (neither instance nor parameter)
        """
        if runtime is None:
            runtime = self.runtime

        if runtime is None:
            raise ValueError("No runtime provided. Either pass runtime to __init__ or to execute()")

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


class _DefaultRuntime(Runtime):
    """
    Default runtime that prints actions to stdout.

    This is used when no runtime is provided to Grammar.__init__().
    Output goes to standard output (stdout) - typically the console/terminal.

    For custom output destinations (files, databases, APIs, etc.),
    create a custom Runtime implementation.
    """

    def execute(self, action: Action) -> None:
        """Print action to stdout (standard output/console)."""
        print(f"Action: {action.kind} with payload: {action.payload}")
