#
# eqnp - functions.py
#
# Copyright (C) 2022 Kian Kasad
#
# This file is made available under a modified BSD license. See the provided
# LICENSE file for more information.
#
# SPDX-License-Identifier: BSD-2-Clause-Patent
#

from abc import ABC, abstractmethod
from math import sin, cos, tan
from .expressions import *

class Function(UnaryExpression, ABC):
    pass

class AbsoluteValue(Function):
    def evaluate(self, vm: VariableMap = None):
        return abs(self.value.evaluate(vm))

    def differentiate(self, respectTo: str, vm: VariableMap = None):
        return Multiplication(
            Division(self, self.value),
            self.value.differentiate(respectTo, vm)
        )

    def simplify(self):
        self.value = self.value.simplify()

        # For constants > 0, return the constant
        if isinstance(self.value, Number) and self.value.evaluate() >= 0:
            return self.value

        # Even exponents are never negative
        if isinstance(self.value, Exponent) \
                and isinstance(self.value.right, Number) \
                and self.value.right.evaluate() % 2 == 0:
            return self.value

        return self

# Alias for AbsoluteValue
ABS = AbsoluteValue

class Sine(Function):
    def evaluate(self, vm: VariableMap = None):
        return sin(self.value.evaluate(vm))

    def differentiate(self, respectTo: str, vm: VariableMap = None):
        return Multiplication(
            Cosine(self.value),
            self.value.differentiate(respectTo, vm)
        )

    def simplify(self):
        # TODO: return fractions for common angles.
        #       E.g. sin(pi/4) -> sqrt(2)/2
        return self

class Cosine(Function):
    def evaluate(self, vm: VariableMap = None):
        return cos(self.value.evaluate(vm))

    def differentiate(self, respectTo: str, vm: VariableMap = None):
        return Multiplication(
            Number(-1),
            Multiplication(
                Sine(self.value),
                self.value.differentiate(respectTo, vm)
            )
        )

    def simplify(self):
        # TODO: return fractions for common angles.
        #       E.g. cos(pi/4) -> sqrt(2)/2
        return self

class Tangent(Function):
    def evaluate(self, vm: VariableMap = None):
        return tan(self.value.evaluate(vm))

    def differentiate(self, respectTo: str, vm: VariableMap = None):
        return Multiplication(
            Exponent(
                Secant(self.value),
                2
            ),
            self.value.differentiate(respectTo, vm)
        )

    def simplify(self):
        # TODO: return fractions for common angles.
        #       E.g. cos(pi/4) -> sqrt(2)/2
        return self

class Secant(Function):
    def evaluate(self, vm: VariableMap = None):
        return 1 / sin(self.value.evaluate(vm))

    def differentiate(self, respectTo: str, vm: VariableMap = None):
        return Multiplication(
            Multiplication(
                Secant(self.value),
                Tangent(self.value)
            ),
            self.value.differentiate(respectTo, vm)
        )

    def simplify(self):
        # TODO: return fractions for common angles.
        #       E.g. sec(pi/4) -> sqrt(2)
        return self

class Cosecant(Function):
    def evaluate(self, vm: VariableMap = None):
        return 1 / cos(self.value.evaluate(vm))

    def differentiate(self, respectTo: str, vm: VariableMap = None):
        return Multiplication(
            Multiplication(
                Cosecant(self.value),
                Cotangent(self.value)
            ),
            Multiplication(
                self.value.differentiate(respectTo, vm),
                Number(-1)
            )
        )

    def simplify(self):
        # TODO: return fractions for common angles.
        #       E.g. csc(pi/4) -> sqrt(2)
        return self

class Cotangent(Function):
    def evaluate(self, vm: VariableMap = None):
        return 1 / tan(self.value.evaluate(vm))

    def differentiate(self, respectTo: str, vm: VariableMap = None):
        return Multiplication(
            -1,
            Exponent(
                Cosecant(self.value),
                2
            )
        )

    def simplify(self):
        # TODO: return fractions for common angles.
        #       E.g. cot(pi/4) -> 1
        return self

# Define exports
__all__ = [
    'ABS',
    'AbsoluteValue',
    'Cosecant',
    'Cosine',
    'Cotangent',
    'Function',
    'Secant',
    'Sine',
    'Tangent',
]
