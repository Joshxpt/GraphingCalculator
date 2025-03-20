import re
from fractions import Fraction

def parse_equation(equation_str):
    """
    Parses a linear or quadratic equation of the form:
    - Linear: y = mx + b
    - Quadratic: y = ax^2 + bx + c

    Returns:
    - (equation_type, coefficients, dependent variable, independent variable)
    """
    equation_str = equation_str.replace(" ", "")

    quadratic_match = re.match(
        r"([a-zA-Z])=([\+\-]?[0-9/\.]*)?([a-zA-Z])?\^2([\+\-]?[0-9/\.]*)?([a-zA-Z])?([\+\-]?[0-9/\.]*)?", equation_str)

    if quadratic_match:
        dependent_var = quadratic_match.group(1)  # y, s, f, etc.
        independent_var = quadratic_match.group(3) or quadratic_match.group(5)  # x, d, etc.

        a_str = quadratic_match.group(2) or "1"
        b_str = quadratic_match.group(4) or "0"
        c_str = quadratic_match.group(6) or "0"

        a = eval(a_str) if a_str else 1
        b = eval(b_str) if b_str else 0
        c = eval(c_str) if c_str else 0

        return "quadratic", (float(a), float(b), float(c)), dependent_var, independent_var

    linear_match = re.match(r"([a-zA-Z])=([\+\-]?[0-9/\.]*)?([a-zA-Z])([\+\-].*)?", equation_str)

    if linear_match:
        dependent_var = linear_match.group(1)  # y, s, f, etc.
        independent_var = linear_match.group(3)  # x, d, etc.

        m_str = linear_match.group(2)

        if m_str == "-":
            m = -1
        else:
            m = eval(m_str) if m_str else 1

        # Convert intercept (b)
        b_str = linear_match.group(4)
        b = eval(b_str) if b_str else 0

        return "linear", (float(m), float(b)), dependent_var, independent_var

    return None