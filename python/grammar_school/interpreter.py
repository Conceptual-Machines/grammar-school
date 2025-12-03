"""Interpreter for Grammar School."""

from typing import Any

from grammar_school.ast import CallChain, Value


class Interpreter:
    """Interprets CallChain AST and executes methods directly."""

    def __init__(self, dsl_instance: Any):
        """Initialize interpreter with a DSL instance containing method handlers."""
        self.dsl = dsl_instance
        self._method_handlers = self._collect_methods()

    def _collect_methods(self) -> dict[str, Any]:
        """Collect all methods marked with @method decorator."""
        methods = {}
        for name in dir(self.dsl):
            attr = getattr(self.dsl, name)
            if callable(attr) and getattr(attr, "_is_method", False):
                methods[name] = attr
        return methods

    def interpret(self, call_chain: CallChain) -> list[None]:
        """
        Interpret a CallChain by executing methods directly.

        Note: This method exists for compatibility but methods execute directly
        during interpret_stream. The returned list will contain None values
        (one per method call executed).
        """
        return list(self.interpret_stream(call_chain))

    def interpret_stream(self, call_chain: CallChain):
        """
        Interpret a CallChain by executing methods directly (streaming).

        This is a generator that executes methods one at a time, allowing
        for memory-efficient processing of large DSL programs.

        Yields:
            None: One None per method executed (for compatibility with Action-based interface)
        """
        for call in call_chain.calls:
            if call.name not in self._method_handlers:
                raise ValueError(f"Unknown method: {call.name}")

            handler = self._method_handlers[call.name]
            args = self._coerce_args(call.args)
            # Remove _context from args if present (methods don't need it)
            args.pop("_context", None)
            # Call method directly - it executes immediately
            handler(**args)
            # Yield None to indicate execution (for compatibility)
            yield None

    def _coerce_args(self, args: dict[str, Value]) -> dict[str, Any]:
        """
        Coerce Value objects to native Python types.

        Function references (kind="function") are resolved to actual function handlers
        if they exist in the method handlers, otherwise passed as string identifiers.

        Positional arguments are extracted and passed in order as *args.
        """
        coerced = {}
        positional_args = []

        # Collect positional arguments in order
        for name, value in sorted(args.items()):
            if name.startswith("_positional_"):
                try:
                    index = int(name.split("_")[-1])
                    positional_args.append((index, value))
                except ValueError:
                    # Argument name does not match expected '_positional_N' pattern; skip it.
                    pass

        # Sort by index and extract values
        positional_values = [v for _, v in sorted(positional_args)]

        # Process all named arguments (non-positional)
        for name, value in args.items():
            if name.startswith("_positional_"):
                continue  # Already handled above

            if value.kind == "function":
                # Function reference - try to resolve to handler, otherwise pass as string
                func_name = value.value
                coerced[name] = self._method_handlers.get(func_name, func_name)
            else:
                coerced[name] = value.value

        # Handle positional arguments - pass as *args if multiple, or single value if one
        if positional_values:
            # Coerce each positional value
            coerced_positionals = []
            for value in positional_values:
                if value.kind == "function":
                    func_name = value.value
                    if func_name in self._method_handlers:
                        coerced_positionals.append(self._method_handlers[func_name])
                    else:
                        coerced_positionals.append(func_name)
                else:
                    coerced_positionals.append(value.value)

            # If handler accepts *args, we need to pass them separately
            # For now, pass as _positional_0, _positional_1, etc. for backward compat
            # But also support passing as a list if handler expects it
            if len(coerced_positionals) == 1:
                coerced["_positional"] = coerced_positionals[0]
            else:
                # Multiple positionals - pass as list
                coerced["_positional"] = coerced_positionals

        return coerced
