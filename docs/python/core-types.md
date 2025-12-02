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

## Method Decorators

### @method

Decorator to mark a method as a DSL handler. Methods contain their implementation directly.

```python
@method
def greet(self, name):
    print(f"Hello, {name}!")
```

**Note:** The `Action` and `Runtime` types still exist internally for the two-layer architecture, but users don't need to interact with them directly when using `@method`.
