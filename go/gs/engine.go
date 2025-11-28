package gs

import (
	"context"
	"fmt"
	"reflect"
)

// Engine is the main Grammar School engine that orchestrates parsing, interpretation, and execution.
type Engine struct {
	grammar string
	parser  Parser
	verbs   map[string]VerbHandler
	dsl     interface{}
}

// NewEngine creates a new Engine with the given grammar, DSL instance, and parser.
func NewEngine(grammar string, dsl interface{}, parser Parser) (*Engine, error) {
	engine := &Engine{
		grammar: grammar,
		parser:  parser,
		verbs:   make(map[string]VerbHandler),
		dsl:     dsl,
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

// Execute executes a plan of actions using the given runtime.
func (e *Engine) Execute(ctx context.Context, runtime Runtime, plan []Action) error {
	for _, action := range plan {
		if err := runtime.ExecuteAction(ctx, action); err != nil {
			return fmt.Errorf("execute action %s error: %w", action.Kind, err)
		}
	}
	return nil
}
