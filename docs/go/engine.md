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

## Compiling DSL Code

The `Compile` method parses and interprets DSL code into Actions:

```go
plan, err := engine.Compile(`greet(name="World")`)
if err != nil {
    log.Fatal(err)
}
```

## Executing Actions

The `Execute` method runs a plan of actions using a Runtime:

```go
runtime := &MyRuntime{}
err := engine.Execute(context.Background(), runtime, plan)
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

## Verb Discovery

The Engine uses reflection to automatically discover verb handlers. A method is considered a verb handler if it matches this signature:

```go
func (d *MyDSL) VerbName(args gs.Args, ctx *gs.Context) ([]gs.Action, *gs.Context, error)
```

The Engine will automatically register all methods with this signature.

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

