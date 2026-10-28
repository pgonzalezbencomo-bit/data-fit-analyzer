import streamlit as st
from error_propagation import get_form, error_propagation, calculator
import pandas as pd


st.title("Calculadora de errores")

with st.expander("Ejemplo"):
    st.write("Fórmula de ejemplo: a+b/2+c*4-c**2")
    df = pd.DataFrame({"Datos a": [1,2,3], "Error a":[0.1,0.2,0.3], "Datos b":[3,2,1], "Error b":[0.3,0.2,0.1], "Datos c":[6,4,2], "Error c":[0.2,0.4,0.6]})

if formula := st.text_input("Introduce tu fórmula"):
    expresion = get_form(formula)
    formula_error, variables, formula_bon, variables_bon = error_propagation(expresion)

    st.write(fr"Fórmula propagada: $\Delta F = {formula_bon}$")
    texto_variables = ", ".join([fr"${v}$" for v in variables_bon])
    st.write(f"Variables detectadas: {texto_variables}")

    if file := st.file_uploader(
        "Sube tus datos para calcular los valores obtenidos", accept_multiple_files=False, type="csv"
    ):
        ...

    if on := st.toggle("Escribir los datos a mano"):
        columnas = []
        for i in variables_bon:
            columnas.append(fr"{i}")

        df = pd.DataFrame(columns=columnas)

        tabla_interactiva = st.data_editor(df, num_rows="dynamic")

        if st.checkbox("Terminado"):
            datos = []
            for i in columnas:
               dato = pd.to_numeric(tabla_interactiva[i], errors="coerce")
               datos.append(dato)

            calculadora_valor = calculator(expresion, variables)
            calculadora_error = calculator(formula_error, variables)

            F_valor = calculadora_valor(*datos)
            F_error = calculadora_error(*datos)

            diccionario_tabla = {}
          
            diccionario_tabla[r"$F$"] = F_valor
            diccionario_tabla[r"$ \Delta F$"] = F_error

            for nombre, columna in zip(variables_bon, datos):
                diccionario_tabla[fr"${nombre}$"] = columna
            data = pd.DataFrame(diccionario_tabla)

            if st.toggle("Obtener medida"):
                st.write(data)    