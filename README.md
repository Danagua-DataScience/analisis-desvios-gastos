# Análisis y Control de Desvíos de Gastos Mensuales

## Descripción del proyecto

Este proyecto tiene como objetivo analizar, controlar y explicar los desvíos mensuales de gastos contables, combinando análisis estadístico, criterios de materialidad y visualización ejecutiva mediante dashboards interactivos.

El enfoque está orientado a control de gestión, permitiendo identificar:

- Qué cuentas explican el gasto del período  
- Qué desvíos son significativos  
- Qué variaciones son atípicas  
- Qué cuentas requieren justificación según una política de desvíos definida  

## Nota sobre los datos

Los archivos con datos originales no se incluyen en este repositorio por contener información sensible de la empresa (mayores contables
exportados desde ERP).

El proyecto fue desarrollado sobre datos reales, con un volumen aproximado de más de 1 millón de registros anuales.

El pipeline es completamente reproducible utilizando cualquier mayor contable que respete una estructura similar (cuenta, fecha, debe, haber, centro de costo, negocio).


## Objetivo del análisis

El análisis busca responder las siguientes preguntas de negocio:

- ¿Qué cuentas concentran la mayor parte del gasto mensual?  
- ¿Cuáles presentan desvíos relevantes respecto al período anterior?  
- ¿Qué desvíos son atípicos y requieren análisis operativo?  
- ¿Qué cuentas adicionales deben justificarse para cumplir con una política de control de desvíos?  

El resultado final permite priorizar esfuerzos de análisis, reducir ruido operativo y focalizar la gestión en los verdaderos drivers del desvío mensual.

## Metodología de análisis

El análisis se estructura en cuatro etapas secuenciales, cada una filtrando y refinando el universo de cuentas.

### Etapa B.1 — Análisis Pareto mensual

Se aplica un análisis de Pareto sobre los gastos del período actual, utilizando importes absolutos para:

- Identificar las cuentas que explican el 80 % de la magnitud económica del gasto  
- Clasificar las cuentas en categorías A, B y C  
- Definir el universo relevante para el análisis posterior  

La clasificación se recalcula mensualmente y es válida solo para el período analizado.

### Etapa B.2 — Análisis de desvíos vs período anterior

Sobre las cuentas Pareto A se calculan:

- Variación absoluta  
- Variación porcentual  
- Impacto de cada cuenta sobre el desvío total mensual  

Una cuenta se considera con desvío significativo si cumple al menos uno de los siguientes criterios:

- Impacto ≥ 10 % del desvío total  
- Variación mensual ≥ ±20 %  

Estas cuentas avanzan a la siguiente etapa del análisis.

### Etapa B.3 — Detección de outliers (IQR)

Se aplica el método **Interquartile Range (IQR)** sobre los desvíos absolutos de las cuentas con desvíos significativos para:

- Identificar variaciones atípicas dentro del conjunto  
- Detectar cuentas cuyo comportamiento se aleja significativamente del resto  

Las cuentas clasificadas como outliers requieren justificación obligatoria, independientemente del desvío total del período.

### Etapa B.4 — Selección de cuentas adicionales

Según la política definida, el desvío mensual absoluto no puede superar un umbral sin justificar.

Si las cuentas outliers no alcanzan para reducir el desvío residual hasta el nivel permitido, se seleccionan cuentas adicionales (no outliers) siguiendo estos criterios:

- Pertenecer al universo Pareto A  
- Tener desvíos absolutos significativos  
- Ordenarse por impacto hasta cumplir con el umbral de la política  

Esto permite determinar qué cuentas deben justificarse adicionalmente para cumplir con el control establecido.

## Herramientas utilizadas

### Python
- pandas (procesamiento y análisis)
- matplotlib (visualización técnica)

### Power BI
- Storytelling  
- Dashboards
- Power Query
- Dax  

### CSV
- Capa intermedia entre análisis y visualización  

## Estructura del proyecto

```
analisis-desvios-gastos/
│
├── data/
│ ├── raw/          # Archivos originales del ERP (no incluidos)
│ ├── processed/    # Archivos normalizados y unificados (no incluidos)
│ └── mapping/      # Archivos externos de clasificación
│
├── outputs/
│ ├── pareto_mes.csv
│ ├── desvios_mes_total.csv
│ ├── desvios_mes_A.csv
│ ├── outliers_iqr.csv
│ └── cuentas_adicionales.csv
│
├── src/
│ └── ingest_eda.py
│
├── notebooks/
│ ├── 01_eda_gastos_contables.ipynb
│ └── 02_analisis_contable_gastos.ipynb
│
├── report/
│ └── power_bi_dashboard.pbix   # Archivos originales del ERP (no incluido)
│
├── requirements.txt
└── README.md
```

## Resultados principales

El proyecto permite:

- Identificar cuentas clave que explican el gasto mensual  
- Detectar desvíos relevantes y atípicos  
- Separar desvíos justificados, a justificar y residuales  
- Priorizar análisis operativo y documentación  
- Comunicar resultados de forma clara mediante dashboards  

El enfoque combina criterio contable, análisis estadístico y visualización.

## Estado del proyecto

**Estado actual:** funcional y en desarrollo continuo.

### Implementado
- Pipeline de análisis en Python  
- Metodología completa de control de desvíos  
- Dashboard en Power BI con storytelling  

### Pendiente / futuras mejoras
- Automatización completa mensual  
- Justificaciones documentadas por cuenta  
- Análisis histórico de tendencias  
- Alertas automáticas  

## Autor

**Dylan Anagua**  
Data Analyst | Finance & Reporting  

Proyecto orientado a automatización, análisis contable y reporting.


