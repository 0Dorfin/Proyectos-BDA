# Proyectos BDA

Repositorio con los proyectos del módulo de BDA

**Estructura de Directorios**

* **Proyecto-Analisis-Academico/**
  * **Ingesta-NiFi/**
      * `Analisis_Academico_Flujo.json` (Flujo NIFI)
      * `configuracion.md`
  * **Arquitectura-Datos/**
      * `Arquitectura_Data_Lakehouse.md` (Definición de buckets S3)
      * `diseño_data_warehouse.png` (Esquema en copo de nieve) 
  * **Gobernanza-Calidad-Dato/**
      * `DATA_CATALOG.xlsx` (Catálogo de Datos)
      * `DATA_LINEAGE.xlsx` (Linaje de Datos)
  * **Orquestacion-Airflow/** (Orquestación con Airflow y Arquitectura Medallón)
    * **dags/** (Definición de DAGs y lógica de negocio)
        * **include/** (Utils para DAGs)
          * `ingesta_utils.py`
          * `transformaciones_utils.py`
          * `carga_warehouse_utils.py`
        * `dag_ingesta.py` (Capa Bronze: Validación e ingesta raw)
        * `dag_transformaciones.py` (Capa Silver: Limpieza y aplanado)
        * `dag_carga_warehouse.py` (Capa Gold: Carga final a MySQL)
    * `docker-compose.yaml` (Configuración de infraestructura Airflow)
    * `README.md` (Documentación de Práctica 5.1)
  * `csv_to_parquet.py`
  * `Readme_Analisis.md` (Documentación del Proyecto Análisis Académico)
* **Proyecto-Smart-City/**
    * **Proyecto Fiware/**
       * **Scripts/**
         * `crear_entidades.py`
         * `crear_suscripcion.py`
         * `carga_datos.py`
       * `README.md` (Documentación de Tarea 2: Infraestructura FIWARE)  
    * `README_SmartCity.md` (Documentación del Proyecto Smart City)
* `README.md` (Guía del repositorio)
