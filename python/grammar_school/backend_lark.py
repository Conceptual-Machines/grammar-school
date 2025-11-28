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
     | IDENTIFIER
     | BOOL

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
        return CallChain(calls=list(calls))

    def call(self, name, args=None):
        args_dict = {}
        if args:
            for arg in args:
                if isinstance(arg, Arg):
                    args_dict[arg.name] = arg.value
                else:
                    args_dict["_positional"] = arg
        return Call(name=str(name), args=args_dict)

    def args(self, *arg_list):
        return list(arg_list)

    def arg(self, *parts):
        if len(parts) == 2:
            name, value = parts
            return Arg(name=str(name), value=value)
        else:
            return parts[0]

    def value(self, token):
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
