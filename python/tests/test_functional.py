"""Tests for functional programming features."""

from grammar_school import Action, FunctionalMixin, Grammar, verb


class TestFunctionalMixin:
    """Test FunctionalMixin operations."""

    def test_map_with_function_reference(self):
        """Test map operation with function reference."""

        class TestGrammar(Grammar, FunctionalMixin):
            @verb
            def square(self, x, _context=None):
                return Action(kind="square", payload={"value": x * x})

        grammar = TestGrammar()
        actions = grammar.compile("map(@square, data)")

        assert len(actions) == 1
        assert actions[0].kind == "map"
        assert actions[0].payload["func"] == "square"
        assert actions[0].payload["data"] == "data"
        assert "_func_ref" in actions[0].payload

    def test_filter_with_function_reference(self):
        """Test filter operation with function reference."""

        class TestGrammar(Grammar, FunctionalMixin):
            @verb
            def is_even(self, x, _context=None):
                return Action(kind="is_even", payload={"value": x % 2 == 0})

        grammar = TestGrammar()
        actions = grammar.compile("filter(@is_even, data)")

        assert len(actions) == 1
        assert actions[0].kind == "filter"
        assert actions[0].payload["predicate"] == "is_even"
        assert actions[0].payload["data"] == "data"
        assert "_predicate_ref" in actions[0].payload

    def test_reduce_with_function_reference(self):
        """Test reduce operation with function reference."""

        class TestGrammar(Grammar, FunctionalMixin):
            @verb
            def add(self, a, b, _context=None):
                return Action(kind="add", payload={"result": a + b})

        grammar = TestGrammar()
        actions = grammar.compile("reduce(@add, data, 0)")

        assert len(actions) == 1
        assert actions[0].kind == "reduce"
        assert actions[0].payload["func"] == "add"
        assert actions[0].payload["data"] == "data"
        assert actions[0].payload["initial"] == 0
        assert "_func_ref" in actions[0].payload

    def test_compose_with_function_references(self):
        """Test compose operation with multiple function references."""

        class TestGrammar(Grammar, FunctionalMixin):
            @verb
            def square(self, x, _context=None):
                return Action(kind="square", payload={"value": x * x})

            @verb
            def double(self, x, _context=None):
                return Action(kind="double", payload={"value": x * 2})

        grammar = TestGrammar()
        actions = grammar.compile("compose(@square, @double)")

        assert len(actions) == 1
        assert actions[0].kind == "compose"
        assert actions[0].payload["functions"] == ["square", "double"]
        assert len(actions[0].payload["_func_refs"]) == 2

    def test_pipe_with_function_references(self):
        """Test pipe operation with function references."""

        class TestGrammar(Grammar, FunctionalMixin):
            @verb
            def square(self, x, _context=None):
                return Action(kind="square", payload={"value": x * x})

            @verb
            def double(self, x, _context=None):
                return Action(kind="double", payload={"value": x * 2})

        grammar = TestGrammar()
        actions = grammar.compile("pipe(data, @double, @square)")

        assert len(actions) == 1
        assert actions[0].kind == "pipe"
        assert actions[0].payload["data"] == "data"
        assert actions[0].payload["functions"] == ["double", "square"]
        assert len(actions[0].payload["_func_refs"]) == 2

    def test_chained_functional_operations(self):
        """Test chaining functional operations."""

        class TestGrammar(Grammar, FunctionalMixin):
            @verb
            def square(self, x, _context=None):
                return Action(kind="square", payload={"value": x * x})

            @verb
            def is_even(self, x, _context=None):
                return Action(kind="is_even", payload={"value": x % 2 == 0})

        grammar = TestGrammar()
        actions = grammar.compile("map(@square, data).filter(@is_even, data)")

        assert len(actions) == 2
        assert actions[0].kind == "map"
        assert actions[0].payload["func"] == "square"
        assert actions[1].kind == "filter"
        assert actions[1].payload["predicate"] == "is_even"

    def test_function_reference_resolution(self):
        """Test that function references resolve to actual handlers."""

        class TestGrammar(Grammar, FunctionalMixin):
            @verb
            def square(self, x, _context=None):
                return Action(kind="square", payload={"value": x * x})

        grammar = TestGrammar()
        actions = grammar.compile("map(@square, data)")

        # Check that the function reference is resolved to the actual method
        func_ref = actions[0].payload["_func_ref"]
        assert callable(func_ref)
        assert func_ref.__name__ == "square"

    def test_reduce_without_initial(self):
        """Test reduce operation without initial value."""

        class TestGrammar(Grammar, FunctionalMixin):
            @verb
            def add(self, a, b, _context=None):
                return Action(kind="add", payload={"result": a + b})

        grammar = TestGrammar()
        actions = grammar.compile("reduce(@add, data)")

        assert len(actions) == 1
        assert actions[0].kind == "reduce"
        assert actions[0].payload["func"] == "add"
        assert actions[0].payload["data"] == "data"
        assert actions[0].payload["initial"] is None


