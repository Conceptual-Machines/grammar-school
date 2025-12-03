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
class User(BaseModel):
    """User model for structured output."""

    name: str
    age: int
    email: str


class FilteredUsersResponse(BaseModel):
    """Response model for filtered users."""

    users: list[User]
```

```python
    try:
        # LLM calls MCP via tools - MCP server MUST be publicly accessible
        response = client.responses.parse(
            model=model,
            input=[
                {"role": "system", "content": "You are a data processing assistant."},
                {"role": "user", "content": prompt},
            ],
            text_format=FilteredUsersResponse,
            tools=[
                {
                    "type": "mcp",
                    "server_label": "user_database",
                    "server_description": "A database MCP server for fetching and managing users.",
                    "server_url": f"{mcp_public_url}/mcp",  # MUST be public URL
```

**What happens:**
1. LLM receives prompt
2. LLM calls MCP server (public URL required)
3. MCP returns 100 users → **flows into LLM context**
4. LLM processes all 100 users in context
5. LLM generates JSON with filtered results

### DSL Approach Implementation

```python
class DataProcessingDSL(Grammar):
    """DSL for data processing - runtime handles MCP calls."""

    def __init__(self, mcp_local_url: str = "http://localhost:8000"):
        super().__init__()
        self.users: list[dict] = []
        self.filtered_users: list[dict] = []
        self.mcp_local_url = mcp_local_url

    @method
    def fetch_users(self, limit: int = 10):
        """
        Fetch users - runtime calls MCP server directly.
        MCP can be local/private because runtime calls it, not LLM.
        """
        # Runtime calls MCP directly (can be localhost or private endpoint)
        mcp_url = f"{self.mcp_local_url}/mcp"
        mcp_data = call_mcp_local(mcp_url, limit=limit)
        self.users = mcp_data.get("users", [])
        print(f"  [Runtime] Fetched {len(self.users)} users from MCP (local)")
        return self

    @method
    def filter(self, *args, users=None, condition=None, **kwargs):  # noqa: ARG002
        """Filter users - simplified for basic grammar (no expressions)."""
        # With basic grammar, we can't parse expressions like "age > 25"
        # So we hardcode the filter logic in runtime
        # In production, you'd use advanced grammar with expressions
        # Handle both positional and keyword arguments (including _positional from runtime)
        # Ignore any unexpected kwargs (like _positional from interpreter)
        self.filtered_users = [u for u in self.users if u.get("age", 0) > 25]
        print(f"  [Runtime] Filtered to {len(self.filtered_users)} users")
        return self

    @method
    def send_email(self, recipients=None, template="notification"):
        """Send email - runtime calls MCP directly."""
        if recipients is None:
            recipients = self.filtered_users
        emails = [u["email"] for u in recipients if isinstance(u, dict) and "email" in u]

        # Runtime calls MCP directly (can be localhost - no public URL needed!)
        try:
            mcp_url = f"{self.mcp_local_url}/mcp"
            asyncio.run(_call_mcp_send_email_local(mcp_url, emails, template))
            print(f"  [Runtime] Sending email to {len(emails)} recipients via MCP (local)")
        except Exception as e:
            print(f"  [Runtime] Email send failed: {e}")
```

```python
    # Measure latency
    start_time = time.time()

    try:
        # Use CFG tool to generate DSL code
        response = client.responses.create(
            model=model,
            input=[
                {"role": "system", "content": "You are a data processing assistant."},
                {"role": "user", "content": prompt},
            ],
            text={"format": {"type": "text"}},
            tools=[
                {
                    "type": "custom",
                    "name": "data_processing_dsl",
                    "description": (
                        "Executes data processing operations using Grammar School DSL. "
                        "Available verbs: fetch_users(limit), filter(users, condition), send_email(recipients, template). "
                        "YOU MUST REASON HEAVILY ABOUT THE QUERY AND MAKE SURE IT OBEYS THE GRAMMAR."
                    ),
                    "format": {
                        "type": "grammar",
                        "syntax": "lark",
                        "definition": grammar_def,
                    },
                }
            ],
        )

        # Extract DSL code from response
        dsl_code = None
        for item in response.output:
            if hasattr(item, "type") and item.type == "custom_tool_call":
                dsl_code = item.input
                break

        if not dsl_code:
            # Fallback: try output_text
            dsl_code = getattr(response, "output_text", None)

        usage = response.usage

        if dsl_code:
            print(f"\n✓ Generated DSL code: {dsl_code}")
            print("  Token usage:")
            print(f"    Input: {usage.input_tokens}")
            print(f"    Output: {usage.output_tokens}")
            print(f"    Total: {usage.total_tokens}")

            print("\n  Executing DSL code in runtime...")
            runtime_start = time.time()

            # Execute DSL code in runtime
            dsl = DataProcessingDSL(mcp_local_url=mcp_local_url)
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

**Key Insights**:

1. **At Low Scale (10 users)**: JSON wins because the DSL approach includes the full grammar definition in the LLM context. This grammar overhead (~2,000+ tokens) exceeds the small amount of data (10 users) that would flow through JSON.

2. **At Scale (100+ users)**: DSL becomes dramatically more efficient because:
   - The grammar definition is a **one-time cost** that doesn't grow with data size
   - JSON tokens grow **linearly** because all data flows through LLM context
   - DSL tokens remain **constant** because only instructions (not data) are in context

3. **The Crossover Point**: Around 100 users, the grammar overhead is amortized and DSL's constant token usage becomes more efficient than JSON's linear growth.

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
cd python
python examples/json_vs_dsl_comparison/comparison.py
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
