# JSON vs DSL: A Complete Walkthrough

This walkthrough demonstrates the fundamental difference between JSON/structured output and Domain-Specific Language (DSL) approaches when integrating LLMs with external data sources.

## Overview

When building LLM applications that need to interact with data sources, developers have traditionally relied on **structured output** approaches. This typically involves:

- Using JSON schemas to constrain LLM responses
- Having the LLM call external services (like MCP servers) via function calling tools
- Allowing data to flow through the LLM context as it processes requests

However, with the recent introduction of **Context-Free Grammar (CFG)** support in GPT-5 ([OpenAI Cookbook](https://cookbook.openai.com/examples/gpt-5/gpt-5_new_params_and_tools#3-contextfree-grammar-cfg)), developers now have a powerful new option: **Domain-Specific Languages (DSL)**.

This new capability enables a fundamentally different approach:

1. **JSON/Structured Output** (Traditional): LLM calls external services via tools, data flows through LLM context
2. **DSL with CFG** (New): LLM generates code using CFG constraints, runtime executes it, data stays in runtime

The key innovation is that CFG allows you to enforce strict syntax rules on the LLM's output, enabling it to generate valid code in your custom DSL that can be executed by a runtime environment. This opens up new possibilities for building scalable, cost-effective LLM applications.

## Key Differences

### JSON Approach

- **Infrastructure**: External services (MCP servers) **MUST** be publicly accessible
- **Data Flow**: `MCP Server (public) → LLM Context → JSON Output`
- **Token Usage**: Grows linearly with data size (all data in LLM context)
- **Latency**: Increases with data size (data transfer through LLM)

### DSL Approach

- **Infrastructure**: External services can be **local/private** (no public URLs needed)
- **Data Flow**: `LLM → DSL Code → Runtime → MCP Server (local)`
- **Token Usage**: Remains constant (no data in LLM context)
- **Latency**: More consistent (data doesn't flow through LLM)

## Example: User Data Processing

Let's compare both approaches using a real-world scenario: fetching users, filtering them, and sending emails.

### Scenario

- Fetch N users from a database
- Filter to only include users older than 25
- Send notification emails to filtered users

### JSON Approach Implementation

```python
--8<-- "../python/examples/json_vs_dsl_comparison/structured_output.py:15:28"
```

```python
--8<-- "../python/examples/json_vs_dsl_comparison/structured_output.py:63:77"
```

**What happens:**
1. LLM receives prompt
2. LLM calls MCP server (public URL required)
3. MCP returns 100 users → **flows into LLM context**
4. LLM processes all 100 users in context
5. LLM generates JSON with filtered results

### DSL Approach Implementation

```python
--8<-- "../python/examples/json_vs_dsl_comparison/domain_specific_language.py:58:106"
```

```python
--8<-- "../python/examples/json_vs_dsl_comparison/domain_specific_language.py:140:195"
```

**What happens:**
1. LLM receives prompt
2. LLM generates DSL code: `fetch_users(limit=100).filter().send_email()`
3. Runtime executes DSL code
4. Runtime calls MCP server (can be localhost)
5. Runtime processes data locally
6. **No data flows through LLM context**

## Performance Comparison

### Token Usage

| Users | JSON Tokens | DSL Tokens | DSL Savings |
|-------|-------------|------------|-------------|
| 10    | 1,848       | 2,853      | -54.4% (JSON wins) |
| 100   | 10,234      | 2,721      | **73.4%** |
| 1,000 | 27,111      | 2,662      | **90.2%** |
| 10,000| 254,791     | 3,108      | **98.8%** |

**Key Insight**: JSON tokens grow linearly because all data flows through LLM context. DSL tokens remain constant because only instructions (not data) are in context.

### Latency

| Users | JSON Latency | DSL Latency | Difference |
|-------|--------------|-------------|------------|
| 10    | 10.32s       | 21.36s      | JSON faster (small overhead) |
| 100   | 70.81s       | 24.67s      | **DSL 2.9x faster** |
| 1,000 | 34.44s       | 21.06s      | **DSL 1.6x faster** |
| 10,000| 52.93s       | 30.32s      | **DSL 1.7x faster** |

!!! note "Latency Variability"
    LLM latency can vary significantly between calls due to factors like model load, network conditions, and token generation complexity. However, we can observe a clear pattern: **DSL latency remains relatively constant** (21-30s range) regardless of data size, while JSON latency shows more variability and tends to increase with larger datasets. This consistency in DSL is because the LLM only generates code (constant complexity), while runtime execution happens locally and doesn't depend on LLM processing time.

**Key Insight**: At scale, DSL latency is more consistent and often faster because data doesn't need to flow through the LLM.

## Infrastructure Requirements

### JSON Approach

```yaml
Requirements:
  - MCP servers: Public URLs (HTTPS)
  - Authentication: API keys required
  - Network: Public internet access
  - Security: Expose internal services publicly
  - Cost: Higher token usage = higher costs
```

**Example Setup:**
- Deploy MCP server to Railway/Heroku/AWS
- Get public URL: `https://your-mcp-server.railway.app`
- Configure CORS and authentication
- Pay for all data tokens flowing through LLM

### DSL Approach

```yaml
Requirements:
  - MCP servers: Can be local/private
  - Authentication: Simple function calls
  - Network: Local network or VPN
  - Security: Keep services private
  - Cost: Lower token usage = lower costs
```

**Example Setup:**
- Run MCP server on localhost: `http://localhost:8000`
- Or deploy to private network/VPN
- No public exposure needed
- Pay only for instruction generation tokens

## When to Use Each Approach

### Use JSON/Structured Output When:

- ✅ Small datasets (< 50 items)
- ✅ Simple transformations
- ✅ You need LLM reasoning on the data
- ✅ Public APIs are acceptable
- ✅ One-time queries

### Use DSL When:

- ✅ Large datasets (> 100 items)
- ✅ Complex data processing pipelines
- ✅ Data privacy is important
- ✅ You want to keep services private
- ✅ Recurring operations
- ✅ Cost optimization is critical

## Running the Comparison

The complete comparison example is available in `python/examples/json_vs_dsl_comparison/`:

```bash
--8<-- "../python/examples/json_vs_dsl_comparison/README.md:27:32"
```

For detailed setup instructions, see the [comparison README](../python/examples/json_vs_dsl_comparison/README.md).

## Key Takeaways

1. **Token Efficiency**: DSL becomes more efficient as data size increases (threshold ~100 items)

2. **Infrastructure**: JSON requires public services; DSL can use private/local services

3. **Latency**: DSL latency is more consistent and often faster at scale

4. **Cost**: DSL significantly reduces token costs for large datasets (up to 98.8% savings)

5. **Privacy**: DSL keeps data in runtime, never exposing it to LLM context

6. **Scalability**: DSL scales better because token usage remains constant regardless of data size

## Conclusion

The choice between JSON and DSL depends on your use case:

- **Small scale, simple queries**: JSON/structured output is simpler
- **Large scale, complex pipelines**: DSL is more efficient and cost-effective
- **Privacy-sensitive data**: DSL keeps data private
- **Public APIs acceptable**: JSON works fine
- **Cost optimization**: DSL saves significantly on tokens

The DSL approach with Grammar School provides a powerful way to build scalable, cost-effective LLM applications that don't require exposing your data infrastructure publicly.
