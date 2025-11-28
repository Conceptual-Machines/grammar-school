# Go Examples

## Music DSL

A simple example DSL for creating music tracks and clips.

```bash
cd go
go run examples/music_dsl.go
```

**Note**: The example currently shows the structure but requires a parser implementation. To use it, you'll need to implement the `Parser` interface from `gs/parser_backend.go` using a library like:
- [participle](https://github.com/alecthomas/participle)
- [pigeon](https://github.com/mna/pigeon)
- Custom PEG/EBNF parser

The example demonstrates:
- Defining verb handlers with the required signature
- Creating an Engine instance
- Using reflection to automatically discover verb handlers
- Executing actions through a Runtime

## Functional DSL

An example demonstrating functional programming patterns using the `FunctionalMixin`:

```bash
cd go
go run examples/functional_dsl.go
```

The example demonstrates:
- **Function references**: Using `@function_name` syntax to pass functions as arguments
- **Higher-order functions**: `map`, `filter`, `reduce` operations
- **Function composition**: `compose` and `pipe` for chaining transformations
- **Mixin pattern**: Embedding `FunctionalMixin` to get functional operations

```go
type FunctionalDSL struct {
    gs.FunctionalMixin
}

func (d *FunctionalDSL) Square(args gs.Args, ctx *gs.Context) ([]gs.Action, *gs.Context, error) {
    x := args["x"].Num
    return []gs.Action{{
        Kind: "square",
        Payload: map[string]interface{}{"value": x * x},
    }}, ctx, nil
}

// Then use: map(@Square, data)
```
