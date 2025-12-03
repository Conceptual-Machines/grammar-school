# JSON vs DSL Comparison

This example demonstrates the fundamental difference between JSON/structured output and DSL approaches when integrating with LLMs and MCP servers.

## Files

- **`comparison.py`** - Main entry point that runs both approaches and compares results
- **`structured_output.py`** - JSON/structured output approach using `client.responses.parse()` with MCP tools
- **`domain_specific_language.py`** - DSL approach using `client.responses.create()` with CFG

## Key Differences

### JSON Approach
- Uses `client.responses.parse()` with Pydantic models
- LLM calls MCP server via tools (MCP **MUST** be publicly accessible)
- Data flows: MCP (public) → LLM context → JSON output
- **High token usage** (data in context)

### DSL Approach
- Uses `client.responses.create()` with CFG tools
- LLM generates DSL code (instructions only, no data)
- Runtime executes DSL code
- Runtime calls MCP directly (can be local/private)
- Data flows: LLM → DSL code → Runtime → MCP (local)
- **Low token usage** (no data in context)

## Running

```bash
cd python
python examples/json_vs_dsl_comparison/comparison.py
```

## Requirements

- OpenAI API key in `.env`: `OPENAI_API_KEY=...`
- MCP public URL in `.env`: `MCP_PUBLIC_URL=https://...` (for JSON approach)
- MCP local server running on `http://localhost:8000` (for DSL approach)

## Infrastructure

- **JSON**: Requires public MCP server (deployed on Railway, Render, etc.)
- **DSL**: Can use local MCP server (no public URL needed)
