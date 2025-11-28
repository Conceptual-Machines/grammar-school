# Grammar School - Python Implementation

A lightweight framework for building tiny LLM-friendly DSLs in Python.

## Installation

```bash
pip install -e .
```

## Quick Start

```python
from grammar_school import Action, Grammar, Runtime, verb

class MyDSL:
    @verb
    def greet(self, name, _context=None):
        return Action(kind="greet", payload={"name": name})

class MyRuntime(Runtime):
    def execute(self, action: Action) -> None:
        print(f"Hello, {action.payload['name']}!")

dsl = MyDSL()
grammar = Grammar(dsl)
runtime = MyRuntime()

grammar.execute('greet(name="World")', runtime)
```

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
