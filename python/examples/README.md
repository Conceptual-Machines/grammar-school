# Grammar School Examples

## DSL vs JSON Comparison

### `json_vs_dsl_comparison.py`

Demonstrates the fundamental difference between JSON and DSL approaches:

- **JSON**: Data must flow through LLM (high token usage)
- **DSL**: Data stays in runtime, LLM only generates instructions (low token usage)

**Run it:**
```bash
cd python
python -m examples.json_vs_dsl_comparison
```

### `mock_mcp_server.py`

Simulates an MCP server to demonstrate how data flows:

- **JSON approach**: MCP → LLM (data) → JSON → Execute
- **DSL approach**: LLM → DSL code → Runtime → MCP (data stays)

**Run it:**
```bash
cd python
python -m examples.mock_mcp_server
```

## Key Insight

The fundamental difference is **where data flows**:

1. **JSON/Structured Output**:
   - MCP fetches data
   - Data sent to LLM as context (expensive!)
   - LLM generates JSON with data included
   - High token usage, limited by context window

2. **DSL**:
   - LLM generates DSL code (instructions only, ~30 tokens)
   - Runtime executes DSL
   - Runtime calls MCP directly (data stays in runtime)
   - Low token usage, unlimited scalability

## Example Flow

### JSON Approach
```
1. MCP: fetch_users() → 1000 users
2. LLM receives: 1000 users (50,000 tokens)
3. LLM generates JSON with user data
4. Execute JSON
```

### DSL Approach
```
1. LLM generates: fetch_users().filter(age > 25).send_email()
2. Runtime executes:
   - Calls MCP: fetch_users() → Data stays in runtime
   - Filters in runtime → No data to LLM
   - Calls MCP: send_email() → Only method call
```

**Token savings: 50,000 → 30 tokens (99.94% reduction!)**
