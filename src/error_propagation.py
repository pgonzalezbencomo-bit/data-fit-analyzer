from sympy import sympify, diff, symbols, lambdify, Abs
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

    for i in variables:
        derivative = Abs(diff(expresion,i))
        var_err = symbols(f"d_{i}")
        formula_error += derivative*var_err
        errores.append(var_err)

    variables += errores
    return formula_error, variables

def calculator(formula, variables):
    return lambdify(variables, formula)




if __name__=="__main__":
    formula = "a*b**2"
    expresion = get_form(formula)
    print(expresion)
    print(expresion.free_symbols)
    formula , variables = error_propagation(expresion)
    print(formula)




