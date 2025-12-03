"""
Domain-Specific Language Approach: CFG with Grammar School

This demonstrates the DSL approach where:
1. LLM generates DSL code (instructions only, no data)
2. Runtime executes DSL code
3. Runtime calls MCP directly (can be local/private)
4. Data never flows through LLM - stays in runtime
"""

import asyncio
import json

from basic_grammar import BASIC_GRAMMAR
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

from grammar_school import Grammar, method
from grammar_school.backend_lark import LarkBackend


# MCP helper functions for runtime
def call_mcp_local(mcp_url: str, limit: int = 10) -> dict:
    """Call MCP server locally (runtime calls directly, can be private)."""
    try:
        return asyncio.run(_call_mcp_local_async(mcp_url, limit))
    except Exception as e:
        print(f"  ⚠️  MCP call failed: {e}")
        return {"users": [], "count": 0}


async def _call_mcp_local_async(mcp_url: str, limit: int) -> dict:
    """Async helper for local MCP call."""
    async with streamablehttp_client(mcp_url) as (read, write, get_session_id):  # noqa: SIM117
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool("fetch_users", {"limit": limit})
            if result.content:
                data = json.loads(result.content[0].text)
                return data
    return {"users": [], "count": 0}


async def _call_mcp_send_email_local(mcp_url: str, recipients: list, template: str) -> dict:
    """Async helper for sending email via MCP."""
    async with streamablehttp_client(mcp_url) as (read, write, get_session_id):  # noqa: SIM117
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(
                "send_email", {"recipients": recipients, "template": template}
            )
            if result.content:
                return json.loads(result.content[0].text)
    return {}


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
    def filter(self, users=None, condition=None):  # noqa: ARG002
        """Filter users - simplified for basic grammar (no expressions)."""
        # With basic grammar, we can't parse expressions like "age > 25"
        # So we hardcode the filter logic in runtime
        # In production, you'd use advanced grammar with expressions
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


def dsl_approach(
    client, mcp_local_url: str, model: str = "gpt-5-nano-2025-08-07", num_users: int = 10
):
    """
    DSL approach using client.responses.create() with CFG.

    Args:
        client: OpenAI client instance
        mcp_local_url: Local URL of MCP server (can be private)
        model: Model to use
        num_users: Number of users to fetch

    Returns:
        tuple: (total_tokens, dsl_code) or (0, None) on error
    """
    print("\n" + "=" * 70)
    print("DSL APPROACH: CFG with Grammar School")
    print("=" * 70)

    # Get grammar definition for CFG (using basic grammar without operators)
    grammar_def = LarkBackend.clean_grammar_for_cfg(BASIC_GRAMMAR)

    prompt = f"""
    Fetch {num_users} users, filter them to only include users older than 25,
    and send them a notification email.
    """

    print(f"\nPrompt: {prompt.strip()}")
    print(f"\nMCP Server (can be local/private): {mcp_local_url}")
    print("\nCalling OpenAI API with CFG tool...")

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

            # Execute DSL code in runtime
            dsl = DataProcessingDSL(mcp_local_url=mcp_local_url)
            dsl.execute(dsl_code)
        else:
            print("\n✗ No DSL code generated in response")
            print(f"  Response: {response}")
            return 0, None

        print("\n✅ Note: In DSL approach:")
        print(f"    - MCP servers can be local/private: {mcp_local_url}")
        print("    - Data flows: LLM → DSL code → Runtime → MCP (local)")
        print(f"    - Low token usage: {usage.total_tokens} tokens (no data in context)")

        return usage.total_tokens, dsl_code

    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("  (This is expected if API key is not set or model not available)")
        return 0, None
