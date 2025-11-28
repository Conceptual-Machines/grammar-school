# Go API Overview

The Go implementation of Grammar School uses reflection to automatically discover verb handlers.

## Quick Example

```go
package main

import (
    "context"
    "fmt"
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
    // Note: Requires a Parser implementation
    // engine, _ := gs.NewEngine("", dsl, parser)
    // runtime := &MyRuntime{}
    // plan, _ := engine.Compile(`greet(name="World")`)
    // engine.Execute(context.Background(), runtime, plan)
}
```

## Key Components

### Engine

The `Engine` orchestrates parsing, interpretation, and execution:

```go
engine, err := gs.NewEngine(grammar, dsl, parser)
```

### Verb Handlers

Verb handlers must match this signature:

```go
func (d *MyDSL) VerbName(args gs.Args, ctx *gs.Context) ([]gs.Action, *gs.Context, error)
```

The Engine uses reflection to automatically discover and register methods with this signature.

### Core Types

- `Value` / `ValueKind` - AST value node
- `Arg` - Named argument
- `Call` - Function call
- `CallChain` - Chain of calls
- `Action` - Runtime action
- `Context` - Execution context
- `Args` - Map of string to Value
- `Runtime` - Interface for executing actions
- `Parser` - Pluggable parser interface

## See Also

- [API Reference](api-reference.md) - Complete API documentation
- [Core Types](core-types.md) - Detailed type information
- [Engine](engine.md) - Engine usage guide

