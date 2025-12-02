"""
Example: Integrating Grammar School with GPT-5 using CFG (Context-Free Grammar).

This example demonstrates how to use Grammar School's grammar definition
as a CFG constraint for GPT-5's custom tools, ensuring the model generates
only valid DSL code that can be executed by Grammar School.
"""

from openai import OpenAI

from grammar_school import Grammar, method


class TaskGrammar(Grammar):
    """A simple task management DSL for creating and managing tasks."""

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

    @method
    def list_tasks(self):
        """List all tasks."""
        if not self.tasks:
            print("No tasks found.")
            return
        print("\nTasks:")
        for name, task in self.tasks.items():
            status = "✓" if task["completed"] else "○"
            print(f"  {status} {name} (priority: {task['priority']})")


def get_grammar_definition() -> str:
    """
    Get the Grammar School grammar definition in Lark format.

    This can be used as a CFG for GPT-5's custom tools to ensure
    the model only generates valid Grammar School DSL code.

    **Low-level explanation of what happens:**

    1. **DEFAULT_GRAMMAR** defines the *syntax* (parsing rules):
       - How to parse: "create_task(name='test', priority='high')"
       - Rules like: call_chain, call, args, value, etc.
       - This is a Lark grammar that describes the structure of valid DSL code

    2. **TaskGrammar** defines the *semantics* (what verbs do):
       - The @verb methods: create_task, complete_task, list_tasks
       - These are Python functions that return Action objects
       - They define WHAT happens when a verb is called

    3. **Execution flow when GPT-5 generates code:**
       a. GPT-5 uses DEFAULT_GRAMMAR to generate valid syntax:
          "create_task(name='Write docs', priority='high')"
       b. TaskGrammar.parse() uses DEFAULT_GRAMMAR to parse the string into AST:
          CallChain(calls=[Call(name="create_task", args=[...])])
       c. TaskGrammar.compile() uses Interpreter to convert AST to Actions:
          Interpreter looks up "create_task" in TaskGrammar's @verb methods
          Calls TaskGrammar.create_task() → returns Action(kind="create_task", ...)
       d. TaskGrammar.execute() runs the Runtime:
          Runtime.execute(action) → actually creates the task

    So DEFAULT_GRAMMAR tells GPT-5 HOW to write code (syntax),
    while TaskGrammar tells Grammar School WHAT the code means (semantics).

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
    grammar = TaskGrammar()

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
    grammar = TaskGrammar()

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
