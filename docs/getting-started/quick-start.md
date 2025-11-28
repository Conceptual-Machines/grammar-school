# Quick Start

Get up and running with Grammar School in minutes.

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

## Your First DSL

Let's create a simple greeting DSL that demonstrates the core concepts.

=== "Python"

    ```python
    from grammar_school import Action, Grammar, Runtime, verb

    class GreetingDSL:
        @verb
        def greet(self, name, message="Hello", _context=None):
            return Action(
                kind="greet",
                payload={"name": name, "message": message}
            )

    class GreetingRuntime(Runtime):
        def execute(self, action: Action) -> None:
            msg = action.payload["message"]
            name = action.payload["name"]
            print(f"{msg}, {name}!")

    # Use the DSL
    dsl = GreetingDSL()
    grammar = Grammar(dsl)
    runtime = GreetingRuntime()

    grammar.execute('greet(name="Alice")', runtime)
    # Output: Hello, Alice!

    grammar.execute('greet(name="Bob", message="Hi")', runtime)
    # Output: Hi, Bob!
    ```

=== "Go"

    ```go
    package main

    import (
        "context"
        "fmt"
        "grammar-school/go/gs"
    )

    type GreetingDSL struct{}

    func (d *GreetingDSL) Greet(args gs.Args, ctx *gs.Context) ([]gs.Action, *gs.Context, error) {
        name := args["name"].Str
        message := "Hello"
        if msg, ok := args["message"]; ok {
            message = msg.Str
        }

        action := gs.Action{
            Kind: "greet",
            Payload: map[string]interface{}{
                "name":    name,
                "message": message,
            },
        }
        return []gs.Action{action}, ctx, nil
    }

    type GreetingRuntime struct{}

    func (r *GreetingRuntime) ExecuteAction(ctx context.Context, a gs.Action) error {
        msg := a.Payload["message"].(string)
        name := a.Payload["name"].(string)
        fmt.Printf("%s, %s!\n", msg, name)
        return nil
    }

    func main() {
        dsl := &GreetingDSL{}
        // Note: You'll need to implement a Parser
        // engine, _ := gs.NewEngine("", dsl, parser)
        // runtime := &GreetingRuntime{}
        // plan, _ := engine.Compile(`greet(name="Alice")`)
        // engine.Execute(context.Background(), runtime, plan)
    }
    ```

## How It Works

1. **Define Verbs** - Create methods marked with `@verb` (Python) or matching the `VerbHandler` signature (Go)
2. **Create Grammar** - Instantiate a `Grammar` (Python) or `Engine` (Go) with your DSL
3. **Execute** - Parse and execute DSL code, which gets converted to Actions and run by your Runtime

## Next Steps

- Learn about [Core Concepts](concepts.md)
- Explore the [Python API](../python/overview.md) or [Go API](../go/overview.md)
- Check out [Examples](../examples/music-dsl.md)
