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
┌────────────────────────────┐           ┌─────────────────────────────────────┐           ┌────────────────────────────┐
│        dim_empresas        │           │      fact_clausulas_detectadas      │           │       dim_categorias       │
├────────────────────────────┤           ├─────────────────────────────────────┤           ├────────────────────────────┤
│ empresa_anio (PK)          │───┐       │ id_deteccion (PK)                   │       ┌───│ id_categoria (PK)          │
│ id_empresa                 │   │       │ empresa_anio (FK)          ◄────────┼───────┘   │ categoria                  │
│ empresa                    │   │       │ id_categoria (FK)          ◄────────┼───────────┘ gravedad                   │
│ anio                       │   └──────►│ id_empresa                          │           │ articulo_trlgdcu           │
│ servicio                   │           │ empresa                             │           │ descripcion_legal          │
│ archivo_origen             │           │ anio                                │           │ empresas_afectadas         │
│ categoria_predominante     │           │ archivo                             │           │ num_empresas_afectadas     │
│ densidad_lexica            │           │ categoria                           │           │ total_detecciones          │
│ indice_abusividad          │           │ gravedad                            │           │ total_patrones             │
│ orden_empresa              │           │ patron_detectado                    │           │                            │
│ total_clausulas_abusivas   │           │ texto_limpio                        │           │                            │
│ total_lineas               │           │ texto_original                      │           │                            │
│ total_lineas_limpias       │           │ Texto_Corto                         │           │                            │
│ total_palabras             │           └─────────────────────────────────────┘           └────────────────────────────┘
└────────────────────────────┘
```

---

### Tecnologías Utilizadas
* **Motor:** Apache Spark (PySpark) 
* **Lenguaje:** Python 3.x
* **Visualización:** Power BI
