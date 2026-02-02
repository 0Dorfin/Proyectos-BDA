import os
import pandas as pd
from datetime import datetime

def limpiar_alumnos(temp_path, silver_path):
    subcarpetas = [d for d in os.listdir(temp_path) if os.path.isdir(os.path.join(temp_path, d))]
    
    for anyo_folder in subcarpetas:
        ruta_csv = os.path.join(temp_path, anyo_folder, 'Alumnos.csv')
        
        if not os.path.exists(ruta_csv): continue
            
        df = pd.read_csv(ruta_csv)
        cols = ['anyo', 'NIA', 'fecha_nac', 'sexo', 'estado_matricula', 'curso', 'grupo', 'turno']
        
        df = df[cols].copy().drop_duplicates()
        
        folder_dest = os.path.join(silver_path, anyo_folder.replace("/", "-"))
        if not os.path.exists(folder_dest): os.makedirs(folder_dest)
        
        df.to_csv(os.path.join(folder_dest, 'Alumnos.csv'), index=False)

def limpiar_calificaciones(temp_path, silver_path):
    subcarpetas = [d for d in os.listdir(temp_path) if os.path.isdir(os.path.join(temp_path, d))]
    
    for anyo_folder in subcarpetas:
        ruta_csv = os.path.join(temp_path, anyo_folder, 'Calificaciones.csv')
        
        if not os.path.exists(ruta_csv): continue
            
        df = pd.read_csv(ruta_csv)
        
        df['nota_numerica'] = pd.to_numeric(df['nota_numerica'], errors='coerce')
        df = df.dropna(subset=['nota_numerica'])
        df.rename(columns={'alumno': 'nia'}, inplace=True)
        df['evaluacion'] = df['evaluacion'].astype(str)
        df['contenido'] = df['contenido'].astype(str)
        df['nota_numerica'] = df['nota_numerica'].astype(int)
        
        columnas = ['anyo', 'evaluacion', 'nia', 'curso', 'contenido', 'nota_numerica', 'tipo_nota']
        df_final = df[columnas]
        
        folder_dest = os.path.join(silver_path, anyo_folder.replace("/", "-"))
        if not os.path.exists(folder_dest): os.makedirs(folder_dest)
        
        df_final.to_csv(os.path.join(folder_dest, 'Calificaciones.csv'), index=False)

def limpiar_cursos_modulos(temp_path, silver_path):
    subcarpetas = [d for d in os.listdir(temp_path) if os.path.isdir(os.path.join(temp_path, d))]
    
    for anyo_folder in subcarpetas:
        ruta_anyo_temp = os.path.join(temp_path, anyo_folder)
        
        file_mod = os.path.join(ruta_anyo_temp, 'Modulos.csv')
        file_cur = os.path.join(ruta_anyo_temp, 'Cursos.csv')
        
        if not os.path.exists(file_mod) or not os.path.exists(file_cur):
            continue

        df_m = pd.read_csv(file_mod)
        df_c = pd.read_csv(file_cur)
        
        df_c['codigo'] = df_c['codigo'].fillna('').astype(str).str.replace(r'\.0$', '', regex=True)
        df_c['padre'] = df_c['padre'].fillna('').astype(str).str.replace(r'\.0$', '', regex=True)
        df_m['curso'] = df_m['curso'].fillna('').astype(str).str.replace(r'\.0$', '', regex=True)

        df_c = df_c.rename(columns={'codigo': 'curso', 'nombre_cas': 'nombre', 'padre': 'padre'})
        cols_interes = ['anyo', 'curso', 'nombre', 'padre']
        df_base = df_c[cols_interes].copy()

        df_flat = pd.merge(df_base, df_base[['curso', 'nombre', 'padre']], 
                           left_on='padre', right_on='curso', how='left', suffixes=('', '_ciclo'))
        df_flat = pd.merge(df_flat, df_base[['curso', 'nombre', 'padre']], 
                           left_on='padre_ciclo', right_on='curso', how='left', suffixes=('', '_grado'))
        df_flat = pd.merge(df_flat, df_base[['curso', 'nombre']], 
                           left_on='padre_grado', right_on='curso', how='left', suffixes=('', '_familia'))

        df_flat = df_flat.rename(columns={
            'nombre_familia': 'familia',
            'nombre_grado': 'grado',
            'nombre_ciclo': 'ciclo_nombre',
            'nombre': 'curso_nombre'
        })
        
        cols_finales_cursos = ['anyo', 'curso', 'curso_nombre', 'ciclo_nombre', 'grado', 'familia']
        df_flat_final = df_flat[cols_finales_cursos]

        ruta_control = os.path.join(ruta_anyo_temp, 'Cursos_aplanado.csv')
        df_flat_final.to_csv(ruta_control, index=False)
        print(f"[{anyo_folder}] Aplanado guardado en: {ruta_control}")

        folder_silver = os.path.join(silver_path, anyo_folder.replace("/", "-"))
        if not os.path.exists(folder_silver): os.makedirs(folder_silver)
        
        df_flat_final.to_csv(os.path.join(folder_silver, 'Cursos.csv'), index=False)
        
        df_m_final = df_m[['anyo', 'curso', 'codigo', 'nombre_cas']].rename(columns={'nombre_cas': 'nombre'})
        df_m_final.to_csv(os.path.join(folder_silver, 'Modulos.csv'), index=False)

def registro_log_silver(silver_path, log_path):
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    archivos = [f for f in os.listdir(silver_path) if f.endswith('.csv')]
    cantidad = len(archivos)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mensaje = f"[{timestamp}] Transformaciones completadas. Se han procesado {cantidad} archivos CSV en la carpeta {silver_path}\n"
    with open(os.path.join(log_path, 'log_etl.txt'), 'a') as f:
        f.write(mensaje)
