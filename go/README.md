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
    "fmt"
    "grammar-school/go/gs"
)

type MyDSL struct{}

// Methods execute directly - no Action return needed
func (d *MyDSL) Greet(args gs.Args) error {
    name := args["name"].Str
    fmt.Printf("Hello, %s!\n", name)
    return nil
}

func main() {
    dsl := &MyDSL{}
    parser := &MyParser{} // Implement gs.Parser interface

    // No runtime needed - methods execute directly
    engine, _ := gs.NewEngine("", dsl, parser)

    // Execute DSL code - methods run directly
    engine.Execute(context.Background(), `greet(name="World")`)
    // Output: Hello, World!
}
```

## Understanding the Architecture

Grammar School provides a **unified interface**:

1. **Methods execute directly** - Methods contain their implementation
2. **Framework handles the rest** - Parsing, interpretation, and execution happen automatically

**Benefits:**
- Simple and intuitive - just write methods with your logic
- No need to separate concerns - methods can do anything
- State management via struct fields
- The Grammar/Runtime split is handled internally but hidden from you

## Streaming Execution

For large DSL programs or real-time processing, you can stream method executions:

```go
engine, _ := gs.NewEngine("", dsl, parser)

// Stream method executions one at a time (memory efficient)
errors := engine.Stream(context.Background(), `greet(name="A").greet(name="B").greet(name="C")`)
for err := range errors {
    if err != nil {
        log.Fatal(err)
    }
    // Methods execute as they're called
}
```

This is useful for:
- **Large programs**: Don't load all method calls into memory at once
- **Real-time processing**: Start executing methods before parsing completes
- **Memory efficiency**: Process methods incrementally

## Functional Programming Support

Grammar School allows you to implement functional programming patterns by defining your own methods:

```go
type MyDSL struct {
}

func (d *MyDSL) Square(args gs.Args) error {
    x := args["x"].Num
    fmt.Printf("Square: %v\n", x*x)
    return nil
}

func (d *MyDSL) Map(args gs.Args) error {
    // Implement your own map logic
    funcRef := args["_positional_0"]
    data := args["_positional_1"]
    // ... your implementation
    return nil
}

func (d *MyDSL) Filter(args gs.Args) error {
    // Implement your own filter logic
    predicate := args["_positional_0"]
    data := args["_positional_1"]
    // ... your implementation
    return nil
}

// Use functional operations - you provide the implementation
// map(@Square, data)
// filter(@IsEven, data)
// map(@Square, data).filter(@IsEven, data)
```

**Function references:** Use `@function_name` syntax to pass functions as arguments. The parser must support parsing `@IDENTIFIER` as a `ValueFunction` kind.

## Examples

See the `examples/` directory for complete DSL implementations.

## API Reference

### Core Types

- `Value`: AST value node (number, string, identifier, bool, function)
- `Arg`: Named argument
- `Call`: Function call with arguments
- `CallChain`: Chain of calls (method chaining)
- `Args`: Map of string to Value for method arguments

### Interfaces

- `Parser`: Pluggable parser interface (implement with participle, pigeon, etc.)
- `MethodHandler`: Function signature for method handlers

### Functional Programming

Implement your own functional methods (`map`, `filter`, `reduce`, etc.) as regular `@method` handlers. The framework doesn't provide these - you implement them for your specific domain.

### Engine

- `NewEngine`: Create a new engine with grammar, DSL instance, and parser
- `Execute`: Parse and execute DSL code - methods run directly
- `Stream`: Stream method executions for large programs

## Parser Backends

The `Parser` interface allows you to use any parser library:

- [participle](https://github.com/alecthomas/participle) - PEG parser
- [pigeon](https://github.com/mna/pigeon) - PEG parser generator
- Custom PEG/EBNF parsers
