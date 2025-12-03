# GPT-5 Integration with Grammar School

This example demonstrates how to integrate Grammar School with GPT-5 using Context-Free Grammar (CFG) constraints.

## Overview

Grammar School is designed to create LLM-friendly DSLs. When combined with GPT-5's CFG feature, you can ensure that the model generates only valid DSL code that can be executed by Grammar School.

## Key Features

1. **CFG Constraint**: Use Grammar School's Lark grammar definition as a CFG for GPT-5's custom tools
2. **Type Safety**: GPT-5 can only generate syntactically valid DSL code
3. **Direct Execution**: Generated code can be executed immediately without parsing errors

## How It Works

1. **Grammar Definition**: Grammar School uses Lark to define the DSL grammar
2. **CFG Export**: The grammar can be exported and used as a CFG constraint in GPT-5
3. **Tool Definition**: Define a GPT-5 custom tool with the grammar as a CFG
4. **Code Generation**: GPT-5 generates DSL code that conforms to the grammar
5. **Execution**: Execute the generated code using Grammar School's interpreter

## Example Usage

```python
from grammar_school import Grammar, method
from openai import OpenAI

class TaskGrammar(Grammar):
    """A simple task management DSL."""

    def __init__(self):
        super().__init__()
        self.tasks = {}

    @method
    def create_task(self, name: str, priority: str = "medium"):
        """Create a new task with a name and optional priority."""
        self.tasks[name] = {"priority": priority, "completed": False}
        print(f"✓ Created task: {name} (priority: {priority})")

    @method
    def complete_task(self, name: str):
        """Mark a task as completed."""
        if name in self.tasks:
            self.tasks[name]["completed"] = True
            print(f"✓ Completed task: {name}")
        else:
            print(f"✗ Task not found: {name}")

# Initialize Grammar School
grammar = TaskGrammar()

# Use CFG provider to build OpenAI tool and generate DSL code
from grammar_school.cfg_vendor import OpenAICFGProvider
from grammar_school.openai_utils import OpenAICFG

# Create CFG provider (OpenAI)
provider = OpenAICFGProvider()

# Build the CFG tool payload
cfg_tool = provider.build_tool(
    tool_name="task_dsl",
    description="Executes task management operations using Grammar School DSL.",
    grammar=grammar.backend.grammar,  # Get grammar from Grammar instance
    syntax="lark",
)

# Get text format configuration (required for CFG)
text_format = provider.get_text_format()

# Generate DSL code using OpenAI
client = OpenAI()
response = client.chat.completions.create(
    model="gpt-5",
    messages=[{"role": "user", "content": "Create a task called 'Write docs' with high priority"}],
    tools=[cfg_tool],
    tool_choice={"type": "required", "tool": {"name": "task_dsl"}},
    **text_format,
)

# Extract DSL code from response
dsl_code = provider.extract_dsl_code(response)

# Execute the generated DSL code
if dsl_code:
    try:
        grammar.execute(dsl_code)
        print("Task created successfully!")
    except Exception as e:
        print(f"Error executing DSL: {e}")
```

## Benefits

- **Reliability**: GPT-5 can only generate valid DSL code
- **No Parsing Errors**: Generated code is guaranteed to be syntactically correct
- **Type Safety**: The grammar enforces correct argument types and structure
- **Easy Integration**: Use Grammar School's existing grammar definitions

## Using OpenAI CFG - The Simple Way

For OpenAI, you can use the convenient `OpenAICFG` class:

```python
from grammar_school.openai_utils import OpenAICFG

# Create OpenAI CFG configuration
cfg = OpenAICFG(
    tool_name="task_dsl",
    description="Task management DSL",
    grammar=grammar.backend.grammar,  # Or use default Grammar School grammar
)

# Build tool and get text format
tool = cfg.build_tool()
text_format = cfg.get_text_format()

# Use with OpenAI client
from openai import OpenAI
client = OpenAI()
response = client.chat.completions.create(
    model="gpt-5",
    messages=[{"role": "user", "content": "Create a task"}],
    tools=[tool],
    tool_choice={"type": "required", "tool": {"name": "task_dsl"}},
    **text_format,
)
```

