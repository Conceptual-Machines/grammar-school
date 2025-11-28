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

// Verb handlers transform DSL syntax → Actions (pure, no side effects)
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

// Runtime executes Actions → Real world effects (side effects, state management)
func (r *MyRuntime) ExecuteAction(ctx context.Context, a gs.Action) error {
    fmt.Printf("Hello, %v!\n", a.Payload["name"])
    return nil
}

func main() {
    dsl := &MyDSL{}
    parser := &MyParser{} // Implement gs.Parser interface

    // Runtime is stored in Engine (aligned with Python)
    // Pass nil to use default runtime that prints actions
    engine, _ := gs.NewEngine("", dsl, parser, &MyRuntime{})

    plan, _ := engine.Compile(`greet(name="World")`)
    // Runtime is stored in engine, so Execute doesn't need it
    engine.Execute(context.Background(), plan)

    // Or override with a different runtime for this call:
    // engine.Execute(context.Background(), plan, &OtherRuntime{})
}
```

## Understanding the Architecture

Grammar School uses a **two-layer architecture** (aligned with Python):

1. **Verb handlers (methods on DSL struct)**: Transform DSL syntax → Actions (pure, no side effects)
2. **Runtime**: Execute Actions → Real world effects (side effects, state management)

**Why this separation?**
- Same Engine works with different Runtimes (testing, production, mocking)
- Verb handlers are pure and easily testable
- Runtime handles all state and side effects independently

## Runtime Output

**Default Runtime**: Prints actions to **stdout** (standard output/console)

**Custom Runtimes**: Can output anywhere:
- Files (write to disk)
- Databases (store in SQL/NoSQL)
- APIs (HTTP requests)
- Logging systems
- In-memory structures
- Or any combination

Example custom runtime that writes to a file:
```go
type FileRuntime struct {
    filename string
}

func (r *FileRuntime) ExecuteAction(ctx context.Context, a gs.Action) error {
    f, err := os.OpenFile(r.filename, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
    if err != nil {
        return err
    }
    defer f.Close()
    _, err = fmt.Fprintf(f, "%s: %v\n", a.Kind, a.Payload)
    return err
}

engine, _ := gs.NewEngine("", dsl, parser, &FileRuntime{filename: "output.log"})
```

## Streaming Actions

For large DSL programs or real-time processing, you can stream actions as they're generated:

```go
engine, _ := gs.NewEngine("", dsl, parser, runtime)

// Stream actions one at a time (memory efficient)
actions, errors := engine.Stream(`track(name="A").track(name="B").track(name="C")`)
for {
    select {
    case action, ok := <-actions:
        if !ok {
            return // Channel closed
        }
        fmt.Printf("Got action: %s\n", action.Kind)
        // Process action immediately, don't wait for all actions
        runtime.ExecuteAction(context.Background(), action)
    case err := <-errors:
        if err != nil {
            log.Fatal(err)
        }
    }
}
```

This is useful for:
- **Large programs**: Don't load all actions into memory at once
- **Real-time processing**: Start executing actions before compilation completes
- **Memory efficiency**: Process actions incrementally

## Functional Programming Support

Grammar School supports functional programming paradigms through the `FunctionalMixin`:

```go
type MyDSL struct {
    gs.FunctionalMixin
}

func (d *MyDSL) Square(args gs.Args, ctx *gs.Context) ([]gs.Action, *gs.Context, error) {
    x := args["x"].Num
    return []gs.Action{{
        Kind: "square",
        Payload: map[string]interface{}{"value": x * x},
    }}, ctx, nil
}

// Use functional operations with function references
// map(@Square, data)
// filter(@IsEven, data)
// map(@Square, data).filter(@IsEven, data)
```

**Available functional operations:**
- `map(@function, data)` - Map a function over data
- `filter(@predicate, data)` - Filter data using a predicate
- `reduce(@function, data, initial)` - Reduce data using a function
- `compose(@f, @g, @h)` - Compose multiple functions
- `pipe(data, @f, @g, @h)` - Pipe data through functions

**Function references:** Use `@function_name` syntax to pass functions as arguments. The parser must support parsing `@IDENTIFIER` as a `ValueFunction` kind.

## Examples

See the `examples/` directory for complete DSL implementations.

## API Reference

### Core Types

- `Value`: AST value node (number, string, identifier, bool, function)
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

### Functional Programming

- `FunctionalMixin`: Embed this struct in your DSL to get `map`, `filter`, `reduce`, `compose`, and `pipe` operations

### Engine

- `NewEngine`: Create a new engine with grammar, DSL instance, and parser
- `Compile`: Parse and interpret DSL code into Actions
- `Execute`: Execute a plan of actions using a Runtime

## Parser Backends

The `Parser` interface allows you to use any parser library:

- [participle](https://github.com/alecthomas/participle) - PEG parser
- [pigeon](https://github.com/mna/pigeon) - PEG parser generator
- Custom PEG/EBNF parsers
