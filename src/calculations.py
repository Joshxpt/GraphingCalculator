import re
from fractions import Fraction

def parse_linear_equation(equation_str):
    # Parses a linear equation of the form 'letter = m(letter) + b' and returns (m, b, variable).
    equation_str = equation_str.replace(" ", "")

    # Match equations like: y=2x+4/2, s=-3/2x-5, f=7/3d+8/4
    match = re.match(r"([a-zA-Z])=([\-0-9/\.]*)?([a-zA-Z])([\+\-].*)?", equation_str)

    if match:
        dependent_var = match.group(1)  # y, s, f, etc.
        independent_var = match.group(3)  # x, d, etc.

        # Convert slope (m)
        m_str = match.group(2)
        m = eval(m_str) if m_str else 1  # Evaluate math expressions like "7/3", "-3/2"

        # Convert intercept (b)
        b_str = match.group(4)
        b = eval(b_str) if b_str else 0  # Ensures 4/2 becomes 2, "-1/3" becomes -0.333

        return float(m), float(b), dependent_var, independent_var

    return None