from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.datasets import Dataset as Asset
from datetime import datetime
from include.transformaciones_utils import limpiar_alumnos, limpiar_calificaciones, limpiar_cursos_modulos, combinar_archivos_silver, registro_log_silver

SILVER_PATH = "/opt/airflow/S3/silver/"
LOG_PATH = "/opt/airflow/output/logs/"
TEMP_PATH = "/opt/airflow/data/temp/"

RAW_BATCH_READY = Asset("file:///opt/airflow/data/raw/batch_ready")
CURATED_READY = Asset("file:///opt/airflow/data/curated/curated_ready")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
}

with DAG(
    dag_id="dag_transformaciones",
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule=[RAW_BATCH_READY],
    catchup=False,
    tags=["etl", "transformaciones"],
) as dag:
        
    t_alumnos = PythonOperator(
        task_id="limpiar_alumnos",
        python_callable=limpiar_alumnos,
        op_kwargs={"temp_path": TEMP_PATH, "silver_path": SILVER_PATH}
    )
    
    t_calificaciones = PythonOperator(
        task_id="limpiar_calificaciones",
        python_callable=limpiar_calificaciones,
        op_kwargs={"temp_path": TEMP_PATH, "silver_path": SILVER_PATH}
    )
    t_cursos_modulos = PythonOperator(
        task_id="limpiar_cursos_modulos",
        python_callable=limpiar_cursos_modulos,
        op_kwargs={"temp_path": TEMP_PATH, "silver_path": SILVER_PATH}
    )

    t_combinar_archivos_silver = PythonOperator(
        task_id="combinar_archivos_silver",
        python_callable=combinar_archivos_silver,
    )

    t_log_silver = PythonOperator(
        task_id="registrar_log_silver",
        python_callable=registro_log_silver,
        op_kwargs={
            "conteos": [
                "{{ ti.xcom_pull(task_ids='limpiar_alumnos') }}",
                "{{ ti.xcom_pull(task_ids='limpiar_calificaciones') }}",
                "{{ ti.xcom_pull(task_ids='limpiar_cursos_modulos') }}"
            ],
            "silver_path": SILVER_PATH, 
            "log_path": LOG_PATH
        },
        outlets=[CURATED_READY]
    )

    [t_alumnos, t_calificaciones, t_cursos_modulos] >> t_combinar_archivos_silver >> t_log_silver
