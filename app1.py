import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Mesa de Votación JAC",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 900px;
    }
    .titulo {
        text-align: center;
        font-size: 2.3rem;
        font-weight: 800;
        color: #1f2f46;
        margin-bottom: 0.3rem;
    }
    .subtitulo {
        text-align: center;
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .resultado-box {
        background-color: #f5f7fb;
        padding: 1rem 1.2rem;
        border-radius: 12px;
        border: 1px solid #dfe6f1;
        margin-top: 1rem;
    }
    .campo {
        margin-bottom: 0.65rem;
        font-size: 1.03rem;
    }
    .campo b {
        color: #1f2f46;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def cargar_datos():
    df = pd.read_excel("datos.xlsx")
    df.columns = [str(c).strip() for c in df.columns]
    return df

def normalizar_texto(valor):
    if pd.isna(valor):
        return ""
    texto = str(valor).strip()
    if texto.endswith(".0"):
        texto = texto[:-2]
    return texto

def buscar_por_documento(df, documento):
    documento = normalizar_texto(documento)

    for columna in df.columns:
        serie = df[columna].apply(normalizar_texto)
        coincidencias = df[serie == documento]
        if not coincidencias.empty:
            return coincidencias

    return pd.DataFrame()

def obtener_valor_fila(fila, posibles_nombres):
    columnas_normalizadas = {str(col).strip().lower(): col for col in fila.index}

    for nombre in posibles_nombres:
        nombre_limpio = nombre.strip().lower()
        if nombre_limpio in columnas_normalizadas:
            col_real = columnas_normalizadas[nombre_limpio]
            valor = fila[col_real]
            if pd.notna(valor) and str(valor).strip() != "":
                return normalizar_texto(valor)

    return None

def mostrar_resultado_principal(fila):
    documento = obtener_valor_fila(fila, [
        "documento", "cedula", "cédula", "numero_documento",
        "nro_documento", "identificacion", "identificación"
    ])

    nombres = obtener_valor_fila(fila, [
        "nombres", "nombre", "nombre_completo", "apellidos y nombres"
    ])

    apellidos = obtener_valor_fila(fila, [
        "apellidos", "apellido"
    ])

    codigo = obtener_valor_fila(fila, [
        "codigo", "código", "codigo_votacion", "código_votación",
        "codigo de votacion", "código de votación", "mesa", "puesto", "codigo mesa"
    ])

    st.success("Registro encontrado")

    st.markdown('<div class="resultado-box">', unsafe_allow_html=True)

    if documento:
        st.markdown(f'<div class="campo"><b>Documento:</b> {documento}</div>', unsafe_allow_html=True)

    if nombres and apellidos:
        st.markdown(f'<div class="campo"><b>Nombres:</b> {nombres} {apellidos}</div>', unsafe_allow_html=True)
    elif nombres:
        st.markdown(f'<div class="campo"><b>Nombres:</b> {nombres}</div>', unsafe_allow_html=True)

    if codigo:
        st.markdown(f'<div class="campo"><b>Código de votación:</b> {codigo}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

def mostrar_detalle_completo(fila):
    with st.expander("Ver información completa del registro"):
        for col in fila.index:
            valor = fila[col]
            valor_limpio = normalizar_texto(valor)
            if valor_limpio != "":
                st.write(f"**{col}:** {valor_limpio}")

df = cargar_datos()

st.markdown('<div class="titulo">MESA DE VOTACIÓN JAC</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitulo">Consulta el código de votación por número de documento</div>',
    unsafe_allow_html=True
)

documento = st.text_input(
    "Digite la cédula del ciudadano",
    placeholder="Ejemplo: 1007066317"
)

buscar = st.button("🔎 Buscar en el libro", use_container_width=True)

if buscar:
    if not documento.strip():
        st.warning("Por favor digite un número de documento.")
    else:
        resultado = buscar_por_documento(df, documento)

        if resultado.empty:
            st.error("No se encontró ningún registro con ese número de documento.")
        else:
            fila = resultado.iloc[0]
            mostrar_resultado_principal(fila)
            mostrar_detalle_completo(fila)

st.caption("App Diseñada por Edeldaza")
