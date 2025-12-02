# Engine

The Engine orchestrates parsing, interpretation, and execution in the Go implementation.

## Overview

The `Engine` is the main entry point for Grammar School in Go. It manages the parser, verb handlers, and execution flow.

## Creating an Engine

```go
dsl := &MyDSL{}
parser := &MyParser{}  // You need to implement Parser interface
engine, err := gs.NewEngine("", dsl, parser)
if err != nil {
    log.Fatal(err)
}
```

## Executing DSL Code

The `Execute` method parses and executes DSL code by calling methods directly:

```go
err := engine.Execute(context.Background(), `greet(name="World")`)
if err != nil {
    log.Fatal(err)
}
```

## Complete Example

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

## Method Discovery

The Engine uses reflection to automatically discover method handlers. A method is considered a handler if it matches this signature:

```go
func (d *MyDSL) MethodName(args gs.Args) error
```

The Engine will automatically register all methods with this signature.
Methods execute directly when called - no Action return needed.

## Custom Grammar

You can provide a custom grammar string:

```go
customGrammar := `
start: call_chain
call_chain: call ('.' call)*
// ... more rules
`
engine, err := gs.NewEngine(customGrammar, dsl, parser)
```
