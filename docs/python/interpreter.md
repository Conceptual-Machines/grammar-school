# Interpreter

The interpreter converts AST (CallChain) into Actions.

## Overview

The `Interpreter` class walks the `CallChain` AST, coerces `Value` objects to native Python types, dispatches to verb handlers, and collects returned `Action` objects.

## Basic Usage

```python
from grammar_school import Grammar, Interpreter

dsl = MyDSL()
grammar = Grammar(dsl)

# The interpreter is created automatically by Grammar
# But you can access it directly:
interpreter = grammar.interpreter

call_chain = grammar.parse('greet(name="Alice")')
actions = interpreter.interpret(call_chain)
```

## How It Works

1. **Walk the CallChain** - Iterates through each `Call` in the chain
2. **Coerce Values** - Converts `Value` objects to native Python types (str, int, float, bool)
3. **Dispatch to Verbs** - Calls the appropriate verb handler method
4. **Collect Actions** - Gathers all returned `Action` objects

## Value Coercion

The interpreter automatically coerces `Value` objects:

- `Value(kind="string", value="hello")` → `"hello"`
- `Value(kind="number", value=42)` → `42`
- `Value(kind="bool", value=True)` → `True`
- `Value(kind="identifier", value="myVar")` → `"myVar"`

## Verb Handler Return Values

Verb handlers can return:

1. **Single Action**: `return Action(...)`
2. **Action and Context**: `return Action(...), context`
3. **List of Actions**: `return [Action(...), Action(...)]`

## Context Passing

The interpreter maintains context between calls in a chain:

```python
@verb
def track(self, name, _context=None):
    # _context contains the previous action or None
    return Action(...)

@verb
def add_clip(self, start, length, _context=None):
    # _context contains the action from track()
    track_name = _context.payload["name"] if _context else None
    return Action(...)
```
