# Grammar School - Go Implementation

A lightweight framework for building tiny LLM-friendly DSLs in Go.

## Installation

```bash
go mod init grammar-school
go get .
```

## Quick Start

```go
package main

import (
    "context"
    "grammar-school/go/gs"
)

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

func main() {
    dsl := &MyDSL{}
    parser := &MyParser{} // Implement gs.Parser interface
    engine, _ := gs.NewEngine("", dsl, parser)
    runtime := &MyRuntime{}
    
    plan, _ := engine.Compile(`greet(name="World")`)
    engine.Execute(context.Background(), runtime, plan)
}
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
- `Context`: Execution context passed between verb handlers
- `Args`: Map of string to Value for verb handler arguments

### Interfaces

- `Parser`: Pluggable parser interface (implement with participle, pigeon, etc.)
- `Runtime`: Interface for executing actions
- `VerbHandler`: Function signature for verb handlers

### Engine

- `NewEngine`: Create a new engine with grammar, DSL instance, and parser
- `Compile`: Parse and interpret DSL code into Actions
- `Execute`: Execute a plan of actions using a Runtime

## Parser Backends

The `Parser` interface allows you to use any parser library:

- [participle](https://github.com/alecthomas/participle) - PEG parser
- [pigeon](https://github.com/mna/pigeon) - PEG parser generator
- Custom PEG/EBNF parsers

