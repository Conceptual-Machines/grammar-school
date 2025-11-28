# Runtime

The Runtime executes Actions produced by the interpreter.

## Overview

The `Runtime` is a protocol (interface) that defines how Actions are executed. You implement this protocol to define the behavior of your DSL.

## Implementing Runtime

```python
from grammar_school import Action, Runtime

class MyRuntime(Runtime):
    def execute(self, action: Action) -> None:
        if action.kind == "greet":
            name = action.payload["name"]
            print(f"Hello, {name}!")
        elif action.kind == "create_track":
            # Handle track creation
            pass
```

## Action Execution

Actions are executed in the order they're produced by the interpreter:

```python
grammar.execute('track(name="Drums").add_clip(start=0, length=8)', runtime)
```

This will:
1. Execute the `create_track` action
2. Execute the `add_clip` action

## State Management

The Runtime can maintain state across action executions:

```python
class MusicRuntime(Runtime):
    def __init__(self):
        self.tracks = []
        self.current_track = None
    
    def execute(self, action: Action) -> None:
        if action.kind == "create_track":
            self.current_track = {
                "name": action.payload["name"],
                "clips": []
            }
            self.tracks.append(self.current_track)
        elif action.kind == "add_clip":
            if self.current_track:
                self.current_track["clips"].append({
                    "start": action.payload["start"],
                    "length": action.payload["length"]
                })
```

## Error Handling

You can raise exceptions in `execute()` to handle errors:

```python
def execute(self, action: Action) -> None:
    if action.kind == "create_track":
        if action.payload["name"] in self.tracks:
            raise ValueError(f"Track {action.payload['name']} already exists")
        # ...
```

