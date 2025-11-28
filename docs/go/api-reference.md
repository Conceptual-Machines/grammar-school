# Go API Reference

Complete API reference for the Grammar School Go implementation.

## Core Types

### Value and ValueKind

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

### Arg

```go
type Arg struct {
    Name  string
    Value Value
}
```

### Call

```go
type Call struct {
    Name string
    Args []Arg
}
```

### CallChain

```go
type CallChain struct {
    Calls []Call
}
```

## Action

```go
type Action struct {
    Kind    string
    Payload map[string]interface{}
}
```

## Context

```go
type Context struct {
    Data map[string]interface{}
}

func NewContext() *Context
func (c *Context) Get(key string) (interface{}, bool)
func (c *Context) Set(key string, value interface{})
```

## Args

```go
type Args map[string]Value
```

## Engine

```go
type Engine struct {
    grammar string
    parser  Parser
    verbs   map[string]VerbHandler
    dsl     interface{}
}

func NewEngine(grammar string, dsl interface{}, parser Parser) (*Engine, error)
func (e *Engine) Compile(code string) ([]Action, error)
func (e *Engine) Execute(ctx context.Context, runtime Runtime, plan []Action) error
```

## Parser Interface

```go
type Parser interface {
    Parse(input string) (*CallChain, error)
}
```

## Runtime Interface

```go
type Runtime interface {
    ExecuteAction(ctx context.Context, a Action) error
}
```

## VerbHandler

```go
type VerbHandler func(args Args, ctx *Context) ([]Action, *Context, error)
```

Verb handlers must match this signature. The Engine uses reflection to automatically discover and register methods with this signature.
