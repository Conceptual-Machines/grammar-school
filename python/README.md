# Grammar School - Python Implementation

A lightweight framework for building tiny LLM-friendly DSLs in Python.

## Installation

```bash
pip install grammar-school
```

For development:

```bash
pip install -e ".[dev]"
```

## Quick Start

```python
from grammar_school import Action, Grammar, verb

class MyGrammar(Grammar):
    @verb
    def greet(self, name, _context=None):
        # @verb methods return Actions (data structures)
        # They are pure - no side effects here!
        return Action(kind="greet", payload={"name": name})

# Default runtime prints actions - no Runtime import needed!
grammar = MyGrammar()
grammar.execute('greet(name="World")')

# Or provide a custom runtime for actual behavior
from grammar_school import Runtime

class MyRuntime(Runtime):
    def __init__(self):
        self.greetings = []  # Runtime manages state

    def execute(self, action: Action) -> None:
        # Runtime performs actual side effects
        if action.kind == "greet":
            name = action.payload["name"]
            self.greetings.append(name)
            print(f"Hello, {name}!")

grammar = MyGrammar(runtime=MyRuntime())
grammar.execute('greet(name="World")')
```

## Understanding the Architecture

Grammar School uses a **two-layer architecture**:

1. **Grammar + @verb methods**: Transform DSL syntax → Actions (pure, no side effects)
2. **Runtime**: Execute Actions → Real world effects (side effects, state management)

**Why this separation?**
- Same Grammar works with different Runtimes (testing, production, mocking)
- @verb methods are pure and easily testable
- Runtime handles all state and side effects independently

## Runtime Output

**Default Runtime**: Prints actions to **stdout** (standard output/console)

**Custom Runtimes**: Can output anywhere:
- Files (write to disk)
- Databases (store in SQL/NoSQL)
- APIs (HTTP requests)
- Logging systems
- In-memory structures
- Or any combination

Example custom runtime that writes to a file:
```python
class FileRuntime(Runtime):
    def __init__(self, filename: str):
        self.filename = filename

    def execute(self, action: Action) -> None:
        with open(self.filename, 'a') as f:
            f.write(f"{action.kind}: {action.payload}\n")

grammar = MyGrammar(runtime=FileRuntime("output.log"))
```

## Streaming Actions

For large DSL programs or real-time processing, you can stream actions as they're generated:

```python
grammar = MyGrammar()

# Stream actions one at a time (memory efficient)
for action in grammar.stream('track(name="A").track(name="B").track(name="C")'):
    print(f"Got action: {action.kind}")
    # Process action immediately, don't wait for all actions
    runtime.execute(action)  # Execute as they arrive
```

This is useful for:
- **Large programs**: Don't load all actions into memory at once
- **Real-time processing**: Start executing actions before compilation completes
- **Memory efficiency**: Process actions incrementally

## Functional Programming Support

Grammar School supports functional programming paradigms through the `FunctionalMixin`:

```python
from grammar_school import Grammar, FunctionalMixin, verb, Action

class MyGrammar(Grammar, FunctionalMixin):
    @verb
    def square(self, x, _context=None):
        return Action(kind="square", payload={"value": x * x})

    @verb
    def is_even(self, x, _context=None):
        return Action(kind="is_even", payload={"value": x % 2 == 0})

grammar = MyGrammar()
# Use functional operations with function references
grammar.execute('map(@square, data)')
grammar.execute('filter(@is_even, data)')
grammar.execute('map(@square, data).filter(@is_even, data)')
```

**Available functional operations:**
- `map(@function, data)` - Map a function over data
- `filter(@predicate, data)` - Filter data using a predicate
- `reduce(@function, data, initial)` - Reduce data using a function
- `compose(@f, @g, @h)` - Compose multiple functions
- `pipe(data, @f, @g, @h)` - Pipe data through functions

**Function references:** Use `@function_name` syntax to pass functions as arguments.

## Examples

See the `examples/` directory for complete DSL implementations.

## API Reference

### Core Types

- `Value`: AST value node (number, string, identifier, bool)
- `Arg`: Named argument
- `Call`: Function call with arguments
- `CallChain`: Chain of calls (method chaining)
- `Action`: Runtime action produced by interpreter
- `Runtime`: Protocol for executing actions

### Decorators

- `@verb`: Mark a method as a verb handler
- `@rule`: Define grammar rules (for custom grammars)

### Classes

- `Grammar`: Main grammar class that orchestrates parsing and interpretation
- `Interpreter`: Interprets CallChain AST into Actions
- `LarkBackend`: Lark-based parser backend
