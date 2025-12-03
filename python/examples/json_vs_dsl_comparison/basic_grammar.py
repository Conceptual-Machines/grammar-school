"""
Basic Grammar for DSL Comparison Tests

This is a simplified grammar without operators/expressions to reduce token overhead
and better demonstrate the core benefit: data stays in runtime, not in LLM context.
"""

BASIC_GRAMMAR = """
start: statement+

// Statement is a call chain (which can be a single call or multiple chained calls)
statement: call_chain

call_chain: call (DOT call)*
call: IDENTIFIER "(" args? ")"
args: arg (COMMA arg)*
arg: IDENTIFIER "=" value
    | value

// Simplified value - no expressions, just basic types
value: NUMBER
    | STRING
    | BOOL
    | IDENTIFIER
    | property_access

// Property access: user.age
property_access: IDENTIFIER (DOT IDENTIFIER)+

// Terminals
DOT: "."
COMMA: ","
NUMBER: /-?\\d+(\\.\\d+)?/
STRING: /"([^"\\\\]|\\\\.)*"|'([^'\\\\]|\\\\.)*'/
IDENTIFIER: /[a-zA-Z_][a-zA-Z0-9_]*/
BOOL: "true" | "false"

%import common.WS
%ignore WS
"""
