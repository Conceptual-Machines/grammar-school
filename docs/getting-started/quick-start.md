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
    from grammar_school import Grammar, method

    class GreetingDSL(Grammar):
        @method
        def greet(self, name, message="Hello"):
            print(f"{message}, {name}!")

    # Use the DSL
    dsl = GreetingDSL()
    dsl.execute('greet(name="Alice")')
    # Output: Hello, Alice!

    dsl.execute('greet(name="Bob", message="Hi")')
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

    func (d *GreetingDSL) Greet(args gs.Args) error {
        name := args["name"].Str
        message := "Hello"
        if msg, ok := args["message"]; ok {
            message = msg.Str
        }
        fmt.Printf("%s, %s!\n", message, name)
        return nil
    }

    func main() {
        dsl := &GreetingDSL{}
        parser := &MyParser{} // Implement gs.Parser interface
        engine, _ := gs.NewEngine("", dsl, parser)
        engine.Execute(context.Background(), `greet(name="Alice")`)
        // Output: Hello, Alice!
        engine.Execute(context.Background(), `greet(name="Bob", message="Hi")`)
        // Output: Hi, Bob!
    }
    ```

## How It Works

1. **Define Methods** - Create methods marked with `@method` (Python) that contain your implementation
2. **Create Grammar** - Instantiate your Grammar class (Python) or Engine (Go) with your DSL
3. **Execute** - Parse and execute DSL code - methods run directly when called

## Next Steps

- Learn about [Core Concepts](concepts.md)
- Explore the [Python API](../python/overview.md) or [Go API](../go/overview.md)
- Check out [Examples](../examples/music-dsl.md)
