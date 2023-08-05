# eqnp
A simple expression parser/calculator

## Goal

The goal of eqnp is to be a program which can parse expressions (and maybe
equations at some point) and can manipulate them in various ways. This might
include:

 * Simplifying
 * Differentiating (finding derivatives)
 * Integrating (finding integrals)
 * Solving (isolating variables)

In addition, this is a project that I'm creating only from my own knowledge. My
goal is to not use any resources relating to the actual function of eqnp.
(Python documentation is acceptable, of course.)

## Usage

Import the `parse_expression()` function from `eqnp.parser`:

```python
from eqnp.parser import parse_expression

# or

from eqnp import *
```

Then run `parse_expression(...)`, passing in a string which is an expression.
[See below](#expression-string-syntax) for syntax.

### Example

```python
In [1]: import eqnp

In [2]: function = eqnp.parse_expression(' 1 / x^2 ')

In [3]: print(function)
Out[3]: Division(1, Exponent(x, 2))

In [4]: derivative = function.differentiate(respectTo='x')

In [5]: print(derivative)
Out[5]: Division(Subtraction(Multiplication(0, Exponent(x, 2)), Multiplication(1, Multiplication(Multiplication(2, Exponent(x, Subtraction(2, 1))), 1))), Exponent(Exponent(x, 2), 2))

In [6]: derivative = derivative.simplify_fully()

In [7]: print(derivative)
Out[7]: Division(Subtraction(0, Multiplication(2, x)), Exponent(x, 4))

      # Out[7] is equivalent to '(-2 * x) / (x ^ 4)'
```

### Expression string syntax

Currently, the following operators, functions, and other syntactical structures
are supported (`...` means an expression):

| Syntax      | Meaning                                                         |
| ---         | ---                                                             |
| `... + ...` | Addition -- Must have operands on either side                   |
| `... - ...` | Subtraction -- Must have operands on either side                |
| `... * ...` | Multiplication -- Must have operands on either side             |
| `... / ...` | Division -- Must have operands on either side                   |
| `(...)`     | Grouping -- used to group operations to enforce a certain order |
| `\|...\|`     | Absolute value -- same as `abs(...)`                            |
| `abs(...)`  | Absolute value                                                  |
| `sin(...)`  | Sine function                                                   |
| `cos(...)`  | Cosine function                                                 |
| `tan(...)`  | Tangent function                                                |
| `csc(...)`  | Cosecant function                                               |
| `sec(...)`  | Secant function                                                 |
| `cot(...)`  | Cotangent function                                              |
| `-n`        | Negation -- `n` must be a constant number                       |

> Note: The absolute value bars do not have to be escaped. They're only that way in the markdown file because the table syntax uses pipe characters.

## To do

There are still a lot of features that I want to implement. Some are listed as
`# TODO:` comments in the source code, but I'll put a list here too:

* Pull all constants out of nested multiplication expressions
* Flip negative exponents in fractions to opposite side
* Add inverse trigonometric functions
* Implement integration
