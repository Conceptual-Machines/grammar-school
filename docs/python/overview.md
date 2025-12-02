# Python API Overview

The Python implementation of Grammar School provides a clean, decorator-based API for building DSLs.

## Quick Example

```python
from grammar_school import Grammar, method

class MyDSL(Grammar):
    @method
    def greet(self, name):
        print(f"Hello, {name}!")

dsl = MyDSL()
dsl.execute('greet(name="World")')
```

## Key Components

### Grammar

The `Grammar` class orchestrates parsing and interpretation:

```python
class MyDSL(Grammar):
    @method
    def greet(self, name):
        print(f"Hello, {name}!")

dsl = MyDSL()
dsl.execute('greet(name="World")')
```

### Decorators

- `@method` - Marks a method as a DSL handler (contains implementation)
- `@rule` - Defines custom grammar rules (advanced)

### Core Types

- `Value` - AST value node
- `Arg` - Named argument
- `Call` - Function call
- `CallChain` - Chain of calls

## See Also

- [API Reference](api-reference.md) - Complete API documentation
- [Core Types](core-types.md) - Detailed type information
- [Grammar](grammar.md) - Grammar definition guide
