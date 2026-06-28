import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch

st.set_page_config(page_title="EDA", page_icon="📊", layout="wide")
st.title("📊 Análisis Exploratorio de Datos")

@st.cache_data
def load_data():
    return pd.read_csv("data/processed/streaming_users_clean.csv")

df = load_data()
sns.set_theme(style="whitegrid", palette="muted")
orden_plan = ['Básico', 'Estándar', 'Premium']
colors_plan = ['#5b9bd5', '#70ad47', '#ed7d31']

st.markdown("---")
st.markdown("## Análisis univariado")

# VIZ 1
st.markdown("### Visualización 1 — Distribución del tiempo de visualización mensual")
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].hist(df['monthly_watch_time_mins'], bins=40, color='steelblue', edgecolor='white')
med = df['monthly_watch_time_mins'].median()
axes[0].axvline(med, color='red', linestyle='--', label=f'Mediana: {med:.0f}')
axes[0].set_title('Distribución del watch time')
axes[0].set_xlabel('Minutos por mes')
axes[0].set_ylabel('Frecuencia')
axes[0].legend()
axes[1].boxplot(df['monthly_watch_time_mins'], patch_artist=True,
                boxprops=dict(facecolor='steelblue', alpha=0.6))
axes[1].set_title('Boxplot del watch time')
axes[1].set_ylabel('Minutos por mes')
plt.tight_layout()
st.pyplot(fig)
st.info("""
**Interpretación:** La distribución del tiempo de visualización es aproximadamente simétrica,
con la mayoría de los usuarios entre 300 y 1200 minutos mensuales (mediana ~760 min, ~12.7 horas).
La ausencia de asimetría marcada sugiere un comportamiento homogéneo en la base de usuarios,
lo que hace relevante explorar si el plan de suscripción introduce diferencias dentro de esta distribución.
""")

# VIZ 2
st.markdown("### Visualización 2 — Distribución de usuarios por plan de suscripción")
fig2, axes2 = plt.subplots(1, 2, figsize=(11, 4))
conteo = df['subscription_plan'].value_counts().reindex(orden_plan)
axes2[0].bar(conteo.index, conteo.values, color=colors_plan, edgecolor='white')
axes2[0].set_title('Usuarios por plan')
axes2[0].set_xlabel('Plan')
axes2[0].set_ylabel('Cantidad')
for i, v in enumerate(conteo.values):
    axes2[0].text(i, v + 20, str(v), ha='center', fontweight='bold')
axes2[1].pie(conteo.values, labels=conteo.index, autopct='%1.1f%%',
             colors=colors_plan, startangle=90)
axes2[1].set_title('Proporción por plan')
plt.tight_layout()
st.pyplot(fig2)
st.info("""
**Interpretación:** Los tres planes tienen distribución relativamente equilibrada, con leve
predominancia del plan Básico. Este balance es favorable para comparar comportamientos entre
grupos: un desbalance muy marcado dificultaría las comparaciones bivariadas de la Pregunta 1.
""")

st.markdown("---")
st.markdown("## Análisis bivariado")

# VIZ 3
st.markdown("### Visualización 3 — Watch time según plan de suscripción")
fig3, axes3 = plt.subplots(1, 2, figsize=(13, 5))
grupos = [df[df['subscription_plan'] == p]['monthly_watch_time_mins'] for p in orden_plan]
bp = axes3[0].boxplot(grupos, labels=orden_plan, patch_artist=True)
for patch, color in zip(bp['boxes'], colors_plan):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
axes3[0].set_title('Distribución de watch time por plan')
axes3[0].set_xlabel('Plan')
axes3[0].set_ylabel('Minutos por mes')
medias = df.groupby('subscription_plan')['monthly_watch_time_mins'].mean().reindex(orden_plan)
axes3[1].bar(orden_plan, medias.values, color=colors_plan, edgecolor='white')
axes3[1].set_title('Watch time promedio por plan')
axes3[1].set_xlabel('Plan')
axes3[1].set_ylabel('Minutos promedio')
for i, v in enumerate(medias.values):
    axes3[1].text(i, v + 5, f'{v:.0f}', ha='center', fontweight='bold')
