# JSON vs DSL: A Complete Walkthrough

This walkthrough demonstrates the fundamental difference between JSON/structured output and Domain-Specific Language (DSL) approaches when integrating LLMs with external data sources.

!!! note "Inspiration"
    This walkthrough and the Grammar School library were partly inspired by Anthropic's article on [Code execution with MCP: Building more efficient agents](https://www.anthropic.com/engineering/code-execution-with-mcp). The article explores how code execution enables agents to interact with MCP servers more efficiently by writing code instead of making direct tool calls, reducing token consumption and improving scalability.

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
    count: int

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
                    "require_approval": "never",
                }
            ],
        )

        result = response.output_parsed
        usage = response.usage
        elapsed_time = time.time() - start_time

        # Inspect MCP tool calls in the response
        print("\n  MCP Tool Call Inspection:")
        # ... MCP inspection code ...
    except Exception as e:
        print("Error:", e)
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
        return self

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
            dsl.execute(dsl_code)

            runtime_time = time.time() - runtime_start
            total_time = time.time() - start_time

            print("\n  Latency:")
            print(f"    LLM generation: {total_time - runtime_time:.2f}s")
            print(f"    Runtime execution: {runtime_time:.2f}s")
            print(f"    Total time: {total_time:.2f}s")
    except Exception as e:
        print("Error:", e)
```
<｜tool▁call▁begin｜>
run_terminal_cmd

**What happens:**

1. LLM receives prompt
2. LLM generates DSL code (example shown below)
3. Runtime executes DSL code
4. Runtime calls external service (MCP server, REST API, or any HTTP endpoint - can be localhost)
5. Runtime processes data locally
6. **No data flows through LLM context**

**Example Generated DSL Code:**

For a prompt like "Fetch 100 users, filter to those older than 25, and send them notification emails", the LLM generates:

```python
fetch_users(limit=100).filter().send_email()
```

Or with more explicit parameters:

```python
fetch_users(limit=100).filter(condition="age > 25").send_email(template="notification")
```

This DSL code is then executed by the runtime, which handles all the actual data fetching, filtering, and email sending without exposing any data to the LLM context.

!!! note "MCP vs REST API"
    In this example, we use MCP (Model Context Protocol) for convenience, but **MCP is not required** for the DSL approach. The runtime can call any REST API, HTTP endpoint, or even local functions. The key advantage is that these services can be private/local, unlike the structured output approach where the LLM must be able to call them directly (requiring public URLs).

## API Request Comparison

The fundamental difference between the two approaches is visible in the OpenAI API request payloads. Here's a side-by-side comparison:

### Structured Output (JSON) Request

```python
response = client.responses.parse(
    model=model,
    input=[...],
    text_format=FilteredUsersResponse,  # Pydantic model → JSON schema
    tools=[
        {
            "type": "mcp",
            "server_label": "user_database",
            "server_description": "A database MCP server...",
            "server_url": f"{mcp_public_url}/mcp",  # MUST be public
        }
    ],
)
```

**Key Points:**

- **`text_format`**: Uses a Pydantic model (`FilteredUsersResponse`), which corresponds to `{"type": "json"}` with a JSON schema under the hood
- **`tools`**: Defines MCP servers that the LLM can call to fetch data
- **Data Flow**: MCP returns data → flows into LLM context → LLM generates JSON matching the schema

### DSL (CFG) Request

```python
response = client.responses.create(
    model=model,
    input=[...],
    text={"format": {"type": "text"}},  # Freeform text (default)
    tools=[
        {
            "type": "custom",
            "name": "data_processing_dsl",
            "description": "Executes data processing operations...",
            "format": {
                "type": "grammar",
                "syntax": "lark",
                "definition": grammar_def,  # Full grammar definition
            },
        }
    ],
)
```

**Key Points:**

- **`text`**: Uses freeform text format (default `{"type": "text"}`)
- **`tools`**: Defines a custom tool with a grammar constraint (CFG) that enforces DSL syntax
- **Data Flow**: LLM generates DSL code → runtime executes → runtime calls MCP (no data in LLM context)

### Comparison Table

| Aspect | Structured Output | DSL with CFG |
|--------|------------------|--------------|
| **API Method** | `responses.parse()` | `responses.create()` |
| **Text Format** | `text_format=PydanticModel` → JSON schema | `text={"format": {"type": "text"}}` (freeform) |
| **Tools Purpose** | Define MCP servers for LLM to call | Define grammar constraints for code generation |
| **Tool Type** | `"type": "mcp"` | `"type": "custom"` with `"format": {"type": "grammar"}` |
| **Grammar Overhead** | None (uses JSON schema) | ~2,000+ tokens (full grammar definition) |
| **Data in Context** | Yes (all data from MCP flows through) | No (only instructions, not data) |

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
  - External services: Can be local/private (REST API, MCP, or any HTTP endpoint)
  - Authentication: Handled by runtime (not LLM)
  - Network: Local network or VPN
  - Security: Keep services private
  - Cost: Lower token usage = lower costs
```

**Example Setup:**
- Run service on localhost: `http://localhost:8000` (REST API, MCP, or any HTTP endpoint)
- Or deploy to private network/VPN
- No public exposure needed
- Pay only for instruction generation tokens

