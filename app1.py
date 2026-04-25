import re
from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Control de Votantes - JAC", page_icon="🗳️", layout="centered")

DATA_FILE = Path(__file__).with_name("datos.xlsx")


def normalizar_documento(valor):
    if valor is None:
        return ""
    texto = str(valor).strip()
    texto = re.sub(r"[^0-9A-Za-z]", "", texto)
    return texto.upper()


@st.cache_data
def cargar_datos():
    df = pd.read_excel(DATA_FILE)
    columnas_requeridas = {"Codigo", "Nombres", "Documento"}
    faltantes = columnas_requeridas - set(df.columns)
    if faltantes:
        raise ValueError(f"Faltan columnas requeridas: {', '.join(sorted(faltantes))}")

    df = df[["Codigo", "Nombres", "Documento"]].copy()
    df["Codigo"] = df["Codigo"].astype(str).str.strip()
    df["Nombres"] = df["Nombres"].astype(str).str.strip()
    df["Documento_normalizado"] = df["Documento"].apply(normalizar_documento)
    df = df[df["Documento_normalizado"] != ""]

    base = {}
    duplicados = []
    for _, row in df.iterrows():
        doc = row["Documento_normalizado"]
        registro = {
            "codigo": row["Codigo"],
            "nombre": row["Nombres"],
            "documento": doc,
        }
        if doc in base:
            duplicados.append(doc)
        else:
            base[doc] = registro

    return base, len(df), sorted(set(duplicados))


st.markdown(
    """
    <style>
    .main-title {text-align:center; font-size:2rem; font-weight:700; margin-bottom:0.25rem;}
    .subtitle {text-align:center; color:#666; margin-bottom:1.5rem;}
    .result-box {padding:1.25rem; border-radius:1rem; background:#f5f7fb; border:1px solid #dfe6f1;}
    .codigo {font-size:2.2rem; font-weight:800; color:#0052cc; text-align:center; margin-top:1rem;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">MESA DE VOTACIÓN JAC</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Consulta el código de votación por número de documento</div>', unsafe_allow_html=True)

if not DATA_FILE.exists():
    st.error("No se encontró el archivo datos.xlsx en la misma carpeta de la app.")
    st.stop()

try:
    base_datos, total_registros, duplicados = cargar_datos()
except Exception as e:
    st.error(f"Error cargando la base de datos: {e}")
    st.stop()

with st.sidebar:
    st.header("Información")
    st.write(f"Registros cargados: {total_registros}")
    st.write(f"Documentos únicos: {len(base_datos)}")
    if duplicados:
        st.warning(f"Documentos duplicados detectados: {len(duplicados)}")

cedula = st.text_input("Digite la cédula del ciudadano", placeholder="Ej: 1122410822", max_chars=20)
buscar = st.button("🔍 Buscar en el libro", use_container_width=True)

if buscar:
    documento = normalizar_documento(cedula)

    if not documento:
        st.warning("Por favor, digite un número de documento.")
    else:
        usuario = base_datos.get(documento)
        if usuario:
            st.success("Registro encontrado")
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.write(f"**Documento:** {usuario['documento']}")
            st.write(f"**Nombres:** {usuario['nombre']}")
            st.markdown(f'<div class="codigo">Código de votación:<br>{usuario["codigo"]}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error("❌ El ciudadano no aparece en el libro de inscritos.")

st.caption("App Diseñada por Edeldaza")
