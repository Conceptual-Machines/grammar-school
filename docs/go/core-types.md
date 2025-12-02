# Go Core Types

Detailed documentation of core types in the Grammar School Go implementation.

## AST Types

### Value and ValueKind

Represents a value in the AST with its kind.

```go
type ValueKind int

const (
    ValueNumber ValueKind = iota
    ValueString
    ValueIdentifier
    ValueBool
)

type Value struct {
    Kind ValueKind
    Num  float64
    Str  string
    Bool bool
}
```

**Example:**
```go
value := Value{
    Kind: ValueString,
    Str:  "hello",
}
```

### Arg

Represents a named argument to a call.

```go
type Arg struct {
    Name  string
    Value Value
}
```

**Example:**
```go
arg := Arg{
    Name:  "name",
    Value: Value{Kind: ValueString, Str: "Alice"},
}
```

### Call

Represents a single function call with named arguments.

```go
type Call struct {
    Name string
    Args []Arg
}
```

**Example:**
```go
call := Call{
    Name: "greet",
    Args: []Arg{
        {Name: "name", Value: Value{Kind: ValueString, Str: "Alice"}},
    },
}
```

### CallChain

Represents a chain of calls connected by dots (method chaining).

```go
type CallChain struct {
    Calls []Call
}
```

**Example:**
```go
chain := CallChain{
    Calls: []Call{
        {Name: "track", Args: []Arg{}},
        {Name: "add_clip", Args: []Arg{}},
    },
}
```

## Method Handlers

Methods execute directly - no Action return needed. See the MethodHandler section below.

### Args

Map of string to Value for method handler arguments.

```go
type Args map[string]Value
```

**Example:**
```go
args := Args{
    "name":  Value{Kind: ValueString, Str: "Alice"},
    "count": Value{Kind: ValueNumber, Num: 2},
}
```

## Method Handlers

### MethodHandler

Function signature for method handlers. Methods execute directly - no Action return needed.

```go
type MethodHandler func(args Args) error
```

**Example:**
```go
func (d *MyDSL) Greet(args Args) error {
    name := args["name"].Str
    fmt.Printf("Hello, %s!\n", name)
    return nil
}
```

**Note:** The `Action`, `Context`, and `Runtime` types still exist internally for the two-layer architecture, but users don't need to interact with them directly when using the unified interface.
