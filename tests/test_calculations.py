import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from calculations import parse_equation

import sympy as sp

def test_parse_linear_equation():
    result = parse_equation("y = 2x + 3")
    assert result is not None
    eq_type, expr, dep_var, indep_var = result
    assert eq_type == "symbolic"
    assert str(dep_var) == "y"
    assert str(indep_var) == "x"
    assert sp.simplify(expr - (2*sp.Symbol("x") + 3)) == 0

def test_invalid_equation():
    assert parse_equation("2x +") is None
