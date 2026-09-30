from sympy import sympify, lambdify, diff, symbols, Abs
import sys

def procesar_expresion(a:str):
    if not isinstance(a,str):
        sys.exit("Not a string")

    expresion = sympify(a, evaluate=False)
    variables = sorted(list(expresion.free_symbols), key=lambda x: x.name)

    return (expresion, variables)

def calcular_error(exp, variables:list):
    suma_errores = 0
    variables_error = []
    for var in variables:
        var_error = symbols(f"d_{var.name}")
        variables_error.append(var_error)

        derivada = diff(exp, var)
        suma_errores += Abs(derivada) * var_error

    expresion_error = suma_errores
    todas_variables = variables + variables_error

    funcion_error = lambdify(todas_variables, expresion_error)
    return funcion_error

if __name__ == "__main__":
    formula_usuario = "x**2 * y"

    # 1. Procesar la expresión
    expresion, lista_variables = procesar_expresion(formula_usuario)
    print(f"Variables detectadas en orden: {lista_variables}")

    # 2. Fabricar la función calculadora
    calculadora = calcular_error(expresion, lista_variables)

    # 3. Usar la calculadora
    # Como las variables eran [x, y], todas_variables quedó como [x, y, d_x, d_y]
    # Por tanto, le pasamos: x=2, y=3, d_x=0.1, d_y=0.2
    resultado = calculadora(2, 3, 0.1, 0.2)
    print(f"El error propagado es: {resultado}")

