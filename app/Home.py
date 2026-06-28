import streamlit as st

st.set_page_config(
    page_title="Proyecto Integrador — Minería de Datos 1",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Análisis de Usuarios de Streaming")
st.subheader("Proyecto Integrador — Minería de Datos 1")
st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    st.markdown("### 📋 Información del proyecto")
    st.markdown("""
    **Materia:** Minería de Datos 1  
    **Comisión:** Nueva Espreanza-Turno Mañana  
    **Fecha de entrega:** 30/06/26  
    **Integrante:**
    - Ruiz Mariano
    
    """)

with col2:
    st.markdown("### 🎯 Contexto")
    st.markdown("""
    Este proyecto analiza un dataset de usuarios de una plataforma de streaming con el objetivo
    de comprender el comportamiento de consumo, la relación entre el plan de suscripción y el
    uso de la plataforma, y detectar perfiles diferenciados de usuarios.

    El análisis incluye inspección inicial, limpieza de datos, análisis exploratorio (EDA),
    reducción de dimensionalidad mediante PCA y comunicación de resultados.
    """)

st.markdown("---")
st.markdown("### ❓ Preguntas de análisis")
col1, col2, col3 = st.columns(3)
with col1:
    st.info("**Pregunta 1**\n\n¿El plan de suscripción influye en el tiempo de visualización mensual?")
with col2:
    st.info("**Pregunta 2**\n\n¿Los usuarios con mayor tiempo de visualización generan menos tickets de soporte?")
with col3:
    st.info("**Pregunta 3**\n\n¿Existen perfiles diferenciados de usuarios según su comportamiento de consumo y soporte?")

st.markdown("---")
st.markdown("### 🔗 Repositorio")
st.markdown("📁 [Ver repositorio en GitHub](https://github.com/[usuario]/PI_Mineria_Datos_1)")
st.caption("Navegá por las secciones usando el menú lateral.")