!!! note "MCP Not Required"
    While this example uses MCP for convenience, the DSL approach works with **any REST API or HTTP endpoint**. The runtime can call any service that your application has access to - it doesn't need to be MCP-compatible. This gives you maximum flexibility in choosing your backend services.

## Effort Comparison: Developer, LLM, Runtime, and MCP

This section breaks down where effort is required in each approach across four dimensions: developer effort, LLM effort, runtime effort, and MCP/server effort.

### Structured Output (JSON) Approach

| Effort Type | Description | Examples |
|------------|-------------|----------|
| **Developer Effort** | Low - Define data models only | Create Pydantic models (`User`, `FilteredUsersResponse`) |
| **LLM Effort** | High - Processes all data in context | LLM receives 100 users, filters them, generates JSON response |
| **Runtime Effort** | Minimal - Just parse response | Parse JSON from LLM response |
| **MCP/Server Effort** | Medium - Handles LLM requests | MCP server receives requests from LLM, returns data, must be publicly accessible |

**Effort Distribution:**
- Developer: ~5% (data models)
- LLM: ~85% (data processing, reasoning, generation)
- Runtime: ~5% (parsing)
- MCP/Server: ~5% (handling LLM requests)

### DSL Approach

| Effort Type | Description | Examples |
|------------|-------------|----------|
| **Developer Effort** | Medium - Write runtime implementation | Define grammar, implement `fetch_users()`, `filter()`, `send_email()` methods |
| **LLM Effort** | Low - Only generates code | LLM generates `fetch_users(limit=100).filter().send_email()` |
| **Runtime Effort** | High - Parses AST and executes DSL code | Runtime parses DSL into AST, executes code, calls MCP, processes data, handles errors, manages state |
| **MCP/Server Effort** | Medium - Handles runtime requests | MCP server receives requests from runtime (can be local/private), returns data |

**Effort Distribution:**
- Developer: ~30% (grammar + runtime code)
- LLM: ~20% (code generation only)
- Runtime: ~35% (AST parsing, code execution, data processing, state management)
- MCP/Server: ~15% (handling runtime requests)

### Comparison Summary

| Aspect | Structured Output | DSL |
|--------|------------------|-----|
| **Developer writes** | Data models | Grammar + Runtime code |
| **LLM does** | Data processing + Generation | Code generation only |
| **Runtime does** | Parse JSON | Parse AST + Execute DSL code + Process data + Manage state |
| **MCP/Server does** | Handle LLM requests (public) | Handle runtime requests (can be private) |
| **Best for** | Quick prototypes, small datasets | Production systems, large datasets |

**Key Insight:** Structured output shifts effort to the LLM (which processes data), while DSL shifts effort to the developer (who writes runtime code) and runtime (which executes and processes data). The runtime in DSL does more work than the developer, handling execution, data processing, and state management. This trade-off makes DSL more efficient at scale because the LLM doesn't process data.

## Developer Effort Comparison

### Structured Output (JSON)

**Setup Requirements:**
- Define Pydantic models (data schemas)
- Deploy MCP server to public URL
- Configure API authentication

**Code Required:**
- Data models only (e.g., `User`, `FilteredUsersResponse`)
- Minimal boilerplate for API calls

**Example:**
```python
class User(BaseModel):
    name: str
    age: int
    email: str

class FilteredUsersResponse(BaseModel):
    users: list[User]
    count: int

# That's it! The LLM handles the rest via MCP tools.
```

### DSL Approach

**Setup Requirements:**
- Define grammar (syntax rules)
- Write runtime implementation (verbs/methods)
- Implement data processing logic
- Handle MCP/API calls in runtime

**Code Required:**
- Grammar definition
- Runtime class with method implementations
- Data processing logic
- Error handling
- API/MCP integration code

**Example:**
```python
class DataProcessingDSL(Grammar):
    def __init__(self, mcp_local_url: str = "http://localhost:8000"):
        super().__init__()
        self.users: list[dict] = []
        self.filtered_users: list[dict] = []
        self.mcp_local_url = mcp_local_url

    @method
    def fetch_users(self, limit: int = 10):
        # Runtime implementation - you write this
        mcp_url = f"{self.mcp_local_url}/mcp"
        mcp_data = call_mcp_local(mcp_url, limit=limit)
        self.users = mcp_data.get("users", [])
        return self

    @method
    def filter(self, *args, **kwargs):
        # Filter logic - you write this
        self.filtered_users = [u for u in self.users if u.get("age", 0) > 25]
        return self

    @method
    def send_email(self, recipients=None, template="notification"):
        # Email sending logic - you write this
        # ... implementation ...
        return self
```

**Key Difference:**
- **Structured Output**: Define data models → LLM handles execution
- **DSL**: Define grammar + write runtime code → You control execution

## When to Use Each Approach

### Use JSON/Structured Output When:

- ✅ Small datasets (< 50 items)
- ✅ Simple transformations
- ✅ You need LLM reasoning on the data
- ✅ Public APIs are acceptable
- ✅ One-time queries
- ✅ Latency is not critical

### Use DSL When:

- ✅ **Latency is critical** - DSL provides more consistent and often faster response times, especially at scale
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

1. **Latency**: DSL provides more consistent and often faster response times, especially at scale - **critical for latency-sensitive applications**

2. **Token Efficiency**: DSL becomes more efficient as data size increases (threshold ~100 items)

3. **Infrastructure**: JSON requires public services; DSL can use private/local services

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
