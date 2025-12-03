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
from grammar_school import Grammar, method

class MusicDSL(Grammar):
    def __init__(self):
        super().__init__()
        self.tracks = []
        self.current_track = None

    @method
    def track(self, name, color=None):
        self.current_track = {
            "name": name,
            "color": color or "default",
            "clips": [],
            "effects": []
        }
        self.tracks.append(self.current_track)
        print(f"Created track: {name}" + (f" (color: {color})" if color else ""))

    @method
    def add_clip(self, start, length):
        if self.current_track:
            self.current_track["clips"].append({
                "start": start,
                "length": length
            })
            print(f"Added clip: start={start}, length={length}")

    @method
    def add_effect(self, name, amount=1.0):
        if self.current_track:
            self.current_track["effects"].append({
                "name": name,
                "amount": amount
            })
            print(f"Added effect: {name} (amount: {amount})")

# Usage
dsl = MusicDSL()

code = '''
track(name="Drums", color="blue").add_clip(start=0, length=8)
track(name="Bass").add_clip(start=0, length=4).add_effect(name="reverb", amount=0.5)
'''

dsl.execute(code)
print(dsl.tracks)
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
2. **State Management** - Methods can access and modify state via `self` attributes
3. **Direct Execution** - Methods execute directly when called
4. **Runtime State** - The runtime maintains state across action executions
