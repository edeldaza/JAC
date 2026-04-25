import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Mesa de Votación JAC",
    page_icon="🗳️",
    layout="centered"
)

@st.cache_data
def cargar_datos():
    df = pd.read_excel("datos.xlsx")
    df.columns = [str(c).strip() for c in df.columns]
    return df

def buscar_registro(df, documento_buscado):
    documento_buscado = str(documento_buscado).strip()
    coincidencias = df[df.astype(str).apply(
        lambda fila: fila.str.strip().eq(documento_buscado).any(), axis=1
    )]
    return coincidencias

df = cargar_datos()

st.markdown(
    """
    <h1 style='text-align: center; margin-bottom: 0.2rem;'>MESA DE VOTACIÓN JAC</h1>
    <p style='text-align: center; color: #666; margin-bottom: 2rem;'>
        Consulta el código de votación por número de documento
    </p>
    """,
    unsafe_allow_html=True
)

documento = st.text_input("Digite la cédula del ciudadano")

if st.button("🔍 Buscar en el libro", use_container_width=True):
    if not documento.strip():
        st.warning("Por favor, digite un número de documento.")
    else:
        resultado = buscar_registro(df, documento)

        if not resultado.empty:
            st.success("Registro encontrado")
            fila = resultado.iloc[0]

            st.markdown("---")

            for col in df.columns:
                valor = fila[col]
                if pd.notna(valor) and str(valor).strip() != "":
                    st.markdown(f"**{col}:** {valor}")
        else:
            st.error("No se encontró ningún registro con ese documento.")

st.caption("App Diseñada por Edeldaza")
