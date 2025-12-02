"""Tests for Grammar class."""

from grammar_school import Grammar, method
from grammar_school.runtime import Action, Runtime

# For backward compatibility in tests - will be updated later
verb = method  # type: ignore[misc]


class TestGrammar:
    """Test Grammar class."""

    def test_grammar_with_default_runtime(self):
        """Test grammar with default runtime."""

        class TestGrammar(Grammar):
            @verb
            def greet(self, name, _context=None):
                return Action(kind="greet", payload={"name": name})

        grammar = TestGrammar()
        # Default runtime should print to stdout
        # We can't easily test stdout, but we can verify it doesn't crash
        grammar.execute('greet(name="World")')

    def test_grammar_with_custom_runtime(self):
        """Test grammar with custom runtime."""

        class TestRuntime(Runtime):
            def __init__(self):
                self.actions = []

            def execute(self, action: Action) -> None:
                self.actions.append(action)

        class TestGrammar(Grammar):
            @verb
            def greet(self, name, _context=None):
                return Action(kind="greet", payload={"name": name})

        runtime = TestRuntime()
        grammar = TestGrammar(runtime=runtime)
        grammar.execute('greet(name="World")')

        assert len(runtime.actions) == 1
        assert runtime.actions[0].kind == "greet"
        assert runtime.actions[0].payload["name"] == "World"

    def test_grammar_parse(self):
        """Test grammar parse method."""

        class TestGrammar(Grammar):
            @verb
            def greet(self, name, _context=None):
                return Action(kind="greet", payload={"name": name})

        grammar = TestGrammar()
        call_chain = grammar.parse('greet(name="World")')

        assert call_chain is not None
        assert len(call_chain.calls) == 1
        assert call_chain.calls[0].name == "greet"

    def test_grammar_compile(self):
        """Test grammar compile method."""

        class TestGrammar(Grammar):
            @verb
            def greet(self, name, _context=None):
                return Action(kind="greet", payload={"name": name})

        grammar = TestGrammar()
        actions = grammar.compile('greet(name="World")')

        assert len(actions) == 1
        assert actions[0].kind == "greet"
        assert actions[0].payload["name"] == "World"

    def test_grammar_stream(self):
        """Test grammar stream method."""

        class TestGrammar(Grammar):
            @verb
            def track(self, name, _context=None):
                return Action(kind="track", payload={"name": name})

        grammar = TestGrammar()
        actions = list(grammar.stream('track(name="A").track(name="B")'))

        assert len(actions) == 2
        assert actions[0].kind == "track"
        assert actions[0].payload["name"] == "A"
        assert actions[1].kind == "track"
        assert actions[1].payload["name"] == "B"

    def test_grammar_execute_with_string(self):
        """Test grammar execute with string code."""

        class TestRuntime(Runtime):
            def __init__(self):
                self.actions = []

            def execute(self, action: Action) -> None:
                self.actions.append(action)

        class TestGrammar(Grammar):
            @verb
            def greet(self, name, _context=None):
                return Action(kind="greet", payload={"name": name})

        runtime = TestRuntime()
        grammar = TestGrammar(runtime=runtime)
        grammar.execute('greet(name="World")')

        assert len(runtime.actions) == 1

    def test_grammar_execute_with_action_list(self):
        """Test grammar execute with action list."""

        class TestRuntime(Runtime):
            def __init__(self):
                self.actions = []

            def execute(self, action: Action) -> None:
                self.actions.append(action)

        class TestGrammar(Grammar):
            @verb
            def greet(self, name, _context=None):
                return Action(kind="greet", payload={"name": name})

        runtime = TestRuntime()
        grammar = TestGrammar(runtime=runtime)
        actions = [
            Action(kind="greet", payload={"name": "World"}),
            Action(kind="greet", payload={"name": "Universe"}),
        ]
        grammar.execute(actions)

        assert len(runtime.actions) == 2
        assert runtime.actions[0].payload["name"] == "World"
        assert runtime.actions[1].payload["name"] == "Universe"

    def test_grammar_multiple_verbs(self):
        """Test grammar with multiple verbs."""

        class TestGrammar(Grammar):
            @verb
            def greet(self, name, _context=None):
                return Action(kind="greet", payload={"name": name})

            @verb
            def farewell(self, name, _context=None):
                return Action(kind="farewell", payload={"name": name})

        grammar = TestGrammar()
        actions = grammar.compile('greet(name="Hello").farewell(name="Goodbye")')

        assert len(actions) == 2
        assert actions[0].kind == "greet"
        assert actions[1].kind == "farewell"

    def test_grammar_chained_calls(self):
        """Test grammar with chained method calls."""

        class TestGrammar(Grammar):
            @verb
            def track(self, name, _context=None):
                return Action(kind="track", payload={"name": name})

            @verb
            def add_clip(self, start, end, _context=None):
                return Action(kind="add_clip", payload={"start": start, "end": end})

        grammar = TestGrammar()
        actions = grammar.compile('track(name="A").add_clip(start=0, end=10)')

        assert len(actions) == 2
        assert actions[0].kind == "track"
        assert actions[1].kind == "add_clip"
        assert actions[1].payload["start"] == 0
        assert actions[1].payload["end"] == 10
