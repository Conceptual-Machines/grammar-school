# Go Examples

## Music DSL

A simple example DSL for creating music tracks and clips.

```bash
cd go
go run examples/music_dsl.go
```

**Note**: The example currently shows the structure but requires a parser implementation. To use it, you'll need to implement the `Parser` interface from `gs/parser_backend.go` using a library like:
- [participle](https://github.com/alecthomas/participle)
- [pigeon](https://github.com/mna/pigeon)
- Custom PEG/EBNF parser

The example demonstrates:
- Defining verb handlers with the required signature
- Creating an Engine instance
- Using reflection to automatically discover verb handlers
- Executing actions through a Runtime
