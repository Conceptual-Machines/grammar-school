# Python Core Types

Detailed documentation of core types in the Grammar School Python implementation.

## AST Types

### Value

Represents a value in the AST (number, string, identifier, bool).

```python
@dataclass
class Value:
    kind: str  # "number" | "string" | "identifier" | "bool"
    value: Any
```

**Example:**
```python
value = Value(kind="string", value="hello")
```

### Arg

Represents a named argument to a call.

```python
@dataclass
class Arg:
    name: str
    value: Value
```

**Example:**
```python
arg = Arg(name="name", value=Value(kind="string", value="Alice"))
```

### Call

Represents a single function call with named arguments.

```python
@dataclass
class Call:
    name: str
    args: dict[str, Value]
```

**Example:**
```python
call = Call(
    name="greet",
    args={"name": Value(kind="string", value="Alice")}
)
```

### CallChain

Represents a chain of calls connected by dots (method chaining).

```python
@dataclass
class CallChain:
    calls: list[Call]
```

**Example:**
```python
chain = CallChain(calls=[
    Call(name="track", args={}),
    Call(name="add_clip", args={})
])
```

## Runtime Types

### Action

Represents a runtime action produced by the interpreter.

```python
@dataclass
class Action:
    kind: str
    payload: dict[str, Any]
```

**Example:**
```python
action = Action(
    kind="create_track",
    payload={"name": "Drums", "color": "blue"}
)
```

### Runtime

Protocol for executing actions.

```python
class Runtime(Protocol):
    def execute(self, action: Action) -> None:
        ...
```

**Example:**
```python
class MyRuntime(Runtime):
    def execute(self, action: Action) -> None:
        if action.kind == "create_track":
            # Handle track creation
            pass
```

