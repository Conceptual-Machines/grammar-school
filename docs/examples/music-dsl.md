# Music DSL Example

A complete example of building a music production DSL with Grammar School.

## Overview

This DSL allows you to create tracks, add clips, and apply effects using a simple syntax:

```text
track(name="Drums", color="blue").add_clip(start=0, length=8)
track(name="Bass").add_clip(start=0, length=4).add_effect(name="reverb", amount=0.5)
Cmaj7(1, 1), Fmaj7(2, 1), Gmaj7(3, 1)
```

## Python Implementation

```python
from grammar_school import Action, Grammar, Runtime, verb

class MusicDSL:
    @verb
    def track(self, name, color=None, _context=None):
        return Action(
            kind="create_track",
            payload={"name": name, "color": color or "default"}
        )

    @verb
    def add_clip(self, start, length, _context=None):
        return Action(
            kind="add_clip",
            payload={"start": start, "length": length}
        )

    @verb
    def add_effect(self, name, amount=1.0, _context=None):
        return Action(
            kind="add_effect",
            payload={"name": name, "amount": amount}
        )

class MusicRuntime(Runtime):
    def __init__(self):
        self.tracks = []
        self.current_track = None

    def execute(self, action: Action) -> None:
        if action.kind == "create_track":
            self.current_track = {
                "name": action.payload["name"],
                "color": action.payload["color"],
                "clips": [],
                "effects": []
            }
            self.tracks.append(self.current_track)

        elif action.kind == "add_clip":
            if self.current_track:
                self.current_track["clips"].append({
                    "start": action.payload["start"],
                    "length": action.payload["length"]
                })

        elif action.kind == "add_effect":
            if self.current_track:
                self.current_track["effects"].append({
                    "name": action.payload["name"],
                    "amount": action.payload["amount"]
                })

# Usage
dsl = MusicDSL()
grammar = Grammar(dsl)
runtime = MusicRuntime()

code = '''
track(name="Drums", color="blue").add_clip(start=0, length=8)
track(name="Bass").add_clip(start=0, length=4).add_effect(name="reverb", amount=0.5)
'''

grammar.execute(code, runtime)
print(runtime.tracks)
```

## Go Implementation

```go
package main

import (
    "context"
    "fmt"
    "grammar-school/go/gs"
)

type MusicDSL struct{}

func (d *MusicDSL) Track(args gs.Args, ctx *gs.Context) ([]gs.Action, *gs.Context, error) {
    name := args["name"].Str
    color := "default"
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

type MusicRuntime struct {
    tracks       []map[string]interface{}
    currentTrack map[string]interface{}
}

func (r *MusicRuntime) ExecuteAction(ctx context.Context, a gs.Action) error {
    switch a.Kind {
    case "create_track":
        r.currentTrack = map[string]interface{}{
            "name":    a.Payload["name"],
            "color":   a.Payload["color"],
            "clips":   []interface{}{},
            "effects": []interface{}{},
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

## Key Concepts Demonstrated

1. **Method Chaining** - `track(...).add_clip(...).add_effect(...)`
2. **Context Passing** - The `_context` parameter allows verbs to access previous actions
3. **Action Composition** - Multiple actions can be returned from a single verb
4. **Runtime State** - The runtime maintains state across action executions
