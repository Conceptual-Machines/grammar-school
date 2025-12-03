"""
Test Structured Output Approach in Isolation

Tests the JSON/structured output approach at different scales (10 vs 100 users)
to see how token usage scales with data size.
"""

import os

from dotenv import load_dotenv
from openai import OpenAI
from structured_output import structured_output_approach

# Load environment variables
load_dotenv()

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

if not api_key:
    print("⚠️  Warning: OPENAI_API_KEY not set in .env file")
    exit(1)

client = OpenAI(api_key=api_key, base_url=base_url)

# MCP server URL
MCP_PUBLIC_URL = os.getenv("MCP_PUBLIC_URL", "https://mock-mcp-server-production.up.railway.app")
MODEL = os.getenv("OPENAI_MODEL", "gpt-5-nano-2025-08-07")


def main():
    """Test structured output at different scales."""
    print("\n" + "=" * 70)
    print("TESTING STRUCTURED OUTPUT APPROACH (JSON)")
    print("=" * 70)

    # Test with 10 users
    print("\n" + "=" * 70)
    print("TEST 1: 10 USERS")
    print("=" * 70)
    tokens_10, result_10 = structured_output_approach(
        client=client, mcp_public_url=MCP_PUBLIC_URL, model=MODEL, num_users=10
    )

    # Test with 100 users
    print("\n" + "=" * 70)
    print("TEST 2: 100 USERS")
    print("=" * 70)
    tokens_100, result_100 = structured_output_approach(
        client=client, mcp_public_url=MCP_PUBLIC_URL, model=MODEL, num_users=100
    )

    # Comparison
    if tokens_10 > 0 and tokens_100 > 0:
        increase = tokens_100 - tokens_10
        percent_increase = ((tokens_100 / tokens_10) - 1) * 100

        print("\n" + "=" * 70)
        print("SCALING ANALYSIS: 10 vs 100 USERS")
        print("=" * 70)
        print("\nToken Usage:")
        print(f"  10 users:  {tokens_10:,} tokens")
        print(f"  100 users: {tokens_100:,} tokens")
        print(f"  Increase:  {increase:,} tokens ({percent_increase:.1f}%)")

        print("\nData Returned:")
        if result_10:
            print(f"  10 users:  {result_10.count} users (after filtering age > 25)")
        if result_100:
            print(f"  100 users: {result_100.count} users (after filtering age > 25)")

        print("\nKey Insight:")
        print(
            f"  Token usage increased by {percent_increase:.1f}% when scaling from 10 to 100 users."
        )
        print(f"  This is because ALL {100} users flow through the LLM context,")
        print(
            f"  even though only {result_100.count if result_100 else 'N/A'} users are returned after filtering."
        )

        print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
