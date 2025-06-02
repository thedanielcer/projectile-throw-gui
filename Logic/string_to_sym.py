import re
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

def string_to_sympy(equation_str) -> sp.Expr:
    #  1)Remove whitespace
    equation_str = equation_str.replace(" ", "")

    # 2) Convert to carret notation
    equation_str = equation_str.replace("^", "**")

    # 3) Set transformations
    transformations = standard_transformations + (implicit_multiplication_application,)

    # 4) Convert to sympy expression
    equation_sympy = parse_expr(equation_str, transformations=transformations)

    return equation_sympy

