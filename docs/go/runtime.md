# Runtime (Internal Architecture)

**Note:** With the unified interface, you don't need to implement Runtime. Methods execute directly. This page documents the internal architecture for advanced users.

## Overview

Internally, Grammar School maintains a two-layer architecture:
1. **Grammar layer**: Parses DSL and calls methods
2. **Runtime layer**: Executes methods (handled automatically)

When using the unified interface, the Runtime layer is handled automatically - you just write methods with their implementation.

## Using Methods (Recommended)

With the unified interface, you don't need Runtime:

```go
type MyDSL struct {
    tracks []map[string]interface{}
    currentTrack map[string]interface{}
}

func (d *MyDSL) Track(args gs.Args) error {
    name := args["name"].Str
    d.currentTrack = map[string]interface{}{
        "name":  name,
        "clips": []interface{}{},
    }
    d.tracks = append(d.tracks, d.currentTrack)
    fmt.Printf("Created track: %s\n", name)
    return nil
}

func (d *MyDSL) AddClip(args gs.Args) error {
    start := args["start"].Num
    length := args["length"].Num
    if d.currentTrack != nil {
        clips := d.currentTrack["clips"].([]interface{})
        clips = append(clips, map[string]interface{}{
            "start":  start,
            "length": length,
        })
        d.currentTrack["clips"] = clips
    }
    return nil
}

// Usage
dsl := &MyDSL{}
engine, _ := gs.NewEngine("", dsl, parser)
engine.Execute(context.Background(), `track(name="Drums").add_clip(start=0, length=8)`)
```

## Internal Architecture

The `Runtime` interface still exists internally, but is handled automatically when using methods. The framework:
1. Parses DSL code
2. Calls your method handlers directly
3. Methods execute immediately

You can manage state using struct fields in your DSL struct.
