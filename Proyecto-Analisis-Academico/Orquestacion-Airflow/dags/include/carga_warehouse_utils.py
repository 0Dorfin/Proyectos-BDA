import os
import pandas as pd
import hashlib
from datetime import datetime
from sqlalchemy import create_engine, text
from airflow.hooks.base import BaseHook

def get_aws_engine(conn_id='mysql_db'):
    connection = BaseHook.get_connection(conn_id)
    db_url = f"mysql+pymysql://{connection.login}:{connection.password}@{connection.host}:{connection.port}/{connection.schema}"
    engine = create_engine(db_url)
    return engine

def crear_tablas(conn_id='mysql_db'):
    engine = get_aws_engine(conn_id)
    
    queries = [
        "CREATE DATABASE IF NOT EXISTS Analisis;",
        
        """CREATE TABLE IF NOT EXISTS Analisis.Log_Actividad (
            id INT AUTO_INCREMENT PRIMARY KEY,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            estado VARCHAR(10),
            mensaje VARCHAR(255),
            origen VARCHAR(100)
        );""",
        
        """CREATE TABLE IF NOT EXISTS Analisis.Dim_Alumnos (
            anyo INT NOT NULL,
            NIA VARCHAR(64) NOT NULL, -- Hash del NIA
            fecha_nac DATE,
            sexo VARCHAR(10),
            estado_matricula VARCHAR(50),
            curso VARCHAR(50),
            grupo VARCHAR(20),
            turno VARCHAR(10),
            PRIMARY KEY (NIA, anyo)
        );""",

        """CREATE TABLE IF NOT EXISTS Analisis.Dim_Modulos (
            anyo INT NOT NULL,
            codigo VARCHAR(50) NOT NULL,
            nombre VARCHAR(255),
            curso VARCHAR(50), -- El código del curso
            curso_nombre VARCHAR(100), -- "1º DAM A"
            ciclo_nombre VARCHAR(255), -- "Desarrollo de Aplicaciones..."
            grado VARCHAR(100), -- "FP Grado Superior"
            familia VARCHAR(100), -- "Informática y Comunicaciones"
            PRIMARY KEY (codigo, curso, anyo)
        );""",
        
        """CREATE TABLE IF NOT EXISTS Analisis.Fact_Calificaciones (
            anyo INT NOT NULL,
            evaluacion VARCHAR(20) NOT NULL,
            nia VARCHAR(64) NOT NULL,
            curso VARCHAR(50),
            contenido VARCHAR(50) NOT NULL,
            nota_numerica INT,
            tipo_nota VARCHAR(50),
            PRIMARY KEY (nia, curso, contenido, anyo, evaluacion)
        );"""
    ]
    
    with engine.connect() as conn:
        for q in queries:
            conn.execute(text(q))

def cargar_datos_bd(path_parquet, tabla_destino, conn_id='mysql_db'):
    if not os.path.exists(path_parquet):
        print(f"No existe el archivo {path_parquet}")
        return

    df = pd.read_parquet(path_parquet)
    
    if df.empty:
        return

    anyo_lote = df['anyo'].iloc[0] 

    engine = get_aws_engine(conn_id)
    
    with engine.connect() as conn:
        print(f"Iniciando transacción para tabla {tabla_destino} - Año {anyo_lote}")
        
        sql_delete = text(f"DELETE FROM {tabla_destino} WHERE anyo = :anyo")
        conn.execute(sql_delete, {"anyo": anyo_lote})
        print(f"Datos del año {anyo_lote} eliminados.")
        
        df.to_sql(
            name=tabla_destino.split('.')[-1], 
            schema=tabla_destino.split('.')[0], 
            con=engine, 
            if_exists='append', 
            index=False
        )
        print(f"Insertados {len(df)} registros correctamente.")

