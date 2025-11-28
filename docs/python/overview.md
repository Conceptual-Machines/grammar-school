# Python API Overview

The Python implementation of Grammar School provides a clean, decorator-based API for building DSLs.

## Quick Example

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

## Key Components

### Grammar

The `Grammar` class orchestrates parsing and interpretation:

```python
grammar = Grammar(dsl_instance, grammar=optional_custom_grammar)
```

### Decorators

- `@verb` - Marks a method as a verb handler
- `@rule` - Defines custom grammar rules (advanced)

### Core Types

- `Value` - AST value node
- `Arg` - Named argument
- `Call` - Function call
- `CallChain` - Chain of calls
- `Action` - Runtime action
- `Runtime` - Protocol for executing actions

## See Also

- [API Reference](api-reference.md) - Complete API documentation
- [Core Types](core-types.md) - Detailed type information
- [Grammar](grammar.md) - Grammar definition guide

