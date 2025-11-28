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

// MusicParser is a placeholder parser (would need actual implementation).
type MusicParser struct{}

func (p *MusicParser) Parse(input string) (*gs.CallChain, error) {
	// This is a placeholder - in a real implementation, you'd use
	// a parser library like participle or pigeon here.
	// For now, we'll return an error indicating a parser is needed.
	return nil, fmt.Errorf("parser not implemented - use a real parser backend")
}

func main() {
	dsl := &MusicDSL{}
	parser := &MusicParser{}
	runtime := &MusicRuntime{}

	// Runtime is now stored in Engine (aligned with Python)
	// Pass nil to use default runtime that prints actions
	_, err := gs.NewEngine("", dsl, parser, runtime)
	if err != nil {
		fmt.Printf("Error creating engine: %v\n", err)
		return
	}

	// Note: This won't work until a real parser is implemented
	code := `track(name="Drums").add_clip(start=0, length=8)`
	fmt.Printf("Code: %s\n", code)
	fmt.Println("\nNote: Parser implementation needed to run this example")
	fmt.Println("See parser_backend.go for the Parser interface")

	// Once parser is implemented, uncomment:
	// engine, _ := gs.NewEngine("", dsl, parser, runtime)
	// plan, err := engine.Compile(code)
	// if err != nil {
	// 	fmt.Printf("Error compiling: %v\n", err)
	// 	return
	// }
	// Runtime is stored in engine, so Execute doesn't need it (aligned with Python)
	// engine.Execute(context.Background(), plan)
	// Or override with a different runtime:
	// engine.Execute(context.Background(), plan, &OtherRuntime{})
}
