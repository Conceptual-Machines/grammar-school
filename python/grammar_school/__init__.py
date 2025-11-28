"""Grammar School - A lightweight framework for building tiny LLM-friendly DSLs."""

from grammar_school.ast import Arg, Call, CallChain, Value
from grammar_school.backend_lark import DEFAULT_GRAMMAR, LarkBackend
from grammar_school.grammar import Engine, Grammar, rule, verb
from grammar_school.interpreter import Interpreter
from grammar_school.runtime import Action, Runtime
from grammar_school.version import __version__

__all__ = [
    "Action",
    "Arg",
    "Call",
    "CallChain",
    "Engine",
    "Grammar",
    "Interpreter",
    "LarkBackend",
    "Runtime",
    "Value",
    "__version__",
    "rule",
    "verb",
    "DEFAULT_GRAMMAR",
]
