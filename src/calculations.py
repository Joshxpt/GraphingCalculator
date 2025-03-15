import re

def parse_linear_equation(equation_str):
    # Parses a linear equation of the form 'letter = m(letter) + b' and returns (m, b, variable).
    equation_str = equation_str.replace(" ", "")

    match = re.match(r"([a-zA-Z])=(-?\d*\.?\d*)?([a-zA-Z])([\+\-]\d+\.?\d*)?", equation_str)

    if match:
        dependent_var = match.group(1)
        independent_var = match.group(3)

        m = float(match.group(2)) if match.group(2) not in ["", "-"] else -1 if match.group(2) == "-" else 1
        b = float(match.group(4)) if match.group(4) else 0

        return m, b, dependent_var, independent_var

    return None