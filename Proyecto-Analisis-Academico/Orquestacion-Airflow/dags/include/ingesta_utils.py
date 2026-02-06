import os
import pandas as pd
import shutil
import xml.etree.ElementTree as ET
from datetime import datetime

def validar_xml(path):
    if not os.path.exists(path):
        os.makedirs(path)
        raise ValueError(f"La carpeta {path} no existía (se ha creado), por tanto no hay XMLs.")
        
    archivos = [f for f in os.listdir(path) if f.endswith('.xml')]
    if not archivos:
        raise ValueError("No se detectaron archivos XML en la carpeta de entrada")
    
    for f in archivos:
        if os.path.getsize(os.path.join(path, f)) == 0:
            raise ValueError(f"El archivo {f} está vacío")
    print(f"{len(archivos)} archivos XML encontrados.")

def procesar_nodo(root, tag_busqueda, columnas, datos_globales, mapa_columnas={}):
    data = []
    nodos = root.findall(tag_busqueda)
    
    for nodo in nodos:
        fila = datos_globales.copy()
        for col in columnas:
            if col in ['anyo', 'fecha_exportacion']:
                continue
            
            xml_attr = col
            for k, v in mapa_columnas.items():
                if v == col:
                    xml_attr = k
                    break
            
            fila[col] = nodo.attrib.get(xml_attr, '')
        data.append(fila)
    return data


def xml_a_csv(input_path, temp_path):
    print(f"--- Procesando XMLs desde {input_path} ---")
    
    datos_por_anyo = {}

    cols_alumnos = [
        'anyo', 'fecha_exportacion', 'NIA', 'fecha_nac', 'municipio_nac', 'municipio_nac_ext', 
        'provincia_nac', 'pais_nac', 'nacionalidad', 'sexo', 'tipo_doc', 'expediente', 
        'libro_escolaridad', 'cod_postal', 'provincia', 'municipio', 'localidad', 'ampa', 
        'seguro', 'dictamen', 'fecha_resolucion', 'informe_psicoped', 'informado_posib', 
        'fecha_matricula', 'fecha_ingreso_centro', 'estado_matricula', 'tipo_matricula', 
        'repite', 'num_repeticion', 'ensenanza', 'curso', 'grupo', 'turno', 'linea', 
        'trabaja', 'fuera_comunidad', 'matricula_parcial', 'matricula_condic'
    ]
    cols_calif = [
        'anyo', 'fecha_exportacion', 'evaluacion', 'alumno', 'ensenanza', 'curso', 
        'contenido', 'bloque_contenido', 'nota_numerica', 'tipo_nota', 'observacion', 
        'capacidades_inf', 'medidas_inf', 'borrar', 'sobreescribir'
    ]
    cols_grupos = ['anyo', 'fecha_exportacion', 'codigo', 'nombre', 'ensenanza', 'linea', 'turno', 'modalidad', 'aula', 'capacidad', 'oficial']
    cols_cursos = ['anyo', 'fecha_exportacion', 'ensenanza', 'codigo', 'abreviatura', 'nombre_cas', 'nombre_val', 'padre']
    cols_modulos = ['anyo', 'fecha_exportacion', 'ensenanza', 'curso', 'codigo', 'nombre_cas', 'nombre_val']

    for raiz, dirs, archivos in os.walk(input_path):
        for f in archivos:
            if f.endswith('.xml'):
                full_path = os.path.join(raiz, f)
                tree = ET.parse(full_path)
                root = tree.getroot()
                
                anyo = root.attrib.get('curso', 'desconocido')
                
                if anyo not in datos_por_anyo:
                    datos_por_anyo[anyo] = {
                        'Alumnos': [], 'Calificaciones': [], 'Grupos': [], 'Cursos': [], 'Modulos': []
                    }

                datos_globales = {
                    'anyo': anyo,
                    'fecha_exportacion': root.attrib.get('fechaExportacion', '')
                }

                datos_por_anyo[anyo]['Alumnos'].extend(procesar_nodo(root, 'alumnos/alumno', cols_alumnos, datos_globales))
                datos_por_anyo[anyo]['Calificaciones'].extend(procesar_nodo(root, './/calificacion', cols_calif, datos_globales))
                datos_por_anyo[anyo]['Grupos'].extend(procesar_nodo(root, './/grupo', cols_grupos, datos_globales))
                datos_por_anyo[anyo]['Cursos'].extend(procesar_nodo(root, './/curso', cols_cursos, datos_globales))
                datos_por_anyo[anyo]['Modulos'].extend(procesar_nodo(root, './/contenido', cols_modulos, datos_globales))

    for anyo, tablas in datos_por_anyo.items():
        path_anyo = os.path.join(temp_path, str(anyo))
        if not os.path.exists(path_anyo):
            os.makedirs(path_anyo)
            
        for nombre_archivo, lista_datos in tablas.items():
            if nombre_archivo == 'Alumnos': cols = cols_alumnos
            elif nombre_archivo == 'Calificaciones': cols = cols_calif
            elif nombre_archivo == 'Grupos': cols = cols_grupos
            elif nombre_archivo == 'Cursos': cols = cols_cursos
            elif nombre_archivo == 'Modulos': cols = cols_modulos
            
            if lista_datos:
                df = pd.DataFrame(lista_datos, columns=cols)
                output_file = os.path.join(path_anyo, f"{nombre_archivo}.csv")
                df.to_csv(output_file, index=False, encoding='utf-8')
                print(f"[{anyo}] Generado {output_file} con {len(df)} registros.")

