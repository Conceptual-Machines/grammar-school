"""Functional programming utilities for Grammar School DSLs."""

from grammar_school.grammar import verb
from grammar_school.runtime import Action


class FunctionalMixin:
    """
    Mixin class providing functional programming operations.

    Inherit from this alongside Grammar to get map, filter, reduce, etc.

    Example:
        ```python
        class MyGrammar(Grammar, FunctionalMixin):
            @verb
            def square(self, x, _context=None):
                return Action(kind="square", payload={"value": x * x})

        grammar = MyGrammar()
        grammar.execute('map(@square, data)')
        ```
    """

    @verb
    def map(self, _positional=None, _context=None):
        """
        Map a function over data.

        Usage: map(@function, data)

        Args:
            _positional: List containing [function, data] or single value
            _context: Execution context

        Returns:
            Action with kind="map" and payload containing func and data
        """
        if isinstance(_positional, list) and len(_positional) >= 2:
            func, data = _positional[0], _positional[1]
        else:
            func, data = _positional, None

        func_name = func.__name__ if callable(func) else func
        return Action(kind="map", payload={"func": func_name, "data": data, "_func_ref": func})

    @verb
    def filter(self, _positional=None, _context=None):
        """
        Filter data using a predicate function.

        Usage: filter(@predicate, data)

        Args:
            _positional: List containing [predicate, data] or single value
            _context: Execution context

        Returns:
            Action with kind="filter" and payload containing predicate and data
        """
        if isinstance(_positional, list) and len(_positional) >= 2:
            predicate, data = _positional[0], _positional[1]
        else:
            predicate, data = _positional, None

        pred_name = predicate.__name__ if callable(predicate) else predicate
        return Action(
            kind="filter",
            payload={"predicate": pred_name, "data": data, "_predicate_ref": predicate},
        )

    @verb
    def reduce(self, _positional=None, _context=None):
        """
        Reduce data using a function.

        Usage: reduce(@function, data, initial)

        Args:
            _positional: List containing [function, data, initial] or single value
            _context: Execution context

        Returns:
            Action with kind="reduce" and payload containing func, data, and initial
        """
        if isinstance(_positional, list):
            if len(_positional) >= 2:
                func, data = _positional[0], _positional[1]
                initial = _positional[2] if len(_positional) > 2 else None
            else:
                func, data, initial = _positional[0], None, None
        else:
            func, data, initial = _positional, None, None

        func_name = func.__name__ if callable(func) else func
        return Action(
            kind="reduce",
            payload={"func": func_name, "data": data, "initial": initial, "_func_ref": func},
        )

    @verb
    def compose(self, _positional=None, _context=None):
        """
        Compose multiple functions.

        Usage: compose(@f, @g, @h) -> returns a function that applies h, then g, then f

        Args:
            _positional: List of functions to compose
            _context: Execution context

        Returns:
            Action with kind="compose" and payload containing functions
        """
        if isinstance(_positional, list):
            functions = _positional
        else:
            functions = [_positional] if _positional else []

        func_names = [f.__name__ if callable(f) else f for f in functions]
        return Action(kind="compose", payload={"functions": func_names, "_func_refs": functions})

    @verb
    def pipe(self, _positional=None, _context=None):
        """
        Pipe data through a series of functions.

        Usage: pipe(data, @f, @g, @h) -> applies f, then g, then h to data

        Args:
            _positional: List containing [data, *functions]
            _context: Execution context

        Returns:
            Action with kind="pipe" and payload containing data and functions
        """
        if isinstance(_positional, list) and len(_positional) >= 2:
            data = _positional[0]
            functions = _positional[1:]
        else:
            data, functions = _positional, []

        func_names = [f.__name__ if callable(f) else f for f in functions]
        return Action(
            kind="pipe", payload={"data": data, "functions": func_names, "_func_refs": functions}
        )
