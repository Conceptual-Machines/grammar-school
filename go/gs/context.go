package gs

// Context represents execution context that can be passed between verb handlers.
type Context struct {
	Data map[string]interface{}
}

// NewContext creates a new empty context.
func NewContext() *Context {
	return &Context{
		Data: make(map[string]interface{}),
	}
}

// Get retrieves a value from the context.
func (c *Context) Get(key string) (interface{}, bool) {
	if c == nil {
		return nil, false
	}
	val, ok := c.Data[key]
	return val, ok
}

// Set stores a value in the context.
func (c *Context) Set(key string, value interface{}) {
	if c == nil {
		return
	}
	if c.Data == nil {
		c.Data = make(map[string]interface{})
	}
	c.Data[key] = value
}

// Args represents named arguments as a map.
type Args map[string]Value

// VerbHandler is the signature for verb handler methods.
// Returns: actions, new context (can be nil to keep current), error
type VerbHandler func(args Args, ctx *Context) ([]Action, *Context, error)

