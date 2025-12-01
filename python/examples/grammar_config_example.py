"""Example: Using config files (YAML/TOML) to define grammars."""

from pathlib import Path

from grammar_school import Action, Grammar, Runtime, load_grammar_from_config, verb


class TaskGrammar(Grammar):
    """A simple task management DSL."""

    @verb
    def create_task(self, name: str, priority: str = "medium", _context=None):
        """Create a new task."""
        return Action(kind="create_task", payload={"name": name, "priority": priority})

    @verb
    def complete_task(self, name: str, _context=None):
        """Mark a task as completed."""
        return Action(kind="complete_task", payload={"name": name})


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


def example_config_dict():
    """Example: Load grammar from a config dictionary."""
    print("=" * 60)
    print("Example: Grammar from Config Dictionary")
    print("=" * 60)

    # Define grammar as a config dict (matching default grammar structure)
    config = {
        "start": "start",
        "rules": [
            {"name": "start", "definition": "call_chain", "description": "Entry point"},
            {
                "name": "call_chain",
                "definition": "call (DOT call)*",
                "description": "Chain of calls",
            },
            {
                "name": "call",
                "definition": 'IDENTIFIER "(" args? ")"',
                "description": "Function call",
            },
            {"name": "args", "definition": "arg (COMMA arg)*", "description": "Arguments"},
            {
                "name": "arg",
                "definition": 'IDENTIFIER "=" value | value',
                "description": "Argument",
            },
            {"name": "value", "definition": "NUMBER | STRING | IDENTIFIER", "description": "Value"},
        ],
        "terminals": [
            {"name": "DOT", "pattern": ".", "description": "Dot separator"},
            {"name": "COMMA", "pattern": ",", "description": "Comma separator"},
            {"name": "NUMBER", "pattern": "/-?\\d+(\\.\\d+)?/", "description": "Number"},
            {"name": "STRING", "pattern": '/"([^"\\\\]|\\\\.)*"/', "description": "String"},
            {
                "name": "IDENTIFIER",
                "pattern": "/[a-zA-Z_][a-zA-Z0-9_]*/",
                "description": "Identifier",
            },
        ],
        "directives": ["%import common.WS", "%ignore WS"],
    }

    # Load grammar from config
    grammar_str = load_grammar_from_config(config)
    grammar = TaskGrammar(runtime=TaskRuntime(), grammar=grammar_str)

    # Single statement with chaining (multiple statements would require AST transformer updates)
    code = 'create_task(name="Write docs", priority="high").complete_task(name="Write docs")'

    print("\nCode:")
    print(code)
    print("\nExecution:")
    print("-" * 60)
    grammar.execute(code)


def example_yaml_file():
    """Example: Load grammar from a YAML file."""
    print("\n" + "=" * 60)
    print("Example: Grammar from YAML File")
    print("=" * 60)

    # Create example YAML file (matching default grammar structure)
    yaml_content = """start: start

rules:
  - name: start
    definition: call_chain
    description: Entry point
  - name: call_chain
    definition: call (DOT call)*
    description: Chain of calls
  - name: call
    definition: 'IDENTIFIER "(" args? ")"'
    description: Function call
  - name: args
    definition: arg (COMMA arg)*
    description: Arguments
  - name: arg
    definition: 'IDENTIFIER "=" value | value'
    description: Argument
  - name: value
    definition: NUMBER | STRING | IDENTIFIER
    description: Value

terminals:
  - name: DOT
    pattern: "."
    description: Dot separator
  - name: COMMA
    pattern: ","
    description: Comma separator
  - name: NUMBER
    pattern: /-?\\d+(\\.\\d+)?/
    description: Number
  - name: STRING
    pattern: /"([^"\\\\]|\\\\.)*"/
    description: String
  - name: IDENTIFIER
    pattern: /[a-zA-Z_][a-zA-Z0-9_]*/
    description: Identifier

directives:
  - "%import common.WS"
  - "%ignore WS"
"""

    yaml_path = Path("/tmp/example_grammar.yaml")
    yaml_path.write_text(yaml_content)

    try:
        from grammar_school import load_grammar_from_yaml

        grammar_str = load_grammar_from_yaml(yaml_path)
        grammar = TaskGrammar(runtime=TaskRuntime(), grammar=grammar_str)

        code = 'create_task(name="Write docs", priority="high").complete_task(name="Write docs")'

        print("\nCode:")
        print(code)
        print("\nExecution:")
        print("-" * 60)
        grammar.execute(code)
    except ImportError:
        print("\n⚠️  PyYAML not installed. Install with: pip install pyyaml")
    finally:
        if yaml_path.exists():
            yaml_path.unlink()


if __name__ == "__main__":
    example_config_dict()
    example_yaml_file()
