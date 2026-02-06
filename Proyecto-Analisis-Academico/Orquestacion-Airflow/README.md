## ANALISIS ACADEMICO CON AIRFLOW

**Objetivo:** Implementar una solución para automatizar la ingesta, transformación y carga de datos académicos provenientes de archivos XML utilizando **Python** y **Apache Airflow**, orquestando el flujo a través de una arquitectura de datos moderna.

### 5.1. Practica 1. Creación de un DAG en Airflow para el proyecto Análisis Académico

### Arquitectura de Datos
El flujo sigue el patrón de arquitectura de medallón:

* **Bronze:** Ingesta de archivos XML organizados por año académico, validación de integridad y archivado.
* **Silver:** Extracción de entidades a CSV, limpieza de nulos, normalización y aplanado.
* **Gold:** Generación de Parquet y carga en Data Warehouse (MySQL) en tablas de dimensiones y hechos.

> **Gestión de Temporales:** Una vez que el flujo termina de manera exitosa, se hace limpieza de la capa temporal, evitando duplicar datos en ejecuciones consecutivas.

### Estructura del Proyecto
```text
ORQUESTACION-AIRFLOW/
├── dags/                       # Directorio principal de DAGs y recursos
│   ├── dag_ingesta.py          # Capa Bronze
│   ├── dag_transformaciones.py # Capa Silver
│   ├── dag_carga_warehouse.py  # Capa Gold
│   ├── include/                # Utils para DAGs
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

### Tecnologías Utilizadas
* **Orquestador:** Apache Airflow 2.x
* **Lenguaje:** Python 3.x (Pandas, SQLAlchemy, ElementTree)
* **Base de Datos:** MySQL (Data Warehouse)
* **Contenedores:** Docker y Docker Compose

### Puesta en marcha
1. Clonar el repositorio.
2. Configurar las variables de entorno en .env.
3. Levantar el entorno:
```bash
docker compose up -d
```
4. Conexiones Airflow:
```text
| ID | Tipo | Parámetros |
| fs_default | File (path) | Extra Fields JSON: {"path": "/"} |
| id | MySQL | Host: ...rds.amazonaws.com | Port: 3306 | Schema: mysql |
```

### Flujo de Trabajo (DAGs)
El sistema fucniona mediante un enfoque Data Driven (dirigido por datos) para hacer la ejecución basada en la disponibilidad de la información:
1. **dag_ingesta_academica**:
   * Escucha la carpeta **data/raw/** cada 5 minutos.
   * Valida los XML y los mueve a **S3/bronze**
   * Extrae datos crudos a **data/temp**
   * Produce el **batch_ready**
2. **dag_transformaciones**:
   * Se activa automáticamente al recibir el **batch_ready**.
   * Limpia y normaliza alumnos, calificaciones, cursos y modulos.
   * Genera CSVs en **S3/silver**
   * Produce el **curated_ready**
3. **dag_carga_warehouse**:
   * Se activa automáticamente al recibir el **curated_ready**.
   * Crea tablas en MySQL si no existen.
   * Transforma CSVs a Parquet en **S3/gold**
   * **Carga transaccional:** Inserta datos en MySQL con lógica de borrado previo por año
   * **Limpieza:** Elimina los archivos de **data/temp** para dejar el entorno listo para el siguiente lote

### Sistema de Logs y Auditoría
* **Log Físico:** El fichero **output/logs/log_etl.txt** registra el número de archivos procesados en cada capa, validando el movimiento físico de datos.
* **Log de Base de Datos:** **La tabla Analisis.Log_Actividad** registra el estado de cada carga  en el Warehouse con métricas detalladas.
