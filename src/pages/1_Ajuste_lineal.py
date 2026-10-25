import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from model_fit import ajuste_lineal, funcion_ajuste_lineal, metricas_lineal

# Botones interactivos generales
def botones(x, y, err_x, err_y):
    if st.button("Representación de los datos (sin ajuste)"):
        fig , ax = plt.subplots()
        ax = plt.errorbar(x, y, xerr=err_x, yerr=err_y, fmt="o")
        st.pyplot(fig)

    on = st.toggle("Realizar ajuste lineal")

    if on:
        resultado = ajuste_lineal(x,y)
        modelo = funcion_ajuste_lineal(x, resultado)

        st.write("Personalización de las gráficas")

        col_color, col_grid, col_lims, col_grosor, col_labels, col_leyenda = st.columns(6)

        with col_color:
            colorg = st.color_picker("Escoge el color de la gráfica", "#00f900")
            colorp = st.color_picker("Escoge el color de los puntos", "#FF0000")
        with col_grid:
            grid = st.toggle("¿Quieres que se vea la grid?")
        with col_lims:
            xlim = st.slider("Límites del eje x", float(min(x)-100), float(max(x)+100), (float(min(x)), float(max(x))))
            ylim = st.slider("Límites del eje y", float(min(y)-100), float(max(y)+100), (float(min(y)), float(max(y))))
        with col_grosor:
            grosorg = st.slider("Grosor de la gráfica", 1, 5, 2)
            grosorp = st.slider("Grosor de los puntos", 1, 5, 2)
        with col_labels:
            title = st.text_input("Título", "")
            xlabel = st.text_input("Eje x", "")
            ylabel = st.text_input("Eje y", "")
        with col_leyenda:
            ley = st.toggle("¿Quieres una leyenda?")

        fig, ax = plt.subplots()

        ax.errorbar(x, y, xerr=err_x, yerr=err_y, color=colorp, fmt="o", markersize=grosorp, label="Datos")
        ax.plot(x, modelo, color=colorg, linewidth=grosorg, label="Ajuste")

        if grid:
            ax.grid(True)
            
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        
        if ley:
            ax.legend()
            
        st.pyplot(fig)


#Principio de la pagina

st.title("Ajuste Lineal")
st.write("Escoge la opción que quieras usar")

#Formas de pasar los datos a la app

action = st.selectbox("Como pasarás los datos",("Escribiendo la tabla aquí", "Importar Archivo CSV"))

#Datos escritos a mano

if action == "Escribiendo la tabla aquí":
    st.write("Los decimales se escriben con punto, si los escribes con coma no funcionan")
    df = pd.DataFrame(columns=["Datos x", "Error x", "Datos y", "Error y"])

    tabla_interactiva = st.data_editor(df,num_rows="dynamic")

    x = pd.to_numeric(tabla_interactiva["Datos x"], errors="coerce")
    y = pd.to_numeric(tabla_interactiva["Datos y"], errors="coerce")
    xerr = pd.to_numeric(tabla_interactiva["Error x"], errors="coerce")
    yerr = pd.to_numeric(tabla_interactiva["Error y"], errors="coerce")

    botones(x,y,xerr,yerr)


# CSV

elif action == "Importar Archivo CSV":
    df = pd.DataFrame({"Datos x": [3,4,5,6], "Error x":[0.1,0.1,0.1,0.1], "Datos y":[6,5,4,3], "Error y":[0.3,0.2,0.6,0.1]})
    expander = st.expander("Ver formato de ejemplo")
    expander.write(df)

    uploaded_file = st.file_uploader(
        "Sube tus datos", accept_multiple_files=False, type="csv"
    )
    if uploaded_file != None:
        df = pd.read_csv(uploaded_file)
        st.write("Tus datos:")
        st.write(df)

        x = pd.to_numeric(df["Datos x"], errors="coerce")
        y = pd.to_numeric(df["Datos y"], errors="coerce")
        xerr = pd.to_numeric(df["Error x"], errors="coerce")
        yerr = pd.to_numeric(df["Error y"], errors="coerce")

        botones(x,y,xerr,yerr)
        

    
    

    