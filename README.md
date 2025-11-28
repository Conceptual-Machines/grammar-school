# 🦉 Grammar School

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Go](https://img.shields.io/badge/Go-1.21+-00ADD8.svg)](https://golang.org/)
[![Documentation](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://conceptual-machines.github.io/grammar-school/)

**🦉 A lightweight framework for building tiny LLM-friendly Domain-Specific Languages (DSLs)**

[Features](#features) • [Quick Start](#quick-start) • [Documentation](https://conceptual-machines.github.io/grammar-school/) • [Examples](#examples)

</div>

## 🦉 What is Grammar School?

Grammar School is a multi-language framework designed to help you quickly build **tiny, LLM-friendly DSLs** (Domain-Specific Languages). It provides a simple, consistent API across Python and Go that lets you:

- ⚡ **Define DSLs in minutes** - Just subclass `Grammar` and add `@verb` methods
- 🔍 **Parse and interpret** - Built-in parser backends (Lark for Python, pluggable for Go)
- 🛡️ **Execute safely** - Two-layer architecture separates DSL logic from side effects
- 🤖 **Integrate with LLMs** - Use your grammar as CFG constraints for GPT-5 and other LLMs
- 🎯 **Functional programming** - Built-in support for `map`, `filter`, `reduce`, `compose`, and `pipe`

Perfect for building:
- 🛠️ **LLM tool interfaces** - Define structured commands that LLMs can generate
- 📝 **Configuration DSLs** - Human-readable configuration languages
- ⚙️ **Workflow engines** - Chain operations with method chaining
- 🎨 **Domain-specific commands** - Music, graphics, data processing, etc.

## ✨ Features

- 🚀 **Simple API** - Define DSLs with just a few `@verb` methods
- 🔄 **Method Chaining** - Natural syntax: `track(name="A").add_clip(start=0)`
- 🎯 **LLM-Friendly** - Use grammars as CFG constraints for GPT-5 and other LLMs
- 🔧 **Functional Programming** - Built-in `map`, `filter`, `reduce`, `compose`, `pipe`
- 🌐 **Multi-Language** - Consistent API across Python and Go
- 🧪 **Well-Tested** - Comprehensive test suite with 80%+ coverage
- 📚 **Well-Documented** - Full API docs and examples

## 🚀 Quick Start

### 🐍 Python

```bash
pip install grammar-school
```

```python
from grammar_school import Grammar, verb, Action

class MyGrammar(Grammar):
    @verb
    def greet(self, name, _context=None):
        return Action(kind="greet", payload={"name": name})

grammar = MyGrammar()
grammar.execute('greet(name="World")')
```

### 🐹 Go

```bash
go get grammar-school/go/gs
```

```go
type MyDSL struct{}

func (d *MyDSL) Greet(args gs.Args, ctx *gs.Context) ([]gs.Action, *gs.Context, error) {
    name := args["name"].Str
    return []gs.Action{{
        Kind: "greet",
        Payload: map[string]interface{}{"name": name},
    }}, ctx, nil
}
```

## 📖 Documentation

📚 **[Full Documentation](https://conceptual-machines.github.io/grammar-school/)** - Complete API reference, guides, and examples

- 🐍 [Python API Reference](https://conceptual-machines.github.io/grammar-school/python/)
- 🐹 [Go API Reference](https://conceptual-machines.github.io/grammar-school/go/)
- 💡 [Examples](https://conceptual-machines.github.io/grammar-school/examples/)
- 🤝 [Contributing Guide](https://conceptual-machines.github.io/grammar-school/contributing/)

## 💡 Examples

See the `python/examples/` and `go/examples/` directories for complete DSL implementations:

- 🎵 **Music DSL** - Create tracks and clips with method chaining
- 🤖 **GPT-5 Integration** - Use Grammar School with OpenAI's GPT-5 using CFG constraints
- 🔧 **Functional DSL** - Demonstrate functional programming patterns with `map`, `filter`, `reduce`

## 🧠 Core Concepts

All implementations follow the same conceptual design:

1. 📝 **DSL Program**: Plain string input (typically LLM-generated)
2. 🌳 **AST**: Abstract Syntax Tree (CallChain → Call → Arg → Value)
3. ⚡ **Actions**: Semantic evaluation output (runtime instructions)
4. 🔄 **Pipeline**: Parse → Interpret → Execute

See [SPEC.md](./SPEC.md) for the complete specification.

## 📁 Repository Structure

```
grammar-school/
  README.md          # This file
  SPEC.md            # Shared conceptual specification

  python/            # 🐍 Python implementation
    grammar_school/
    examples/

  go/                # 🐹 Go implementation
    gs/
    examples/

  docs/              # 📚 Additional documentation
```

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.
