import re
import sympy as sp
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor,
    function_exponentiation
)

def parse_equation(equation_str):
    equation_str = equation_str.replace(" ", "")

    match = re.match(r"^([a-zA-Z])=(.+)", equation_str)
    if not match:
        return None

    dependent_var = match.group(1)
    rhs_str = match.group(2)

    # Fix bracketless trig/log/ln functions: sinx → sin(x), etc.
    functions = ["sin", "cos", "tan", "log", "ln", "arcsin", "arccos", "arctan"]
    for func in functions:
        rhs_str = re.sub(rf"{func}([a-zA-Z0-9\(])", rf"{func}(\1", rhs_str)
        rhs_str = re.sub(rf"{func}\(([^()]+)\)", rf"{func}(\1)", rhs_str)

    # Fix exponentials like e^3x → e^(3x)
    rhs_str = re.sub(r"e\^([a-zA-Z0-9\+\-\*/\^]+)", r"e^(\1)", rhs_str)

    # Close all unmatched open brackets
    open_count = rhs_str.count('(')
    close_count = rhs_str.count(')')
    if open_count > close_count:
        rhs_str += ')' * (open_count - close_count)

    try:
        transformations = standard_transformations + (
            implicit_multiplication_application,
            convert_xor,
            function_exponentiation,
        )

        # Map 'e' to Euler's constant
        local_dict = {
            "e": sp.E,
            "sin": sp.sin,
            "cos": sp.cos,
            "tan": sp.tan,
            "log": sp.log,
            "ln": sp.ln,
            "arcsin": sp.asin,
            "arccos": sp.acos,
            "arctan": sp.atan,
        }

        expr = parse_expr(rhs_str, transformations=transformations, local_dict=local_dict)

    except (sp.SympifyError, SyntaxError):
        return None

    symbols = expr.free_symbols
    if not symbols:
        return None

    independent_var = str(list(symbols)[0])

    return "symbolic", expr, dependent_var, independent_var