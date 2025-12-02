"""Functional programming utilities for Grammar School DSLs."""

from grammar_school.grammar import method


class FunctionalMixin:
    """
    Mixin class providing functional programming operations.

    Inherit from this alongside Grammar to get map, filter, reduce, etc.

    Example:
        ```python
        class MyGrammar(Grammar, FunctionalMixin):
            @method
            def square(self, x):
                return x * x

        grammar = MyGrammar()
        grammar.execute('map(@square, data)')
        ```
    """

    @method
    def map(self, _positional=None):
        """Map a function over data. Usage: map(@function, data)"""
        # Placeholder - will be implemented properly later
        print(f"Map operation: {_positional}")

    @method
    def filter(self, _positional=None):
        """Filter data using a predicate. Usage: filter(@predicate, data)"""
        # Placeholder - will be implemented properly later
        print(f"Filter operation: {_positional}")

    @method
    def reduce(self, _positional=None):
        """Reduce data using a function. Usage: reduce(@function, data, initial)"""
        # Placeholder - will be implemented properly later
        print(f"Reduce operation: {_positional}")

    @method
    def compose(self, _positional=None):
        """Compose multiple functions. Usage: compose(@f, @g, @h)"""
        # Placeholder - will be implemented properly later
        print(f"Compose operation: {_positional}")

    @method
    def pipe(self, _positional=None):
        """Pipe data through functions. Usage: pipe(data, @f, @g, @h)"""
        # Placeholder - will be implemented properly later
        print(f"Pipe operation: {_positional}")
