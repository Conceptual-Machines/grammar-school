"""Example: Using GrammarBuilder to define grammars programmatically."""

from grammar_school import Grammar, GrammarBuilder, method


class TaskGrammar(Grammar):
    """A simple task management DSL."""

    def __init__(self, grammar=None):
        super().__init__(grammar=grammar)
        self.tasks = {}

    @method
    def create_task(self, name: str, priority: str = "medium"):
        """Create a new task."""
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


def example_programmatic_grammar():
    """Example: Build grammar programmatically with GrammarBuilder."""
    print("=" * 60)
    print("Example: Programmatic Grammar Definition")
    print("=" * 60)

    # Build a custom grammar (same as default, but built programmatically)
    builder = GrammarBuilder()
    builder.rule("start", "call_chain", "Entry point: a chain of function calls")
    builder.rule("call_chain", "call (DOT call)*", "Chain of calls")
    builder.rule("call", 'IDENTIFIER "(" args? ")"', "Function call")
    builder.rule("args", "arg (COMMA arg)*", "Arguments")
    builder.rule("arg", 'IDENTIFIER "=" value | value', "Argument")
    builder.rule("value", "NUMBER | STRING | IDENTIFIER", "Value")
    builder.terminal("DOT", ".", "Dot separator")
    builder.terminal("COMMA", ",", "Comma separator")
    builder.terminal("NUMBER", "/-?\\d+(\\.\\d+)?/", "Number")
    builder.terminal("STRING", '/"([^"\\\\]|\\\\.)*"/', "String")
    builder.terminal("IDENTIFIER", "/[a-zA-Z_][a-zA-Z0-9_]*/", "Identifier")
    builder.directive("%import common.WS")
    builder.directive("%ignore WS")

    # Use the built grammar
    grammar = TaskGrammar(grammar=builder)

    # Single statement with chaining (works with current grammar)
    code = 'create_task(name="Write docs", priority="high").complete_task(name="Write docs")'

    print("\nCode:")
    print(code)
    print("\nExecution:")
    print("-" * 60)
    grammar.execute(code)

    print("\nNote: Multiple statements (separated by newlines) would require")
    print("      extending the AST transformer to handle statement lists.")


def example_default_grammar():
    """Example: Use the default grammar builder."""
    print("\n" + "=" * 60)
    print("Example: Default Grammar")
    print("=" * 60)

    # Get default grammar
    builder = GrammarBuilder.default()
    grammar = TaskGrammar(grammar=builder)

    # Single statement (default grammar supports this)
    code = 'create_task(name="Write docs", priority="high").complete_task(name="Write docs")'

    print("\nCode:")
    print(code)
    print("\nExecution:")
    print("-" * 60)
    grammar.execute(code)


if __name__ == "__main__":
    example_programmatic_grammar()
    example_default_grammar()