def crear_dim_alumnos(temp_path, gold_path):
    subcarpetas = [d for d in os.listdir(temp_path) if os.path.isdir(os.path.join(temp_path, d))]
    
    import hashlib

    for anyo_folder in subcarpetas:
        ruta_csv = os.path.join(temp_path, anyo_folder, 'Alumnos.csv')
        if not os.path.exists(ruta_csv): continue
            
        df = pd.read_csv(ruta_csv)
        
        df['NIA'] = df['NIA'].astype(str).apply(lambda x: hashlib.sha256(x.encode()).hexdigest()[:10])

        cols_db = ['anyo', 'NIA', 'fecha_nac', 'sexo', 'estado_matricula', 'curso', 'grupo', 'turno']
        df = df[cols_db].copy()
        
        df = df.drop_duplicates(subset=['NIA', 'anyo'], keep='last')

        folder_dest = os.path.join(gold_path, anyo_folder.replace("/", "-"))
        if not os.path.exists(folder_dest): os.makedirs(folder_dest)
        
        archivo_parquet = os.path.join(folder_dest, 'Dim_Alumnos.parquet')
        df.to_parquet(archivo_parquet, index=False)
        
        cargar_datos_bd(archivo_parquet, 'Analisis.Dim_Alumnos')

def crear_dim_modulos(temp_path, gold_path):
    
    subcarpetas = [d for d in os.listdir(temp_path) if os.path.isdir(os.path.join(temp_path, d))]
    
    for anyo_folder in subcarpetas:
        ruta_anyo_temp = os.path.join(temp_path, anyo_folder)
        
        file_mod = os.path.join(ruta_anyo_temp, 'Modulos.csv')
        file_cur_flat = os.path.join(ruta_anyo_temp, 'Cursos_aplanado.csv')

        if not os.path.exists(file_mod) or not os.path.exists(file_cur_flat):
            continue

        df_mod = pd.read_csv(file_mod, dtype={'curso': str, 'codigo': str})
        df_cur = pd.read_csv(file_cur_flat, dtype={'curso': str})

        if 'nombre_cas' in df_mod.columns: df_mod = df_mod.rename(columns={'nombre_cas': 'nombre'})
        if 'nombre_cas' in df_cur.columns: df_cur = df_cur.rename(columns={'nombre_cas': 'texto'})

        if df_mod.empty or df_cur.empty: continue

        df_join = pd.merge(df_mod, df_cur, on=['curso', 'anyo'], how='inner')
        
        cols_deseadas = ['anyo', 'codigo', 'nombre', 'curso', 'curso_nombre', 'ciclo_nombre', 'grado', 'familia']
        cols_finales = [c for c in cols_deseadas if c in df_join.columns]
        df_final = df_join[cols_finales]
        
        folder_gold = os.path.join(gold_path, anyo_folder.replace("/", "-"))
        if not os.path.exists(folder_gold): os.makedirs(folder_gold)
        
        archivo_parquet = os.path.join(folder_gold, 'Dim_Modulos.parquet')
        
        df_final.to_parquet(archivo_parquet, index=False)
        print(f"[{anyo_folder}] Parquet generado.")
        
        cargar_datos_bd(archivo_parquet, 'Analisis.Dim_Modulos')


def crear_fact_calificaciones(temp_path, gold_path):
    subcarpetas = [d for d in os.listdir(temp_path) if os.path.isdir(os.path.join(temp_path, d))]
    
    for anyo_folder in subcarpetas:
        ruta_csv = os.path.join(temp_path, anyo_folder, 'Calificaciones.csv')
        if not os.path.exists(ruta_csv): continue
            
        df = pd.read_csv(ruta_csv)
        
        if 'alumno' in df.columns: df = df.rename(columns={'alumno': 'nia'})
            
        cols_db = ['anyo', 'evaluacion', 'nia', 'curso', 'contenido', 'nota_numerica', 'tipo_nota']
        cols_finales = [c for c in cols_db if c in df.columns]
        df = df[cols_finales].copy()

        folder_dest = os.path.join(gold_path, anyo_folder.replace("/", "-"))
        if not os.path.exists(folder_dest): os.makedirs(folder_dest)
        
        archivo_parquet = os.path.join(folder_dest, 'Fact_Calificaciones.parquet')
        df.to_parquet(archivo_parquet, index=False)
        
        cargar_datos_bd(archivo_parquet, 'Analisis.Fact_Calificaciones')

def registro_log_gold(gold_path, log_path):
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    archivos = [f for f in os.listdir(gold_path) if f.endswith('.parquet')]
    cantidad = len(archivos)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mensaje = f"[{timestamp}] Se han procesado {cantidad} archivos Parquet en la carpeta {gold_path}\n"
    with open(os.path.join(log_path, 'log_etl.txt'), 'a') as f:
        f.write(mensaje)
