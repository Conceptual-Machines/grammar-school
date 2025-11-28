"""Interpreter for Grammar School."""

from typing import Any

from grammar_school.ast import Arg, Call, CallChain, Value
from grammar_school.runtime import Action


class Interpreter:
    """Interprets CallChain AST into Actions."""
    
    def __init__(self, dsl_instance: Any):
        """Initialize interpreter with a DSL instance containing verb handlers."""
        self.dsl = dsl_instance
        self._verb_handlers = self._collect_verbs()
    
    def _collect_verbs(self) -> dict[str, Any]:
        """Collect all methods marked with @verb decorator."""
        verbs = {}
        for name in dir(self.dsl):
            attr = getattr(self.dsl, name)
            if callable(attr) and getattr(attr, "_is_verb", False):
                verbs[name] = attr
        return verbs
    
    def interpret(self, call_chain: CallChain) -> list[Action]:
        """
        Interpret a CallChain into a list of Actions.

        Walks the call chain, coerce Values to native types,
        dispatch to verb methods, and collect Actions.
        """
        actions = []
        context = None
        
        for call in call_chain.calls:
            if call.name not in self._verb_handlers:
                raise ValueError(f"Unknown verb: {call.name}")
            
            handler = self._verb_handlers[call.name]
            args = self._coerce_args(call.args)
            
            result = handler(**args, _context=context)
            
            if isinstance(result, Action):
                actions.append(result)
                context = result
            elif isinstance(result, tuple) and len(result) == 2:
                action, new_context = result
                actions.append(action)
                context = new_context
            elif isinstance(result, list):
                actions.extend(result)
                if result:
                    context = result[-1]
            else:
                raise ValueError(f"Verb handler {call.name} returned invalid result: {result}")
        
        return actions

    def _coerce_args(self, args: dict[str, Value]) -> dict[str, Any]:
        """Coerce Value objects to native Python types."""
        coerced = {}
        for name, value in args.items():
            coerced[name] = value.value
        return coerced

