"""Example Functional DSL using Grammar School with function references."""

from grammar_school import FunctionalMixin, Grammar, method


class FunctionalGrammar(Grammar, FunctionalMixin):
    """
    A functional DSL demonstrating map, filter, and reduce patterns.

    Uses FunctionalMixin to get map, filter, reduce, compose, and pipe operations.
    """

    @method
    def square(self, x):
        """Square a number."""
        return x * x

    @method
    def double(self, x):
        """Double a number."""
        return x * 2

    @method
    def is_even(self, x):
        """Check if number is even."""
        return x % 2 == 0


def main():
    """Example usage of the Functional DSL."""
    grammar = FunctionalGrammar()

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
