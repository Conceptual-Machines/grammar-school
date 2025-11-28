# Python Examples

## Music DSL

A simple example DSL for creating music tracks and clips.

```bash
cd python
pip install -e .
python examples/music_dsl.py
```

The example demonstrates:
- Defining verbs with the `@verb` decorator
- Creating a Grammar instance
- Executing DSL code that chains method calls
- Using a Runtime to execute actions

## GPT-5 Integration

An example showing how to integrate Grammar School with GPT-5 using Context-Free Grammar (CFG) constraints.

```bash
cd python
pip install -e . openai
export OPENAI_API_KEY=your-api-key
python examples/gpt_integration.py
```

The example demonstrates:
- Using Grammar School's grammar as a CFG for GPT-5 custom tools
- Ensuring GPT-5 generates only valid DSL code
- Executing GPT-5-generated code with Grammar School
- Building LLM-friendly DSLs with type safety

See `gpt_integration_readme.md` for detailed documentation.

## Functional DSL

An example demonstrating functional programming patterns using the `FunctionalMixin`:

```bash
cd python
pip install -e .
python examples/functional_dsl.py
```

The example demonstrates:
- **Function references**: Using `@function_name` syntax to pass functions as arguments
- **Higher-order functions**: `map`, `filter`, `reduce` operations
- **Function composition**: `compose` and `pipe` for chaining transformations
- **Mixin pattern**: Inheriting from `FunctionalMixin` to get functional operations

```python
from grammar_school import Grammar, FunctionalMixin, verb, Action

class MyGrammar(Grammar, FunctionalMixin):
    @verb
    def square(self, x, _context=None):
        return Action(kind="square", payload={"value": x * x})

grammar = MyGrammar()
grammar.execute('map(@square, data)')
grammar.execute('filter(@is_even, data)')
grammar.execute('map(@square, data).filter(@is_even, data)')
```
