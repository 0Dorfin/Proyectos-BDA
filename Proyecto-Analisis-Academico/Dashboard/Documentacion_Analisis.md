## ANÁLISIS DE CLÁUSULAS ABUSIVAS EN APLICACIONES DE STREAMING

**Objetivo:** Implementar un pipeline de procesamiento de datos con Apache Spark (PySpark) para detectar y clasificar cláusulas potencialmente abusivas en los Términos de Servicio de las principales plataformas de streaming.

---

## Arquitectura de Datos

El flujo sigue un pipeline ETL en dos fases con guardado intermedio en Parquet:

| Fase | Flujo | Descripción |
|------|-------|-------------|
| **FASE 1 — ETL** | `.txt → Load RDD → RDD prework → RDD clean → Parquet` | Ingesta de contratos, limpieza de texto y persistencia. |
| **FASE 2 — Análisis** | `READ Parquet → RDD work → .csv` | Lectura del Parquet limpio, clasificación por diccionario de patrones abusivos, crear dimensiones, hechos y métricas. |
| **FASE 3 — Visualización** | `Load CSV → Power BI` | Carga de los CSVs en Power BI para cuadros de mando. |

Cada paso del pipeline se registra en una **Tabla de Log** con columnas `FASE | STEP | F_inicio | F_Fin | Length | TIPO`.

---

## Estructura del Proyecto

```text
proyecto_clausulas/
├── scripts/                                          
│   └── Analisis_Clausulas_Abusivas_Spark.ipynb       # Pipeline principal
├── datos/
│   └── datos/                                        # Archivos fuente (ToS en texto plano)
│       ├── Apple Music/                                # 4 documentos (2015, 2018, 2024, 2025)
│       ├── HBO Max/                                    # 4 documentos (2017, 2021, 2024, 2025)
│       ├── Netflix/                                    # 4 documentos (2015, 2018, 2023, 2025)
│       ├── Prime Video/                                # 4 documentos (2016, 2018, 2023, 2025)
│       └── Spotify/                                    # 4 documentos (2015, 2018, 2019, 2025)
├── salida/                                           # Datos intermedios en Parquet
│   ├── contratos_limpios.parquet/                      # Texto limpio + original por línea
│   ├── metadata_documentos.parquet/                    # Metadatos por documento
│   └── metadata_empresas.parquet/                      # Metadatos de empresas
└── resultados/                                       # CSVs para consumo en Power BI
    ├── fact_clausulas_detectadas.csv                   # Tabla de hechos — cada detección
    ├── dim_empresas.csv                                # Dimensión empresas con métricas
    ├── dim_categorias.csv                              # Dimensión categorías con base legal
    ├── resumen_matriz.csv                              # Matriz pivotada empresa por categoría
    ├── palabras_frecuentes.csv                         # Top 20 palabras por empresa
    ├── co_ocurrencias.csv                              # Co-ocurrencia de categorías abusivas
    └── tabla_log.csv                                   # Log de ejecución del pipeline
 ```

---

## Modelo de Datos

```text
                    ┌─────────────────────┐
                    │   dim_categorias     │
                    │─────────────────────│
                    │ id_categoria (PK)    │
                    │ categoria            │
                    │ articulo_trlgdcu     │
                    │ descripcion_legal    │
                    │ gravedad             │
                    │ total_patrones       │
                    │ total_detecciones    │
                    └────────┬────────────┘
                             │
┌─────────────────────┐      │      ┌──────────────────────────┐
│   dim_empresas       │      │      │ fact_clausulas_detectadas │
│─────────────────────│      │      │──────────────────────────│
│ id_empresa (PK)      │◄─────┼─────►│ id_deteccion (PK)        │
│ empresa              │      │      │ id_empresa (FK)           │
│ anio                 │      │      │ id_categoria (FK)         │
│ servicio             │      └──────│ empresa                   │
│ archivo_origen       │             │ anio                      │
│ total_lineas         │             │ archivo                   │
│ total_lineas_limpias │             │ categoria                 │
│ total_palabras       │             │ patron_detectado          │
│ densidad_lexica      │             │ texto_limpio              │
│ total_clausulas_abus.│             │ texto_original            │
│ indice_abusividad    │             │ gravedad                  │
│ cat_predominante     │             └──────────────────────────┘
└─────────────────────┘
```

---

### Tecnologías Utilizadas
* **Motor:** Apache Spark (PySpark) 
* **Lenguaje:** Python 3.x
* **Visualización:** Power BI
