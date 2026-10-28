from sympy import sympify, diff, symbols, lambdify, Abs, latex
import sys

def get_form(form:str):
    if not isinstance(form,str):
        sys.exit()
    expresion = sympify(form, evaluate=False)
    return expresion

def error_propagation(expresion):
    formula_error = 0
    variables = sorted(expresion.free_symbols, key=lambda x: x.name)
    errores = []

    terminos_bon = []
    variables_bon = [fr"{i}" for i in variables]


    for i in variables:
        derivative = Abs(diff(expresion,i))
        var_err = symbols(f"d_{i}")

        formula_error += derivative*var_err
        errores.append(var_err)

        derivada_bon = latex(derivative)
        termino_bon = fr"{derivada_bon} \cdot \Delta {i}"
        terminos_bon.append(termino_bon)

        variable_bon = fr"\Delta {i}"
        variables_bon.append(variable_bon)

    formula_bonita = " + ".join(terminos_bon)

    variables += errores
    return formula_error, variables, formula_bonita, variables_bon

def calculator(formula, variables):
    return lambdify(variables, formula)






