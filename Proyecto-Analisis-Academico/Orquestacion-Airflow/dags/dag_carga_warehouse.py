from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.datasets import Dataset as Asset
from datetime import datetime
from include.carga_warehouse_utils import crear_tablas, crear_dim_modulos, crear_dim_alumnos, crear_fact_calificaciones,registro_log_gold

CURATED_READY = Asset("file:///opt/airflow/data/curated/curated_ready")

TEMP_PATH = "/opt/airflow/data/temp/"
GOLD_PATH = "/opt/airflow/S3/gold/"
LOG_PATH = "/opt/airflow/output/logs/"

with DAG(
    dag_id="dag_carga_warehouse",
    start_date=datetime(2026, 1, 1),
    schedule=[CURATED_READY],
    catchup=False,
    tags=["etl", "carga_warehouse"],
) as dag:

    t_crear_tablas = PythonOperator(
        task_id="crear_tablas",
        python_callable=crear_tablas,
        op_kwargs={"conn_id": "mysql_db"}
    )

    t_dim_modulos = PythonOperator(
        task_id="crear_dim_modulos",
        python_callable=crear_dim_modulos,
        op_kwargs={"temp_path": TEMP_PATH, "gold_path": GOLD_PATH}
    )
    
    t_fact = PythonOperator(
        task_id="crear_fact_calificaciones",
        python_callable=crear_fact_calificaciones,
        op_kwargs={"temp_path": TEMP_PATH, "gold_path": GOLD_PATH}
    )
    
    t_dim_alum = PythonOperator(
        task_id="crear_dim_alumnos",
        python_callable=crear_dim_alumnos,
        op_kwargs={"temp_path": TEMP_PATH, "gold_path": GOLD_PATH}
    )

    t_log_gold = PythonOperator(
        task_id="registrar_log_gold",
        python_callable=registro_log_gold,
        op_kwargs={"gold_path": GOLD_PATH, "log_path": LOG_PATH}
    )

    t_crear_tablas >> [t_dim_modulos, t_fact, t_dim_alum] >> t_log_gold