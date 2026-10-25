import streamlit as st
from error_propagation import get_form, error_propagation, calculator
import pandas as pd

st.title("Calculadora de errores")

with st.expander("Ejemplo"):
    st.write("Fórmula de ejemplo: a+b/2+c*4-c**2")
    df = pd.DataFrame({"Datos a": [1,2,3], "Error a":[0.1,0.2,0.3], "Datos b":[3,2,1], "Error b":[0.3,0.2,0.1], "Datos c":[6,4,2], "Error c":[0.2,0.4,0.6]})

if formula := st.text_input("Introduce tu fórmula"):
    expresion = get_form(formula)
    formula_error, variables = error_propagation(expresion)

    st.write(f"Fórmula propagada: {formula_error}")
    st.write(f"Variables detectadas: {variables}")

    if file := st.file_uploader(
        "Sube tus datos para calcular los valores obtenidos, en csv", accept_multiple_files=False, type="csv"
    ):
        ...

    if on := st.toggle("Escribir los datos a mano"):
        columnas = []
        for i in variables:
            columnas = columnas.append(i)

        df = pd.DataFrame(columns=columnas)

        tabla_interactiva = st.data_editor(df, num_rows="dynamic")