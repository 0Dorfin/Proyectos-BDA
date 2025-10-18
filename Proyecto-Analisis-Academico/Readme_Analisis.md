# ANALISIS ACADEMICO

**Objetivo:** Ayudar a un centro educativo a entender sus resultados académicos. Partiremos de varios ficheros CSV "sucios" y los transformaremos en un sistema de Business Intelligence (BI) coherente que permita tomar decisiones.

## Tareas

### Tarea 1. Inspeccion datos

## Carpeta Indicadores

### Separador de columnas:
En todos los ficheros el separador es `,`. El único que está de una manera diferente es **`Indicadores_Finales.csv`**, que utiliza `;`.

### Encabezados:
Todos los archivos tienen una primera fila con los encabezados. En general los encabezados son claros.

### Inspección de valores faltantes o extraños:
* En el fichero `Indicadores_Finales.csv` tenemos una gran cantidad de celdas vacías, sobre todo en `Valor-T1`, `Valor-T2` y `Valor-T3`, cuando el indicador es anual.
* Del mismo modo, en `Valor-A` tenemos columnas vacías para todos los indicadores que tienen una periodicidad trimestral.
* También tenemos valores faltantes en `Escala` y `Objetivo`, lo que dificultará evaluar si el resultado fue bueno o malo con las expectativas puestas.

**Consistencia de Datos:**
* El campo `Indicador` en ocasiones tiene números entre corchetes que deberían limpiarse.
* Tenemos inconsistencias en el separador decimal: en algunos valores se usan la coma (`,`) y en otros se usa el punto (`.`).
* En el campo `identificador` tenemos en algunos sufijos con `-a` y `-b`. Estos no tienen correspondencia con los demás ficheros.
* En los ficheros `Lineas.csv`, `Objetivos.csv` y `Procesos.csv` los datos se ven limpios, bien estructurados y sin valores faltantes o extraños.

### Claves para relacionar:
* **`Indicadores_Finales.csv`**:
    * Clave Primaria: `Identificador`
* **`Lineas.csv`**:
    * Clave Primaria: `Linea`
* **`Objetivos.csv`**:
    * Clave Primaria: `Objetivo_PAA`
    * Clave Foránea: `Linea`
* **`Procesos.csv`**:
    * Clave Primaria: `Proceso`

### Relación entre ficheros:
Tenemos como tabla principal `Indicadores_Finales.csv` en el que:
* La columna `Cod_PAA` se conecta con `Objetivo_PAA` (de `Objetivos.csv`).
* La columna `Cod_SQ` se conecta con `Proceso` (de `Procesos.csv`).

**Lógica de Identificadores:**

> El identificador (`IPC01.01`) por ejemplo, sale de relacionar el proceso al que está asociado (`PC01`) que corresponde a "Organització del curs acadèmic" y (`.01`) es el número que diferencia los indicadores dentro del mismo proceso.
>
> *`IPC01.01: Satisfacció del professorat amb la gestió d’horaris.`*

> A su vez, para (`PAA-1A1`), sale de relacionar (`PAA`) con (`1A`) que es el objetivo "Maximitzar l'èxit acadèmic en l'FP inicial" que pertenece a la línea 1 y (`1`) es la línea 1 que es "FORMACIÓ PROFESSIONAL INICIAL DE QUALITAT".

---

## Carpeta Datos_2022

### Separador de columnas:
En todos los ficheros el separador de columnas es `,`.

### Encabezados:
Todos los archivos tienen una primera fila con los encabezados. En general los encabezados son claros.

### Inspección de valores faltantes o extraños:
* **`Alumnos.csv`**:
    * Tenemos muchos valores faltantes. Las columnas `dictamen` y `fecha_resolucion` están **totalmente vacías**.
    * Múltiples celdas vacías en: `municipio_nac_ext`, `libro_escolaridad`, `informado_posib`, `informe_psicoped`, `ampa`, `tipo_matricula`, `municipio_nac`, `provincia_nac`, `cod_postal`, `expediente`, `num_repeticion`, `localidad`, `municipio`, `provincia` y `grupo`.
    * Tenemos dos filas que tienen celdas vacias tanto en `municipio_nac`, `municipio_nac_ext` y `provincia_nac`.

