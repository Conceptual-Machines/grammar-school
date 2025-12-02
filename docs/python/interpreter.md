# Interpreter

The interpreter executes methods directly from the AST.

## Overview

The `Interpreter` class walks the `CallChain` AST, coerces `Value` objects to native Python types, and calls `@method` handlers directly. Methods execute immediately when called.

## Basic Usage

```python
from grammar_school import Grammar, method

class MyDSL(Grammar):
    @method
    def greet(self, name):
        print(f"Hello, {name}!")

dsl = MyDSL()

# The interpreter is created automatically by Grammar
# Methods execute directly when called
dsl.execute('greet(name="Alice")')  # Prints: Hello, Alice!
```

## How It Works

1. **Walk the CallChain** - Iterates through each `Call` in the chain
2. **Coerce Values** - Converts `Value` objects to native Python types (str, int, float, bool)
3. **Dispatch to Methods** - Calls the appropriate `@method` handler
4. **Execute Directly** - Methods run immediately with their implementation

## Value Coercion

The interpreter automatically coerces `Value` objects:

- `Value(kind="string", value="hello")` → `"hello"`
- `Value(kind="number", value=42)` → `42`
- `Value(kind="bool", value=True)` → `True`
- `Value(kind="identifier", value="myVar")` → `"myVar"`

## Method Execution

Methods execute directly - they can do anything:

```python
class MusicDSL(Grammar):
    def __init__(self):
        super().__init__()
        self.tracks = []
        self.current_track = None

    @method
    def track(self, name):
        # Implementation runs directly
        self.current_track = {"name": name, "clips": []}
        self.tracks.append(self.current_track)

    @method
    def add_clip(self, start, length):
        # Access state via self
        if self.current_track:
            self.current_track["clips"].append({
                "start": start,
                "length": length
            })
```

Methods can:
- Perform side effects (print, file I/O, API calls)
- Maintain state via `self` attributes
- Return values (if needed)
- Access previous state from `self`
