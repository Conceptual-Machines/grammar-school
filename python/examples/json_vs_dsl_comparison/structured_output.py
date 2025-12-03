"""
Structured Output Approach: JSON with MCP Tools

This demonstrates the JSON/structured output approach where:
1. LLM calls MCP server via tools (MCP MUST be public)
2. MCP returns data → flows into LLM context
3. LLM generates JSON with data included
4. High token usage because data is in context
"""

import time

from openai import OpenAI
from pydantic import BaseModel


class User(BaseModel):
    """User model for structured output."""

    name: str
    age: int
    email: str


class FilteredUsersResponse(BaseModel):
    """Response model for filtered users."""

    users: list[User]
    count: int


def structured_output_approach(
    client: OpenAI, mcp_public_url: str, model: str = "gpt-5-nano-2025-08-07", num_users: int = 10
):
    """
    JSON approach using client.responses.parse() with Pydantic + MCP tools.

    Args:
        client: OpenAI client instance
        mcp_public_url: Public URL of MCP server (MUST be accessible)
        model: Model to use
        num_users: Number of users to fetch

    Returns:
        tuple: (total_tokens, result) or (0, None) on error
    """
    print("=" * 70)
    print("JSON APPROACH: Structured Output with Pydantic + MCP Tools")
    print("=" * 70)

    prompt = f"""
    Fetch {num_users} users from the database and filter them to only include users
    older than 25. Return the filtered users in the specified format.
    """

    print(f"\nPrompt: {prompt.strip()}")
    print(f"\nMCP Server (MUST be public): {mcp_public_url}")
    print("\nCalling OpenAI API with MCP tools...")

    # Measure latency
    start_time = time.time()

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
        try:
            import json

            if hasattr(response, "model_dump"):
                response_dict = response.model_dump()
                # Find MCP tool calls in the output
                if "output" in response_dict and isinstance(response_dict["output"], list):
                    for item in response_dict["output"]:
                        if isinstance(item, dict) and item.get("type") == "mcp_call":
                            print(f"    Tool: {item.get('name', 'unknown')}")
                            args = json.loads(item.get("arguments", "{}"))
                            print(f"    Arguments: {args}")
                            if "limit" in args:
                                print(f"    → LLM requested limit={args['limit']} users")

                            # Check the output to see how many users were returned
                            if "output" in item:
                                output_data = json.loads(item["output"])
                                users_returned = output_data.get("users", [])
                                print(f"    → MCP returned {len(users_returned)} users")
                                print(f"    → MCP output count: {output_data.get('count', 'N/A')}")

                                # Warn if MCP didn't return the requested amount
                                if "limit" in args and len(users_returned) != args["limit"]:
                                    print(
                                        f"    ⚠️  WARNING: Requested {args['limit']} users but MCP returned {len(users_returned)}"
                                    )
                                    print(
                                        "       This means the deployed MCP server may not be respecting the limit parameter."
                                    )
                                    print(
                                        "       Token usage will be incorrect - need to redeploy MCP server."
                                    )
        except Exception as e:
            print(f"    Could not inspect tool calls: {e}")

        print("\n✓ LLM called MCP server and generated JSON")
        print(f"  Users in response: {result.count}")
        print(f"  Requested: {num_users} users (filtered to age > 25)")

        # Verify the data
        print("\n  Data Verification:")
        if result.users:
            print(f"    ✓ Received {len(result.users)} users in response")
            # Check ages
            ages = [u.age for u in result.users]
            all_over_25 = all(age > 25 for age in ages)
            print(f"    ✓ All users are over 25: {all_over_25}")
            if ages:
                print(f"    ✓ Age range: {min(ages)} - {max(ages)}")
            # Show sample
            if len(result.users) <= 3:
                sample = [
                    {"name": u.name, "age": u.age, "email": u.email} for u in result.users[:3]
                ]
                print(f"    ✓ Sample data: {sample}")
            else:
                sample = [
                    {"name": u.name, "age": u.age, "email": u.email} for u in result.users[:3]
                ]
                print(f"    ✓ Sample (first 3): {sample}")
        else:
            print("    ⚠️  No users in response!")

        # Check if count matches
        if result.count != len(result.users):
            print(
                f"    ⚠️  WARNING: count field ({result.count}) doesn't match users list length ({len(result.users)})"
            )

        print("\n  Token usage (from response.usage - includes ALL LLM consumption):")
        print(f"    Input: {usage.input_tokens:,}")
        print(f"    Output: {usage.output_tokens:,}")
        print(f"    Total: {usage.total_tokens:,}")
        print("\n  This includes ALL tokens consumed by LLM:")
        print("    - Prompt tokens")
        print("    - MCP tool call request")
        print(f"    - MCP tool response data (all {num_users} users flow through LLM context)")
        print("    - Generated JSON response")

        print("\n⚠️  Key Point:")
        print(f"    - MCP server MUST be publicly accessible: {mcp_public_url}")
        print("    - LLM calls MCP via tools → data flows into LLM context")
        print(f"    - High token usage: {usage.total_tokens} tokens (data in context)")
        print(f"    - Latency: {elapsed_time:.2f}s (includes data transfer through LLM)")

        return usage.total_tokens, result, elapsed_time

    except Exception as e:
        elapsed_time = time.time() - start_time
        print(f"\n✗ Error: {e}")
        print("  (This is expected if API key is not set or model not available)")
        return 0, None, elapsed_time
