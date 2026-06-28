import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from matplotlib.patches import Patch

st.set_page_config(page_title="PCA", page_icon="🔬", layout="wide")
st.title("🔬 Reducción de Dimensionalidad — PCA")

@st.cache_data
def load_and_compute():
    df = pd.read_csv("data/processed/streaming_users_clean.csv")
    plan_ord = {'Básico': 1, 'Estándar': 2, 'Premium': 3}
    df['plan_num'] = df['subscription_plan'].map(plan_ord)
    variables_pca = ['age', 'monthly_watch_time_mins', 'customer_support_tickets', 'plan_num']
    X = df[variables_pca].values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    pca = PCA(n_components=4)
    X_pca = pca.fit_transform(X_scaled)
    return df, X_pca, pca, variables_pca

df, X_pca, pca, variables_pca = load_and_compute()

st.markdown("## Variables y escalamiento")
st.markdown("""
**Variables incluidas:** `age`, `monthly_watch_time_mins`, `customer_support_tickets`, `plan_num`

**Justificación de la selección:** Se incluyeron las tres variables numéricas continuas y `plan_num`
(codificación ordinal del plan: Básico=1, Estándar=2, Premium=3), ya que el EDA mostró que el plan
se asocia al nivel de consumo. Se excluyó `user_id` (identificador sin valor analítico), `country`
y `favorite_genre` (categóricas nominales sin orden con muchas categorías).

**Escalamiento aplicado:** StandardScaler (media=0, desvío estándar=1 por variable).
Sin escalamiento, `monthly_watch_time_mins` (en cientos de minutos) dominaría las componentes
por su mayor varianza absoluta, ocultando la contribución del resto de las variables.
""")

st.markdown("---")
varianza = pca.explained_variance_ratio_
varianza_acum = np.cumsum(varianza)

col1, col2, col3 = st.columns(3)
col1.metric("PC1 explica", f"{varianza[0]*100:.1f}%")
col2.metric("PC2 explica", f"{varianza[1]*100:.1f}%")
col3.metric("PC1+PC2 acumulado", f"{varianza_acum[1]*100:.1f}%")

st.markdown("### Visualización 1 — Varianza explicada (Scree plot)")
fig1, axes1 = plt.subplots(1, 2, figsize=(12, 4))
axes1[0].bar(range(1, 5), varianza * 100, color='steelblue', edgecolor='white')
axes1[0].set_title('Varianza explicada por componente')
axes1[0].set_xlabel('Componente principal')
axes1[0].set_ylabel('Varianza explicada (%)')
for i, v in enumerate(varianza * 100):
    axes1[0].text(i + 1, v + 0.3, f'{v:.1f}%', ha='center')
axes1[1].plot(range(1, 5), varianza_acum * 100, 'o-', color='steelblue')
axes1[1].axhline(80, linestyle='--', color='coral', label='80%')
axes1[1].set_title('Varianza acumulada')
axes1[1].set_xlabel('Número de componentes')
axes1[1].set_ylabel('Varianza acumulada (%)')
axes1[1].legend()
plt.tight_layout()
st.pyplot(fig1)
st.info("""
**Interpretación:** Las cuatro variables aportan varianza de forma distribuida, coherente
con las bajas correlaciones detectadas en el EDA. Las dos primeras componentes explican
aproximadamente el 55-65% de la varianza total. Se trabaja con PC1 y PC2 para la visualización
bidimensional, que captura la mayor parte de la estructura disponible.
""")

st.markdown("---")
st.markdown("## Interpretación de componentes (loadings)")
loadings = pd.DataFrame(
    pca.components_.T,
    index=variables_pca,
    columns=[f'PC{i+1}' for i in range(4)]
)
st.dataframe(loadings[['PC1', 'PC2']].round(3))
st.markdown("""
- **PC1** captura principalmente `plan_num` y `monthly_watch_time_mins`: **perfil de consumo y plan**.
- **PC2** captura principalmente `age` y `customer_support_tickets`: **perfil demográfico y soporte**.
""")

st.markdown("---")
st.markdown("### Visualización 2 — Proyección de usuarios en PC1-PC2")
plan_color_map = {'Básico': '#5b9bd5', 'Estándar': '#70ad47', 'Premium': '#ed7d31'}
colors_scatter = df['subscription_plan'].map(plan_color_map)

fig2, axes2 = plt.subplots(1, 2, figsize=(14, 5))
axes2[0].scatter(X_pca[:, 0], X_pca[:, 1], c=colors_scatter, alpha=0.35, s=12)
axes2[0].set_title('PC1 vs PC2 — coloreado por plan')
axes2[0].set_xlabel('PC1 (consumo / plan)')
axes2[0].set_ylabel('PC2 (edad / soporte)')
legend_elements = [Patch(facecolor=c, label=p) for p, c in plan_color_map.items()]
axes2[0].legend(handles=legend_elements, title='Plan')
sc = axes2[1].scatter(X_pca[:, 0], X_pca[:, 1],
                      c=df['monthly_watch_time_mins'], cmap='YlOrRd', alpha=0.4, s=12)
axes2[1].set_title('PC1 vs PC2 — coloreado por watch time')
axes2[1].set_xlabel('PC1 (consumo / plan)')
axes2[1].set_ylabel('PC2 (edad / soporte)')
plt.colorbar(sc, ax=axes2[1], label='Minutos de visualización')
plt.tight_layout()
st.pyplot(fig2)
st.info("""
**Interpretación:** La proyección muestra cierta separación entre planes en el eje PC1,
coherente con que PC1 captura la dimensión de consumo y plan. Sin embargo, la separación
no es perfectamente limpia: hay superposición entre grupos, lo que indica que el plan
es solo uno de los factores que definen el perfil del usuario. El gradiente de watch time
confirma que PC1 organiza a los usuarios según su nivel de consumo.
""")
