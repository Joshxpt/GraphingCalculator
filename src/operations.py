import sympy as sp


def convert_to_sympy(coefficients, equation_type, indep_var):

    independent_symbol = sp.Symbol(indep_var)

    if equation_type == "linear":
        m, b = coefficients
        equation = m * independent_symbol + b
    elif equation_type == "quadratic":
        a, b, c = coefficients
        equation = a * independent_symbol ** 2 + b * independent_symbol + c
    else:
        raise ValueError("Unsupported equation type")

    return equation

def solve_equation(equation_type, coefficients, indep_var):

    if not isinstance(indep_var, str):
        raise TypeError(f"Expected 'indep_var' to be a string, got {type(indep_var)}")

    x = sp.Symbol(indep_var)
    equation = convert_to_sympy(coefficients, equation_type, indep_var)

    # Solve for x when y = 0 (x-intercepts)
    x_intercepts = sp.solve(equation, x)

    if not x_intercepts:
        x_intercept_str = "No Real Solution"
    else:
        # Format solutions as strings
        x_intercept_str = ', '.join([str(val) for val in x_intercepts])

    # Solve for y when x = 0 (y-intercept)
    y_intercept = equation.subs(x, 0)

    # Return plain text format
    return f"When y=0: {x_intercept_str}\nWhen x=0: {y_intercept}"


def differentiate(equation_type, coefficients, indep_var):

    independent_symbol = sp.Symbol(indep_var)
    equation = convert_to_sympy(coefficients, equation_type, indep_var)

    return sp.diff(equation, independent_symbol)


def integrate(equation_type, coefficients, indep_var):

    independent_symbol = sp.Symbol(indep_var)
    equation = convert_to_sympy(coefficients, equation_type, indep_var)

    return sp.integrate(equation, independent_symbol)


def find_maximum(equation_type, coefficients):

    if equation_type == "quadratic":
        a, b, c = coefficients
        if a < 0:  # Downward-facing parabola has a maximum
            x_vertex = -b / (2 * a)
            y_vertex = a * (x_vertex ** 2) + b * x_vertex + c
            return (x_vertex, y_vertex)
        return sp.Symbol("No Maximum")
    return sp.Symbol("No Maximum (Linear Functions Do Not Have One)")


def find_minimum(equation_type, coefficients):

    if equation_type == "quadratic":
        a, b, c = coefficients
        if a > 0:  # Upward-facing parabola has a minimum
            x_vertex = -b / (2 * a)
            y_vertex = a * (x_vertex ** 2) + b * x_vertex + c
            return (x_vertex, y_vertex)
        return sp.Symbol("No Minimum")
    return sp.Symbol("No Minimum (Linear Functions Do Not Have One)")