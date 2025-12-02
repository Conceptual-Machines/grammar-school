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
//	func (d *MyDSL) Square(args Args) error {
//		x := args["x"].Num
//		fmt.Printf("Square: %v\n", x*x)
//		return nil
//	}
//
//	// Then use: map(@Square, data)
type FunctionalMixin struct{}

// Map maps a function over data.
// Usage: map(@function, data)
func (f *FunctionalMixin) Map(args Args) error {
	// Extract function reference and data from positional args
	funcRef := args["_positional_0"]
	data := args["_positional_1"]

	funcName := funcRef.Str
	// TODO: Actually call the function on each element of data
	// For now, just a placeholder - functional operations need special handling
	fmt.Printf("Map %s over %v\n", funcName, data)
	return nil
}

// Filter filters data using a predicate function.
// Usage: filter(@predicate, data)
func (f *FunctionalMixin) Filter(args Args) error {
	predicate := args["_positional_0"]
	data := args["_positional_1"]

	predName := predicate.Str
	// TODO: Actually call the predicate on each element of data
	// For now, just a placeholder - functional operations need special handling
	fmt.Printf("Filter %s over %v\n", predName, data)
	return nil
}

// Reduce reduces data using a function.
// Usage: reduce(@function, data, initial)
func (f *FunctionalMixin) Reduce(args Args) error {
	funcRef := args["_positional_0"]
	data := args["_positional_1"]
	initial, hasInitial := args["_positional_2"]

	funcName := funcRef.Str
	// TODO: Actually call the function to reduce data
	// For now, just a placeholder - functional operations need special handling
	if hasInitial {
		fmt.Printf("Reduce %s over %v with initial %v\n", funcName, data, initial)
	} else {
		fmt.Printf("Reduce %s over %v\n", funcName, data)
	}
	return nil
}

// Compose composes multiple functions.
// Usage: compose(@f, @g, @h) -> returns a function that applies h, then g, then f
func (f *FunctionalMixin) Compose(args Args) error {
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

	// TODO: Actually compose the functions
	// For now, just a placeholder - functional operations need special handling
	fmt.Printf("Compose functions: %v\n", funcNames)
	return nil
}

// Pipe pipes data through a series of functions.
// Usage: pipe(data, @f, @g, @h) -> applies f, then g, then h to data
func (f *FunctionalMixin) Pipe(args Args) error {
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

	// TODO: Actually pipe data through functions
	// For now, just a placeholder - functional operations need special handling
	fmt.Printf("Pipe %v through functions: %v\n", data, funcNames)
	return nil
}

// positionalKey returns the key for a positional argument.
func positionalKey(index int) string {
	return fmt.Sprintf("_positional_%d", index)
}
