# Python Examples

## Music DSL

A simple example DSL for creating music tracks and clips.

```bash
pip install grammar-school
python examples/music_dsl.py
```

The example demonstrates:
- Defining methods with the `@method` decorator
- Creating a Grammar instance
- Executing DSL code that chains method calls
- Methods execute directly with their implementation

## GPT-5 Integration

An example showing how to integrate Grammar School with GPT-5 using Context-Free Grammar (CFG) constraints.

```bash
pip install grammar-school openai
export OPENAI_API_KEY=your-api-key
python examples/gpt_integration.py
```

The example demonstrates:
- Using Grammar School's grammar as a CFG for GPT-5 custom tools
- Ensuring GPT-5 generates only valid DSL code
- Executing GPT-5-generated code with Grammar School
- Building LLM-friendly DSLs with type safety

See `gpt_integration_readme.md` for detailed documentation.

## Grammar Builder

Examples showing how to define grammars programmatically or via config files.

```bash
pip install grammar-school
python examples/grammar_builder_example.py
python examples/grammar_config_example.py
```

The examples demonstrate:
- **Programmatic grammar definition**: Build grammars using the `GrammarBuilder` API
- **Config-based grammars**: Define grammars in YAML/TOML files
- **Method chaining**: Fluent API for building grammars
- **Human-readable**: Automatic comments and descriptions

```python
from grammar_school import GrammarBuilder

builder = GrammarBuilder()
builder.rule("start", "call_chain", "Entry point")
builder.rule("call_chain", "call (DOT call)*", "Chain of calls")
builder.terminal("DOT", ".", "Dot separator")
grammar = MyGrammar(grammar=builder.build())
```

## Functional DSL

Users implement their own functional methods (map, filter, reduce, etc.) as regular `@method` handlers. The framework doesn't provide these - you implement them for your specific domain needs.

```python
from grammar_school import Grammar, method

class MyGrammar(Grammar):
    @method
    def square(self, x):
        return x * x

    @method
    def map(self, func, data):
        # Your implementation
        return [func(x) for x in data]

    @method
    def filter(self, predicate, data):
        # Your implementation
        return [x for x in data if predicate(x)]

grammar = MyGrammar()
grammar.execute('map(@square, data)')
grammar.execute('filter(@is_even, data)')
```
