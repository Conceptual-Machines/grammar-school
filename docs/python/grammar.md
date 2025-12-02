# Grammar Definition

Guide to defining grammars in Grammar School Python.

## Default Grammar

Grammar School provides a default grammar that supports:

- Function calls: `greet(name="Alice")`
- Method chaining: `track().add_clip()`
- Named arguments: `func(name="value", count=2)`
- Positional arguments: `func("value", 2)`
- Various value types: numbers, strings, identifiers, booleans

## Using the Default Grammar

```python
from grammar_school import Grammar, method

class MyDSL(Grammar):
    @method
    def greet(self, name):
        print(f"Hello, {name}!")

dsl = MyDSL()  # Uses default grammar
```

## Custom Grammar

You can provide a custom grammar string:

```python
custom_grammar = """
start: call_chain

call_chain: call ('.' call)*
call: IDENTIFIER "(" args? ")"
args: arg (',' arg)*
arg: IDENTIFIER "=" value | value
value: NUMBER | STRING | IDENTIFIER | BOOL

IDENTIFIER: /[a-zA-Z_][a-zA-Z0-9_]*/
NUMBER: /-?\\d+(\\.\\d+)?/
STRING: /"([^"\\\\]|\\\\.)*"|'([^'\\\\]|\\\\.)*'/
BOOL: "true" | "false"
"""

class MyDSL(Grammar):
    @method
    def greet(self, name):
        print(f"Hello, {name}!")

dsl = MyDSL(grammar=custom_grammar)
```

## Grammar Rules with @rule Decorator

For advanced use cases, you can use the `@rule` decorator:

```python
from grammar_school import rule

@rule("call_chain: call ('.' call)*")
class MyDSL(Grammar):
    @method
    def greet(self, name):
        print(f"Hello, {name}!")
```

## Grammar Syntax

Grammar School uses [Lark](https://github.com/lark-parser/lark) for parsing, which supports:

- EBNF-style rules
- Regular expressions for terminals
- Operator precedence
- Ambiguity resolution

See the [Lark documentation](https://lark-parser.readthedocs.io/) for complete grammar syntax.
