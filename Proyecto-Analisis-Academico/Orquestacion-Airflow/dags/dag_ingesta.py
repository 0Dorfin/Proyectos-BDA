from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.filesystem import FileSensor
from airflow.datasets import Dataset as Asset
from datetime import datetime
import os
import shutil
from include.ingesta_utils import validar_xml, xml_a_csv, registro_log_bronze, copiar_xml_a_s3_bronze

RAW_PATH = "/opt/airflow/data/raw/"
ARCHIVE_PATH = "/opt/airflow/data/archive/"
BRONZE_PATH = "/opt/airflow/S3/bronze/"
LOG_PATH = "/opt/airflow/output/logs/"
TEMP_PATH = "/opt/airflow/data/temp/"

RAW_BATCH_READY = Asset("file:///opt/airflow/data/raw/batch_ready")

def archivar_xml():
    if not os.path.exists(ARCHIVE_PATH): os.makedirs(ARCHIVE_PATH)
    for f in os.listdir(RAW_PATH):
        if f.endswith('.xml'):
            shutil.move(os.path.join(RAW_PATH, f), os.path.join(ARCHIVE_PATH, f))

with DAG(
    dag_id="dag_ingesta_academica",
    start_date=datetime(2026, 1, 1),
    schedule="*/5 * * * *",
    catchup=False,
    tags=["ingesta_academica"],
) as dag:

    esperar_xml = FileSensor(
        task_id="esperar_xml",
        fs_conn_id="fs_default",
        filepath=RAW_PATH,
        poke_interval=30,
        timeout=120,
        mode="reschedule",
        soft_fail=True,
    )

    t_validar_xml = PythonOperator(
        task_id="tarea_validar_xml",
        python_callable=validar_xml,
        op_kwargs={"path": RAW_PATH},
    )
    
    t_copiar_xml_s3 = PythonOperator(
        task_id="copiar_xml_a_s3_bronze",
        python_callable=copiar_xml_a_s3_bronze,
        op_kwargs={"raw_path": RAW_PATH, "s3_bronze_path": BRONZE_PATH},
    )
    
    t_xml_a_csv = PythonOperator(
        task_id="tarea_xml_a_csv",
        python_callable=xml_a_csv,
        op_kwargs={"input_path": RAW_PATH,"temp_path": TEMP_PATH},
        outlets=[RAW_BATCH_READY],
    )

    t_log = PythonOperator(
        task_id='registrar_log_bronze',
        python_callable=registro_log_bronze,
        op_kwargs={'bronze_path': BRONZE_PATH, 'log_path': LOG_PATH}
    )

    t_archivar = PythonOperator(
        task_id='archivar_xml',
        python_callable=archivar_xml,
    )

    esperar_xml >> t_validar_xml >> t_copiar_xml_s3 >> t_xml_a_csv >> t_log >> t_archivar
