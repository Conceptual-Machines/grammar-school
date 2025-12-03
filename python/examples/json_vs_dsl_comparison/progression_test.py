"""
Progression Test: JSON vs DSL at Different Scales

Tests both approaches at multiple scales to find the threshold point:
- 10 users: JSON likely wins (low overhead)
- 100 users: Close
- 1000 users: DSL should win
- 10000 users: DSL wins and remains constant
"""

import os

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

from domain_specific_language import dsl_approach
from openai import OpenAI
from structured_output import structured_output_approach

# Load environment variables from .env file (at project root)
if load_dotenv:
    load_dotenv()  # Automatically finds .env in project root

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

if not api_key:
    print("⚠️  Warning: OPENAI_API_KEY not set in .env file")
    print("   Please add your OpenAI API key to the .env file")

# Support AI gateway with custom base_url
client = OpenAI(api_key=api_key, base_url=base_url) if api_key else None

# MCP server URLs
MCP_PUBLIC_URL = os.getenv("MCP_PUBLIC_URL", "https://mock-mcp-server-production.up.railway.app")
MCP_LOCAL_URL = os.getenv("MCP_LOCAL_URL", "http://localhost:8000")
MODEL = os.getenv("OPENAI_MODEL", "gpt-5-nano-2025-08-07")

# Test scales
SCALES = [10, 100, 1000, 10000]


def run_scale_test(num_users: int):
    """Run both approaches for a given number of users."""
    print("\n" + "=" * 70)
    print(f"TESTING WITH {num_users} USERS")
    print("=" * 70)

    # JSON Approach
    print(f"\n[1/2] JSON Approach ({num_users} users)...")
    json_tokens, json_result = structured_output_approach(
        client=client,
        mcp_public_url=MCP_PUBLIC_URL,
        model=MODEL,
        num_users=num_users,
    )

    # DSL Approach
    print(f"\n[2/2] DSL Approach ({num_users} users)...")
    dsl_tokens, dsl_code = dsl_approach(
        client=client,
        mcp_local_url=MCP_LOCAL_URL,
        model=MODEL,
        num_users=num_users,
    )

    # Comparison
    if json_tokens > 0 and dsl_tokens > 0:
        reduction = ((json_tokens - dsl_tokens) / json_tokens * 100) if json_tokens > 0 else 0
        winner = "DSL" if dsl_tokens < json_tokens else "JSON"

        print(f"\n{'=' * 70}")
        print(f"RESULTS FOR {num_users} USERS")
        print(f"{'=' * 70}")
        print(f"JSON: {json_tokens:,} tokens")
        print(f"DSL:  {dsl_tokens:,} tokens")
        print(f"Winner: {winner}")
        if reduction > 0:
            print(f"DSL saves: {reduction:.1f}%")
        else:
            print(f"JSON saves: {abs(reduction):.1f}%")

        return {
            "users": num_users,
            "json_tokens": json_tokens,
            "dsl_tokens": dsl_tokens,
            "winner": winner,
            "reduction": reduction,
        }

    return None


def main():
    """Run progression test across multiple scales."""
    print("\n" + "=" * 70)
    print("PROGRESSION TEST: JSON vs DSL at Different Scales")
    print("=" * 70)
    print("\nTesting scales:", ", ".join(str(s) for s in SCALES))
    print("\nExpected behavior:")
    print("  - Small scale (10): JSON may win (low overhead)")
    print("  - Medium scale (100): Close")
    print("  - Large scale (1000+): DSL wins and remains constant")
    print("=" * 70)

    if not client:
        print("\n✗ OpenAI client not initialized. Please set OPENAI_API_KEY in .env")
        return

    results = []

    for scale in SCALES:
        result = run_scale_test(scale)
        if result:
            results.append(result)

    # Summary
    print("\n" + "=" * 70)
    print("PROGRESSION SUMMARY")
    print("=" * 70)
    print(f"\n{'Users':<10} {'JSON Tokens':<15} {'DSL Tokens':<15} {'Winner':<10} {'Savings':<10}")
    print("-" * 70)

    for r in results:
        savings_str = (
            f"{r['reduction']:.1f}%" if r["reduction"] > 0 else f"-{abs(r['reduction']):.1f}%"
        )
        print(
            f"{r['users']:<10} {r['json_tokens']:<15,} {r['dsl_tokens']:<15,} "
            f"{r['winner']:<10} {savings_str:<10}"
        )

    print("\n" + "=" * 70)
    print("KEY INSIGHT")
    print("=" * 70)
    print("\nAs dataset size increases:")
    print("  - JSON tokens grow linearly (data in context)")
    print("  - DSL tokens remain constant (no data in context)")
    print("\nThreshold point: Where DSL becomes more efficient")
    print("=" * 70)


if __name__ == "__main__":
    main()
