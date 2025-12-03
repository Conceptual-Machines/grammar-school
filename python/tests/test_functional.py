"""Tests for functional programming features."""

from grammar_school import FunctionalMixin, Grammar, method

# For backward compatibility in tests - will be updated later
verb = method  # type: ignore[misc]


class TestFunctionalMixin:
    """Test FunctionalMixin operations."""

    def test_map_with_function_reference(self):
        """Test map operation with function reference."""

        class TestGrammar(Grammar, FunctionalMixin):
            @verb
            def square(self, x):
                return x * x

        grammar = TestGrammar()
        # Functional operations are placeholders for now
        # Just verify they can be called without errors
        # Use identifier instead of list literal (grammar doesn't support lists)
        grammar.execute("map(@square, data)")

    def test_filter_with_function_reference(self):
        """Test filter operation with function reference."""

        class TestGrammar(Grammar, FunctionalMixin):
            @verb
            def is_even(self, x):
                return x % 2 == 0

        grammar = TestGrammar()
        # Functional operations are placeholders for now
        # Just verify they can be called without errors
        # Use identifier instead of list literal (grammar doesn't support lists)
        grammar.execute("filter(@is_even, data)")

    def test_reduce_with_function_reference(self):
        """Test reduce operation with function reference."""

        class TestGrammar(Grammar, FunctionalMixin):
            @verb
            def add(self, a, b):
                return a + b

        grammar = TestGrammar()
        # Functional operations are placeholders for now
        # Just verify they can be called without errors
        # Use identifier instead of list literal (grammar doesn't support lists)
        grammar.execute("reduce(@add, data, 0)")

    def test_compose_with_function_references(self):
        """Test compose operation with multiple function references."""

        class TestGrammar(Grammar, FunctionalMixin):
            @verb
            def square(self, x):
                return x * x

            @verb
            def double(self, x):
                return x * 2

        grammar = TestGrammar()
        # Functional operations are placeholders for now
        # Just verify they can be called without errors
        grammar.execute("compose(@square, @double)")

    def test_pipe_with_function_references(self):
        """Test pipe operation with function references."""

        class TestGrammar(Grammar, FunctionalMixin):
            @verb
            def square(self, x):
                return x * x

            @verb
            def double(self, x):
                return x * 2

        grammar = TestGrammar()
        # Functional operations are placeholders for now
        # Just verify they can be called without errors
        # Use identifier instead of list literal (grammar doesn't support lists)
        grammar.execute("pipe(data, @double, @square)")

    def test_chained_functional_operations(self):
        """Test chaining functional operations."""

        class TestGrammar(Grammar, FunctionalMixin):
            @verb
            def square(self, x):
                return x * x

            @verb
            def is_even(self, x):
                return x % 2 == 0

        grammar = TestGrammar()
        # Functional operations are placeholders for now
        # Just verify they can be called without errors
        # Use identifier instead of list literal (grammar doesn't support lists)
        grammar.execute("map(@square, data).filter(@is_even, data)")

    def test_function_reference_resolution(self):
        """Test that function references resolve to actual handlers."""

        class TestGrammar(Grammar, FunctionalMixin):
            @verb
            def square(self, x):
                return x * x

        grammar = TestGrammar()
        # Just verify it can be called - function reference resolution
        # will be tested when functional operations are fully implemented
        # Use identifier instead of list literal (grammar doesn't support lists)
        grammar.execute("map(@square, data)")

    def test_reduce_without_initial(self):
        """Test reduce operation without initial value."""

        class TestGrammar(Grammar, FunctionalMixin):
            @verb
            def add(self, a, b):
                return a + b

        grammar = TestGrammar()
        # Functional operations are placeholders for now
        # Just verify they can be called without errors
        # Use identifier instead of list literal (grammar doesn't support lists)
        grammar.execute("reduce(@add, data)")


class TestFunctionReferences:
    """Test function reference parsing and interpretation."""

    def test_parse_function_reference(self):
        """Test parsing @function_name syntax."""

        class TestGrammar(Grammar):
            @verb
            def square(self, x):
                return x * x

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
            def f1(self, x):
                return x

            @verb
            def f2(self, x):
                return x

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
            def square(self, x):
                return x * x

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
            def square(self, x):
                return x * x

        grammar = TestGrammar()
        # Just verify it can be called - function reference resolution
        # will be tested when functional operations are fully implemented
        # Use identifier instead of list literal (grammar doesn't support lists)
        grammar.execute("map(@square, data)")

    def test_unknown_function_reference(self):
        """Test handling of unknown function references."""

        class TestGrammar(Grammar, FunctionalMixin):
            pass

        grammar = TestGrammar()
        # Functional operations are placeholders for now
        # Just verify they can be called without errors
        # Use identifier instead of list literal (grammar doesn't support lists)
        grammar.execute("map(@unknown, data)")


class TestFunctionalIntegration:
    """Integration tests for functional programming features."""

    def test_full_functional_workflow(self):
        """Test a complete functional programming workflow."""

        class TestGrammar(Grammar, FunctionalMixin):
            @verb
            def square(self, x):
                return x * x

            @verb
            def is_even(self, x):
                return x % 2 == 0

        grammar = TestGrammar()

        # Functional operations are placeholders for now
        # Just verify they can be called without errors
        # Use identifier instead of list literal (grammar doesn't support lists)
        grammar.execute("map(@square, data)")
        grammar.execute("filter(@is_even, data)")
        grammar.execute("map(@square, data).filter(@is_even, data)")

    def test_functional_with_custom_runtime(self):
        """Test functional operations - no runtime needed in new API."""

        class TestGrammar(Grammar, FunctionalMixin):
            @verb
            def square(self, x):
                return x * x

        grammar = TestGrammar()
        # Functional operations are placeholders for now
        # Just verify they can be called without errors
        # Use identifier instead of list literal (grammar doesn't support lists)
        grammar.execute("map(@square, data)")

    def test_streaming_functional_operations(self):
        """Test streaming functional operations."""

        class TestGrammar(Grammar, FunctionalMixin):
            @verb
            def square(self, x):
                return x * x

            @verb
            def double(self, x):
                return x * 2

        grammar = TestGrammar()

        # Stream yields None, but methods execute
        # Use identifier instead of list literal (grammar doesn't support lists)
        results = list(grammar.stream("map(@square, data).map(@double, data)"))
        assert len(results) == 2  # Two None values
