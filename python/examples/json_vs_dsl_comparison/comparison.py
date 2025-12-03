"""
Real API Comparison: JSON vs DSL with Actual OpenAI API Calls

This demonstrates the fundamental difference with REAL API calls:

JSON Approach:
- Uses client.responses.parse() with Pydantic + MCP tools
- LLM calls MCP via tools (MCP MUST be public)
- Data flows: MCP (public) → LLM → JSON output
- High token usage (data in context)

DSL Approach:
- Uses client.responses.create() with CFG tools
- LLM generates DSL code (instructions only)
- Runtime executes DSL code
- Runtime calls MCP directly (can be local/private)
- Data flows: LLM → DSL code → Runtime → MCP (local)
- Low token usage (no data in context)
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


def main():
    """Main comparison function."""
    print("\n" + "=" * 70)
    print("REAL API COMPARISON: JSON vs DSL")
    print("=" * 70)
    print("\nThis example makes REAL OpenAI API calls to demonstrate:")
    print("  1. JSON: client.responses.parse() with Pydantic + MCP tools")
    print("  2. DSL: client.responses.create() with CFG")
    print("\nKey Difference:")
    print("  JSON: MCP must be public → Data flows through LLM")
    print("  DSL:  MCP can be local → Data stays in runtime")
    print("=" * 70)

    if not client:
        print("\n✗ OpenAI client not initialized. Please set OPENAI_API_KEY in .env")
        return

    # JSON Approach
    json_tokens, json_result = structured_output_approach(
        client=client, mcp_public_url=MCP_PUBLIC_URL, model=MODEL
    )

    # DSL Approach
    dsl_tokens, dsl_code = dsl_approach(client=client, mcp_local_url=MCP_LOCAL_URL, model=MODEL)

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    if json_tokens > 0 and dsl_tokens > 0:
        reduction = ((json_tokens - dsl_tokens) / json_tokens * 100) if json_tokens > 0 else 0
        print("\nToken Usage:")
        print(f"  JSON: {json_tokens} tokens")
        print(f"  DSL:  {dsl_tokens} tokens")
        if reduction > 0:
            print(f"  Reduction: {reduction:.1f}%")
        else:
            print(f"  Increase: {abs(reduction):.1f}%")

    print("\nInfrastructure Requirements:")
    print("  JSON:")
    print("    - MCP servers: Public URLs (HTTPS)")
    print("    - Authentication/API keys required")
    print("    - Data flows: MCP → LLM → JSON")
    print("  DSL:")
    print("    - MCP servers: Can be local/private")
    print("    - Simple function calls")
    print("    - Data flows: LLM → DSL → Runtime → MCP")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
