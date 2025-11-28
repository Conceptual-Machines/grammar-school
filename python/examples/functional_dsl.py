"""Example Functional DSL using Grammar School with function references."""

from grammar_school import Action, FunctionalMixin, Grammar, Runtime, verb


class FunctionalGrammar(Grammar, FunctionalMixin):
    """
    A functional DSL demonstrating map, filter, and reduce patterns.

    Uses FunctionalMixin to get map, filter, reduce, compose, and pipe operations.
    """

    @verb
    def square(self, x, _context=None):
        """Square a number."""
        return Action(kind="square", payload={"value": x * x})

    @verb
    def double(self, x, _context=None):
        """Double a number."""
        return Action(kind="double", payload={"value": x * 2})

    @verb
    def is_even(self, x, _context=None):
        """Check if number is even."""
        return Action(kind="is_even", payload={"value": x % 2 == 0})


class FunctionalRuntime(Runtime):
    """Runtime that executes functional operations."""

    def execute(self, action: Action) -> None:
        """Execute functional actions."""
        if action.kind == "map":
            func = action.payload["func"]
            data = action.payload["data"]
            print(f"Map {func} over {data}")
        elif action.kind == "filter":
            predicate = action.payload["predicate"]
            data = action.payload["data"]
            print(f"Filter {data} using {predicate}")
        elif action.kind == "reduce":
            func = action.payload["func"]
            data = action.payload["data"]
            initial = action.payload.get("initial")
            print(f"Reduce {data} using {func}" + (f" with initial {initial}" if initial else ""))
        else:
            print(f"Action: {action.kind} with payload: {action.payload}")


def main():
    """Example usage of the Functional DSL."""
    grammar = FunctionalGrammar(runtime=FunctionalRuntime())

    # Functional programming examples
    print("=" * 60)
    print("Functional DSL Examples")
    print("=" * 60)

    # Map function over data
    print("\n1. Map:")
    grammar.execute("map(@square, data)")

    # Filter using predicate
    print("\n2. Filter:")
    grammar.execute("filter(@is_even, data)")

    # Chain operations
    print("\n3. Chained operations:")
    grammar.execute("map(@double, data).filter(@is_even, data)")

    # Compose functions
    print("\n4. Compose:")
    grammar.execute("compose(@square, @double)")

    # Pipe data through functions
    print("\n5. Pipe:")
    grammar.execute("pipe(data, @double, @square)")


if __name__ == "__main__":
    main()
