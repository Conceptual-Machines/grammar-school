# Runtime

The Runtime executes Actions produced by the interpreter.

## Overview

The `Runtime` interface defines how Actions are executed. You implement this interface to define the behavior of your DSL.

## Implementing Runtime

```go
type MyRuntime struct{}

func (r *MyRuntime) ExecuteAction(ctx context.Context, a gs.Action) error {
    switch a.Kind {
    case "greet":
        name := a.Payload["name"].(string)
        fmt.Printf("Hello, %s!\n", name)
    case "create_track":
        // Handle track creation
    }
    return nil
}
```

## Action Execution

Actions are executed in the order they're produced by the interpreter:

```go
plan, _ := engine.Compile(`track(name="Drums").add_clip(start=0, length=8)`)
engine.Execute(context.Background(), runtime, plan)
```

This will:
1. Execute the `create_track` action
2. Execute the `add_clip` action

## State Management

The Runtime can maintain state across action executions:

```go
type MusicRuntime struct {
    tracks       []map[string]interface{}
    currentTrack map[string]interface{}
}

func (r *MusicRuntime) ExecuteAction(ctx context.Context, a gs.Action) error {
    switch a.Kind {
    case "create_track":
        r.currentTrack = map[string]interface{}{
            "name":  a.Payload["name"],
            "clips": []interface{}{},
        }
        r.tracks = append(r.tracks, r.currentTrack)
    case "add_clip":
        if r.currentTrack != nil {
            clips := r.currentTrack["clips"].([]interface{})
            clips = append(clips, map[string]interface{}{
                "start":  a.Payload["start"],
                "length": a.Payload["length"],
            })
            r.currentTrack["clips"] = clips
        }
    }
    return nil
}
```

## Error Handling

Return errors from `ExecuteAction` to handle failures:

```go
func (r *MyRuntime) ExecuteAction(ctx context.Context, a gs.Action) error {
    if a.Kind == "create_track" {
        name := a.Payload["name"].(string)
        for _, track := range r.tracks {
            if track["name"] == name {
                return fmt.Errorf("track %s already exists", name)
            }
        }
        // ...
    }
    return nil
}
```

## Context Usage

The `context.Context` parameter allows you to:
- Handle cancellation
- Pass request-scoped values
- Set timeouts

```go
func (r *MyRuntime) ExecuteAction(ctx context.Context, a gs.Action) error {
    select {
    case <-ctx.Done():
        return ctx.Err()
    default:
        // Execute action
    }
    return nil
}
```