class TestFunctionReferences:
    """Test function reference parsing and interpretation."""

    def test_parse_function_reference(self):
        """Test parsing @function_name syntax."""

        class TestGrammar(Grammar):
            @verb
            def square(self, x, _context=None):
                return Action(kind="square", payload={"value": x * x})

        grammar = TestGrammar()
        call_chain = grammar.parse("map(@square, data)")

        assert len(call_chain.calls) == 1
        call = call_chain.calls[0]
        assert call.name == "map"
        assert len(call.args) == 2

        # Check first argument is a function reference
        first_arg = call.args["_positional_0"]
        assert first_arg.kind == "function"
        assert first_arg.value == "square"

        # Check second argument is an identifier
        second_arg = call.args["_positional_1"]
        assert second_arg.kind == "identifier"
        assert second_arg.value == "data"

    def test_function_reference_in_multiple_args(self):
        """Test function references in multiple arguments."""

        class TestGrammar(Grammar):
            @verb
            def f1(self, x, _context=None):
                return Action(kind="f1", payload={"value": x})

            @verb
            def f2(self, x, _context=None):
                return Action(kind="f2", payload={"value": x})

        grammar = TestGrammar()
        call_chain = grammar.parse("compose(@f1, @f2)")

        assert len(call_chain.calls) == 1
        call = call_chain.calls[0]
        assert call.name == "compose"

        # Both arguments should be function references
        first_arg = call.args["_positional_0"]
        assert first_arg.kind == "function"
        assert first_arg.value == "f1"

        second_arg = call.args["_positional_1"]
        assert second_arg.kind == "function"
        assert second_arg.value == "f2"

    def test_function_reference_with_regular_args(self):
        """Test mixing function references with regular arguments."""

        class TestGrammar(Grammar):
            @verb
            def square(self, x, _context=None):
                return Action(kind="square", payload={"value": x * x})

        grammar = TestGrammar()
        call_chain = grammar.parse("map(@square, data, extra=123)")

        assert len(call_chain.calls) == 1
        call = call_chain.calls[0]
        assert call.name == "map"

        # Positional args
        assert call.args["_positional_0"].kind == "function"
        assert call.args["_positional_1"].kind == "identifier"

        # Named arg
        assert call.args["extra"].kind == "number"
        assert call.args["extra"].value == 123

    def test_function_reference_resolution_in_interpreter(self):
        """Test that interpreter resolves function references correctly."""

        class TestGrammar(Grammar, FunctionalMixin):
            @verb
            def square(self, x, _context=None):
                return Action(kind="square", payload={"value": x * x})

        grammar = TestGrammar()
        actions = grammar.compile("map(@square, data)")

        # The function reference should be resolved to the actual handler
        func_ref = actions[0].payload["_func_ref"]
        assert callable(func_ref)

        # Verify it's the square method
        assert func_ref.__name__ == "square"
        assert hasattr(func_ref, "__self__")  # It's a bound method

    def test_unknown_function_reference(self):
        """Test handling of unknown function references."""

        class TestGrammar(Grammar, FunctionalMixin):
            pass

        grammar = TestGrammar()
        actions = grammar.compile("map(@unknown, data)")

        # Should still work, but function reference won't be resolved
        assert len(actions) == 1
        assert actions[0].kind == "map"
        assert actions[0].payload["func"] == "unknown"
        # _func_ref should be the string "unknown" since it's not found
        assert actions[0].payload["_func_ref"] == "unknown"


class TestFunctionalIntegration:
    """Integration tests for functional programming features."""

    def test_full_functional_workflow(self):
        """Test a complete functional programming workflow."""

        class TestGrammar(Grammar, FunctionalMixin):
            @verb
            def square(self, x, _context=None):
                return Action(kind="square", payload={"value": x * x})

            @verb
            def is_even(self, x, _context=None):
                return Action(kind="is_even", payload={"value": x % 2 == 0})

        grammar = TestGrammar()

        # Test map
        actions = grammar.compile("map(@square, numbers)")
        assert actions[0].kind == "map"
        assert actions[0].payload["func"] == "square"

        # Test filter
        actions = grammar.compile("filter(@is_even, numbers)")
        assert actions[0].kind == "filter"
        assert actions[0].payload["predicate"] == "is_even"

        # Test chaining
        actions = grammar.compile("map(@square, numbers).filter(@is_even, numbers)")
        assert len(actions) == 2
        assert actions[0].kind == "map"
        assert actions[1].kind == "filter"

    def test_functional_with_custom_runtime(self):
        """Test functional operations with custom runtime."""

        class TestRuntime:
            def __init__(self):
                self.executed_actions = []

            def execute(self, action: Action) -> None:
                self.executed_actions.append(action)

        class TestGrammar(Grammar, FunctionalMixin):
            @verb
            def square(self, x, _context=None):
                return Action(kind="square", payload={"value": x * x})

        runtime = TestRuntime()
        grammar = TestGrammar(runtime=runtime)

        grammar.execute("map(@square, data)")

        assert len(runtime.executed_actions) == 1
        assert runtime.executed_actions[0].kind == "map"

    def test_streaming_functional_operations(self):
        """Test streaming functional operations."""

        class TestGrammar(Grammar, FunctionalMixin):
            @verb
            def square(self, x, _context=None):
                return Action(kind="square", payload={"value": x * x})

            @verb
            def double(self, x, _context=None):
                return Action(kind="double", payload={"value": x * 2})

        grammar = TestGrammar()

        actions = list(grammar.stream("map(@square, data).map(@double, data)"))

        assert len(actions) == 2
        assert actions[0].kind == "map"
        assert actions[0].payload["func"] == "square"
        assert actions[1].kind == "map"
        assert actions[1].payload["func"] == "double"
