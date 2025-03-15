import sympy as sp

def convert_to_sympy(m, b):
    # Converts parsed linear equation into a SymPy expression.
    x = sp.Symbol('x')  # Define x as a symbolic variable
    equation = m*x + b  # SymPy expression for y = mx + b
    return equation

def solve_equation(m, b):
    # Solves a linear equation for x when y = 0 (finds the x-intercept).
    x = sp.Symbol('x')
    equation = m * x + b
    solution = sp.solve(equation, x)

    if not solution:
        return sp.Symbol("No Solution")

    return solution[0] if len(solution) == 1 else solution

def differentiate(m, b):
    # Finds the derivative of the given linear equation.
    x = sp.Symbol('x')
    equation = convert_to_sympy(m, b)
    derivative = sp.diff(equation, x)
    return derivative  # Returns the slope (which is just m for linear equations)

def integrate(m, b):
    # Finds the integral of the given linear equation.
    x = sp.Symbol('x')
    equation = convert_to_sympy(m, b)
    integral = sp.integrate(equation, x)
    return integral  # Returns the antiderivative

def find_maximum(m, b):
    # Finds the maximum of a function (Linear functions have no maximum).
    return sp.Symbol("No Maximum")

def find_minimum(m, b):
    # Finds the minimum of a function (Linear functions have no minimum).
    return sp.Symbol("No Minimum")
