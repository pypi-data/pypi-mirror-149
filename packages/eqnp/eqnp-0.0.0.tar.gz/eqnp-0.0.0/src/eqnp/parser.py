#
# eqnp - parser.py
#
# Copyright (C) 2022 Kian Kasad
#
# This file is made available under a modified BSD license. See the provided
# LICENSE file for more information.
#
# SPDX-License-Identifier: BSD-2-Clause-Patent
#

from .expressions import *
from .functions import *

# Map from operator characters to their corresponding expression classes
OperatorMap = {
    '+': Addition,
    '-': Subtraction,
    '*': Multiplication,
    '/': Division,
    '^': Exponent,
    # No operator for Root yet
}

# Map from function abbreviations to their corresponding function classes
FunctionMap = {
    'abs': AbsoluteValue,
    'cos': Cosine,
    'cot': Cotangent,
    'csc': Cosecant,
    'sec': Secant,
    'sin': Sine,
    'tan': Tangent,
}

# List of operator characters in reverse order of operation precedence
OperatorSets = [
    ['+', '-'],
    ['*', '/'],
    ['^'],
]

def isnumstr(text: str) -> bool:
    try:
        float(text)
        return True
    except ValueError:
        return False

def check_prefixes(text, *args) -> (bool, str):
    if len(args) < 1:
        return TypeError('checkprefixes() requires at least one argument')
    for prefix in args:
        if text.startswith(prefix):
            return (True, prefix)
    return (False, '')

def parse_expression(text: str) -> Expression:
    # Remove all whitespace
    text = text.replace(' ', '')

    # How many levels of parentheses we're in
    depth = 0

    # Same as depth but specific to absolute value bars
    abs_depth = 0

    # If string is a number, return the number
    if isnumstr(text):
        try:
            num = int(text) if int(text) == float(text) else float(text)
        except ValueError:
            num = float(text)
        return Number(num)

    # Search for top-level operators
    for opset in OperatorSets:
        i = 0
        while i < len(text):

            if text[i] == '(':
                depth += 1
            elif text[i] == ')':
                depth -= 1
            elif text[i] == '|':
                if abs_depth > 0:
                    depth -= 1
                    abs_depth -= 1
                else:
                    depth += 1
                    abs_depth += 1
            elif depth == 0 and text[i] in opset:
                # TODO: fix operator precedence
                lhs = text[:i]
                rhs = text[i+1:]
                exp_class = OperatorMap[text[i]]
                return exp_class(parse_expression(lhs), parse_expression(rhs))

            i += 1

    # If not a number and has no top-level operators, check for a parenthesized
    # expression
    if text[0] == '(' and text[-1] == ')':
        # Parse expression inside parentheses
        return parse_expression(text[1:-1])

    # Check for absolute value bars
    if text[0] == '|' and text[-1] == '|':
        return AbsoluteValue(parse_expression(text[1:-1]))

    # Lastly, treat all letter strings as variable names
    if text.isalpha():
        return Variable(text)

    # Check for functions
    is_func, func_prefix = check_prefixes(text, *FunctionMap.keys())
    if is_func and text[len(func_prefix)] == '(' and text[-1] == ')':
        func_class = FunctionMap[func_prefix]
        return func_class(parse_expression(text[len(func_prefix)+1 : -1]))

    raise ValueError('Invalid expression string: ' + text)

# Define exports
__all__ = [
    'FunctionMap',
    'OperatorMap',
    'OperatorSets',
    'parse_expression',
]