def copiar_xml_a_s3_bronze(raw_path, s3_bronze_path):
    if not os.path.exists(s3_bronze_path):
        os.makedirs(s3_bronze_path)
    
    archivos_raw = [f for f in os.listdir(raw_path) if f.endswith('.xml')]
    count = 0
    
    for f in archivos_raw:
        ruta_f = os.path.join(raw_path, f)
        tree = ET.parse(ruta_f)
        root = tree.getroot()
        anyo_raw = root.attrib.get('curso', '')
        
        if anyo_raw:
            anyo_folder = anyo_raw.replace("/", "-")
            carpeta_destino = os.path.join(s3_bronze_path, anyo_folder)
            
            if os.path.exists(carpeta_destino):
                shutil.rmtree(carpeta_destino)
            
            os.makedirs(carpeta_destino)
            shutil.copy(ruta_f, os.path.join(carpeta_destino, f))
            count += 1
            
    return count

def anonimizar_xml(input_path, output_path):
    try:
        tree = ET.parse(input_path)
        root = tree.getroot()
        
        campos_texto = [
            'nombre', 'apellido1', 'apellido2', 'domicilio', 
            'nombre_padre', 'nombre_madre'
        ]
        
        campos_contacto = [
            'telefono1', 'telefono2', 'telefono3', 
            'email1', 'email2'
        ]
        
        campos_identificacion = [
            'documento', 'sip', 'nuss', 'libro_escolaridad'
        ]

        count = 0
        for alumno in root.findall('.//alumno'):
            count += 1
            
            for campo in campos_texto:
                if alumno.get(campo):
                    original = alumno.get(campo)
                    mascara = 'X' * len(original)
                    alumno.set(campo, mascara)

            for campo in campos_contacto:
                val = alumno.get(campo)
                if val and val.strip():
                    if 'email' in campo:
                        alumno.set(campo, 'anonimo@gmail.com')
                    else:
                        alumno.set(campo, '000000000')

            for campo in campos_identificacion:
                if alumno.get(campo):
                    alumno.set(campo, '00000000X')

        tree.write(output_path, encoding='utf-8', xml_declaration=True)
        print(f"Proceso completado. {count} alumnos anonimizados.")
        print(f"Archivo guardado en: {output_path}")

    except Exception as e:
        print(f"Error al procesar el XML: {e}")

def registro_log_bronze(bronze_path, log_path, cantidad):
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    
    palabra = "archivo" if cantidad == 1 else "archivos"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    mensaje = f"[{timestamp}] Ingesta completada. Se ha procesado {cantidad} {palabra} XML en la carpeta {bronze_path}\n"

    with open(os.path.join(log_path, 'log_etl.txt'), 'a') as f:
        f.write(mensaje)
