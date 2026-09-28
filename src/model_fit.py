from scipy.optimize import curve_fit
from scipy.stats import linregress
import numpy as np
from typing import NamedTuple

class Resultados(NamedTuple):
    r2: float
    chi2:float
    chi2_reducido: float

#Ajuste Lineal

def ajuste_lineal(xdata, ydata):
    resultado = linregress(xdata,ydata)
    return resultado

def funcion_ajuste_lineal(xdata, datos_ajuste):
    m = datos_ajuste.slope
    b = datos_ajuste.intercept
    return m * xdata + b

#Ajustes No Lineales

def ajuste_lm(f,x, y, p0, sigma):
    return curve_fit(f= f, xdata=x, ydata=y, p0=p0, sigma=sigma, absolute_sigma=True, method='lm', full_output=True, check_finite=True, nan_policy='raise')


def ajuste_Trf(f, x, y, p0, sigma, inferior, superior):
    return  curve_fit(f=f, xdata=x, ydata=y, p0=p0, bounds=(inferior, superior),sigma=sigma, absolute_sigma=True, method='trf', full_output=True, check_finite=True, nan_policy='raise')

def ajuste_dogbox(f, x, y, p0, sigma, inferior, superior):
    return curve_fit(f=f, xdata=x, ydata=y, p0=p0, bounds=(inferior, superior),sigma=sigma, absolute_sigma=True, method='dogbox', full_output=True, check_finite=True, nan_policy='raise')


# Control de errores

def comprobar_ier(ier, metodo, mesg):
    if metodo == 'lm':
        if ier in [0,5,6,7,8]:
            print(mesg)
            return False
        else:
            return True

    elif metodo in ["trf", "dogbox"]:
        if ier in [-1,0]:
            print(mesg)
            return False
        else:
            return True

#Metricas
 
def metricas_lineal(datos_ajuste, ajuste, datos_y, error_y) -> Resultados:
    r2 = datos_ajuste.rvalue**2
    chi2 = np.sum(((datos_y - ajuste)/error_y)**2)
    gdl = len(datos_y) - 2
    chi2_reducido = chi2/gdl
    return Resultados(r2, chi2, chi2_reducido)

def metricas_curve_fit(datos_y, ajuste_y, error_y, num_parametros) -> Resultados:
    suma_residuos_cuadrados = np.sum((datos_y-ajuste_y)**2)
    suma_total_cuadrados = np.sum((datos_y - np.mean(datos_y))**2)
    r2 = 1-(suma_residuos_cuadrados/suma_total_cuadrados)

    chi2 = np.sum(((datos_y-ajuste_y)/error_y)**2)
    gdl = len(datos_y) - num_parametros
    chi2_reducido = chi2 / gdl

    return Resultados(r2, chi2, chi2_reducido)






