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

## OpenAI CFG Utilities

Grammar School provides utilities for integrating with OpenAI's Context-Free Grammar (CFG) feature, allowing you to use Grammar School grammars as constraints for GPT-5.

### CFGConfig

```go
type CFGConfig struct {
    ToolName    string // Name of the tool that will receive the DSL output
    Description string // Description of what the tool does
    Grammar     string // Lark or regex grammar definition
    Syntax      string // "lark" or "regex" (default: "lark")
}
```

Configuration for building an OpenAI CFG tool.

### BuildOpenAICFGTool

```go
func BuildOpenAICFGTool(config CFGConfig) map[string]any
```

Builds an OpenAI CFG tool payload from a CFGConfig. This function:
- Cleans the grammar using `CleanGrammarForCFG()` to remove unsupported Lark directives
- Returns the properly formatted OpenAI tool structure
- Ensures the syntax defaults to "lark" if not specified

**Example:**

```go
import "grammar-school/go/gs"

tool := gs.BuildOpenAICFGTool(gs.CFGConfig{
    ToolName:    "magda_dsl",
    Description: "Generates MAGDA DSL code for REAPER automation",
    Grammar:     grammarString,
    Syntax:      gs.SyntaxLark,
})
// Add tool to OpenAI request: tools = append(tools, tool)
```

### GetOpenAITextFormatForCFG

```go
func GetOpenAITextFormatForCFG() map[string]any
```

Returns the text format configuration that should be used when making OpenAI requests with CFG tools. When using CFG, the text format must be set to "text" (not JSON schema) because the output is DSL code, not JSON.

**Example:**

```go
paramsMap["text"] = gs.GetOpenAITextFormatForCFG()
```

### Constants

```go
const (
    SyntaxLark     = "lark"   // Default syntax for CFG grammars
    SyntaxRegex    = "regex"  // Regex syntax for CFG grammars
    TextFormatType = "text"   // Text format type for OpenAI CFG requests
)
```

### CleanGrammarForCFG

```go
func CleanGrammarForCFG(grammar string) string
```

Cleans a grammar string for use with CFG systems (e.g., GPT-5). Removes parser-specific directives that aren't supported in standard CFG:
- Lines starting with `%` (Lark directives like `%import`, `%ignore`)
- Empty lines for cleaner output
- Other parser-specific meta-directives

### CFGProvider Interface

Grammar School provides a `CFGProvider` interface for integrating with different LLM providers that support CFG. This allows you to use the same API with different LLM providers.

```go
type CFGProvider interface {
    BuildTool(toolName, description, grammar, syntax string) map[string]any
    GetTextFormat() map[string]any
    Generate(ctx context.Context, prompt, model string, tools []map[string]any, textFormat map[string]any, client interface{}, kwargs map[string]any) (interface{}, error)
    ExtractDSLCode(response interface{}) (string, error)
}
```

### OpenAICFGProvider

```go
import "grammar-school/go/gs"

provider := &gs.OpenAICFGProvider{}
cfgTool := provider.BuildTool(
    "task_dsl",
    "Task management DSL",
    grammarString,
    gs.SyntaxLark,
)
textFormat := provider.GetTextFormat()
```

The `OpenAICFGProvider` struct implements the `CFGProvider` interface for OpenAI's API. It handles:
- Building OpenAI-specific CFG tool payloads
- Configuring text format for CFG requests
- Generating DSL code using OpenAI's API
- Extracting DSL code from OpenAI responses

**Example:**

```go
import (
    "context"
    "grammar-school/go/gs"
    "github.com/openai/openai-go"
)

provider := &gs.OpenAICFGProvider{}
cfgTool := provider.BuildTool(
    "task_dsl",
    "Task management DSL",
    engine.Grammar(),
    gs.SyntaxLark,
)
textFormat := provider.GetTextFormat()

// Use with OpenAI client
// ... (OpenAI API call) ...

dslCode, _ := provider.ExtractDSLCode(response)
engine.Execute(ctx, dslCode)
```
