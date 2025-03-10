import re

def parse_linear_equation(equation_str):
    # Parses a linear equation of the form 'y = mx + b' and returns (m, b).
    equation_str = equation_str.replace(" ", "")

    # Match "y = mx + b" pattern (including variations)
    match = re.match(r"y=(-?\d*\.?\d*)x([\+\-]\d+\.?\d*)?", equation_str)

    if match:
        m = float(match.group(1)) if match.group(1) not in ["", "-"] else -1 if match.group(1) == "-" else 1
        b = float(match.group(2)) if match.group(2) else 0
        return m, b

    return None  # Invalid equation