plt.tight_layout()
st.pyplot(fig3)
st.info("""
**Interpretación (Pregunta 1):** Se observa una tendencia clara: a mayor categoría de plan,
mayor tiempo de visualización promedio. Los usuarios Premium muestran el mayor consumo mensual,
seguidos por Estándar y Básico. La diferencia es consistente en media y mediana, descartando
que sea resultado de valores extremos. El plan de suscripción sí se asocia al nivel de consumo.
""")

# VIZ 4
st.markdown("### Visualización 4 — Watch time vs tickets de soporte")
fig4, axes4 = plt.subplots(1, 2, figsize=(13, 5))
plan_color_map = dict(zip(orden_plan, colors_plan))
colors_scatter = df['subscription_plan'].map(plan_color_map)
axes4[0].scatter(df['monthly_watch_time_mins'], df['customer_support_tickets'],
                 c=colors_scatter, alpha=0.35, s=12)
axes4[0].set_title('Watch time vs Tickets (color: plan)')
axes4[0].set_xlabel('Minutos de visualización')
axes4[0].set_ylabel('Tickets de soporte')
legend_elements = [Patch(facecolor=c, label=p) for p, c in plan_color_map.items()]
axes4[0].legend(handles=legend_elements, title='Plan')
df['watch_quartile'] = pd.qcut(df['monthly_watch_time_mins'], q=4,
                                labels=['Q1 (bajo)', 'Q2', 'Q3', 'Q4 (alto)'])
tq = df.groupby('watch_quartile', observed=True)['customer_support_tickets'].mean()
axes4[1].bar(tq.index, tq.values, color='steelblue', edgecolor='white')
axes4[1].set_title('Tickets promedio por cuartil de watch time')
axes4[1].set_xlabel('Cuartil de visualización')
axes4[1].set_ylabel('Tickets promedio')
for i, v in enumerate(tq.values):
    axes4[1].text(i, v + 0.01, f'{v:.2f}', ha='center', fontweight='bold')
plt.tight_layout()
st.pyplot(fig4)
st.info("""
**Interpretación (Pregunta 2):** La correlación entre watch time y tickets es cercana a cero.
El análisis por cuartiles confirma que los tickets promedio son similares en todos los grupos
de consumo. Mayor visualización no implica menos tickets: ambas variables son independientes.
Los tickets parecen responder a factores distintos al nivel de uso.
""")

st.markdown("---")
st.markdown("## Análisis multivariado")

# VIZ 5
st.markdown("### Visualización 5 — Correlaciones y watch time por género")
fig5, axes5 = plt.subplots(1, 3, figsize=(16, 5))
corr = df[['age', 'monthly_watch_time_mins', 'customer_support_tickets']].corr()
sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', center=0,
            ax=axes5[0], linewidths=0.5)
axes5[0].set_title('Correlaciones numéricas')
edad_plan = df.groupby('subscription_plan')['age'].mean().reindex(orden_plan)
axes5[1].bar(orden_plan, edad_plan.values, color=colors_plan, edgecolor='white')
axes5[1].set_title('Edad promedio por plan')
axes5[1].set_xlabel('Plan')
axes5[1].set_ylabel('Edad promedio')
for i, v in enumerate(edad_plan.values):
    axes5[1].text(i, v + 0.2, f'{v:.1f}', ha='center', fontweight='bold')
wt_genre = df.groupby('favorite_genre')['monthly_watch_time_mins'].mean().sort_values(ascending=False)
axes5[2].barh(wt_genre.index, wt_genre.values, color='steelblue', edgecolor='white')
axes5[2].set_title('Watch time por género favorito')
axes5[2].set_xlabel('Minutos promedio')
plt.suptitle('Análisis multivariado', fontsize=13)
plt.tight_layout()
st.pyplot(fig5)
st.info("""
**Interpretación (Pregunta 3):** Las variables numéricas tienen correlaciones bajas entre sí:
cada una aporta información independiente al perfil del usuario. La edad promedio aumenta
levemente con el plan, y el watch time varía según el género favorito. Estos patrones indican
que los perfiles de usuarios son multidimensionales: no se definen por una sola variable
sino por la combinación de plan, edad, consumo y preferencias. El PCA explora esta estructura.
""")
