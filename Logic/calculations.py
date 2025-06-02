import sympy as sp

def calculate_initial_velocity(equation_sympy: sp.Expr) -> float:
    velocity_equation = sp.diff(equation_sympy, 't')
    initial_velocity = velocity_equation.subs('t', 0)
    return initial_velocity

def calculate_velocity_at_1s(equation_sympy: sp.Expr) -> float:
    velocity_equation = sp.diff(equation_sympy, 't')
    velocity_at_1s = velocity_equation.subs('t', 1)
    return velocity_at_1s

