# Proyecto Integrador — Minería de Datos 1

**Integrante:** Ruiz Mariano  
**Comisión:** Nueva Esperanza-Turno mañana | **Fecha:** 30/06/26

---

## Información general

Proyecto integrador de la materia Minería de Datos 1. Análisis de un dataset de usuarios de una plataforma de streaming con el objetivo de comprender el comportamiento de consumo, la relación entre el plan de suscripción y el uso de la plataforma, y detectar perfiles diferenciados de usuarios. El trabajo incluye inspección inicial, limpieza de datos, análisis exploratorio, escalamiento, reducción de dimensionalidad mediante PCA y comunicación de resultados a través de una aplicación Streamlit.

---

## Objetivo del proyecto

Aplicar los contenidos de Minería de Datos 1 para construir un análisis de datos con decisiones justificadas, trazabilidad del proceso y comunicación clara de los resultados. Las preguntas definidas son:

1. ¿El plan de suscripción influye en el tiempo de visualización mensual?
2. ¿Los usuarios con mayor tiempo de visualización generan menos tickets de soporte?
3. ¿Existen perfiles diferenciados de usuarios según su comportamiento de consumo y soporte?

El alcance es exploratorio y no incluye modelado predictivo.

---

## Dataset

El dataset `streaming_users_dirty.json` contiene 8160 registros de usuarios con 8 variables: `user_id`, `age`, `subscription_plan` (Básico/Estándar/Premium), `monthly_watch_time_mins`, `country`, `favorite_genre`, `last_login_date` y `customer_support_tickets`.

La variable de mayor interés para el análisis es `monthly_watch_time_mins`. Se detectaron múltiples problemas de calidad: 126 duplicados; 753 nulos distribuidos en `monthly_watch_time_mins` (193), `favorite_genre` (240) y `last_login_date` (320); inconsistencias de capitalización e idioma en `subscription_plan` (15 variantes), `country` (26 variantes) y `favorite_genre` (29 variantes); valores imposibles en `age` (-5, 130, 150), `monthly_watch_time_mins` (negativos, 50000, 99999) y `customer_support_tickets` (-1, 99, 150); y formatos de fecha mixtos con fechas futuras en `last_login_date`.

El dataset original se preservó en `data/raw/`. El dataset procesado está en `data/processed/`.

---

## Estructura del repositorio

```
PI_Mineria_Datos_1/
├── README.md
├── requirements.txt
├── data/
│   ├── raw/           ← dataset original sin modificaciones
│   └── processed/     ← dataset procesado utilizado en el análisis
├── notebooks/
│   ├── 01_inspeccion_inicial.ipynb
│   ├── 02_calidad_y_limpieza.ipynb
│   ├── 03_eda.ipynb
│   ├── 04_pca.ipynb
│   └── 05_conclusiones.ipynb
├── app/
│   ├── Home.py
│   └── pages/
├── reports/
│   └── informe_final.pdf
└── logs/
    └── pipeline_log.csv
```

---

## Preparación y calidad de datos

Ver desarrollo en [`notebooks/02_calidad_y_limpieza.ipynb`](notebooks/02_calidad_y_limpieza.ipynb) y registro completo en [`logs/pipeline_log.csv`](logs/pipeline_log.csv).

Decisiones tomadas: eliminación de 126 duplicados; normalización de `subscription_plan`, `country` y `favorite_genre` mediante mapeo explícito de variantes a categorías correctas; eliminación de registros con valores imposibles en `age` (fuera del rango 13-100), `monthly_watch_time_mins` (negativos o superiores a 10000) y `customer_support_tickets` (negativos o superiores a 50); imputación de nulos en `monthly_watch_time_mins` con la mediana y en `favorite_genre` con la moda; unificación de formatos en `last_login_date` y eliminación de fechas futuras.

El dataset final contiene 6672 registros (retención: 81.8%) sin valores nulos.

---

## Resumen del análisis exploratorio

Ver desarrollo en [`notebooks/03_eda.ipynb`](notebooks/03_eda.ipynb).

La distribución de `monthly_watch_time_mins` es aproximadamente simétrica con mediana ~760 minutos. Los tres planes tienen distribución equilibrada en el dataset.

El hallazgo principal del análisis bivariado es que el plan de suscripción se asocia positivamente al tiempo de visualización: los usuarios Premium tienen el mayor consumo promedio, seguidos por Estándar y Básico. La diferencia es consistente en media y mediana.

En contraste, la correlación entre `monthly_watch_time_mins` y `customer_support_tickets` es cercana a cero: el volumen de tickets no depende del nivel de consumo.

El análisis multivariado mostró que las variables numéricas tienen correlaciones bajas entre sí, indicando que cada una aporta información independiente al perfil del usuario.

---

## Reducción de dimensionalidad

Ver desarrollo en [`notebooks/04_pca.ipynb`](notebooks/04_pca.ipynb).

Se aplicó PCA sobre `age`, `monthly_watch_time_mins`, `customer_support_tickets` y `plan_num` (codificación ordinal del plan), escaladas con StandardScaler. Se excluyeron `user_id`, `country` y `favorite_genre`.

Las cuatro variables aportan varianza de forma distribuida, coherente con las bajas correlaciones del EDA. PC1 captura la dimensión de consumo y plan; PC2 captura la dimensión demográfica y de soporte. Las dos primeras componentes explican aproximadamente el 55-65% de la varianza total. La proyección en PC1-PC2 muestra cierta separación entre planes, con superposición parcial entre grupos.

---

## Visualización interactiva

Aplicación pública: [https://[app].streamlit.app](https://[app].streamlit.app)

La aplicación incluye descripción del dataset y resumen de calidad; 5 visualizaciones con interpretaciones sobre el EDA; scree plot, loadings y proyección PCA; y síntesis de conclusiones, limitaciones y próximos pasos.

---

## Cómo ejecutar localmente

```bash
git clone https://github.com/[usuario]/PI_Mineria_Datos_1.git
cd PI_Mineria_Datos_1
pip install -r requirements.txt
streamlit run app/Home.py
```

Los notebooks pueden ejecutarse en orden (01 al 05) desde la carpeta `notebooks/`.

---

## Conclusiones

El plan de suscripción se asocia positivamente al tiempo de visualización mensual: los usuarios Premium tienen el mayor consumo y los Básico el menor, con diferencias consistentes en toda la distribución. En cambio, el tiempo de visualización no se asocia al volumen de tickets de soporte, que resulta independiente del nivel de consumo. El análisis PCA confirma la existencia de perfiles diferenciados parcialmente, siendo el consumo y el plan las dimensiones principales de separación, con superposición entre grupos.

Las conclusiones están condicionadas por la información disponible y las decisiones documentadas. El análisis es exploratorio y no establece causalidad. Ver [`reports/informe_final.pdf`](reports/informe_final.pdf) para la síntesis completa.
