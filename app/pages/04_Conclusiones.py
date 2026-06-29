import streamlit as st

st.set_page_config(page_title="Conclusiones", page_icon="✅", layout="wide")
st.title(" Conclusiones")
st.markdown("---")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("###  Pregunta 1")
    st.markdown("*¿El plan de suscripción influye en el tiempo de visualización mensual?*")
    st.success("""
**Conclusión: Sí.**

A mayor categoría de plan, mayor tiempo de visualización promedio. Los usuarios Premium
son los de mayor consumo y los Básico los de menor. La relación es gradual y consistente
tanto en media como en mediana.
    """)

with col2:
    st.markdown("###  Pregunta 2")
    st.markdown("*¿Los usuarios con mayor watch time generan menos tickets de soporte?*")
    st.success("""
**Conclusión: No.**

La correlación entre watch time y tickets es cercana a cero. El volumen de tickets es
independiente del nivel de consumo. Los tickets parecen responder a factores distintos
al tiempo de uso, no capturados en el dataset.
    """)

with col3:
    st.markdown("###  Pregunta 3")
    st.markdown("*¿Existen perfiles diferenciados de usuarios?*")
    st.success("""
**Conclusión: Sí, parcialmente.**

Existen perfiles diferenciados según consumo y plan, pero con superposición entre grupos.
El perfil de un usuario está determinado por múltiples dimensiones. PC1 captura consumo/plan
y PC2 captura edad/soporte.
    """)

st.markdown("---")
st.markdown("##  Limitaciones")
st.warning("""
- El alcance está condicionado por la información disponible. El dataset no incluye historial de sesiones, duración individual o historial de pagos.
- La imputación de `monthly_watch_time_mins` con mediana y `favorite_genre` con moda introduce simplificaciones.
- La eliminación de 882 registros con fechas futuras reduce la representatividad del dataset.
- El análisis es exploratorio: las relaciones observadas indican asociación, no causalidad.
""")

st.markdown("---")
st.markdown("##  Próximos pasos")
st.info("""
- Aplicar clustering (k-means, DBSCAN) sobre el espacio PCA para formalizar la segmentación de usuarios.
- Incorporar variables adicionales (historial de pagos, antigüedad, sesiones) para ampliar el análisis de perfiles.
- Explorar qué factores determinan el volumen de tickets de soporte más allá del consumo.
""")

st.markdown("---")
st.markdown("### 🔗 Referencias")
st.markdown("""
- 📁 [Repositorio GitHub](https://github.com/MarianoRuiz-ai/TPI_Mineria_Datos_1)
- 🌐 [Aplicación Streamlit Cloud](https://tpimineriadatos1-ruizmariano1.streamlit.app/)
- 📓 Notebooks: `notebooks/` (01 al 05)
- 📄 Informe final: `reports/informe_final.pdf`
- 📋 Log ETL: `logs/pipeline_log.csv`
""")
