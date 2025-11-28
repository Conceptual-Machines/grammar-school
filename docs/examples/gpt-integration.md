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
from grammar_school import Grammar, verb, Action, Runtime
from openai import OpenAI

class TaskGrammar(Grammar):
    """A simple task management DSL."""

    @verb
    def create_task(self, name: str, priority: str = "medium", _context=None):
        """Create a new task with a name and optional priority."""
        return Action(
            kind="create_task",
            payload={"name": name, "priority": priority},
        )

    @verb
    def complete_task(self, name: str, _context=None):
        """Mark a task as completed."""
        return Action(
            kind="complete_task",
            payload={"name": name},
        )

class TaskRuntime(Runtime):
    """Runtime that executes task management actions."""

    def __init__(self):
        self.tasks = {}

    def execute(self, action: Action) -> None:
        if action.kind == "create_task":
            name = action.payload["name"]
            priority = action.payload.get("priority", "medium")
            self.tasks[name] = {"priority": priority, "completed": False}
            print(f"✓ Created task: {name} (priority: {priority})")
        elif action.kind == "complete_task":
            name = action.payload["name"]
            if name in self.tasks:
                self.tasks[name]["completed"] = True
                print(f"✓ Completed task: {name}")

# Initialize Grammar School
grammar = TaskGrammar(runtime=TaskRuntime())

# Get grammar definition for CFG
from grammar_school.backend_lark import DEFAULT_GRAMMAR, LarkBackend

# Clean up grammar for GPT-5 CFG (remove unsupported directives)
cleaned_grammar = LarkBackend.clean_grammar_for_cfg(DEFAULT_GRAMMAR)

# Call GPT-5 with CFG constraint
client = OpenAI()
response = client.responses.create(
    model="gpt-5",
    input="Create a task called 'Write docs' with high priority",
    tools=[{
        "type": "custom",
        "name": "task_dsl",
        "description": "Executes task management operations using Grammar School DSL.",
        "format": {
            "type": "grammar",
            "syntax": "lark",
            "definition": cleaned_grammar,
        },
    }],
)

# Execute the generated DSL code
for item in response.output:
    if hasattr(item, "type") and item.type == "custom_tool_call":
        dsl_code = item.input
        grammar.execute(dsl_code)
```

## Benefits

- **Reliability**: GPT-5 can only generate valid DSL code
- **No Parsing Errors**: Generated code is guaranteed to be syntactically correct
- **Type Safety**: The grammar enforces correct argument types and structure
- **Easy Integration**: Use Grammar School's existing grammar definitions

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
