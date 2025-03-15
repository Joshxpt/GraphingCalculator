import sympy as sp

def convert_to_sympy(m, b, indep_var):
    # Converts parsed linear equation into a SymPy expression.
    independent_symbol = sp.Symbol(indep_var)
    equation = m * independent_symbol + b
    return equation

def solve_equation(m, b, indep_var):
    # Solves a linear equation for x when y = 0 (finds the x-intercept).
    independent_symbol = sp.Symbol(indep_var)
    equation = m * independent_symbol + b
    solution = sp.solve(equation, independent_symbol)

    if not solution:
        return sp.Symbol("No Solution")

    return solution[0] if len(solution) == 1 else solution

def differentiate(m, b, indep_var):
    # Finds the derivative of the given linear equation.
    independent_symbol = sp.Symbol(indep_var)
    equation = convert_to_sympy(m, b, indep_var)
    derivative = sp.diff(equation, independent_symbol)
    return derivative

def integrate(m, b, indep_var):
    # Finds the integral of the given linear equation.
    independent_symbol = sp.Symbol(indep_var)
    equation = convert_to_sympy(m, b, indep_var)
    integral = sp.integrate(equation, independent_symbol)
    return integral

def find_maximum(m, b):
    # Finds the maximum of a function (Linear functions have no maximum).
    return sp.Symbol("No Maximum")

def find_minimum(m, b):
    # Finds the minimum of a function (Linear functions have no minimum).
    return sp.Symbol("No Minimum")