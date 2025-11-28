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

## Runtime Types

### Action

Represents a runtime action produced by the interpreter.

```go
type Action struct {
    Kind    string
    Payload map[string]interface{}
}
```

**Example:**
```go
action := Action{
    Kind: "create_track",
    Payload: map[string]interface{}{
        "name":  "Drums",
        "color": "blue",
    },
}
```

### Context

Represents execution context passed between verb handlers.

```go
type Context struct {
    Data map[string]interface{}
}

func NewContext() *Context
func (c *Context) Get(key string) (interface{}, bool)
func (c *Context) Set(key string, value interface{})
```

**Example:**
```go
ctx := NewContext()
ctx.Set("last_track", "Drums")
value, ok := ctx.Get("last_track")
```

### Args

Map of string to Value for verb handler arguments.

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

### Runtime

Interface for executing actions.

```go
type Runtime interface {
    ExecuteAction(ctx context.Context, a Action) error
}
```

**Example:**
```go
type MyRuntime struct{}

func (r *MyRuntime) ExecuteAction(ctx context.Context, a Action) error {
    switch a.Kind {
    case "greet":
        name := a.Payload["name"].(string)
        fmt.Printf("Hello, %s!\n", name)
    }
    return nil
}
```
