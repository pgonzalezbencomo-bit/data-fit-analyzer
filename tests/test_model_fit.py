import pytest
import numpy as np


from model_fit import (
    ajuste_lineal, 
    funcion_ajuste_lineal, 
    ajuste_lm, 
    ajuste_Trf, 
    ajuste_dogbox, 
    comprobar_ier, 
    metricas_lineal, 
    metricas_curve_fit,
    Resultados
)


@pytest.fixture
def datos_lineales():
    """Genera datos ruidosos para una recta y = 2.5x + 1.2"""
    np.random.seed(42)
    x = np.linspace(0, 10, 50)
    error_y = np.full(len(x), 0.5)
    # y = mx + b + ruido
    y = 2.5 * x + 1.2 + np.random.normal(0, error_y)
    return x, y, error_y

@pytest.fixture
def datos_exponenciales():
    """Genera datos ruidosos para una curva y = 3.0 * exp(-0.5 * x)"""
    np.random.seed(42)
    x = np.linspace(0, 5, 50)
    error_y = np.full(len(x), 0.2)
    # y = a * exp(-b * x) + ruido
    y = 3.0 * np.exp(-0.5 * x) + np.random.normal(0, error_y)
    return x, y, error_y


def modelo_exponencial(x, a, b):
    return a * np.exp(-b * x)

#Test Ajustes Lineales

def test_ajuste_lineal_y_funcion(datos_lineales):
    x, y, _ = datos_lineales
    
    resultado = ajuste_lineal(x, y)
    assert hasattr(resultado, "slope") and hasattr(resultado, "intercept")
    
    assert resultado.slope == pytest.approx(2.5, rel=0.1)
    
    y_ajuste = funcion_ajuste_lineal(x, resultado)
    assert len(y_ajuste) == len(x)
    assert y_ajuste[0] == pytest.approx(resultado.intercept, rel=0.01)

def test_metricas_lineal(datos_lineales):
    x, y, error_y = datos_lineales
    resultado_ajuste = ajuste_lineal(x, y)
    y_ajuste = funcion_ajuste_lineal(x, resultado_ajuste)
    
    metricas = metricas_lineal(resultado_ajuste, y_ajuste, y, error_y)
    
    assert isinstance(metricas, Resultados)
    assert 0.90 < metricas.r2 <= 1.0 
    assert metricas.chi2 > 0
    assert metricas.chi2_reducido > 0

#Test Ajustes no Lineales

def test_ajuste_lm(datos_exponenciales):
    x, y, error_y = datos_exponenciales
    p0 = [1.0, 0.1]
    

    popt, pcov, infodict, mesg, ier = ajuste_lm(modelo_exponencial, x, y, p0, error_y)
    
    assert len(popt) == 2

    assert popt[0] == pytest.approx(3.0, rel=0.1) 
    assert isinstance(ier, int)
    

    assert comprobar_ier(ier, 'lm', mesg) is True

def test_ajuste_trf_y_dogbox(datos_exponenciales):
    x, y, error_y = datos_exponenciales
    p0 = [1.0, 0.1]
    inferior = [0.0, 0.0]
    superior = [10.0, 5.0]
    
    # Test TRF
    salida_trf = ajuste_Trf(modelo_exponencial, x, y, p0, error_y, inferior, superior)
    popt_trf, _, _, mesg_trf, ier_trf = salida_trf
    assert len(popt_trf) == 2
    assert comprobar_ier(ier_trf, 'trf', mesg_trf) is True
    
    # Test Dogbox
    salida_dog = ajuste_dogbox(modelo_exponencial, x, y, p0, error_y, inferior, superior)
    popt_dog, _, _, mesg_dog, ier_dog = salida_dog
    assert len(popt_dog) == 2
    assert comprobar_ier(ier_dog, 'dogbox', mesg_dog) is True

def test_metricas_curve_fit(datos_exponenciales):
    x, y, error_y = datos_exponenciales
    p0 = [1.0, 0.1]
    popt, *_ = ajuste_lm(modelo_exponencial, x, y, p0, error_y)
    
    y_predichos = modelo_exponencial(x, *popt)
    metricas = metricas_curve_fit(y, y_predichos, error_y, num_parametros=len(popt))
    
    assert isinstance(metricas, Resultados)
    assert 0.90 < metricas.r2 <= 1.0
    assert metricas.chi2_reducido > 0


# Tests Logica de Errores

def test_comprobar_ier_fallos():
    assert comprobar_ier(5, 'lm', "Max calls reached") is False
    assert comprobar_ier(1, 'lm', "Success") is True
    

    assert comprobar_ier(0, 'trf', "Max iterations") is False
    assert comprobar_ier(-1, 'dogbox', "Inconsistent bounds") is False
    assert comprobar_ier(1, 'trf', "Success") is True