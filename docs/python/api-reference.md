# Python API Reference

Complete API reference for the Grammar School Python implementation.

## Core Types

::: grammar_school.ast.Value
    options:
      show_root_heading: true
      show_source: true

::: grammar_school.ast.Arg
    options:
      show_root_heading: true
      show_source: true

::: grammar_school.ast.Call
    options:
      show_root_heading: true
      show_source: true

::: grammar_school.ast.CallChain
    options:
      show_root_heading: true
      show_source: true

## Method Decorators

::: grammar_school.grammar.method
    options:
      show_root_heading: true
      show_source: true

**Note:** The `Action` and `Runtime` types still exist internally for the two-layer architecture, but users don't need to interact with them directly when using the unified `@method` interface.

## Grammar

::: grammar_school.grammar.Grammar
    options:
      show_root_heading: true
      show_source: true

::: grammar_school.grammar.rule
    options:
      show_root_heading: true
      show_source: true

::: grammar_school.grammar.method
    options:
      show_root_heading: true
      show_source: true

## Interpreter

::: grammar_school.interpreter.Interpreter
    options:
      show_root_heading: true
      show_source: true

## Parser Backend

::: grammar_school.backend_lark.LarkBackend
    options:
      show_root_heading: true
      show_source: true

::: grammar_school.backend_lark.DEFAULT_GRAMMAR
    options:
      show_root_heading: true
      show_source: true

## OpenAI CFG Utilities

Grammar School provides utilities for integrating with OpenAI's Context-Free Grammar (CFG) feature, allowing you to use Grammar School grammars as constraints for GPT-5.

### CFGConfig

```python
@dataclass
class CFGConfig:
    tool_name: str
    description: str
    grammar: str
    syntax: str = "lark"
```

Configuration for building an OpenAI CFG tool.

**Example:**

```python
from grammar_school.openai_utils import CFGConfig

config = CFGConfig(
    tool_name="magda_dsl",
    description="Generates MAGDA DSL code for REAPER automation",
    grammar=grammar_string,
    syntax="lark",
)
```

### build_openai_cfg_tool

```python
def build_openai_cfg_tool(config: CFGConfig) -> dict[str, Any]
```

Builds an OpenAI CFG tool payload from a CFGConfig. This function:
- Cleans the grammar using `LarkBackend.clean_grammar_for_cfg()` to remove unsupported Lark directives
- Returns the properly formatted OpenAI tool structure
- Ensures the syntax defaults to "lark" if not specified

**Example:**

```python
from grammar_school.openai_utils import CFGConfig, build_openai_cfg_tool

tool = build_openai_cfg_tool(CFGConfig(
    tool_name="magda_dsl",
    description="Generates MAGDA DSL code for REAPER automation",
    grammar=grammar_string,
    syntax="lark",
))
# Add tool to OpenAI request: tools = [tool]
```

### get_openai_text_format_for_cfg

```python
def get_openai_text_format_for_cfg() -> dict[str, Any]
```

Returns the text format configuration that should be used when making OpenAI requests with CFG tools. When using CFG, the text format must be set to "text" (not JSON schema) because the output is DSL code, not JSON.

**Example:**

```python
from grammar_school.openai_utils import get_openai_text_format_for_cfg

params["text"] = get_openai_text_format_for_cfg()
```

### clean_grammar_for_cfg

```python
@staticmethod
def LarkBackend.clean_grammar_for_cfg(grammar: str) -> str
```

Cleans a Lark grammar for use with CFG systems (e.g., GPT-5). Removes Lark-specific directives that aren't supported in standard CFG:
- `%import` directives
- `%ignore` directives
- Other `%`-prefixed directives

### CFGProvider Interface

Grammar School provides a `CFGProvider` interface for integrating with different LLM providers that support CFG. This allows you to use the same API with different LLM providers.

```python
from abc import ABC, abstractmethod

class CFGProvider(ABC):
    @abstractmethod
    def build_tool(self, tool_name: str, description: str, grammar: str, syntax: str) -> dict[str, Any]:
        """Builds the vendor-specific CFG tool payload."""
        pass

    @abstractmethod
    def get_text_format(self) -> dict[str, Any]:
        """Returns the text format configuration for the vendor's API."""
        pass

    @abstractmethod
    def generate(self, prompt: str, model: str, tools: list[dict], text_format: dict, client=None, **kwargs) -> Any:
        """Generates DSL code using the vendor's LLM."""
        pass

    @abstractmethod
    def extract_dsl_code(self, response: Any) -> str:
        """Extracts DSL code from the vendor's response."""
        pass
```

### OpenAICFGProvider

```python
from grammar_school.cfg_vendor import OpenAICFGProvider

provider = OpenAICFGProvider()
cfg_tool = provider.build_tool(
    tool_name="task_dsl",
    description="Task management DSL",
    grammar=grammar_string,
    syntax="lark",
)
text_format = provider.get_text_format()
```

The `OpenAICFGProvider` class implements the `CFGProvider` interface for OpenAI's API. It handles:
- Building OpenAI-specific CFG tool payloads
- Configuring text format for CFG requests
- Generating DSL code using OpenAI's API
- Extracting DSL code from OpenAI responses

**Example:**

```python
from grammar_school.cfg_vendor import OpenAICFGProvider
from openai import OpenAI

provider = OpenAICFGProvider()
cfg_tool = provider.build_tool(
    tool_name="task_dsl",
    description="Task management DSL",
    grammar=grammar.backend.grammar,
    syntax="lark",
)
text_format = provider.get_text_format()

client = OpenAI()
response = client.chat.completions.create(
    model="gpt-5",
    messages=[{"role": "user", "content": "Create a task"}],
    tools=[cfg_tool],
    tool_choice={"type": "required", "tool": {"name": "task_dsl"}},
    **text_format,
)

dsl_code = provider.extract_dsl_code(response)
grammar.execute(dsl_code)
```
