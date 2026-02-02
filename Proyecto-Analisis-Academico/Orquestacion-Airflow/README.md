## ANALISIS ACADEMICO CON AIRFLOW

**Objetivo:** Implementar una solución para automatizar la ingesta, transformación y carga de datos académicos provenientes de archivos XML utilizando **Python** y **Apache Airflow**, orquestando el flujo a través de una arquitectura de datos moderna.

### 5.1. Practica 1. Creación de un DAG en Airflow para el proyecto Análisis Académico

### Arquitectura de Datos
El flujo sigue el patrón de arquitectura de medallón:

* **Bronze:** Ingesta de archivos XML organizados por año académico, validación de integridad y archivado.
* **Silver:** Extracción de entidades a CSV, limpieza de nulos, normalización y aplanado.
* **Gold:** Generación de Parquet y carga en Data Warehouse (MySQL) en tablas de dimensiones y hechos.

### Estructura del Proyecto
```text
ORQUESTACION-AIRFLOW/
├── dags/                       # Directorio principal de DAGs y recursos
│   ├── dag_ingesta.py          # Capa Bronze
│   ├── dag_transformaciones.py # Capa Silver
│   ├── dag_carga_warehouse.py  # Capa Gold
│   ├── include/                # Utils para dags
│   │   ├── ingesta_utils.py
│   │   ├── transformaciones_utils.py
│   │   └── carga_warehouse_utils.py
│   ├── data/                   # Almacenamiento local
│   │   ├── raw/                # XMLs entrantes
│   │   ├── archive/            # Histórico de XMLs procesado
│   │   └── temp/               # CSVs intermedios
│       └── [año-escolar]/
│   ├── S3/                     # Simulación Cloud Storage
│   │   ├── bronze/
│   │   └── [año-escolar]/        # XMLs validados y archivados
│   │   ├── silver/
│   │   └── [año-escolar]/        # CSVs limpios y normalizados
│   │   ├── gold/
│       └── [año-escolar]/        # Archivos Parquet listos para Warehouse
│   └── output/logs/            # Logs físicos
└── docker-compose.yaml         # Despliegue del entorno
```

### Flujo de Trabajo

### Requisitos e Instalación
Tecnologías Utilizadas
* **Orquestador:** Apache Airflow 2.x
* **Lenguaje:** Python 3.x (Pandas, SQLAlchemy, ElementTree)
* **Base de Datos:** MySQL (Data Warehouse)
* **Contenedores:** Docker y Docker Compose

### Puesta en marcha
1. Clonar el repositorio.
2. Levantar el entorno:
```bash
docker compose up -d
```
4. Conexiones Airflow:
```text
| ID | Tipo | Parámetros |
| fs_default | File (path) | Extra Fields JSON: {"path": "/"} |
| id | MySQL | Host: ...rds.amazonaws.com | Port: 3306 | Schema: mysql |
```

### Registro y Monitoreo
* **Log de Tabla:** La tabla Analisis.Log_Actividad registra el estado de cada carga directamente en el Warehouse.
* **Log de Archivo:** El fichero output/logs/log_etl.txt permite una auditoría rápida del movimiento de archivos entre capas.
