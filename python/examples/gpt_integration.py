"""
Example: Integrating Grammar School with GPT-5 using CFG (Context-Free Grammar).

This example demonstrates how to use Grammar School's grammar definition
as a CFG constraint for GPT-5's custom tools, ensuring the model generates
only valid DSL code that can be executed by Grammar School.
"""

from openai import OpenAI

from grammar_school import Action, Grammar, Runtime, verb


class TaskGrammar(Grammar):
    """A simple task management DSL for creating and managing tasks."""

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

    @verb
    def list_tasks(self, _context=None):
        """List all tasks."""
        return Action(
            kind="list_tasks",
            payload={},
        )


class TaskRuntime(Runtime):
    """Runtime that executes task management actions."""

    def __init__(self):
        self.tasks = {}

    def execute(self, action: Action) -> None:
        """Execute a task management action."""
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
            else:
                print(f"✗ Task not found: {name}")

        elif action.kind == "list_tasks":
            if not self.tasks:
                print("No tasks found.")
            else:
                print("\nTasks:")
                for name, task in self.tasks.items():
                    status = "✓" if task["completed"] else "○"
                    print(f"  {status} {name} (priority: {task['priority']})")


def get_grammar_definition() -> str:
    """
    Get the Grammar School grammar definition in Lark format.

    This can be used as a CFG for GPT-5's custom tools to ensure
    the model only generates valid Grammar School DSL code.

    The grammar is automatically cleaned to work with GPT-5's CFG requirements
    by removing Lark-specific directives (e.g., %import, %ignore).
    """
    from grammar_school.backend_lark import DEFAULT_GRAMMAR, LarkBackend

    # Clean up grammar for GPT-5 CFG (remove unsupported directives)
    return LarkBackend.clean_grammar_for_cfg(DEFAULT_GRAMMAR)


def integrate_with_gpt5():
    """
    Example of integrating Grammar School with GPT-5 using CFG.

    This shows how to:
    1. Use Grammar School's grammar as a CFG constraint for GPT-5
    2. Execute the generated DSL code using Grammar School
    3. Handle the results and provide feedback to GPT-5
    """
    client = OpenAI()

    # Initialize Grammar School
    grammar = TaskGrammar(runtime=TaskRuntime())

    # Get the grammar definition for CFG
    grammar_def = get_grammar_definition()

    # Example prompt for GPT-5
    prompt = (
        "I need to manage my tasks. Please use the task_dsl tool to:\n"
        "1. Create a task called 'Write documentation' with high priority\n"
        "2. Create a task called 'Review code' with medium priority\n"
        "3. List all tasks\n"
        "4. Complete the 'Review code' task\n"
        "5. List all tasks again\n\n"
        "Use the task_dsl tool for each action. Make sure your tool calls "
        "follow the Grammar School DSL syntax exactly."
    )

    print("=" * 60)
    print("GPT-5 Integration Example with Grammar School")
    print("=" * 60)
    print("\nPrompt to GPT-5:")
    print(prompt)
    print("\n" + "=" * 60)

    # Call GPT-5 with CFG constraint
    response = client.responses.create(
        model="gpt-5",
        input=prompt,
        text={"format": {"type": "text"}},
        tools=[
            {
                "type": "custom",
                "name": "task_dsl",
                "description": (
                    "Executes task management operations using Grammar School DSL. "
                    "Available verbs: create_task(name, priority), complete_task(name), list_tasks(). "
                    "YOU MUST REASON HEAVILY ABOUT THE QUERY AND MAKE SURE IT OBEYS THE GRAMMAR. "
                    "Example: create_task(name='test', priority='high').complete_task(name='test').list_tasks()"
                ),
                "format": {
                    "type": "grammar",
                    "syntax": "lark",
                    "definition": grammar_def,
                },
            },
        ],
        parallel_tool_calls=False,
    )

    # Process tool calls from GPT-5
    print("\nGPT-5 Response:")
    print("-" * 60)

    for item in response.output:
        if hasattr(item, "type") and item.type == "custom_tool_call":
            dsl_code = item.input
            print(f"\nGenerated DSL Code: {dsl_code}")
            print("\nExecuting with Grammar School:")
            print("-" * 60)

            try:
                # Execute the DSL code using Grammar School
                grammar.execute(dsl_code)
            except Exception as e:
                print(f"Error executing DSL: {e}")
                # In a real scenario, you'd send this error back to GPT-5

    print("\n" + "=" * 60)
    print("Integration complete!")
    print("=" * 60)


def simple_example():
    """
    Simple example showing Grammar School usage without GPT-5.
    This demonstrates the DSL syntax that GPT-5 should generate.
    """
    print("\n" + "=" * 60)
    print("Simple Grammar School Example (without GPT-5)")
    print("=" * 60)

    # Initialize Grammar School
    grammar = TaskGrammar(runtime=TaskRuntime())

    # Example DSL code
    code = (
        "create_task(name='Write docs', priority='high')"
        ".create_task(name='Review PR', priority='medium')"
        ".list_tasks()"
        ".complete_task(name='Review PR')"
        ".list_tasks()"
    )

    print(f"\nDSL Code: {code}\n")
    print("Execution:")
    print("-" * 60)

    grammar.execute(code)


if __name__ == "__main__":
    # Run simple example first
    simple_example()

    # Note: Uncomment the line below to run the GPT-5 integration
    # You'll need to set OPENAI_API_KEY environment variable
    # integrate_with_gpt5()
