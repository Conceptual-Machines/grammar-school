# Runtime (Internal Architecture)

**Note:** With the unified `@method` interface, you don't need to implement Runtime. Methods execute directly. This page documents the internal architecture for advanced users.

## Overview

Internally, Grammar School maintains a two-layer architecture:
1. **Grammar layer**: Parses DSL and calls methods
2. **Runtime layer**: Executes methods (handled automatically)

When using `@method`, the Runtime layer is handled automatically - you just write methods with their implementation.

## Using @method (Recommended)

With `@method`, you don't need Runtime:

```python
from grammar_school import Grammar, method

class MyDSL(Grammar):
    def __init__(self):
        super().__init__()
        self.tracks = []

    @method
    def track(self, name):
        # Implementation runs directly
        self.tracks.append({"name": name})
        print(f"Created track: {name}")

dsl = MyDSL()
dsl.execute('track(name="Drums")')  # No runtime needed!
```

## Internal Architecture

The `Runtime` protocol still exists internally, but is handled automatically when using `@method`. The framework:
1. Parses DSL code
2. Calls your `@method` handlers directly
3. Methods execute immediately

You can manage state using `self` attributes in your Grammar class.
