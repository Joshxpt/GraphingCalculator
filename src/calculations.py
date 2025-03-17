import re
from fractions import Fraction

def parse_equation(equation_str):
    """
    Parses a linear or quadratic equation of the form:
    - Linear: y = mx + b
    - Quadratic: y = ax^2 + bx + c

    Returns a tuple:
    - (type, coefficients, dependent variable, independent variable)
    - type = "linear" or "quadratic"
    - coefficients = (a, b, c) for quadratic, or (m, b) for linear
    """

    equation_str = equation_str.replace(" ", "")

    # Match quadratic equations like: y=2x^2+3x-5
    quadratic_match = re.match(
        r"([a-zA-Z])=([\-0-9/\.]*)?([a-zA-Z])?\^2([\+\-]?[0-9/\.]*)?([a-zA-Z])?([\+\-]?[0-9/\.]*)?", equation_str)

    if quadratic_match:
        dependent_var = quadratic_match.group(1)  # y, s, f, etc.
        independent_var = quadratic_match.group(3) or quadratic_match.group(5)  # x, d, etc.

        # Extract coefficients (a, b, c)
        a_str = quadratic_match.group(2) or "1"
        b_str = quadratic_match.group(4) or "0"
        c_str = quadratic_match.group(6) or "0"

        a = eval(a_str) if a_str else 1
        b = eval(b_str) if b_str else 0
        c = eval(c_str) if c_str else 0

        return "quadratic", (float(a), float(b), float(c)), dependent_var, independent_var

    # Match linear equations like: y=2x+4
    linear_match = re.match(r"([a-zA-Z])=([\-0-9/\.]*)?([a-zA-Z])([\+\-].*)?", equation_str)

    if linear_match:
        dependent_var = linear_match.group(1)  # y, s, f, etc.
        independent_var = linear_match.group(3)  # x, d, etc.

        # Convert slope (m)
        m_str = linear_match.group(2)
        m = eval(m_str) if m_str else 1  # Evaluate math expressions like "7/3", "-3/2"

        # Convert intercept (b)
        b_str = linear_match.group(4)
        b = eval(b_str) if b_str else 0  # Ensures 4/2 becomes 2, "-1/3" becomes -0.333

        return "linear", (float(m), float(b)), dependent_var, independent_var

    return None  # If the equation doesn't match