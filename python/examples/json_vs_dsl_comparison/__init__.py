"""
JSON vs DSL Comparison Example

This package demonstrates the fundamental difference between JSON/structured output
and DSL approaches when integrating with LLMs and MCP servers.
"""

from .domain_specific_language import dsl_approach
from .structured_output import structured_output_approach

__all__ = ["structured_output_approach", "dsl_approach"]
