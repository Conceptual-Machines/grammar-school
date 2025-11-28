"""Lark parser backend for Grammar School."""

from lark import Lark, Transformer, v_args

from grammar_school.ast import Arg, Call, CallChain, Value

DEFAULT_GRAMMAR = """
start: call_chain

call_chain: call (DOT call)*
call: IDENTIFIER "(" args? ")"
args: arg (COMMA arg)*
arg: IDENTIFIER "=" value
    | value

value: NUMBER
     | STRING
     | BOOL
     | IDENTIFIER
     | function_ref

// Function reference: @function_name syntax
function_ref: "@" IDENTIFIER

DOT: "."
COMMA: ","
NUMBER: /-?\\d+(\\.\\d+)?/
STRING: /"([^"\\\\]|\\\\.)*"|'([^'\\\\]|\\\\.)*'/
IDENTIFIER: /[a-zA-Z_][a-zA-Z0-9_]*/
BOOL: "true" | "false"

%import common.WS
%ignore WS
"""


@v_args(inline=True)
class ASTTransformer(Transformer):
    """Transforms Lark parse tree into Grammar School AST."""

    def start(self, call_chain):
        return call_chain

    def call_chain(self, *calls):
        # Filter out DOT tokens - only keep Call objects
        filtered_calls = [
            call
            for call in calls
            if not (hasattr(call, "type") and call.type == "DOT") and isinstance(call, Call)
        ]
        return CallChain(calls=filtered_calls)

    def call(self, name, args=None):
        args_dict = {}
        positional_index = 0
        if args:
            for arg in args:
                if isinstance(arg, Arg):
                    args_dict[arg.name] = arg.value
                else:
                    # Handle multiple positional arguments
                    args_dict[f"_positional_{positional_index}"] = arg
                    positional_index += 1
        return Call(name=str(name), args=args_dict)

    def args(self, *arg_list):
        # Filter out comma tokens
        return [arg for arg in arg_list if not (hasattr(arg, "type") and arg.type == "COMMA")]

    def arg(self, *parts):
        if len(parts) == 2:
            name, value = parts
            return Arg(name=str(name), value=value)
        else:
            return parts[0]

    def function_ref(self, identifier):
        """Handle function reference syntax @function_name."""
        # Return a Value with kind="function"
        func_name = str(identifier)
        return Value(kind="function", value=func_name)

    def value(self, token):
        # Check if token is already a Value (from function_ref transformation)
        if isinstance(token, Value):
            return token

        token_str = str(token)

        if token.type == "NUMBER":
            try:
                num_val: int | float = int(token_str)
            except ValueError:
                num_val = float(token_str)
            return Value(kind="number", value=num_val)
        elif token.type == "STRING":
            return Value(kind="string", value=token_str.strip('"').strip("'"))
        elif token.type == "BOOL":
            return Value(kind="bool", value=token_str.lower() == "true")
        elif token.type == "IDENTIFIER":
            return Value(kind="identifier", value=token_str)
        else:
            return Value(kind="string", value=token_str)


class LarkBackend:
    """Lark-based parser backend."""

    def __init__(self, grammar: str = DEFAULT_GRAMMAR):
        """Initialize with a Lark grammar string."""
        self.parser = Lark(grammar, start="start", parser="lalr")
        self.transformer = ASTTransformer()

    def parse(self, code: str) -> CallChain:
        """Parse code into a CallChain AST."""
        tree = self.parser.parse(code)
        result = self.transformer.transform(tree)
        return result  # type: ignore[no-any-return]

    @staticmethod
    def clean_grammar_for_cfg(grammar: str) -> str:
        """
        Clean Lark grammar for use with CFG systems (e.g., GPT-5).

        Removes Lark-specific directives that aren't supported in standard CFG:
        - %import directives
        - %ignore directives
        - Other %-prefixed directives

        Args:
            grammar: Lark grammar string with directives

        Returns:
            Cleaned grammar string suitable for CFG systems

        Example:
            ```python
            cleaned = LarkBackend.clean_grammar_for_cfg(DEFAULT_GRAMMAR)
            # Use cleaned grammar with GPT-5 CFG
            ```
        """
        return "\n".join(line for line in grammar.split("\n") if not line.strip().startswith("%"))