The `OpenAICFG` class is a convenient wrapper that handles:
- Building OpenAI CFG tool payloads
- Configuring text format for CFG requests
- Grammar cleaning (removing unsupported Lark directives)

## Using CFG Providers

For more advanced use cases or to support multiple LLM providers, Grammar School provides a `CFGProvider` interface. The `OpenAICFGProvider` handles OpenAI-specific CFG integration:

```python
from grammar_school.cfg_vendor import OpenAICFGProvider
from grammar_school.openai_utils import OpenAICFG

# Initialize your grammar
grammar = TaskGrammar()

# Create CFG provider
provider = OpenAICFGProvider()

# Build the CFG tool payload
cfg_tool = provider.build_tool(
    tool_name="task_dsl",
    description="Task management DSL",
    grammar=grammar.backend.grammar,
    syntax="lark",
)

# Get text format configuration
text_format = provider.get_text_format()

# Use with OpenAI client
from openai import OpenAI
client = OpenAI()
response = client.chat.completions.create(
    model="gpt-5",
    messages=[{"role": "user", "content": "Create a task"}],
    tools=[cfg_tool],
    tool_choice={"type": "required", "tool": {"name": "task_dsl"}},
    **text_format,
)

# Extract and execute DSL code
dsl_code = provider.extract_dsl_code(response)
if dsl_code:
    grammar.execute(dsl_code)
```

You can implement your own provider for other LLM providers:

```python
from grammar_school.cfg_vendor import CFGProvider

class AnthropicCFGProvider(CFGProvider):
    """Custom vendor for Anthropic's Claude API."""

    def build_tool(self, tool_name, description, grammar, syntax):
        # Implement vendor-specific tool structure
        ...

    def get_text_format(self):
        # Return vendor-specific text format
        ...

    def generate(self, prompt, model, tools, text_format, client=None, **kwargs):
        # Implement vendor-specific generation
        ...

    def extract_dsl_code(self, response):
        # Extract DSL code from vendor response
        ...
```

## Requirements

- `grammar-school` package installed
- `openai` Python SDK (version 1.99.2 or later)
- GPT-5 API access
- `OPENAI_API_KEY` environment variable set

## Running the Example

1. Install dependencies:
   ```bash
   pip install grammar-school openai
   ```

2. Set your OpenAI API key:
   ```bash
   export OPENAI_API_KEY=your-api-key-here
   ```

3. Run the example:
   ```bash
   cd python
   python examples/gpt_integration.py
   ```

4. To test with GPT-5, uncomment the `integrate_with_gpt5()` call in the script.

## Advanced Usage

### Custom Grammar Definitions

You can create custom grammar definitions for specific use cases:

```python
from grammar_school import Grammar, rule

@rule("""
    start: call_chain
    call_chain: call ('.' call)*
    call: IDENTIFIER '(' args? ')'
    args: arg (',' arg)*
    arg: IDENTIFIER '=' value
    value: STRING | NUMBER
    IDENTIFIER: /[a-zA-Z_][a-zA-Z0-9_]*/
    STRING: /"[^"]*"/
    NUMBER: /[0-9]+/
""")
class CustomDSL(Grammar):
    # Your DSL implementation
    pass
```

### Error Handling

When GPT-5 generates code that fails to execute, you can provide feedback:

```python
try:
    grammar.execute(generated_code)
except Exception as e:
    # Send error back to GPT-5 for correction
    feedback = f"Error: {e}. Please fix the DSL code."
    # Continue conversation with GPT-5
```

## See Also

- [Grammar School Documentation](../index.md)
- [GPT-5 CFG Documentation](https://platform.openai.com/docs/guides/function-calling)
- [Lark Parser Documentation](https://lark-parser.readthedocs.io/)