* **`Calificaciones.csv`**:
    * `bloque_contenido` tiene todas las celdas vacías.
    * `tipo_nota` tiene 2 celdas vacías.
    * `observacion`, `capacidades_inf` y `medidas_inf` la mayoría están vacías.

* **`Cursos.csv`**:
    * Celdas vacías en el campo `padre` cuando es el nodo raíz de la jerarquía.
    * **Importante:** Tenemos 2 filas con `ensenanza` 6 que no deberían de estar aquí y **habría que eliminarlas**.

* **`Grupos.csv`**:
    * Celdas vacías solamente en el campo `aula`.

* **`Horas.csv`**:
    * No tenemos valores faltantes.

* **`Modulos.csv`**:
    * **Importante:** Tenemos una fila entera toda en blanco que **habría que eliminar**.

### Consistencia de los datos:
* **`Alumnos.csv`**:
    * Inconsistencia en formatos de fecha:
        * `fecha_exportacion`: `DD/MM/AAAA HH:MI:SS`
        * `fecha_ingreso_centro`: `MM/DD/AAAA`
        * `fecha_nac` y `fecha_matricula`: Mezcla de `DD/MM/AAAA` y `MM/DD/AAAA`.

* **`Horas.csv`**:
    * Los nombres de las columnas están en **MAYÚSCULAS** (`CODIGO`), a diferencia del resto de los ficheros que están en minúsculas.

* **Otros Ficheros**:
    * En los demás ficheros los datos son consistentes a lo largo de estos.

### Claves para relacionar:
* **`Alumnos.csv`**:
    * Clave Primaria: `NIA`
    * Claves Foráneas: `curso`, `grupo`
* **`Calificaciones.csv`**:
    * Tabla auxiliar (muchos a muchos): Un "Alumno" cursa muchos "Modulos" y un "Modulo" es cursado por muchos "Alumnos".
    * Claves Foráneas: `alumno`, `contenido`, `curso`.
* **`Cursos.csv`**:
    * Clave Primaria: `codigo`
    * Clave Autorreferencial: `padre` (se enlaza con `codigo` para definir la jerarquía).
* **`Grupos.csv`**:
    * Clave Primaria: `codigo`
* **`Horas.csv`**:
    * Clave Primaria: `CODIGO`

### Relación entre ficheros:
Tenemos como núcleo principal `Calificaciones.csv`. La función de este es registrar las notas y conecta alumnos y asignaturas.
* Para saber quién ha sacado la nota: `Calificaciones.alumno` se enlaza con `Alumnos.NIA`.
* Para saber qué asignatura se ha calificado: `Calificaciones.contenido` se enlaza con `Modulos.codigo`.

A su vez, estas tablas principales (`Alumnos` y `Modulos`) se juntan con otros ficheros:
* `Alumnos.csv` utiliza su clave foránea `grupo` para enlazarse con `Grupos.codigo` (para saber la clase de cada alumno).
* Tanto `Alumnos.csv` como `Modulos.csv`, con la columna `curso`, se enlazan a `Cursos.codigo`.

**Jerarquía en `Cursos.csv`:**
El fichero `Cursos.csv` nos describe toda la jerarquía académica. Este fichero tiene una estructura que se define autorreferenciándose:
> La columna padre de una fila contiene el valor de la columna codigo de otra fila (la fila del nivel superior). Esta relación es la que permite definir la estructura completa, indicando el curso (ej. "Primero", con padre 2837626366) que pertenece al Ciclo (ej. "ACTIVIDADES COMERCIALES", con codigo 2837626366), y Ciclo (con padre 2837626365) pertenece a la Familia (ej. "COMERCIO Y MARKETING", con codigo 2837626365).
