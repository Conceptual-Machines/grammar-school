# Grammar School

*A multi-language framework for building tiny LLM-friendly DSLs*

Grammar School is a lightweight, multi-language framework for creating small, precise, LLM-friendly domain-specific languages (DSLs). It provides a simple way to define grammar rules, map DSL methods to implementations, and execute DSL programs through a clean **parser → AST → interpreter → execute** pipeline.

## Features

- 🎯 **Simple Grammar Definition** - Define grammars via strings or structured combinators
- 🔗 **Method Mapping** - Map DSL methods to implementations with decorators/annotations
- 🔄 **Complete Pipeline** - Parse → Interpret → Execute workflow
- 🌍 **Multi-Language** - Independent implementations in Python and Go
- 🤖 **LLM-Friendly** - Designed for LLM-generated DSL code
- 📦 **Lightweight** - Minimal dependencies, focused API
- 🔧 **OpenAI CFG Integration** - Built-in utilities for GPT-5 Context-Free Grammar constraints

## Quick Example

=== "Python"

    ```python
    from grammar_school import Grammar, method

    class MyDSL(Grammar):
        @method
        def greet(self, name):
            print(f"Hello, {name}!")

    dsl = MyDSL()
    dsl.execute('greet(name="World")')
    # Output: Hello, World!
    ```

=== "Go"

    ```go
    type MyDSL struct{}

    func (d *MyDSL) Greet(args gs.Args, ctx *gs.Context) ([]gs.Action, *gs.Context, error) {
        name := args["name"].Str
        action := gs.Action{
            Kind: "greet",
            Payload: map[string]interface{}{
                "name": name,
            },
        }
        return []gs.Action{action}, ctx, nil
    }

    type MyRuntime struct{}

    func (r *MyRuntime) ExecuteAction(ctx context.Context, a gs.Action) error {
        fmt.Printf("Hello, %v!\n", a.Payload["name"])
        return nil
    }

    dsl := &MyDSL{}
    engine, _ := gs.NewEngine("", dsl, parser)
    runtime := &MyRuntime{}
    plan, _ := engine.Compile(`greet(name="World")`)
    engine.Execute(context.Background(), runtime, plan)
    // Output: Hello, World!
    ```

## Architecture

```
DSL Code (string)
   ↓
Parse → CallChain (AST)
   ↓
Interpret → Execute methods directly
```

All implementations follow the same conceptual design, ensuring consistency across languages while remaining independent.

## Installation

=== "Python"

    ```bash
    pip install grammar-school
    ```

=== "Go"

    ```bash
    cd go
    go mod download
    ```

## Documentation

- [Getting Started](getting-started/quick-start.md) - Quick start guide
- [Python API](python/overview.md) - Python implementation documentation
- [Go API](go/overview.md) - Go implementation documentation
- [Examples](examples/music-dsl.md) - Example DSLs and use cases
- [Specification](specification.md) - Complete framework specification

## License

MIT License - see [LICENSE](../LICENSE) file for details.
