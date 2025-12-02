"""
Utilities for integrating Grammar School with OpenAI's CFG (Context-Free Grammar) tools.

This module provides helper functions to build OpenAI CFG tool payloads
that use Grammar School grammars as constraints.
"""

from typing import Any

from grammar_school.backend_lark import LarkBackend


class CFGConfig:
    """Configuration for building an OpenAI CFG tool."""

    def __init__(
        self,
        tool_name: str,
        description: str,
        grammar: str,
        syntax: str = "lark",
    ):
        """
        Initialize CFG configuration.

        Args:
            tool_name: Name of the tool that will receive the DSL output
            description: Description of what the tool does
            grammar: Lark or regex grammar definition
            syntax: "lark" or "regex" (default: "lark")
        """
        self.tool_name = tool_name
        self.description = description
        self.grammar = grammar
        self.syntax = syntax


def build_openai_cfg_tool(config: CFGConfig) -> dict[str, Any]:
    """
    Build an OpenAI CFG tool payload from a CFGConfig.

    This function:
    - Cleans the grammar using clean_grammar_for_cfg()
    - Returns the properly formatted OpenAI tool structure
    - Ensures the syntax defaults to "lark" if not specified

    Args:
        config: CFGConfig containing tool name, description, grammar, and syntax

    Returns:
        dict: OpenAI tool structure ready to be added to the tools array

    Example:
        ```python
        from grammar_school.openai_utils import CFGConfig, build_openai_cfg_tool

        tool = build_openai_cfg_tool(CFGConfig(
            tool_name="magda_dsl",
            description="Generates MAGDA DSL code for REAPER automation",
            grammar=grammar_string,
            syntax="lark",
        ))
        # Add tool to OpenAI request: tools = [tool]
        ```
    """
    # Clean the grammar for CFG
    cleaned_grammar = LarkBackend.clean_grammar_for_cfg(config.grammar)

    # Default to "lark" if syntax is not specified
    syntax = config.syntax or "lark"

    # Build the OpenAI CFG tool structure
    return {
        "type": "custom",
        "name": config.tool_name,
        "description": config.description,
        "format": {
            "type": "grammar",
            "syntax": syntax,
            "definition": cleaned_grammar,
        },
    }


def get_openai_text_format_for_cfg() -> dict[str, Any]:
    """
    Get the text format configuration that should be used when making OpenAI requests with CFG tools.

    When using CFG, the text format must be set to "text" (not JSON schema) because
    the output is DSL code, not JSON.

    Returns:
        dict: Text format config: {"format": {"type": "text"}}

    Example:
        ```python
        from grammar_school.openai_utils import get_openai_text_format_for_cfg

        params["text"] = get_openai_text_format_for_cfg()
        ```
    """
    return {
        "format": {
            "type": "text",
        },
    }
