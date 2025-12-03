"""
Mock MCP Server using FastMCP with streamable HTTP transport

This simulates an MCP server that can be called:
- By LLM via function calling (JSON approach) - needs public URL
- By runtime directly (DSL approach) - can be localhost
"""

# Mock database - generate users on demand (infinite, deterministic)
import hashlib

from fastmcp import FastMCP

NAMES = [
    "Alice",
    "Bob",
    "Charlie",
    "Diana",
    "Eve",
    "Frank",
    "Grace",
    "Henry",
    "Ivy",
    "Jack",
    "Kate",
    "Liam",
    "Mia",
    "Noah",
    "Olivia",
    "Paul",
    "Quinn",
    "Ryan",
    "Sophia",
    "Tom",
    "Uma",
    "Victor",
    "Wendy",
    "Xavier",
    "Yara",
    "Zoe",
    "Adam",
    "Bella",
    "Chris",
    "Dana",
    "Emma",
    "Felix",
    "Gina",
    "Hugo",
    "Iris",
    "Jake",
    "Kara",
    "Leo",
    "Maya",
    "Nina",
    "Oscar",
    "Pam",
    "Quincy",
    "Rose",
    "Sam",
    "Tina",
    "Ursula",
    "Vince",
    "Willa",
    "Xander",
]


def generate_users(limit: int = 10, offset: int = 0) -> list[dict]:
    """
    Generate users deterministically (same parameters = same users).

    Uses hash-based selection to ensure deterministic results:
    - Same limit + offset always produces the same users
    - Age distribution is deterministic (18-65 range)
    - Names cycle through NAMES list deterministically

    Args:
        limit: Number of users to generate
        offset: Starting offset for pagination (default: 0)

    Returns:
        List of user dictionaries (deterministic)
    """
    users = []
    for i in range(limit):
        # Deterministic user index
        user_index = offset + i

        # Deterministic name selection (cycles through NAMES)
        name_base = NAMES[user_index % len(NAMES)]
        name = f"{name_base}{user_index}"

        # Deterministic age (18-65) using hash
        # Use hash of user_index to get consistent age
        hash_value = int(hashlib.md5(str(user_index).encode()).hexdigest(), 16)
        age = 18 + (hash_value % 48)  # 18-65 range (48 possible ages)

        # Deterministic email
        email = f"{name.lower().replace(' ', '')}@example.com"

        users.append({"name": name, "age": age, "email": email})

    return users


mcp = FastMCP("Mock MCP Server")


@mcp.tool
def fetch_users(limit: int = 10, offset: int = 0) -> dict:
    """
    Fetch users from the database (infinite supply).

    In JSON approach: LLM calls this via function calling
    In DSL approach: Runtime calls this directly

    Args:
        limit: Maximum number of users to fetch
        offset: Starting offset for pagination (default: 0)

    Returns:
        Dictionary with users list and count
    """
    users = generate_users(limit=limit, offset=offset)
    return {
        "users": users,
        "count": len(users),
        "total_available": float("inf"),  # Infinite users available
    }


@mcp.tool
def send_email(recipients: list[str], template: str = "notification") -> dict:
    """
    Send email to recipients.

    In JSON approach: LLM calls this with data in request
    In DSL approach: Runtime calls this directly

    Args:
        recipients: List of email addresses
        template: Email template name

    Returns:
        Dictionary with send status
    """
    return {
        "sent": len(recipients),
        "recipients": recipients,
        "template": template,
        "status": "sent",
    }


if __name__ == "__main__":
    import os

    # Get port from environment (for cloud deployment) or default to 8000
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")

    print("\n" + "=" * 70)
    print("Starting Mock MCP Server with Streamable HTTP transport")
    print("=" * 70)
    print(f"\nFastMCP server running on http://{host}:{port}")
    print("\nTools available:")
    print("  - fetch_users(limit: int)")
    print("  - send_email(recipients: List[str], template: str)")
    print("\nMCP endpoint: http://{host}:{port}/mcp")
    print("\n" + "=" * 70 + "\n")

    # Run with streamable-http transport (OpenAI supports this)
    # This implements MCP protocol over HTTP
    mcp.run(transport="streamable-http", host=host, port=port)
