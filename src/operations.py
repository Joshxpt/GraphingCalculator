import sympy as sp


def convert_to_sympy(coefficients, equation_type, indep_var):
    if equation_type == "symbolic":
        return coefficients  # already a sympy expression

    independent_symbol = sp.Symbol(indep_var)

    if equation_type == "linear":
        m, b = coefficients
        equation = m * independent_symbol + b
    elif equation_type == "quadratic":
        a, b, c = coefficients
        equation = a * independent_symbol ** 2 + b * independent_symbol + c
    elif equation_type == "cubic":
        a, b, c, d = coefficients
        equation = a * independent_symbol ** 3 + b * independent_symbol ** 2 + c * independent_symbol + d
    elif equation_type == "quartic":
        a, b, c, d, e = coefficients
        equation = a * independent_symbol ** 4 + b * independent_symbol ** 3 + c * independent_symbol ** 2 + d * independent_symbol + e
    elif equation_type == "reciprocal":
        numerator, exponent = coefficients
        equation = numerator / independent_symbol ** exponent
    elif equation_type == "exponential":
        (base,) = coefficients
        equation = sp.exp(independent_symbol) if base == "e" else sp.Pow(base, independent_symbol)
    elif equation_type == "logarithmic":
        (base,) = coefficients
        equation = sp.ln(independent_symbol) if base == "e" else sp.log(independent_symbol, base)
    elif equation_type == "trigonometric":
        (func,) = coefficients
        equation = getattr(sp, func)(independent_symbol)
    elif equation_type == "inverse_trig":
        (func,) = coefficients
        equation = getattr(sp, "a" + func)(independent_symbol)
    else:
        raise ValueError("Unsupported equation type")

    return equation


def solve_equation(equation_type, coefficients, indep_var):

    if not isinstance(indep_var, str):
        raise TypeError(f"Expected 'indep_var' to be a string, got {type(indep_var)}")

    if equation_type == "symbolic":
        x = sp.Symbol(indep_var)
        expr = coefficients
        x_intercepts = sp.solve(expr, x)
        x_str = ', '.join([str(val) for val in x_intercepts]) if x_intercepts else "No Real Solution"
        y_at_zero = expr.subs(x, 0)
        y_str = "Undefined (Division by Zero)" if y_at_zero == sp.zoo else str(y_at_zero)
        return f"When y=0: {x_str}\nWhen x=0: {y_str}"

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
    if y_intercept == sp.zoo:
        y_str = "Undefined (Division by Zero)"
    else:
        y_str = str(y_intercept)

    # Return plain text format
    return f"When y=0: {x_intercept_str}\nWhen x=0: {y_str}"


def differentiate(equation_type, coefficients, indep_var):

    independent_symbol = sp.Symbol(indep_var)
    equation = convert_to_sympy(coefficients, equation_type, indep_var)

    return sp.diff(equation, independent_symbol)


def integrate(equation_type, coefficients, indep_var):

    independent_symbol = sp.Symbol(indep_var)
    equation = convert_to_sympy(coefficients, equation_type, indep_var)

    return sp.integrate(equation, independent_symbol)


def find_maximum(equation_type, coefficients):
    x = sp.Symbol('x')

    if equation_type == "linear":
        return sp.Symbol("No Maximum (Linear Functions Do Not Have One)")

    expr = build_expr(equation_type, coefficients, x)

    first_deriv = sp.diff(expr, x)
    critical_points = sp.solve(first_deriv, x)

    second_deriv = sp.diff(first_deriv, x)

    maxima = []
    for point in critical_points:
        if not point.is_real:
            continue
        if second_deriv.subs(x, point).evalf() < 0:
            y_val = expr.subs(x, point)
            maxima.append((float(point.evalf()), float(y_val.evalf())))

    return maxima if maxima else sp.Symbol("No Maximum")

def find_minimum(equation_type, coefficients):
    x = sp.Symbol('x')

    if equation_type == "linear":
        return sp.Symbol("No Minimum (Linear Functions Do Not Have One)")

    expr = build_expr(equation_type, coefficients, x)

    first_deriv = sp.diff(expr, x)
    critical_points = sp.solve(first_deriv, x)

    second_deriv = sp.diff(first_deriv, x)

    minima = []
    for point in critical_points:
        if not point.is_real:
            continue
        if second_deriv.subs(x, point).evalf() > 0:
            y_val = expr.subs(x, point)
            minima.append((float(point.evalf()), float(y_val.evalf())))

    return minima if minima else sp.Symbol("No Minimum")


def build_expr(equation_type, coefficients, x):
    if equation_type == "quadratic":
        a, b, c = coefficients
        return a*x**2 + b*x + c
    elif equation_type == "cubic":
        a, b, c, d = coefficients
        return a*x**3 + b*x**2 + c*x + d
    elif equation_type == "quartic":
        a, b, c, d, e = coefficients
        return a*x**4 + b*x**3 + c*x**2 + d*x + e
    else:
        return sp.Symbol("Unsupported")