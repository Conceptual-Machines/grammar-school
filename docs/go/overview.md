# Go API Overview

The Go implementation of Grammar School uses reflection to automatically discover method handlers.

## Quick Example

```go
package main

import (
    "context"
    "fmt"
    "grammar-school/go/gs"
)

type MyDSL struct{}

func (d *MyDSL) Greet(args gs.Args) error {
    name := args["name"].Str
    fmt.Printf("Hello, %s!\n", name)
    return nil
}

func main() {
    dsl := &MyDSL{}
    parser := &MyParser{} // Implement gs.Parser interface
    engine, _ := gs.NewEngine("", dsl, parser)
    engine.Execute(context.Background(), `greet(name="World")`)
    // Output: Hello, World!
}
```

## Key Components

### Engine

The `Engine` orchestrates parsing, interpretation, and execution:

```go
engine, err := gs.NewEngine(grammar, dsl, parser)
```

### Method Handlers

Method handlers must match this signature:

```go
func (d *MyDSL) MethodName(args gs.Args) error
```

The Engine uses reflection to automatically discover and register methods with this signature.
Methods execute directly when called - no Action return needed.

### Core Types

- `Value` / `ValueKind` - AST value node
- `Arg` - Named argument
- `Call` - Function call
- `CallChain` - Chain of calls
- `Args` - Map of string to Value
- `Parser` - Pluggable parser interface

## See Also

- [API Reference](api-reference.md) - Complete API documentation
- [Core Types](core-types.md) - Detailed type information
- [Engine](engine.md) - Engine usage guide
