import numpy as np

def exponencial(x:int, a:int, b:int):
    return a*np.exp(x*b)

def logaritmico(x: int, a: int, b: int):
    return a*np.log(x) + b

def potencial(x, a, b):
    return a*x**b