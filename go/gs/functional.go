package gs

import "fmt"

// FunctionalMixin provides functional programming operations for DSLs.
// Embed this struct in your DSL struct to get map, filter, reduce, compose, and pipe operations.
//
// Example:
//
//	type MyDSL struct {
//		FunctionalMixin
//	}
//
//	func (d *MyDSL) Square(args Args, ctx *Context) ([]Action, *Context, error) {
//		x := args["x"].Num
//		return []Action{{
//			Kind: "square",
//			Payload: map[string]interface{}{"value": x * x},
//		}}, ctx, nil
//	}
//
//	// Then use: map(@Square, data)
type FunctionalMixin struct{}

// Map maps a function over data.
// Usage: map(@function, data)
func (f *FunctionalMixin) Map(args Args, ctx *Context) ([]Action, *Context, error) {
	// Extract function reference and data from positional args
	funcRef := args["_positional_0"]
	data := args["_positional_1"]

	funcName := funcRef.Str
	if funcRef.Kind != ValueFunction {
		// Fallback to identifier if not a function reference
		funcName = funcRef.Str
	}

	action := Action{
		Kind: "map",
		Payload: map[string]interface{}{
			"func": funcName,
			"data": data,
		},
	}

	return []Action{action}, ctx, nil
}

// Filter filters data using a predicate function.
// Usage: filter(@predicate, data)
func (f *FunctionalMixin) Filter(args Args, ctx *Context) ([]Action, *Context, error) {
	predicate := args["_positional_0"]
	data := args["_positional_1"]

	predName := predicate.Str
	if predicate.Kind != ValueFunction {
		predName = predicate.Str
	}

	action := Action{
		Kind: "filter",
		Payload: map[string]interface{}{
			"predicate": predName,
			"data":      data,
		},
	}

	return []Action{action}, ctx, nil
}

// Reduce reduces data using a function.
// Usage: reduce(@function, data, initial)
func (f *FunctionalMixin) Reduce(args Args, ctx *Context) ([]Action, *Context, error) {
	funcRef := args["_positional_0"]
	data := args["_positional_1"]
	initial, hasInitial := args["_positional_2"]

	funcName := funcRef.Str
	if funcRef.Kind != ValueFunction {
		funcName = funcRef.Str
	}

	payload := map[string]interface{}{
		"func": funcName,
		"data": data,
	}
	if hasInitial {
		payload["initial"] = initial
	}

	action := Action{
		Kind:    "reduce",
		Payload: payload,
	}

	return []Action{action}, ctx, nil
}

// Compose composes multiple functions.
// Usage: compose(@f, @g, @h) -> returns a function that applies h, then g, then f
func (f *FunctionalMixin) Compose(args Args, ctx *Context) ([]Action, *Context, error) {
	var funcNames []string

	// Collect all function references from positional args
	i := 0
	for {
		arg, ok := args[positionalKey(i)]
		if !ok {
			break
		}
		funcName := arg.Str
		if arg.Kind == ValueFunction {
			funcName = arg.Str
		}
		funcNames = append(funcNames, funcName)
		i++
	}

	action := Action{
		Kind: "compose",
		Payload: map[string]interface{}{
			"functions": funcNames,
		},
	}

	return []Action{action}, ctx, nil
}

// Pipe pipes data through a series of functions.
// Usage: pipe(data, @f, @g, @h) -> applies f, then g, then h to data
func (f *FunctionalMixin) Pipe(args Args, ctx *Context) ([]Action, *Context, error) {
	data := args["_positional_0"]
	var funcNames []string

	// Collect function references starting from _positional_1
	i := 1
	for {
		arg, ok := args[positionalKey(i)]
		if !ok {
			break
		}
		funcName := arg.Str
		if arg.Kind == ValueFunction {
			funcName = arg.Str
		}
		funcNames = append(funcNames, funcName)
		i++
	}

	action := Action{
		Kind: "pipe",
		Payload: map[string]interface{}{
			"data":      data,
			"functions": funcNames,
		},
	}

	return []Action{action}, ctx, nil
}

// positionalKey returns the key for a positional argument.
func positionalKey(index int) string {
	return fmt.Sprintf("_positional_%d", index)
}
