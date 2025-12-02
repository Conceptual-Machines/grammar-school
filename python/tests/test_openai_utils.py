"""Tests for OpenAI CFG utility functions."""

from grammar_school.backend_lark import LarkBackend
from grammar_school.openai_utils import (
    CFGConfig,
    build_openai_cfg_tool,
    get_openai_text_format_for_cfg,
)


class TestCFGConfig:
    """Test CFGConfig dataclass."""

    def test_cfg_config_creation(self):
        """Test creating a CFGConfig instance."""
        config = CFGConfig(
            tool_name="test_tool",
            description="Test tool description",
            grammar="start: test",
            syntax="lark",
        )

        assert config.tool_name == "test_tool"
        assert config.description == "Test tool description"
        assert config.grammar == "start: test"
        assert config.syntax == "lark"

    def test_cfg_config_default_syntax(self):
        """Test CFGConfig defaults to 'lark' syntax."""
        config = CFGConfig(
            tool_name="test_tool",
            description="Test tool description",
            grammar="start: test",
        )

        assert config.syntax == "lark"

    def test_cfg_config_repr(self):
        """Test CFGConfig has proper __repr__ from dataclass."""
        config = CFGConfig(
            tool_name="test_tool",
            description="Test tool description",
            grammar="start: test",
        )

        repr_str = repr(config)
        assert "test_tool" in repr_str
        assert "CFGConfig" in repr_str


class TestBuildOpenAICFGTool:
    """Test build_openai_cfg_tool function."""

    def test_build_tool_structure(self):
        """Test that the returned dictionary has the correct structure."""
        config = CFGConfig(
            tool_name="magda_dsl",
            description="Generates MAGDA DSL code",
            grammar="start: track",
            syntax="lark",
        )

        tool = build_openai_cfg_tool(config)

        assert tool["type"] == "custom"
        assert tool["name"] == "magda_dsl"
        assert tool["description"] == "Generates MAGDA DSL code"
        assert "format" in tool
        assert tool["format"]["type"] == "grammar"
        assert tool["format"]["syntax"] == "lark"
        assert "definition" in tool["format"]

    def test_grammar_cleaning(self):
        """Test that grammar is cleaned using clean_grammar_for_cfg."""
        # Grammar with Lark directives that should be removed
        grammar_with_directives = """%import common
start: track
track: "track"
"""
        config = CFGConfig(
            tool_name="test_tool",
            description="Test tool",
            grammar=grammar_with_directives,
            syntax="lark",
        )

        tool = build_openai_cfg_tool(config)
        cleaned_grammar = tool["format"]["definition"]

        # Verify %import directive was removed
        assert "%import" not in cleaned_grammar
        # Verify the actual grammar content is still there
        assert "start: track" in cleaned_grammar
        assert "track: \"track\"" in cleaned_grammar

        # Verify it matches what clean_grammar_for_cfg would produce
        expected_cleaned = LarkBackend.clean_grammar_for_cfg(grammar_with_directives)
        assert cleaned_grammar == expected_cleaned

    def test_default_syntax_handling(self):
        """Test that syntax defaults to 'lark' when not specified."""
        config = CFGConfig(
            tool_name="test_tool",
            description="Test tool",
            grammar="start: test",
            syntax="",  # Empty string should default to "lark"
        )

        tool = build_openai_cfg_tool(config)
        assert tool["format"]["syntax"] == "lark"

    def test_regex_syntax(self):
        """Test that regex syntax is preserved."""
        config = CFGConfig(
            tool_name="test_tool",
            description="Test tool",
            grammar="^\\d+$",
            syntax="regex",
        )

        tool = build_openai_cfg_tool(config)
        assert tool["format"]["syntax"] == "regex"

    def test_all_config_fields_used(self):
        """Test that all config fields are properly used in the tool."""
        config = CFGConfig(
            tool_name="custom_tool",
            description="Custom description with special chars: !@#$",
            grammar="start: custom_rule\ncustom_rule: \"value\"",
            syntax="lark",
        )

        tool = build_openai_cfg_tool(config)

        assert tool["name"] == "custom_tool"
        assert tool["description"] == "Custom description with special chars: !@#$"
        assert tool["format"]["syntax"] == "lark"
        assert "custom_rule" in tool["format"]["definition"]


class TestGetOpenAITextFormatForCFG:
    """Test get_openai_text_format_for_cfg function."""

    def test_text_format_structure(self):
        """Test that the returned dictionary has the correct structure."""
        text_format = get_openai_text_format_for_cfg()

        assert isinstance(text_format, dict)
        assert "format" in text_format
        assert isinstance(text_format["format"], dict)
        assert text_format["format"]["type"] == "text"

    def test_text_format_consistency(self):
        """Test that the function returns the same structure on multiple calls."""
        format1 = get_openai_text_format_for_cfg()
        format2 = get_openai_text_format_for_cfg()

        assert format1 == format2
        assert format1["format"]["type"] == "text"
        assert format2["format"]["type"] == "text"

