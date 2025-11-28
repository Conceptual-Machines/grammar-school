package main

import (
	"context"
	"fmt"
	"grammar-school/gs"
)

// MusicDSL is a simple music DSL for creating tracks and clips.
type MusicDSL struct{}

// Track creates a new track.
func (d *MusicDSL) Track(args gs.Args, ctx *gs.Context) ([]gs.Action, *gs.Context, error) {
	name := args["name"].Str
	color := ""
	if c, ok := args["color"]; ok {
		color = c.Str
	}

	action := gs.Action{
		Kind: "create_track",
		Payload: map[string]interface{}{
			"name":  name,
			"color": color,
		},
	}

	return []gs.Action{action}, ctx, nil
}

// AddClip adds a clip to the current track.
func (d *MusicDSL) AddClip(args gs.Args, ctx *gs.Context) ([]gs.Action, *gs.Context, error) {
	start := args["start"].Num
	length := args["length"].Num

	action := gs.Action{
		Kind: "add_clip",
		Payload: map[string]interface{}{
			"start":  start,
			"length": length,
		},
	}

	return []gs.Action{action}, ctx, nil
}

// Mute mutes the current track.
func (d *MusicDSL) Mute(args gs.Args, ctx *gs.Context) ([]gs.Action, *gs.Context, error) {
	action := gs.Action{
		Kind:    "mute_track",
		Payload: map[string]interface{}{},
	}

	return []gs.Action{action}, ctx, nil
}

// MusicRuntime is a simple runtime that prints actions.
type MusicRuntime struct{}

func (r *MusicRuntime) ExecuteAction(ctx context.Context, a gs.Action) error {
	fmt.Printf("Executing: %s with payload: %v\n", a.Kind, a.Payload)
	return nil
}

// SimpleParser is a placeholder parser (would need actual implementation).
type SimpleParser struct{}

func (p *SimpleParser) Parse(input string) (*gs.CallChain, error) {
	// This is a placeholder - in a real implementation, you'd use
	// a parser library like participle or pigeon here.
	// For now, we'll return an error indicating a parser is needed.
	return nil, fmt.Errorf("parser not implemented - use a real parser backend")
}

func main() {
	dsl := &MusicDSL{}
	parser := &SimpleParser{}
	engine, err := gs.NewEngine("", dsl, parser)
	if err != nil {
		fmt.Printf("Error creating engine: %v\n", err)
		return
	}

	runtime := &MusicRuntime{}

	// Note: This won't work until a real parser is implemented
	code := `track(name="Drums").add_clip(start=0, length=8)`
	fmt.Printf("Code: %s\n", code)
	fmt.Println("\nNote: Parser implementation needed to run this example")
	fmt.Println("See parser_backend.go for the Parser interface")

	// Once parser is implemented, uncomment:
	// plan, err := engine.Compile(code)
	// if err != nil {
	// 	fmt.Printf("Error compiling: %v\n", err)
	// 	return
	// }
	// engine.Execute(context.Background(), runtime, plan)
}
