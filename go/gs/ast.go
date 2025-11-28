package gs

// ValueKind represents the type of a value.
type ValueKind int

const (
	ValueNumber ValueKind = iota
	ValueString
	ValueIdentifier
	ValueBool
)

// Value represents a value in the AST (number, string, identifier, etc.).
type Value struct {
	Kind ValueKind
	Num  float64
	Str  string
	Bool bool
}

// Arg represents a named argument to a call.
type Arg struct {
	Name  string
	Value Value
}

// Call represents a single function call with named arguments.
type Call struct {
	Name string
	Args []Arg
}

// CallChain represents a chain of calls connected by dots (method chaining).
type CallChain struct {
	Calls []Call
}

