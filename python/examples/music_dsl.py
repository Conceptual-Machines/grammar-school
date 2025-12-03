"""Example Music DSL using Grammar School."""

from grammar_school import Grammar, method


class MusicGrammar(Grammar):
    """A simple music DSL for creating tracks and clips."""

    def __init__(self):
        super().__init__()
        self.tracks = []
        self.current_track = None

    @method
    def track(self, name, color=None):
        """Create a new track."""
        track = {"name": name, "color": color, "clips": [], "muted": False}
        self.tracks.append(track)
        self.current_track = track
        print(f"Created track: {name}" + (f" (color: {color})" if color else ""))

    @method
    def add_clip(self, start, length):
        """Add a clip to the current track."""
        if self.current_track is None:
            print("Error: No track selected. Create a track first.")
            return
        clip = {"start": start, "length": length}
        self.current_track["clips"].append(clip)
        print(f"Added clip: start={start}, length={length} to track '{self.current_track['name']}'")

    @method
    def mute(self):
        """Mute the current track."""
        if self.current_track is None:
            print("Error: No track selected. Create a track first.")
            return
        self.current_track["muted"] = True
        print(f"Muted track: {self.current_track['name']}")


def main():
    """Example usage of the Music DSL."""
    grammar = MusicGrammar()

    code = 'track(name="Drums").add_clip(start=0, length=8)'
    print(f"Code: {code}")
    print("\nExecuting:")
    grammar.execute(code)

    print("\n" + "=" * 50)
    code2 = 'track(name="FX", color="blue").mute()'
    print(f"Code: {code2}")
    print("\nExecuting:")
    grammar.execute(code2)

    print("\n" + "=" * 50)
    print("Final state:")
    print(f"Tracks: {grammar.tracks}")


if __name__ == "__main__":
    main()
