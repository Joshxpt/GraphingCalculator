import re


def parse_equation(equation_str):
    equation_str = equation_str.replace(" ", "")

    match = re.match(r"^([a-zA-Z])=(.+)", equation_str)
    if not match:
        return None

    dependent_var = match.group(1)
    rhs = match.group(2)

    exp_match = re.match(r"^([0-9\.eE]+)\^([a-zA-Z])$", rhs)
    if exp_match:
        base_str, independent_var = exp_match.groups()
        base = base_str

        if base.lower() == "e":
            base = "e"
        else:
            try:
                base = float(base)
            except:
                return None

        equation_type = "exponential"
        coefficients = (base,)
        return equation_type, coefficients, dependent_var, independent_var

    reciprocal_match = re.match(r"^([+\-]?\d*(?:\.\d+)?)\/([a-zA-Z])(?:\^(\d+))?$", rhs)
    if reciprocal_match:
        numerator_str, independent_var, exponent_str = reciprocal_match.groups()

        numerator = float(numerator_str) if numerator_str not in ["", "+", "-"] else float(numerator_str + "1")
        exponent = int(exponent_str) if exponent_str else 1

        equation_type = "reciprocal"
        coefficients = (numerator, exponent)

        return equation_type, coefficients, dependent_var, independent_var

    # Logarithmic
    if rhs.startswith("log["):
        log_match = re.match(r"log\[(\d+(\.\d+)?)\]([a-zA-Z])", rhs)
        if log_match:
            base, _, independent_var = log_match.groups()
            base = float(base)
            return "logarithmic", (base,), dependent_var, independent_var

    elif rhs.startswith("log"):
        log_match = re.match(r"log([a-zA-Z])", rhs)
        if log_match:
            independent_var = log_match.group(1)
            return "logarithmic", (10,), dependent_var, independent_var

    elif rhs.startswith("ln"):
        ln_match = re.match(r"ln([a-zA-Z])", rhs)
        if ln_match:
            independent_var = ln_match.group(1)
            return "logarithmic", ("e",), dependent_var, independent_var

    # Handle polynomial equations
    degree_match = re.findall(r"\^(\d+)", rhs)
    max_degree = max([int(d) for d in degree_match], default=1)

    if max_degree > 4:
        return None

    # Find independent variable (e.g., x in x^2)
    var_match = re.search(r"([a-zA-Z])(\^?\d*)", rhs)
    independent_var = var_match.group(1) if var_match else "x"

    # Initialize coefficients for full degree
    coeffs = [0] * (max_degree + 1)

    # Find terms like +3x^2, -x, +5 etc.
    term_pattern = re.findall(r"([+\-]?[^+\-]+)", rhs)

    for term in term_pattern:
        term = term.strip()
        if independent_var in term:
            if "^" in term:
                parts = term.split("^", 1)
                if len(parts) != 2:
                    return None
                base, power = parts
                try:
                    power = int(power)
                except:
                    return None
            else:
                base = term
                power = 1

            base = base.replace(independent_var, "")
            if base in ("", "+"):
                coeff = 1
            elif base == "-":
                coeff = -1
            else:
                try:
                    coeff = float(eval(base))
                except:
                    return None
        else:
            power = 0
            try:
                coeff = float(eval(term))
            except:
                return None

        if power > max_degree or power < 0:
            return None

        coeffs[power] = coeff

    coeffs = coeffs[::-1]
    coeffs = [int(c) if float(c).is_integer() else float(c) for c in coeffs]

    equation_types = {
        1: "linear",
        2: "quadratic",
        3: "cubic",
        4: "quartic"
    }

    return equation_types[max_degree], tuple(coeffs), dependent_var, independent_var
