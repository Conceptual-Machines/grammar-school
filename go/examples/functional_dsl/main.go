package main

import (
	"context"
	"fmt"
	"grammar-school/gs"
	"strings"
)

// FunctionalDSL demonstrates functional programming patterns using FunctionalMixin.
type FunctionalDSL struct {
	gs.FunctionalMixin
}

// Square squares a number.
func (d *FunctionalDSL) Square(args gs.Args, ctx *gs.Context) ([]gs.Action, *gs.Context, error) {
	x := args["x"].Num
	action := gs.Action{
		Kind: "square",
		Payload: map[string]interface{}{
			"value": x * x,
		},
	}
	return []gs.Action{action}, ctx, nil
}

// Double doubles a number.
func (d *FunctionalDSL) Double(args gs.Args, ctx *gs.Context) ([]gs.Action, *gs.Context, error) {
	x := args["x"].Num
	action := gs.Action{
		Kind: "double",
		Payload: map[string]interface{}{
			"value": x * 2,
		},
	}
	return []gs.Action{action}, ctx, nil
}

// IsEven checks if a number is even.
func (d *FunctionalDSL) IsEven(args gs.Args, ctx *gs.Context) ([]gs.Action, *gs.Context, error) {
	x := args["x"].Num
	action := gs.Action{
		Kind: "is_even",
		Payload: map[string]interface{}{
			"value": int(x)%2 == 0,
		},
	}
	return []gs.Action{action}, ctx, nil
}

// FunctionalRuntime executes functional operations.
type FunctionalRuntime struct{}

func (r *FunctionalRuntime) ExecuteAction(ctx context.Context, a gs.Action) error {
	switch a.Kind {
	case "map":
		funcName := a.Payload["func"].(string)
		fmt.Printf("Map %s over data\n", funcName)
	case "filter":
		predicate := a.Payload["predicate"].(string)
		fmt.Printf("Filter data using %s\n", predicate)
	case "reduce":
		funcName := a.Payload["func"].(string)
		fmt.Printf("Reduce data using %s\n", funcName)
	case "compose":
		funcs := a.Payload["functions"].([]string)
		fmt.Printf("Compose functions: %v\n", funcs)
	case "pipe":
		funcs := a.Payload["functions"].([]string)
		fmt.Printf("Pipe data through: %v\n", funcs)
	default:
		fmt.Printf("Action: %s with payload: %v\n", a.Kind, a.Payload)
	}
	return nil
}

// FunctionalParser is a placeholder parser.
type FunctionalParser struct{}

func (p *FunctionalParser) Parse(input string) (*gs.CallChain, error) {
	return nil, fmt.Errorf("parser not implemented - use a real parser backend")
}

func main() {
	dsl := &FunctionalDSL{}
	parser := &FunctionalParser{}
	runtime := &FunctionalRuntime{}

	_, err := gs.NewEngine("", dsl, parser, runtime)
	if err != nil {
		fmt.Printf("Error creating engine: %v\n", err)
		return
	}

	fmt.Println(strings.Repeat("=", 60))
	fmt.Println("Functional DSL Examples")
	fmt.Println(strings.Repeat("=", 60))

	// Note: These examples won't run without a real parser that supports
	// function references (@function_name syntax)
	fmt.Println("\nFunctional operations available:")
	fmt.Println("  - map(@Square, data)")
	fmt.Println("  - filter(@IsEven, data)")
	fmt.Println("  - reduce(@Add, data, 0)")
	fmt.Println("  - compose(@Square, @Double)")
	fmt.Println("  - pipe(data, @Double, @Square)")

	// Once parser is implemented, you could do:
	// actions, _ := engine.Compile("map(@Square, data)")
	// engine.Execute(context.Background(), actions)
}
