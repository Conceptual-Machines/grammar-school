package gs

import (
	"context"
	"fmt"
	"reflect"
)

// Engine is the main Grammar School engine that orchestrates parsing, interpretation, and execution.
// It corresponds to the Grammar class in Python.
//
// The Engine uses a two-layer architecture:
// 1. Verb handlers (methods on the DSL struct): Transform DSL syntax → Actions (pure, no side effects)
// 2. Runtime: Execute Actions → Real world effects (side effects, state management)
//
// This separation allows:
// - Same Engine to work with different Runtimes (testing, production, mocking)
// - Verb handlers to be pure and easily testable
// - Runtime to manage state independently of Engine logic
type Engine struct {
	grammar string
	parser  Parser
	verbs   map[string]VerbHandler
	dsl     interface{}
	runtime Runtime // Runtime is stored internally, like in Python
}

// NewEngine creates a new Engine with the given grammar, DSL instance, parser, and optional runtime.
// If runtime is nil, a default runtime that prints actions is used.
func NewEngine(grammar string, dsl interface{}, parser Parser, runtime Runtime) (*Engine, error) {
	engine := &Engine{
		grammar: grammar,
		parser:  parser,
		verbs:   make(map[string]VerbHandler),
		dsl:     dsl,
		runtime: runtime,
	}

	// Use default runtime if none provided (like Python)
	if engine.runtime == nil {
		engine.runtime = &DefaultRuntime{}
	}

	if err := engine.collectVerbs(); err != nil {
		return nil, fmt.Errorf("failed to collect verbs: %w", err)
	}

	return engine, nil
}

// collectVerbs uses reflection to find all methods on the DSL instance
// that match the VerbHandler signature and register them.
func (e *Engine) collectVerbs() error {
	dslType := reflect.TypeOf(e.dsl)
	dslValue := reflect.ValueOf(e.dsl)

	if dslType.Kind() == reflect.Ptr {
		dslType = dslType.Elem()
		dslValue = dslValue.Elem()
	}

	if dslType.Kind() != reflect.Struct {
		return fmt.Errorf("DSL must be a struct or pointer to struct")
	}

	for i := 0; i < dslType.NumMethod(); i++ {
		method := dslType.Method(i)
		methodType := method.Type

		if methodType.NumIn() != 3 || methodType.NumOut() != 3 {
			continue
		}

		if methodType.In(1) != reflect.TypeOf(Args{}) {
			continue
		}

		if methodType.In(2) != reflect.TypeOf((*Context)(nil)) {
			continue
		}

		if methodType.Out(0) != reflect.TypeOf([]Action{}) {
			continue
		}

		if methodType.Out(1) != reflect.TypeOf((*Context)(nil)) {
			continue
		}

		if methodType.Out(2) != reflect.TypeOf((*error)(nil)).Elem() {
			continue
		}

		methodValue := dslValue.Method(i)
		e.verbs[method.Name] = func(args Args, ctx *Context) ([]Action, *Context, error) {
			results := methodValue.Call([]reflect.Value{
				reflect.ValueOf(args),
				reflect.ValueOf(ctx),
			})

			actions := results[0].Interface().([]Action)
			newCtx := results[1].Interface().(*Context)
			var err error
			if !results[2].IsNil() {
				err = results[2].Interface().(error)
			}

			return actions, newCtx, err
		}
	}

	return nil
}

// Compile parses and interprets DSL code into a list of Actions.
func (e *Engine) Compile(code string) ([]Action, error) {
	callChain, err := e.parser.Parse(code)
	if err != nil {
		return nil, fmt.Errorf("parse error: %w", err)
	}

	return e.interpret(callChain)
}

// Stream parses DSL code and returns a channel that streams Actions as they're generated.
// This allows for memory-efficient processing and real-time execution of large DSL programs.
//
// The channel will be closed when all actions have been generated or an error occurs.
// If an error occurs, it will be sent on the error channel before closing.
//
// Example:
//
//	actions, errors := engine.Stream(`track(name="A").track(name="B")`)
//	for {
//	  select {
//	  case action, ok := <-actions:
//	    if !ok {
//	      return
//	    }
//	    fmt.Printf("Got action: %s\n", action.Kind)
//	  case err := <-errors:
//	    if err != nil {
//	      log.Fatal(err)
//	    }
//	  }
//	}
func (e *Engine) Stream(code string) (<-chan Action, <-chan error) {
	actions := make(chan Action)
	errors := make(chan error, 1)

	go func() {
		defer close(actions)
		defer close(errors)

		callChain, err := e.parser.Parse(code)
		if err != nil {
			errors <- fmt.Errorf("parse error: %w", err)
			return
		}

		if err := e.interpretStream(callChain, actions); err != nil {
			errors <- err
		}
	}()

	return actions, errors
}

// interpret walks the CallChain and dispatches to verb handlers.
func (e *Engine) interpret(callChain *CallChain) ([]Action, error) {
	var actions []Action
	ctx := NewContext()

	for _, call := range callChain.Calls {
		handler, ok := e.verbs[call.Name]
		if !ok {
			return nil, fmt.Errorf("unknown verb: %s", call.Name)
		}

		args := make(Args)
		for _, arg := range call.Args {
			args[arg.Name] = arg.Value
		}

		callActions, newCtx, err := handler(args, ctx)
		if err != nil {
			return nil, fmt.Errorf("verb handler %s error: %w", call.Name, err)
		}

		actions = append(actions, callActions...)
		if newCtx != nil {
			ctx = newCtx
		}
	}

	return actions, nil
}

// interpretStream walks the CallChain and streams Actions to the provided channel.
func (e *Engine) interpretStream(callChain *CallChain, actions chan<- Action) error {
	ctx := NewContext()

	for _, call := range callChain.Calls {
		handler, ok := e.verbs[call.Name]
		if !ok {
			return fmt.Errorf("unknown verb: %s", call.Name)
		}

		args := make(Args)
		for _, arg := range call.Args {
			args[arg.Name] = arg.Value
		}

		callActions, newCtx, err := handler(args, ctx)
		if err != nil {
			return fmt.Errorf("verb handler %s error: %w", call.Name, err)
		}

		// Stream actions as they're generated
		for _, action := range callActions {
			actions <- action
		}

		if newCtx != nil {
			ctx = newCtx
		}
	}

	return nil
}

// Execute executes a plan of actions using the engine's runtime.
// If a runtime is provided, it overrides the engine's default runtime for this call.
func (e *Engine) Execute(ctx context.Context, plan []Action, runtime ...Runtime) error {
	rt := e.runtime
	if len(runtime) > 0 && runtime[0] != nil {
		rt = runtime[0]
	}

	if rt == nil {
		return fmt.Errorf("no runtime available")
	}

	for _, action := range plan {
		if err := rt.ExecuteAction(ctx, action); err != nil {
			return fmt.Errorf("execute action %s error: %w", action.Kind, err)
		}
	}
	return nil
}
