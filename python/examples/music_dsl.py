"""Example Music DSL using Grammar School."""

from grammar_school import Action, Grammar, Runtime, verb


class MusicGrammar(Grammar):
    """A simple music DSL for creating tracks and clips."""

    @verb
    def track(self, name, color=None, _context=None):
        """Create a new track."""
        return Action(kind="create_track", payload={"name": name, "color": color})

    @verb
    def add_clip(self, start, length, _context=None):
        """Add a clip to the current track."""
        return Action(kind="add_clip", payload={"start": start, "length": length})

    @verb
    def mute(self, _context=None):
        """Mute the current track."""
        return Action(kind="mute_track", payload={})


class MusicRuntime(Runtime):
    """Simple runtime that prints actions."""

    def execute(self, action: Action) -> None:
        print(f"Executing: {action.kind} with payload: {action.payload}")


def main():
    """Example usage of the Music DSL."""
    # Using custom runtime
    grammar = MusicGrammar(runtime=MusicRuntime())

    # Or use default runtime (just prints actions):
    # grammar = MusicGrammar()

    code = 'track(name="Drums").add_clip(start=0, length=8)'
    print(f"Code: {code}")
    print("\nExecuting:")
    grammar.execute(code)

    print("\n" + "=" * 50)
    code2 = 'track(name="FX", color="blue").mute()'
    print(f"Code: {code2}")
    print("\nExecuting:")
    grammar.execute(code2)


if __name__ == "__main__":
    main()
